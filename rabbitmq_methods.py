import pika
import time
import logging
from pymongo import MongoClient
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    _mongodbClient = MongoClient("mongodb+srv://sudev:ne46E5KNqwDRhd3q@users.xvkvk7p.mongodb.net/interview_db")
    db = _mongodbClient.interview_db
    collection = db.usernames
except Exception as ex:
    logger.error(f"Error connecting to MongoDB: {str(ex)}")
    exit(1)

def callback(ch, method, properties, body):
    username = body.decode('utf-8')
    user = {'username': username}
    collection.insert_one(user)
    logger.info(f"USERNAME :> {username} Saved.")

def connect_to_rabbitmq():
    retries = 15
    for _ in range(retries):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
            logger.info("Connected to RabbitMQ!")
            channel = connection.channel()
            channel.queue_declare(queue='username_queue', durable=True)
            channel.basic_consume(queue='username_queue', on_message_callback=callback, auto_ack=True)
            logger.info('Consumer Service: Waiting for messages...')
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as ex:
            logger.error("Failed to connect to RabbitMQ. Retrying...")
            time.sleep(2)
        except Exception as ex:
            logger.error(f"Error in RabbitMQ connection: {str(ex)}")
            break

def send_username_to_queue(username):
    try:
        existing_user = collection.find_one({'username': username})
        if existing_user:
            raise HTTPException(status_code=400, detail='Username already exists in the database.')

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='username_queue', durable=True)
        channel.basic_publish(exchange='',
                              routing_key='username_queue',
                              body=username,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,
                              )
        )
        connection.close()
        time.sleep(5)
        return {'detail': f'{username} successfully sent to the queue.'}
    except Exception as ex:
        logger.error(f"Error performing MongoDB operation or sending message to RabbitMQ: {str(ex)}")
        raise HTTPException(status_code=500, detail='Internal Server Error.')
