import json
import os
import queue
import re

from colorama import Fore

from camel.configs import ChatGPTConfig
from camel.societies import RolePlaying
from camel.types import ModelType, TaskType
from format_agent import FormatAgent
from camel.toolkits import MathToolkit



messages_queue = queue.Queue()


def normalize_product_names(data):
    """Normalize product names to lowercase and replace spaces with underscores."""
    if "outlet_inventory" in data:
        normalized_inventory = {}
        for product_name, details in data["outlet_inventory"].items():
            normalized_name = product_name.lower().replace(" ", "_")
            normalized_inventory[normalized_name] = details
        data["outlet_inventory"] = normalized_inventory
    return data


def role_playing(model, chat_turn_limit=30, request_json=None, central_hub_json=None) -> None:
    # Normalize product names in request_json
    request_json = normalize_product_names(request_json)

    if request_json is None:
        # Update the default request json
        # request_json = {
        #     "outlet_id": "1",
        #     "outlet_location": "Chennai",
        #     "central_hub_location": "Bangalore",
        #     "date": "2023-12-07T15:04:05Z",
        #     "event": "Summer Fashion Festival",
        #     "event_description": "The upcoming Summer Fashion Festival is expected to significantly increase the demand for fashion retail. We anticipate higher footfall in our Chennai store due to the festival season. T-shirts and dresses are particularly in demand during summer festivals in South India.",
        #     "client_preferences": "Chennai customers prefer comfortable cotton clothing due to the warm climate. T-shirts and traditional formal wear are popular among the working professionals. Current fashion trends show increased demand for casual tops and western wear.",
        #     "weather": "warm and humid",
        #     "outlet_inventory": {
        #         "t_shirt": {
        #             "current_storage_amount": 100,
        #             "daily_replenishment_without_envent_from_central_hub": 30,
        #             "max_warehouse_capacity": 500
        #         },
        #         "dress": {
        #             "current_storage_amount": 200,
        #             "daily_replenishment_without_envent_from_central_hub": 50,
        #             "max_warehouse_capacity": 300
        #         },
        #         "pants": {
        #             "current_storage_amount": 150,
        #             "daily_replenishment_without_envent_from_central_hub": 40,
        #             "max_warehouse_capacity": 400
        #         },
        #         "tops": {
        #             "current_storage_amount": 150,
        #             "daily_replenishment_without_envent_from_central_hub": 40,
        #             "max_warehouse_capacity": 500
        #         }
        #     }
        # }
        with open('Responsive-AI-Clusters-in-Supply-Chain/data/default_data_role_playing.json', 'r') as f:
            response_json = json.load(f)['outlet']

    # Copy the central hub json
    _central_hub_json = central_hub_json.copy()
    user_id = request_json["outlet_id"]
    with open('Responsive-AI-Clusters-in-Supply-Chain/data/default_data_role_playing.json', 'r') as f:
        response_json = json.load(f)['output_format']
    # response_json = {
    #     "outlet_inventory": {
    #         "t_shirt": {
    #             "future_storage_amount": "<NUM>",
    #             "specific_reason_of_replenishment": "<STRING>",
    #         },
    #         "dress": {
    #             "future_storage_amount": "<NUM>",
    #             "specific_reason_of_replenishment": "<STRING>",
    #         },
    #         "pants": {
    #             "future_storage_amount": "<NUM>",
    #             "specific_reason_of_replenishment": "<STRING>",
    #         },
    #         "tops": {
    #             "future_storage_amount": "<NUM>",
    #             "specific_reason_of_replenishment": "<STRING>",
    #         },
    #     },
    #     "transportation_duration": "<NUM> day"
    # }


    # Add the central hub inventory to the request
    input_json = request_json | central_hub_json

    print('input_json: ', input_json)

    context_text = "===== CONTEXT =====\n" + json.dumps(input_json, indent=4) + """
The \"historical_daily_replenishment_amount_from_central_hub\" means the average daily replenishment amount from the central hub to the outlet in the past. So it could be used as a reference for the replenishment amount in the future.
The \"max_warehouse_capacity\" means the maximum capacity of the warehouse of the outlet.
The \"specific_reason_of_replenishment\" means the specific reason of replenishment for the outlet (the decisions made by the central hub) at present.
THe current storage amount of the outlet should be less than the maximum capacity of the warehouse of the outlet.
While making decisions, the central hub should first consider the neccessary information in the context, and then predict what is the unknown demand of outlet in the event.
"""
    task_prompt = "In order to help the outlet to handle the upcoming events well, " + \
        "please make decisions based on the known information (you need to show the basis and the thoughts specifically). " + \
        "The standard of the task completion is that the AI assistant (Event Logistics Coordinator of Outlet) MUST make sure every BLANKs in the JSON template are filled with sertain values or strings."

    answer_template = "===== JSON TEMPLATE =====\n"
    answer_template += json.dumps(response_json, indent=4)
    print('answer_template: ', answer_template)
    assistant_answer_template = answer_template

    chat_record = context_text
    print('context_text: ', context_text)

    ai_user_role = "Fashion Retail Inventory Manager"
    ai_user_description = """This expert specializes in fashion retail inventory management with deep understanding of:
- Seasonal fashion trends and demand patterns
- Regional clothing preferences across Chennai, Bangalore, Mumbai, and Pune
- Climate-specific clothing requirements
- Festival and event-based fashion demand
- Supply chain optimization for fashion retail
Their duties include forecasting fashion trends, managing stock levels, and ensuring proper distribution across all retail locations."""
    ai_assistant_role = "Fashion Store Operations Coordinator"
    ai_assistant_description = """This expert has extensive experience in fashion retail operations with expertise in:
- Fashion retail event planning
- Regional fashion preferences
- Seasonal collection management
- Store inventory optimization
- Customer demand prediction
Their duties involve coordinating with the central warehouse, planning for fashion events and festivals, and ensuring optimal stock levels for different clothing categories."""

    # You can use the following code to play the role-playing game
    math_toolkit = MathToolkit()
    function_list = math_toolkit.get_tools()
    print('function_list: ', function_list)
    # assistant_model_config = FunctionCallingConfig.from_openai_function_list(
    #     function_list=function_list,
    #     kwargs=dict(temperature=0.7),
    # )
    # print('assistant_model_config: ', assistant_model_config)
    # assistant_model_config = ChatGPTConfig(temperature=0.7)
    # user_model_config = ChatGPTConfig(temperature=0.7)
    sys_msg_meta_dicts = [
        dict(
            assistant_role=ai_assistant_role, user_role=ai_user_role,
            assistant_description=ai_assistant_description + "\n" +
            context_text, user_description=ai_user_description)
        for _ in range(2)
    ]
    role_play_session = RolePlaying(
        assistant_role_name=ai_assistant_role,
        user_role_name=ai_user_role,
        assistant_agent_kwargs=dict(
            model=model,
            tools=function_list,
        ),
        user_agent_kwargs=dict(
            model=model,
        ),
        task_type=TaskType.ROLE_DESCRIPTION,
        task_prompt=task_prompt + "\n" + assistant_answer_template,
        with_task_specify=False,
        extend_sys_msg_meta_dicts=sys_msg_meta_dicts,
    )

    print(Fore.YELLOW + f"Original task prompt:\n{task_prompt}\n")
    print(Fore.CYAN + f"Assistant prompt:\n{role_play_session.assistant_sys_msg.content}\n")
    print(Fore.MAGENTA + f"User prompt:\n{role_play_session.user_sys_msg.content}\n")
 
    n = 0
    input_assistant_msg = role_play_session.init_chat()  # Adjusted to handle single return value
    while n < chat_turn_limit:
        n += 1
        assistant_response, user_response = role_play_session.step(
            input_assistant_msg
        )

        if assistant_response.terminated:
            print(Fore.GREEN +
                  ("AI Assistant terminated. Reason: "
                   f"{assistant_response.info['termination_reasons']}."
                  ))
            break
        if user_response.terminated:
            print(Fore.GREEN +
                  ("AI User terminated. "
                   f"Reason: {user_response.info['termination_reasons']}."
                  ))
            break

        print(Fore.BLUE + f"{ai_user_role}:\n\n{user_response.msg.content}\n")
        print(Fore.GREEN + f"{ai_assistant_role}:\n\n{assistant_response.msg.content}\n")

        # Output the msg to the markdown file: chat_record.md, and if the file does not exist, create it
        event_name = request_json['event'].replace(" ", "_")  # Replace spaces with underscores for filename
        # 'back_end/ai/chat_record/chat_record_<event_name>.md'
        file_path = os.path.join(os.path.dirname(__file__), "chat_record", f"chat_record_{event_name}.md")
        with open(file_path, "a", encoding="utf-8") as f:  # Specify UTF-8 encoding
            user_msg_md = user_response.msg.content.replace('\n', '\n\n')
            assistant_msg_md = assistant_response.msg.content.replace('\n', '\n\n')
            f.write(f"[{ai_user_role}]:\n\n{user_msg_md}\n\n\n")
            f.write(f"[{ai_assistant_role}]:\n\n{assistant_msg_md}\n\n\n")

        messages_queue.put({"sender_id": user_id, "user_message": user_response.msg.content, "assistant_message": assistant_response.msg.content})
        print(Fore.WHITE + f"The length of the messages_queue is {messages_queue.qsize()}\n")

        chat_record += (f"[{ai_user_role}]:{user_response.msg.content}\n\n" + \
            f"[{ai_assistant_role}]:{assistant_response.msg.content}\n\n")

        if "CAMEL_TASK_DONE" in user_response.msg.content or \
            "CAMEL_TASK_DONE" in assistant_response.msg.content:

            format_agent = FormatAgent(model = model)  # To make the output more readable, we use GPT-4 only
            output_text = format_agent.run(
                user_role_name=ai_user_role,
                assistant_role_name=ai_assistant_role,
                chat_record=chat_record,
                answer_template=response_json,
                # functions=math_toolkit.get_functions(),
            ).replace("\'", "\"")
            output_text = re.sub(r'(\w)"(\w)', r'\1\"\2', output_text)
            print(Fore.BLUE + f"output_text:\n{output_text}\n")

            # Extract the json format in the output_text, while the output_text is a string including the json format and other strings
            role_playing_output_json = json.loads(re.search(r'{.*}', output_text, re.DOTALL).group())
            print(Fore.BLUE + f"role_playing_output_json:\n{json.dumps(role_playing_output_json, indent=4)}\n")
            try:
                role_playing_output_json["transportation_duration"] = [int(s) for s in role_playing_output_json["transportation_duration"].split() if s.isdigit()][0]
                if role_play_session["transportation_duration"] >= 7:
                    role_playing_output_json["transportation_duration"] = 3
            except:
                role_playing_output_json["transportation_duration"] = 1
            # Example of role_playing_output_json
            # {
            #     "outlet_inventory": {
            #         "olive_oil": {
            #             "future_storage_amount": "150",
            #             "specific_reason_of_replenishment": "Expected high demand for Bastille Day event"
            #         },
            #         "baguette": {
            #             "future_storage_amount": "250",
            #             "specific_reason_of_replenishment": "Moderate demand expected for Bastille Day event"
            #         },
            #         "manchego_cheese": {
            #             "future_storage_amount": "400",
            #             "specific_reason_of_replenishment": "Strong preference and high demand expected for Bastille Day event"
            #         },
            #         "black_tea": {
            #             "future_storage_amount": "50",
            #             "specific_reason_of_replenishment": "Minimal interest expected for Bastille Day event"
            #         }
            #     },
            #     "transportation_duration": 2
            # }
            break

        input_assistant_msg = assistant_response.msg

    # Convert string into JSON
    outlet_inventory_json = role_playing_output_json["outlet_inventory"]
    trasportation_duration_json = role_playing_output_json["transportation_duration"]

    # Calculate the changed replenishment amount from central hub
    for product in outlet_inventory_json:
        normalized_product = product.lower().replace("_", "-")  # Ensure consistent formatting
        print(request_json["outlet_inventory"])
        current_storage_amount = request_json["outlet_inventory"][normalized_product]["current_storage_amount"]
        future_storage_amount = outlet_inventory_json[product]["future_storage_amount"]
        changed_replenishment_amount_from_central_hub = int(future_storage_amount) - int(current_storage_amount)
        if changed_replenishment_amount_from_central_hub < 0:
            changed_replenishment_amount_from_central_hub = 0
        central_hub_json["central_hub_inventory"][product]["current_storage_amount"] -= changed_replenishment_amount_from_central_hub

        outlet_inventory_json[product]["future_storage_amount"] = int(future_storage_amount)

    # Format the final answer json
    final_answer_json = {
        "outlet_inventory": outlet_inventory_json,
        "central_hub_inventory": central_hub_json["central_hub_inventory"],
        "transportation_duration": trasportation_duration_json
    }

    print(Fore.RED + f"original_outlet_json:\n{json.dumps(request_json, indent=4)}\n")
    print(Fore.RED + f"original_central_hub_json:\n{json.dumps(_central_hub_json, indent=4)}\n")
    print(Fore.RED + f"final_answer_json:\n{json.dumps(final_answer_json, indent=4)}\n")
    print(Fore.RESET)
    return final_answer_json, central_hub_json
