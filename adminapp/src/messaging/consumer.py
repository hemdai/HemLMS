# amqps://wltlylfg:LqIb8xLhIanGaBczd9YOEq3g7djjqgsm@kebnekaise.lmq.cloudamqp.com/wltlylfg
import pika

params = pika.ConnectionParameters(host="localhost")
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue="admin")


def callback(ch, method, properties, body):
    print("recieved in admin_app")
    print(body)


channel.basic_consume(queue="admin", on_message_callback=callback)

print("Started Consuming")

channel.start_consuming()

channel.close()
