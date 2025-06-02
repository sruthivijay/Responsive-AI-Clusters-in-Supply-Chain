from flask import Flask, request, jsonify
import asyncio
import functools
import json
import os
import threading
import time
import websockets
from dotenv import load_dotenv
import os

# Explicitly specify the path to the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)

# Debugging: Print the loaded environment variables
print("AZURE_OPENAI_API_KEY:", os.getenv("AZURE_OPENAI_API_KEY"))
print("AZURE_OPENAI_BASE_URL:", os.getenv("AZURE_OPENAI_BASE_URL"))
print("AZURE_API_VERSION:", os.getenv("AZURE_API_VERSION"))
print("AZURE_DEPLOYMENT_NAME:", os.getenv("AZURE_DEPLOYMENT_NAME"))

from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType

from multi_agent_communication_supply_chain import role_playing, messages_queue

# azure_model_config = {
#     "api_key": os.getenv("AZURE_OPENAI_KEY"),
#     "url": os.getenv("AZURE_OPENAI_BASE_URL"),
#     "api_version": os.getenv("AZURE_API_VERSION"),
#     "azure_deployment_name": os.getenv("AZURE_DEPLOYMENT_NAME"),
#     "temperature": 0.7
# }

if not os.getenv("AZURE_OPENAI_API_KEY"):
    raise EnvironmentError("Missing AZURE_OPENAI_API_KEY environment variable.")
if not os.getenv("AZURE_OPENAI_BASE_URL"):
    raise EnvironmentError("Missing AZURE_OPENAI_BASE_URL environment variable.")
if not os.getenv("AZURE_API_VERSION"):
    raise EnvironmentError("Missing AZURE_API_VERSION environment variable.")
if not os.getenv("AZURE_DEPLOYMENT_NAME"):
    raise EnvironmentError("Missing AZURE_DEPLOYMENT_NAME environment variable.")

azure_model = ModelFactory.create(
    model_platform=ModelPlatformType.AZURE,
    model_type=ModelType.GPT_4O,  # Changed from GPT_4O to GPT_4
    model_config_dict={
        "temperature": 0.7,  # Only include valid Azure OpenAI parameters here
    },
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  # Ensure this is set in the environment
    url=os.getenv("AZURE_OPENAI_BASE_URL"),  # Ensure this is set in the environment
    api_version=os.getenv("AZURE_API_VERSION"),  # Ensure this is set in the environment
    azure_deployment_name=os.getenv("AZURE_DEPLOYMENT_NAME")  # Ensure this is set in the environment
)

# Check if the required environment variables are set


global central_hub_json

# Importing central hub json
with open('../../data/central_hub.json', 'r') as f:
    central_hub_json = json.load(f)

# central_hub_json = {
#     "central_hub_inventory": {
#         "t_shirt": {
#             "current_storage_amount": 1000,
#         },
#         "dress": {
#             "current_storage_amount": 500,
#         },
#         "pants": {
#             "current_storage_amount": 800,
#         },
#         "tops": {
#             "current_storage_amount": 700,
#         },
#     }
# }

# Example of request JSON
# response_json = {
#     "outlet_inventory": {
#         "t_shirt": {
#             "changed_replenishment_amount_from_central_hub": 1000,
#         },
#         "dress": {
#             "changed_replenishment_amount_from_central_hub": 500,
#         },
#         "pants": {
#             "changed_replenishment_amount_from_central_hub": 800,
#         },
#         "tops": {
#             "changed_replenishment_amount_from_central_hub": 700,
#         }
#     },
#     "central_hub_inventory": {
#         "t_shirt": {
#             "current_storage_amount": 1000,
#         },
#         "dress": {
#             "current_storage_amount": 500,
#         },
#         "pants": {
#             "current_storage_amount": 800,
#         },
#         "tops": {
#             "current_storage_amount": 700,
#         },
#     },
#     "transportation_duration": 1
# }


app = Flask(__name__)

async def get_message_from_queue(messages_queue):
    return await asyncio.to_thread(messages_queue.get)

async def send_streaming_message(websocket):
    while True:
        message = await get_message_from_queue(messages_queue)  # Retrieve a message from the queue
        print(f"MESSAGE QUEUE MESSAGES:The message from the message queue:\n{message}")
        if message is None:
            break

        sender_id = message["sender_id"]
        user_message = message["user_message"] + "\n\n"
        assistant_message = message["assistant_message"] + "\n\n"

        for char in user_message:  # user
            msg_to_send = {
                "SpeakerID": sender_id,
                "ReceiverID": "0",
                "text": char,
            }
            time.sleep(0.005)
            await websocket.send(json.dumps(msg_to_send))

        for char in assistant_message:  # assistant
            msg_to_send = {
                "SpeakerID": "0",
                "ReceiverID": sender_id,
                "text": char,
            }
            time.sleep(0.005)
            await websocket.send(json.dumps(msg_to_send))

        messages_queue.task_done()  # Mark the task as done

