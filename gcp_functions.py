import argparse
import os
from google.cloud import pubsub

dir_path = str(os.path.dirname(os.path.realpath('gcp_functions.py')))
os.environ["GOOGLE_CLOUD_PROJECT"] = 'Small-Vivacity-Projects'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '%s/backend/secrets/Small-Vivacity-Projects-f502d9066757.json'%dir_path
pubsub_client = pubsub.Client().from_service_account_json('%s/backend/secrets/Small-Vivacity-Projects-f502d9066757.json'%dir_path)
#topic = pubsub_client.topic(topic)


def publish_message(topic_name, data):
    """Publishes a message to a Pub/Sub topic with the given data."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)

    # Data must be a bytestring
    data = data.encode('utf-8')

    message_id = topic.publish(data)

    print('Message {} published.'.format(message_id))

def receive_message(topic_name, subscription_name):
    """Receives a message from a pull subscription."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)
    subscription = topic.subscription(subscription_name)

    # Change return_immediately=False to block until messages are
    # received.
    results = subscription.pull(return_immediately=True,max_messages=100)

    print('Received {} messages.'.format(len(results)))

    #for ack_id, message in results:
     #   print('* {}: {}, {}'.format(
      #     message.message_id, message.data, message.attributes))
    for ack_id, message in results:
        print('* {}: {}'.format(
            message.message_id, message.data))

    # Acknowledge received messages. If you do not acknowledge, Pub/Sub will
    # redeliver the message.
    if results:
        subscription.acknowledge([ack_id for ack_id, message in results])





