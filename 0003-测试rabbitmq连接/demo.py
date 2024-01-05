import pika

# RabbitMQ服务器的连接参数
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)

try:
    connection = pika.BlockingConnection(parameters)
    print("Successfully connected to RabbitMQ server!")
    connection.close()
except Exception as e:
    print("Failed to connect to RabbitMQ server:", str(e))
