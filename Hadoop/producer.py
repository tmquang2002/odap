import csv
import time
from kafka import KafkaProducer
from confluent_kafka import Producer
from random import randint

def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield row

def send_to_kafka(producer, topic, data):
    value_bytes = bytes(str(data), 'utf-8') if data is not None else None
    assert type(value_bytes) in (bytes, bytearray, memoryview, type(None)), f"Invalid type: {type(value_bytes)}"

    producer.produce(topic, value=value_bytes)
    print(data)
    producer.flush()

def simulate_kafka_producer(csv_file, kafka_topic):
    producer_config = {
        'bootstrap.servers': 'localhost:9092',
        'client.id': 'network-status-producer'
    }
    producer = Producer(producer_config)

    for row in read_csv(csv_file):
        # Simulate random time delay between 1s to 3s
        time.sleep(randint(1, 3))
        
        # Send data to Kafka topic
        send_to_kafka(producer, kafka_topic, str(row))

if __name__ == "__main__":
    csv_file_path = 'credit_card.csv'
    kafka_topic = 'groupseven'

    simulate_kafka_producer(csv_file_path, kafka_topic)
