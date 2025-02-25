from confluent_kafka import Consumer
import json

kafka_consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(kafka_consumer_config)

consumer.subscribe(['transactions'])

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue
    value = msg.value()
    json_value = json.loads(value)
    print("Received message: {}".format(json_value))
    consumer.close()