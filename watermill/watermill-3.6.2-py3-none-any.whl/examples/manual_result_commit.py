import json
import math
import threading
import time
from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
from time import sleep
from typing import List
from typing import Mapping

from botox import Injector
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
from watermill.message_brokers.message_broker import DataKey


@dataclass(frozen=True, eq=True)
class RobotLocation:
    time: int
    x: int
    y: int


@dataclass(frozen=True, eq=True)
class RobotLocationNextStep:
    time: int
    x: int
    y: int


@dataclass(frozen=True, eq=True)
class RobotSpeed:
    time_from: int
    time_to: int
    speed: float


class Processor:
    def __init__(self, mill: WaterMill):
        self._mill = mill
        self._queue = []
        self._stop = False

    def stop(self):
        self._stop = True

    def _thread(self) -> None:
        while True:
            if self._queue:
                prev_location, next_location, data_key = self._queue.pop(0)
                time.sleep(0.3)
                self._mill.save_results(
                    data_key,
                    RobotSpeed(
                        time_from=prev_location.time,
                        time_to=next_location.time,
                        speed=math.sqrt(
                            math.pow(next_location.x - prev_location.x, 2) + math.pow(next_location.y - prev_location.y, 2))
                    )
                )
            if not self._queue and self._stop:
                break
            time.sleep(0.01)

    def calculate(self, prev_location: RobotLocation, next_location: RobotLocationNextStep, data_key: DataKey):
        self._queue.append((prev_location, next_location, data_key))

    def run(self):
        threading.Thread(target=self._thread).start()


def calculate_robot_speed(
        prev_location: RobotLocation,
        next_locations: Mapping[RobotLocation, List[RobotLocationNextStep]],
        data_key: DataKey,
        processor: Processor
) -> None:
    next_location = next_locations[prev_location][0]
    processor.calculate(prev_location, next_location, data_key)


def manual_result_commit():
    message_broker = KafkaMessageBroker(
        topic_names={
            RobotLocation: 'robot-locations',
            RobotLocationNextStep: 'robot-locations',
            RobotSpeed: 'robot-speed',
        },
        kafka_url='kafka:9092'
    )

    injector = Injector()

    mill = WaterMill(
        broker=message_broker,
        process_func=calculate_robot_speed,
        join_tree=join_streams(
            RobotLocation,
            JoinWith(
                with_type=RobotLocationNextStep,
                left_expression=get_field('time') + 10,
                right_expression=get_field('time')
            ),
        ),
        explicit_return_types=[RobotSpeed],
        injector=injector,
    )
    processor = Processor(mill)
    injector.prepare(Processor, processor)

    produce_goods_stream()

    processor.run()
    mill.run()
    processor.stop()

    print('Fetching data from resulting stream')
    result_consumer = KafkaConsumer(
        bootstrap_servers='kafka:9092',
        group_id='result-consumer',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
    )
    result_consumer.subscribe(['robot-speed'])
    for result in result_consumer:
        result_item = json.loads(result.value.decode('utf8'))
        print(json.dumps(result_item))
        if 'eos__' in result_item:
            break


def produce_goods_stream():
    recreate_topics(['robot-locations', 'robot-speed'])
    print('Sending data to input stream')

    kafka_producer = KafkaProducer(bootstrap_servers='kafka:9092')

    goods_file_path = Path(__file__).resolve().parent / 'samples' / 'robot-locations.json'
    with goods_file_path.open('r') as f:
        goods = json.load(f)

    for goods_item in goods:
        print(goods_item)
        kafka_producer.send('robot-locations', value=json.dumps(goods_item).encode('utf8'))

    kafka_producer.send('robot-locations', value=json.dumps(asdict(EndOfStream())).encode('utf8'))
    kafka_producer.flush()


def recreate_topics(topics: List[str]):
    kafka_admin_client = KafkaAdminClient(
        bootstrap_servers='kafka:9092',
    )
    try:
        kafka_admin_client.delete_topics(topics, timeout_ms=10000)
    except Exception as exc:
        print(exc)
    sleep(2)
    try:
        kafka_admin_client.create_topics([NewTopic(name=topic, num_partitions=1, replication_factor=1) for topic in topics])
    except Exception as exc:
        print(exc)


if __name__ == "__main__":
    manual_result_commit()
