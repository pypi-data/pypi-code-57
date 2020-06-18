import json
from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
from time import sleep
from typing import List
from typing import Mapping

from kafka import KafkaAdminClient
from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.admin import NewTopic

from watermill.expressions import get_field
from watermill.message_brokers.kafka_message_broker import KafkaMessageBroker
from watermill.message_brokers.message_broker import EndOfStream
from watermill.mill import WaterMill
from watermill.stream_join import JoinWith
from watermill.stream_join import join_streams
from watermill.stream_types import type_alias
from watermill.windows import window


@dataclass(frozen=True, eq=True)
class RobotLocation:
    robot_id: str
    time: int
    x: int
    y: int


@dataclass(frozen=True, eq=True)
class OccupiedCellsNumber:
    time: int
    cells_number: int


def calculate_cell_occupation(locations: List[RobotLocation], joined_locations: Mapping[RobotLocation, List[RobotLocation]]) -> OccupiedCellsNumber:
    time = locations[0].time
    cell_set = set()
    for location in locations:
        cell_set.add((int(location.x) // 50, int(location.y) // 50))
    return OccupiedCellsNumber(
        time=time,
        cells_number=len(cell_set)
    )


def window_parallel_streams():
    # assume we have N robots
    N = 10

    topic_names = {
        OccupiedCellsNumber: 'cells-occupation',
    }

    for i in range(N):
        topic_names[type_alias(RobotLocation, f"robot-{i}")] = f'robot-locations-{i}'

    message_broker = KafkaMessageBroker(
        topic_names=topic_names,
        kafka_url='kafka:9092'
    )

    mill = WaterMill(
        broker=message_broker,
        process_func=calculate_cell_occupation,
        join_tree=join_streams(
            window(
                cls=type_alias(RobotLocation, f"robot-0"),
                window_expression=get_field('time') // 30
            ),
            *[JoinWith(
                with_type=type_alias(RobotLocation, f"robot-{i}"),
                left_expression=get_field('time') // 30,
                right_expression=get_field('time') // 30
            ) for i in range(1, N)],
        ),
    )

    produce_robot_streams()

    mill.run()

    print('Fetching data from resulting stream')
    result_consumer = KafkaConsumer(
        bootstrap_servers='kafka:9092',
        group_id='result-consumer',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
    )
    result_consumer.subscribe(['cells-occupation'])
    for result in result_consumer:
        result_item = json.loads(result.value.decode('utf8'))
        print(json.dumps(result_item))
        if 'eos__' in result_item:
            break


def produce_robot_streams():
    N = 10
    recreate_topics([*[f'robot-locations-{i}' for i in range(N)], 'cells-occupation'])
    print('Sending data to input stream')

    kafka_producer = KafkaProducer(bootstrap_servers='kafka:9092')

    robots_file_path = Path(__file__).resolve().parent / 'samples' / 'robot-locations.json'
    with robots_file_path.open('r') as f:
        robots = json.load(f)

    for robots_item in robots:
        for i in range(10):
            item = dict(robots_item)
            topic_name = f'robot-locations-{i}'
            item['robot_id'] = str(i)
            item['x'] += i
            item['y'] += 10 - i
            print(item)
            kafka_producer.send(topic_name, value=json.dumps(item).encode('utf8'))

    for i in range(10):
        kafka_producer.send(f'robot-locations-{i}', value=json.dumps(asdict(EndOfStream())).encode('utf8'))
    kafka_producer.flush()


def recreate_topics(topics: List[str]):
    kafka_admin_client = KafkaAdminClient(
        bootstrap_servers='kafka:9092',
    )
    try:
        kafka_admin_client.delete_topics(topics)
    except Exception as exc:
        pass
    sleep(0.1)
    try:
        kafka_admin_client.create_topics([NewTopic(name=topic, num_partitions=1, replication_factor=1) for topic in topics])
    except Exception as exc:
        print(exc)


if __name__ == "__main__":
    window_parallel_streams()
