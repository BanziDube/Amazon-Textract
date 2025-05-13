import glob
import boto3
import json

client = boto3.client('rekognition', region_name='us-west-2')
combined = []

for filename in glob.glob('public/photos/*.jpeg'):
    with open(filename, 'rb') as fd:
        response = client.detect_labels(
            Image={'Bytes': fd.read()}, MaxLabels=10, MinConfidence=70)

        entry = {"Filename": filename.replace("public/", "")}

        # Extract actual labels from Rekognition response
        labels = []
        for label in response['Labels']:
            labels.append({
                "Name": label['Name'],
                "Confidence": label['Confidence'],
                "Parents": [{"Name": parent['Name']} for parent in label.get('Parents', [])]
            })

        entry["Labels"] = labels
        combined.append(entry)

# Print the JSON output
print(json.dumps(combined, indent=2))
