import pika
import sys

class Producor:
    def __init__(self):
        self.username = 'csh'
        self.pwd = 'csh'
        self.user_pwd = pika.PlainCredentials(self.username, self.pwd)
        self.s_conn = pika.BlockingConnection(pika.ConnectionParameters('192.168.142.130', credentials=self.user_pwd))
        self.chan = self.s_conn.channel()
        # durable=True，设置支持持久化
        self.chan.queue_declare(queue='task_queue', durable=True)

    def Publish(self):
        message = ' '.join(sys.argv[1:]) or "Hello World!"
        #properties= 持久化设置
        self.chan.basic_publish(exchange='', routing_key='task_queue', body=message, properties=pika.BasicProperties(delivery_mode=2,))
        print("[Pruducor] send %r"%message)
        self.s_conn.close()

if __name__ == '__main__':
    product = Producor()
    product.Publish()
