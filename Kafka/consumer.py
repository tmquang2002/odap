from kafka import KafkaConsumer

def consume_from_kafka(consumer, topic):
    consumer.subscribe([topic])

    try:
        while True:
            messages = consumer.poll(timeout_ms=1000)  # adjust the timeout as needed
            for partition, record_list in messages.items():
                for record in record_list:
                    print(f"Received message: {record.value.decode('utf-8')}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    kafka_bootstrap_servers = 'localhost:9092'
    kafka_topic = 'groupseven'

    consumer = KafkaConsumer(
        bootstrap_servers=kafka_bootstrap_servers,
        group_id='group7',
        auto_offset_reset='earliest',  # or 'latest' depending on your use case
        enable_auto_commit=True,
        auto_commit_interval_ms=1000,  # adjust the interval as needed
    )

    consume_from_kafka(consumer, kafka_topic)
