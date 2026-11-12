from transaction_generator import generate_transaction
from ingestion import process_transaction
from database import create_database

create_database()

#case 1 : valid transaction
transaction=generate_transaction()
print("generated transaction:",transaction)
process_transaction(transaction)

#Case 2 :invalid transaction(negative amount)
negative=generate_transaction()
negative["amount"]=-100.0
print("generated transaction with negative amount:",negative)
process_transaction(negative)

#Case 3: missing required fileds(customer_id)
missing_field=generate_transaction()
missing_field["customer_id"]= "None"
process_transaction(missing_field)

#Case 4: Duplicate transaction_id
duplicate=generate_transaction()
duplicate["transaction_id"]=transaction["transaction_id"]
print("generated transaction with duplicate transaction_id:",duplicate)
process_transaction(duplicate)