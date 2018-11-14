import pika
import sys

class EmitLog:
    def __init__(self):
        self.username = 'csh'  # 指定远程rabbitmq的用户名密码
        self.pwd = 'csh'
        self.user_pwd = pika.PlainCredentials(self.username, self.pwd)
        self.s_conn = pika.BlockingConnection(pika.ConnectionParameters('192.168.142.130', credentials=self.user_pwd))  # 创建连接
        self.channel = self.s_conn.channel()

        self.channel.exchange_declare(exchange='topic_logs', exchange_type='topic')


    def publish(self):
        routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
        message = ' '.join(sys.argv[2:]) or "Hello World!"
        self.channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=message)
        print(" [x] Sent %r:%r" % (routing_key,message))
        self.s_conn.close()

if __name__ == '__main__':
    emit = EmitLog()
    emit.publish()