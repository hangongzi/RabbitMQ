import pika

class Consumer:
    def __init__(self):
        self.username = 'csh'#指定远程rabbitmq的用户名密码
        self.pwd = 'csh'
        self.user_pwd = pika.PlainCredentials(self.username, self.pwd)
        self.s_conn = pika.BlockingConnection(pika.ConnectionParameters('192.168.142.130', credentials=self.user_pwd))#创建连接
        self.chan = self.s_conn.channel()#在连接上创建一个频道

        self.chan.queue_declare(queue='hello')#声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行


    def callback(ch,method,properties,body): #定义一个回调函数，用来接收生产者发送的消息
        print("[消费者] recv %s" % body)

    def consum_func(self):
        self.chan.basic_consume(self.callback,  #调用回调函数，从队列里取消息
                           queue='hello',#指定取消息的队列名
                           no_ack=True) #取完一条消息后，不给生产者发送确认消息，默认是False的，即  默认给rabbitmq发送一个收到消息的确认，一般默认即可
        print('[消费者] waiting for msg .')
        self.chan.start_consuming()#开始循环取消息

if __name__ == '__main__':
    consumer = Consumer()
    consumer.consum_func()