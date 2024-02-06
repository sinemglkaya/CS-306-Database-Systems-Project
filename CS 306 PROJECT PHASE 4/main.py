from connect import connectDB
from dummy_data import customer_complaints, item_comments
from pymongo import MongoClient, errors
from bson.objectid import ObjectId


def insert_into_collection(db, collection_name, data):
    try:
        collection = db[collection_name]
        result = collection.insert_one(data)
        print("Insertion successfully completed.")
        print(f"Inserted document ID: {result.inserted_id}")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_data_for_customer_complaint():
    return {
        "customer_id": input("Enter customer ID: "),
        "customer_name": input("Enter customer name: "),
        "product_id": input("Enter product ID: "),
        "complaint_description": input("Enter complaint description: "),
    }

def get_data_for_item_comment():
    return {
        "item_type": input("Enter item type (e.g., Smart-Phone, Laptop, TV): "),
        "item_brand": input("Enter item brand (e.g., Apple, Lenovo, LG): "),
        "user_id": input("Enter user ID: "),
        "comment": input("Enter comment: "),
        "rating": int(input("Enter rating (1-5): ")),
    }

def handle_insertion(db):
    print("Please select the collection you want to insert data into:")
    print("1 - Customer Complaints")
    print("2 - Item Comments")
    selected_option = input("Selected option: ")

    if selected_option == "1":
        data = get_data_for_customer_complaint()
        #insert_into_collection(db, "orders", data)
        insert_into_collection(db, "customer_complaints", data)

        
    elif selected_option == "2":
        data = get_data_for_item_comment()
        insert_into_collection(db, "item_comments", data)
        #insert_into_collection(db, "orders", data)
    else:
        print("Invalid collection selected.")

# Define other necessary functions such as delete_record_by_id, update_record_by_id, etc.


def create_collection(db):
    collection_name = input("Enter the name of the new collection to create: ")
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
        print(f"Collection '{collection_name}' created.")
        if (collection_name == "customer_complaints"):
            for item in customer_complaints:
                insert_into_collection(db, "customer_complaints", item)
        elif (collection_name == "item_comments"):
            for item in item_comments:
                insert_into_collection(db, "item_comments", item)
    else:
        print(f"Collection '{collection_name}' already exists.")
# Function to read all data from a collection
def read_all_data(db):
    collection_name = input("Enter the name of the collection to read from: ")
    collection = db[collection_name]
    documents = collection.find()
    for doc in documents:
        print(doc)

# Function to filter and read data from a collection
def filter_data(db):
    collection_name = input("Enter the name of the collection to filter data from: ")
    filter_field = input("Enter the field name to filter by: ")
    filter_value = input("Enter the field value to filter by: ")
    collection = db[collection_name]
    documents = collection.find({filter_field: filter_value})
    for doc in documents:
        print(doc)

# Function to delete data by ID
def delete_record_by_id(db):
    collection_name = input("Enter the collection name to delete from: ")
    record_id_str = input("Please enter the ID of the record to delete: ")
    try:
        collection = db[collection_name]
        result = collection.delete_one({'_id': ObjectId(record_id_str)})
        if result.deleted_count > 0:
            print(f"Successfully deleted record with ID {record_id_str}")
        else:
            print(f"No record found with ID {record_id_str}")
    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")

# Function to update data by ID
def update_record_by_id(db):
    collection_name = input("Enter the collection name to update: ")
    record_id_str = input("Please enter the ID of the record to update: ")
    update_field = input("Enter the field name to update: ")
    update_value = input("Enter the new value for the field: ")
    try:
        collection = db[collection_name]
        result = collection.update_one({'_id': ObjectId(record_id_str)}, {'$set': {update_field: update_value}})
        if result.modified_count > 0:
            print(f"Successfully updated record with ID {record_id_str}")
        else:
            print(f"No record found with ID {record_id_str} or no change was made.")
    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")

def main_menu():
    print("\nWelcome to the Review Portal!")
    user_id = input("Please enter your user id: ")
    print(f"User ID: {user_id} recognized.")
    print("Please pick the option that you want to proceed.")
    print("1 - Create a collection.")
    print("2 - Read all data in a collection.")
    print("3 - Read some part of the data while filtering.")
    print("4 - Insert data.")
    print("5 - Delete data.")
    print("6 - Update data.")
    return input("Selected option: ")

if __name__ == "__main__":
    db = connectDB()

    while True:
        option = main_menu()

        if option == "1":
            create_collection(db)
            #create_collection(db)

        elif option == "2":
            read_all_data(db)
            #read_all_data(db)
        elif option == "3":
            filter_data(db)
        elif option == "4":
            handle_insertion(db)
        elif option == "5":
            delete_record_by_id(db)
        elif option == "6":
            update_record_by_id(db)
        else:
            print("Invalid option selected or exiting the Service Portal.")
            break

        continue_choice = input("Would you like to do something else? (yes/no): ").lower()
        if continue_choice != "yes":
            print("Thank you for using the Review Portal. Goodbye!")
            break

