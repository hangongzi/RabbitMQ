import pika

class ReceiveLog:
    def __init__(self):
        self.username = 'csh'  # 指定远程rabbitmq的用户名密码
        self.pwd = 'csh'
        self.user_pwd = pika.PlainCredentials(self.username, self.pwd)
        self.s_conn = pika.BlockingConnection(
            pika.ConnectionParameters('192.168.142.130', credentials=self.user_pwd))  # 创建连接
        self.channel = self.s_conn.channel()

        self.channel.exchange_declare(exchange='logs',exchange_type='fanout')
        #定义队列类型，一旦连接关闭，队列删除
        self.result = self.channel.queue_declare(exclusive=True)
        #生成随机的队列名
        self.queue_name = self.result.method.queue
        #绑定队列（交换机名，队列名）
        self.channel.queue_bind(exchange='logs',queue=self.queue_name)

    def callback(self, ch, method, properties, body):
        print(" [x] %r"%body)

    def consume(self):
        self.channel.basic_consume(self.callback,queue=self.queue_name,no_ack=True)
        self.channel.start_consuming()

if __name__ == '__main__':
    rece = ReceiveLog()
    rece.consume()