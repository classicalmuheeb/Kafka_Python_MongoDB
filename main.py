from faker import Faker
from info import BenefitsProvider, EthnicityProvider
from kafka import KafkaProducer, KafkaConsumer
import json, random, time, logging
from pymongo import MongoClient

logging.basicConfig(level=logging.ERROR)

my_fake = Faker()

my_fake.add_provider(BenefitsProvider)
my_fake.add_provider(EthnicityProvider)

#Connect to MongoDB and Database
try:
    client = MongoClient('localhost', 27017)
    collection = client.testing_kafka.staff_information
    print('Connection successful')
except:
    print('Oops! sorry, we couldnt connect')


#method to generate message
def staff_information(): 
    message = {
        "Name": my_fake.unique.name(),
        "Address": my_fake.unique.address(),
        "Ethnicity": my_fake.ethnic(),
        "Year_Joined": my_fake.year(),
        "Compensation": my_fake.benefit(),
        "Account_Number": my_fake.iban(),
    }
    return message

#method for producing messages for Kafka
def produce_kafka_messages(hostname='127.0.0.1', 
                            port='9092', 
                            topic_name='staffInformation',
                            nr_messages=10, 
                            max_waiting_time_in_sec=5 #send message after 5 seconds
                            ):
                            producer = KafkaProducer(
                                bootstrap_servers=hostname+":"+port,
                                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                            )

                            if nr_messages <= 0:
                                nr_messages = float('inf')
                            i = 0

                            while i < nr_messages:
                                message = staff_information()
                                print('Sending: {}'.format(message))

                                producer.send(topic_name, value=message)

                                #wait for couple of seconds
                                sleep_time = random.randint(0, max_waiting_time_in_sec + 10) / 10
                                print("Sleeping for ..."+str(sleep_time)+'s')
                                time.sleep(sleep_time)

                                #force flush all messages
                                if (i % 100) == 0:
                                    producer.flush()
                                i = i + 1
                            producer.flush()

#consume the produced Kafka Message and ingest into MongoDB
def consume_kafka_messages():
       consumer = KafkaConsumer('staffInformation', 
                                 bootstrap_servers=['127.0.0.1:9092'], 
                                 auto_offset_reset='earliest', 
                                 enable_auto_commit=True,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')))
       try:
            #Parse data received from Kafka
            for message in consumer:
                record = message.value
                name = record["Name"]
                address = record["Address"]
                ethnicity = record["Ethnicity"]
                year_joined = record["Year_Joined"]
                compensation = record["Compensation"]
                account_number = record['Account_Number']
                
                #create a dictionary of data and parse into 
                try:
                    new_staff_record = {'name':name, 'address':address, 'ethnicity':ethnicity, 'year_joined':year_joined, 'account_number':account_number, 'compensation':compensation, 'account_number':account_number}
                    result = collection.insert_one(new_staff_record)
                    print('Items with {} has been added to {}'.format(result.inserted_id, collection.name))
                except:
                      print('Sorry, couldnot insert into MongoDB')
       except Exception as e:
             logging.error('Error encountered:', exc_info=True) 

       
if __name__ == "__main__":
    produce_kafka_messages()
    consume_kafka_messages()
