from confluent_kafka import Producer
import socket
import random
import json
from time import sleep
import uuid

kafka_producer_config = {
    "bootstrap.servers": "localhost:9092",
    "client.id": socket.gethostname(),
}

producer = Producer(kafka_producer_config)

topic_name = "transactions"
transaction_types = ["Debit", "Credit"]

accounts = []

def generate_account():
    account = {"account_id": random.randint(1, 100), "balance": 100}
    return account


while len(accounts) < 5:
    account = generate_account()
    accounts.append(account)

def produce_event(topic_name):

    created_topics = producer.list_topics().topics

    if topic_name not in created_topics:
        raise Exception(
            f"Error: Topic {topic_name} does not exist. Must be created first using this CLI command: bin/kafka-topics.sh --create --topic {topic_name} --bootstrap-server localhost:9092"
        )
    while True:

        selected_account = accounts[random.randint(0, len(accounts)-1)]
        selected_account_id = selected_account["account_id"]
        amount = random.randint(1, 10)
        transaction_type = random.choice(transaction_types)

        transaction_summary = {}

        if transaction_type == "Debit":
            selected_account["balance"] -= amount
        elif transaction_type == "Credit":
            selected_account["balance"] += amount

        customer_key = f"Transactions for Customer ID {selected_account_id}"
        if customer_key in transaction_summary.keys():
            transaction_summary[f"Transactions for Customer ID {selected_account_id}"] += 1
        else:
            transaction_summary[f"Transactions for Customer ID {selected_account_id}"] = 1

        json_message = json.dumps(
            {
                "transaction_id": f"{selected_account_id}-{transaction_type}-{uuid.uuid1()}",
                "account": selected_account["account_id"],
                "transaction_type": transaction_type,
                "amount": amount,
                "new balance": selected_account["balance"],
                'transaction_summary': transaction_summary 
            }
        )

        producer.produce(
            topic_name,
            key="transaction",
            value=json_message.encode("utf-8"),
        )


        print(json_message)
        producer.flush()
        sleep(1)



produce_event(topic_name)

