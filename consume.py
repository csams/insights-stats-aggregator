#!/usr/bin/env python
import argparse
import logging
import pika
import yaml

Loader = getattr(yaml, "CSafeLoader", yaml.Loader)

log = logging.getLogger(__name__)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("total", type=int)
    return p.parse_args()


class StatConsumer:
    def __init__(self, queue, conn_params, to_consume, auth=None, durable=False):
        self.to_consume = to_consume
        self.consumed = 0
        self.results = []

        creds = None if auth is None else pika.credentials.PlainCredentials(**auth)
        if creds is not None:
            conn_params["credentials"] = creds

        params = pika.ConnectionParameters(**conn_params)
        self.connection = pika.BlockingConnection(params)

        channel = self.connection.channel()
        channel.queue_declare(queue=queue, durable=durable)
        channel.basic_consume(queue=queue, on_message_callback=self._callback)
        self.channel = channel

    def process_results(self):
        pass

    def _callback(self, ch, method, properties, body):
        self.consumed += 1
        msg = yaml.load(body.decode("utf-8"), Loader=Loader)
        self.results.append(msg)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        if self.consumed == self.to_consume:
            self.process_results()
            self.connection.close()

    def run(self):
        self.channel.start_consuming()


def main():
    args = parse_args()
    total = args.total
    consumer = StatConsumer(
        "test_job_response", {"host": "localhost", "port": 5672}, total
    )
    consumer.run()
    print(yaml.dump(consumer.results))


if __name__ == "__main__":
    main()
