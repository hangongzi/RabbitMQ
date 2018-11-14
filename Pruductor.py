import pika
import sys

class Producor:
    def __init__(self):
        self.username = 'csh'
        self.pwd = 'csh'
        self.user_pwd = pika.PlainCredentials(self.username, self.pwd)
        self.s_conn = pika.BlockingConnection(pika.ConnectionParameters('192.168.142.130', credentials=self.user_pwd))
        self.chan = self.s_conn.channel()

    def Publish(self):
        self.chan.queue_declare(queue='hello')
        self.chan.basic_publish(exchange='', routing_key='hello', body='Hello World!')
        print("[Pruducor] send 'Hello World!'")


if __name__ == '__main__':
    product = Producor()
    product.Publish()