def run_websocket_server():
    async def start_server():
        print("Starting WebSocket server on ws://localhost:8000")  # Debug log
        async with websockets.serve(send_streaming_message, 'localhost', 8000):
            await asyncio.Future()  # Run forever

    asyncio.run(start_server())

# Clenup the chat record, path 'back_end/ai/chat_record'
def cleanup_chat_record():
    directory_path = os.path.join(os.path.dirname(__name__), "chat_record")
    # Ensure the directory exists
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)  # Create the directory if it doesn't exist
    # Clean up files in the directory
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        os.remove(file_path)

websocket_server_thread = None
current_messages_queue = None

# Define a route for the AI request
@app.route('/ai', methods=['POST'])
def handle_ai_request():
    # Get JSON data from the request
    request_data = request.get_json()

    def format_product_names(json_data):
        if "outlet_inventory" in json_data:
            formatted_inventory = {}
            for product_name, details in json_data["outlet_inventory"].items():
                # Convert the product name to lowercase and replace spaces with underscores
                formatted_name = product_name.lower().replace(" ", "_")
                formatted_inventory[formatted_name] = details

            json_data["outlet_inventory"] = formatted_inventory
        return json_data

    request_data = format_product_names(request_data)
    print('request data: ', request_data)

    # Perform some AI-related processing with role_playing
    global central_hub_json
    try:
        cleanup_chat_record()  # Cleanup the chat record
        response_json, updated_central_hub_json = role_playing(model= azure_model,request_json=request_data, central_hub_json=central_hub_json)
        print('response_json1: ', response_json)
        print('updated_central_hub_json1: ', updated_central_hub_json)
    except Exception as e:
        raise e
        # If the role_playing function fails, return a default response
        with open('../../data/default_data.json', 'r') as f:
            response_json = json.load(f)
        print('response_json2: ', response_json)
        
        # response_json = {
        #     "outlet_inventory": {
        #         "t_shirt": {
        #             "future_storage_amount": 50,
        #             "specific_reason_of_replenishment": "to meet the moderate demand as per the client's preferences"
        #         },
        #         "dress": {
        #             "future_storage_amount": 30,
        #             "specific_reason_of_replenishment": "to maintain a minimal stock level due to the client's minimal interest"
        #         },
        #         "pants": {
        #             "future_storage_amount": 40,
        #             "specific_reason_of_replenishment": "to meet the strong demand as per the client's preferences"
        #         },
        #         "tops": {
        #             "future_storage_amount": 35,
        #             "specific_reason_of_replenishment": "to meet the strong demand as per the client's preferences"
        #         }
        #     },
        #     "central_hub_inventory": {
        #         "t_shirt": {
        #             "current_storage_amount": 1000
        #         },
        #         "dress": {
        #             "current_storage_amount": 500
        #         },
        #         "pants": {
        #             "current_storage_amount": 800
        #         },
        #         "tops": {
        #             "current_storage_amount": 700
        #         }
        #     },
        #     "transportation_duration": 1
        # }

        # updated_central_hub_json = {
        #     "central_hub_inventory": {
        #         "t_shirt": {
        #             "current_storage_amount": 1000
        #         },
        #         "dress": {
        #             "current_storage_amount": 500
        #         },
        #         "pants": {
        #             "current_storage_amount": 800
        #         },
        #         "tops": {
        #             "current_storage_amount": 700
        #         }
        #     }
        # }

        updated_central_hub_json = {'central_hub_inventory': response_json['central_hub_inventory']}
        print('updated_central_hub_json2 :', updated_central_hub_json)

    for product in updated_central_hub_json["central_hub_inventory"]:
        product_account = int(updated_central_hub_json["central_hub_inventory"][product]["current_storage_amount"])
        print('product_account: ', product_account)
        if product_account <= 0:
            updated_central_hub_json["central_hub_inventory"][product]["current_storage_amount"] = 1000
            print(f"Product {product} is out of stock, replenished to 1000.")
    central_hub_json = updated_central_hub_json

    # Return the response from role_playing
    print(f"Response JSON:\n{response_json}")
    return jsonify(response_json)

def run_flask_app():
    # Running on http://0.0.0.0:5000/ without threading even in debug mode
    app.run(debug=False, host='0.0.0.0', port=5000)

def main():
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    run_websocket_server()

if __name__ == "__main__":
    main()
