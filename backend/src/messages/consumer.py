# amqps://wltlylfg:LqIb8xLhIanGaBczd9YOEq3g7djjqgsm@kebnekaise.lmq.cloudamqp.com/wltlylfg
import pika

connection_parameters = pika.ConnectionParameters("localhost")
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

channel.queue_declare(queue="main")


def callback(ch, method, properties, body):
    print("recieved in backend_main_api")
    print(body)


channel.basic_consume(queue="main", on_message_callback=callback)

print("Started Consuming")

channel.start_consuming()

channel.close()
