import pika
import os
import time
import logging


class Consumer:

    def __init__(self):
      self.msg = ""

    def pdf_process_function(self):
        print(" PDF processing")
        print(" [x] Received " + str(self.msg))

        time.sleep(5)  # delays for 5 seconds
        print(" PDF processing finished")
        return

    # create a function which is called on incoming messages
    def callback(self, ch, method, properties, body):
        self.msg = body
        self.pdf_process_function()

    def consume(self):

        # Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
        url = os.environ.get(
            'CLOUDAMQP_URL', 'amqp://username:password@rabbitmq:5672')

        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()  # start a channel
        channel.queue_declare(queue='pdfprocess')  # Declare a queue

        # set up subscription on the queue
        channel.basic_consume('pdfprocess',
                      self.callback,
                      auto_ack=True)

        # start consuming (blocks)
        channel.start_consuming()
        connection.close()
        return

def callConsumer():
  consumer = Consumer()
  consumer.consume()



