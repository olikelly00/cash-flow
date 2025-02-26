from confluent_kafka import Consumer
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

kafka_consumer_config = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'mygroup',
        'auto.offset.reset': 'earliest'
    }

try:
    consumer = Consumer(kafka_consumer_config)
    consumer.subscribe(['transactions'])
except Exception as e:
    logging.warning("Error connecting to topic {e}.\nMake sure the topic exists by running the following CLI command:  bin/kafka-topics.sh --create --topic [INSERT_TOPIC_NAME] --bootstrap-server localhost:9092")


while True:
    message = consumer.poll(1.0)
    if message is None:
        logging.error("Couldn't retrieve new messages from stream. Will try again in 1 second.")
        continue
    if message.error():
        logging.error("Stream returned an error. {}. Will try again in 1 second.".format(message.error()))
        continue
    value = message.value()
    json_value = json.loads(value)
    logging.info(f"New transaction received! -- Trasaction ID - {json_value['transaction_id']} --  Account Number -- {json_value['account']} -- Transaction Type -- {json_value['transaction_type']}")
