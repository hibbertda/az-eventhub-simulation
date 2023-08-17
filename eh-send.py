# generate and send test data to an azure eventhub
# https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-python-get-started-send
# https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-python-get-started-receive-eph
# https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-python-get-started-send#send-events-to-an-event-hub

import os
import json
import time
import argparse
import logging
import datetime
import asyncio

from random import randint
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient
from faker import Faker

# logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)

# pull variables from environment
EVENTHUB_CONNECTION_STRING = os.environ.get('EVENTHUB_CONNECTION_STRING')
EVENTHUB_NAME = os.environ.get('EVENTHUB_NAME')

fake = Faker('en_US')

# Number of events to be sent to the event hub in each batch.
# 200 events == 100kb
BATCH_COUNT = 200

# Number of batches to be sent.
BATCH_SEND_COUNT = 500

# Generate random data in JSON format.
def generate_data():
  rand_json= {    
    'id': randint(0, 100),    
    'customerInfo': {
      'name': fake.name(), 
      'phone': fake.phone_number(),
      'creditCard': fake.credit_card_full(),
      'address': {
          'street': fake.street_address(),
          'city': fake.city(),
          'state': fake.state(),
          'zip': fake.zipcode(),
          'country': fake.country(),
          'countryCode': fake.country_code()
      }
    },
    'description': fake.text()
    }
  return rand_json


async def send_batch(producer):
  event_data_batch = await producer.create_batch()

  # add events to the batch
  for i in range(BATCH_COUNT):
    data = generate_data()
    event_data_batch.add(EventData(json.dumps(data)))
  
  # send the batch of events to the event hub
  await producer.send_batch(event_data_batch)

async def main():
  async with EventHubProducerClient.from_connection_string(
      conn_str=EVENTHUB_CONNECTION_STRING, eventhub_name=EVENTHUB_NAME
  ) as producer:
      tasks = []
      for i in range(BATCH_SEND_COUNT):
          tasks.append(asyncio.create_task(send_batch(producer)))
      await asyncio.gather(*tasks)


if __name__ == "__main__":
  asyncio.run(main())







