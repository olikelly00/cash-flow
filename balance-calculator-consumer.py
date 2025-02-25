from confluent_kafka import Consumer
import json

consumer = Consumer(
    {'bootstrap.servers': 'localhost:9092', 
     'group.id': 'balance_calculator', 
     'auto.offset.reset': 'latest'}
     )

transaction_summary = {}

consumer.subscribe(['transactions'])

while True:
    message = consumer.poll(1.0)
    if message is None:
        continue
    if message.error():
        print('consumer error')
        continue

    value = message.value()
    json_value = value.decode('utf-8')

    dictionary = json.loads(json_value)

    if 'account' in dictionary:
        account_id = str(dictionary['account'])


    if 'transaction_summary' in dictionary.keys():
        transaction_details = dictionary['transaction_summary']
        print(transaction_details)
        print(transaction_details.keys())
        transaction_summary[f"Transactions for Customer ID {account_id}"] = transaction_summary.get(f"Transactions for Customer ID {account_id}", 0) + 1
       
    print(transaction_summary)
    consumer.close()





