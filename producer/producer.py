import json
import time
import pandas as pd
from confluent_kafka import Producer
kafka_server_config = {
    'bootstrap.servers': '*********************',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': '**************',
    'sasl.password': '******************************************',
    'session.timeout.ms': '45000'
}

def callback(err, event):
    if err:
        print(f'Produce to topic {event.topic()} failed for event: {event.key()}')
    else:
        val = event.value().decode('utf8')
        print(f'{val} sent to partition {event.partition()}.')


if __name__ == '__main__':
    df = pd.read_csv('final_produce.csv')
    df = df.iloc[[25], :-1]
    for index, row in df.iterrows():
        dic = {col: [row[col]] for col in df.columns}
        seri = json.dumps(dic)
        producer = Producer(kafka_server_config)
        producer.produce("transactions", key="10", value=seri, on_delivery=callback)
        producer.flush()
        time.sleep(3)