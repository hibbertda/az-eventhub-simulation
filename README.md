# EventHub Large File input

Using Python generate realistic json data to feed into an Azure Event Hub. The target is to have individual size of 100kb sent in larger batches.

## Requirements

Install required python modules

```bash

pip install -r requirements.txt

```

### Environmental Variables

Environment variables need to be setup with the **eventhub name** and **connection string**.

|variable|description|
|--|--|
|EVENTHUB_NAME|The name of the Eventhub. This needs to be the name of a specific EventHub and not just the EventHub namespace.|
|EVENTHUB_CONNECTION_STRING|The full connection string found under Shared Access Signatures. Requires claims to **Send**.|

```bash
export EVENTHUB_NAME=<your_eventhub_name>
export EVENTHUB_CONNECTION_STRING=<your_connection_string>
```

### Message Batching

In an attempt to push a significant amount of data into the EventHub of both messages in a batch and the number of batches. There are two options that manage the number of messages sent.

|variable|description|
|--|--|
|BATCH_COUNT|The number of records to include in each batch.|
|BATCH_SEND_COUNT|The number of batches to send|

```python
# Number of events to be sent to the event hub in each batch.
# 200 events == 100kb
BATCH_COUNT = 200

# Number of batches to be sent.
BATCH_SEND_COUNT = 500
```

### Data Generation

[Faker](https://faker.readthedocs.io/en/master/) is used to generate realistic looking JSON records. This can be modified to be more in line with the type of data you need to simulate, as long as it is still valid JSON.

```python
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
```
