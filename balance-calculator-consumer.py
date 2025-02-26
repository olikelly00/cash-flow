from confluent_kafka import Consumer
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")
logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s")





transaction_summary = {}

try:
    consumer = Consumer(
    {'bootstrap.servers': 'localhost:9092', 
     'group.id': 'balance_calculator', 
     'auto.offset.reset': 'latest'}
     )
    consumer.subscribe(['transactions'])
except Exception as e:
    logging.warning("Error connecting to topic {e}.\nMake sure the topic exists by running the following CLI command:  bin/kafka-topics.sh --create --topic [INSERT_TOPIC_NAME] --bootstrap-server localhost:9092")



while True:
    message = consumer.poll(1.0)
    if message is None:
        logging.error("Loading new messages from stream... This can take a few moments when starting up. Will try again in 1 second.")
        continue
    if message.error():
        logging.error("Stream returned an error. Will try again in 1 second.")
        continue

    value = message.value()
    json_value = value.decode('utf-8')

    dictionary = json.loads(json_value)

    if 'account' in dictionary:
        account_id = str(dictionary['account'])


    if 'transaction_summary' in dictionary.keys():
        transaction_details = dictionary['transaction_summary']
        
        transaction_summary[f"Transactions for Customer ID {account_id}"] = transaction_summary.get(f"Transactions for Customer ID {account_id}", 0) + 1
       
    logging.info(f"New transaction summary received!\nTransaction ID: {dictionary['transaction_id']}\nAccount Number: {dictionary['account']}\nTransaction Type: {dictionary['transaction_type']}\nChange in balance: {'-' + str(dictionary['amount']) if dictionary['transaction_type'] == 'Debit' else '+' + str(dictionary['amount'])}\nNew Account Balance {dictionary['new balance']}\n--------------------")









