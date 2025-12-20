from datetime import datetime
import pytz
import pandas as pd
from pymongo import MongoClient
connection_string = "Replace this text with MongoDB URL"
client = MongoClient(connection_string)
db = client['shopwithus']
collection = db['users']
documents = collection.find()
for doc in documents:
    print(doc)

documents = list(collection.find())

for doc in documents:
    doc.pop('_id', None)

df = pd.DataFrame(documents)
timestmp = []
for ts in df['timestamp']:
    utc_time = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ")
    utc = pytz.utc
    est = pytz.timezone('US/Eastern')
    utc_time = utc.localize(utc_time)
    est_time = utc_time.astimezone(est)
    est_time = est_time.strftime("%Y-%m-%d %H:%M:%S")
    timestmp.append(est_time)
    new_df = df.drop(columns = ["timestamp"], axis=1)
new_df['timestamp'] = timestmp
new_df.to_csv('users.csv', index=False)
