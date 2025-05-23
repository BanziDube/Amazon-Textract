import glob
import boto3
import json
import csv
import sys

csv_array = []
client = boto3.client('textract')
for filename in glob.glob('raw_images/*.jpg'):
    csv_row = {}
    print(f"Processing: {filename}")
    with open(filename, 'rb') as fd:
        file_bytes = fd.read()

    response = client.analyze_document(
        Document={'Bytes': file_bytes},
        FeatureTypes=["QUERIES"],
        QueriesConfig={
            'Queries': [
                {'Text': 'What is the response id', 'Alias': 'ResponseId'},
                {'Text': 'What are the notes?', 'Alias': 'Notes'},
            ]
        }
    )

    for block in response["Blocks"]:
        if block["BlockType"] == "QUERY":
            query_alias = block["Query"]["Alias"]
            answer_id = next(
                rel["Ids"] for rel in block["Relationships"] if rel['Type'] == "ANSWER")[0]
            answer_text = next(
                b for b in response["Blocks"] if b["Id"] == answer_id)["Text"]
            csv_row[query_alias] = answer_text
    csv_array.append(csv_row)

writer = csv.DictWriter(sys.stdout, fieldnames=[
                        "ResponseId", "Notes"], dialect='excel')
writer.writeheader()
for row in csv_array:
    writer.writerow(row)
