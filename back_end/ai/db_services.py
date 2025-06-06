from pymongo import MongoClient

# MongoDB connection details
MONGO_CONNECTION_STRING = "mongodb+srv://sruthiheidi:LT0gazBKdfpkUdIB@cluster0.awtdiwf.mongodb.net/"
MONGO_DB = "supplychain_management"
MONGO_COLLECTION = "project_inventory"

# Connect to MongoDB
client = MongoClient(MONGO_CONNECTION_STRING)
db = client[MONGO_DB]
inventory_collection = db[MONGO_COLLECTION]

def fetch_inventory_data():
    """
    Fetch inventory data from MongoDB.
    Returns:
        dict: Inventory data with product names as keys and their details as values.
    """
    inventory_data = {}
    # Assuming there is only one document containing the central_hub_inventory
    document = inventory_collection.find_one()
    if document and "central_hub_inventory" in document:
        inventory_data = document["central_hub_inventory"]
    return inventory_data

def replenish_inventory(product_id, amount):
    """
    Replenish inventory for a specific product in MongoDB.
    Args:
        product_id (str): The ID of the product to replenish.
        amount (int): The amount to set as the new storage amount.
    """
    inventory_collection.update_one(
        {"central_hub_inventory." + product_id: {"$exists": True}},
        {"$set": {"central_hub_inventory." + product_id + ".current_storage_amount": amount}}
    )
    print(f"Product {product_id} replenished to {amount}.")