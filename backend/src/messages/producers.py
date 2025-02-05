# amqps://wltlylfg:LqIb8xLhIanGaBczd9YOEq3g7djjqgsm@kebnekaise.lmq.cloudamqp.com/wltlylfg
import pika

params = pika.ConnectionParameters(host="rabbitmq", port=5672)
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish():
    channel.basic_publish(exchange="", routing_key="admin", body="hello")
