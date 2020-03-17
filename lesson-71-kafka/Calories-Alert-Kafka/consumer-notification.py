import json
from time import sleep

from kafka import KafkaConsumer

if __name__ == '__main__':
    parsed_topic_name = 'parsed_recipes'
    # Notify if a recipe has more than 200 calories
    calories_threshold = 400

    try:
        consumer = KafkaConsumer(parsed_topic_name, auto_offset_reset='earliest',
                                bootstrap_servers=['localhost:9092'], api_version=(0, 10), consumer_timeout_ms=1000)
    except Exception as ex:
        print('Exception while connecting KafkaConsumer')
        print(str(ex))
        exit(1)

    all_recipes = []
    for msg in consumer:
        record = json.loads(msg.value)
        all_recipes.append(record)
        calories = int(record['calories'])
        title = record['title']

        if calories > calories_threshold:
            print('Alert: {} calories count is {}'.format(title, calories))
        sleep(1)

    with open("all_recipes.json", "w") as f:
        f.write(json.dumps(all_recipes))

    if consumer is not None:
        consumer.close()
