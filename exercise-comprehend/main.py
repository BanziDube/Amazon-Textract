import boto3
import csv

# read the movies CSV and populate the all_notes rray with all the of notes
with open("movies.csv", 'r') as fd:
    reader = csv.DictReader(
        fd, fieldnames=["ResponseId", "Notes"], dialect='excel')
    all_notes = [row["Notes"] for row in reader]

client = boto3.client('comprehend')

#####
# Complete the call to batch_detect_sentiment
#####
response = client.batch_detect_sentiment(
    TextList=all_notes,
    LanguageCode='en'
)

for result in response["ResultList"]:
    index = result["Index"]
    sentiment = result["Sentiment"]

    print(sentiment, all_notes[index])
