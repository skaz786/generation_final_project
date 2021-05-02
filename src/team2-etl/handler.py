import boto3
import csv
import sys
sys.path.append("..") # Goes back a level in the directory
from src.app import start_transformation


def handle(event, context):
    # Get key and bucket informaition
    key = event['Records'][0]['s3']['object']['key']
    bucket = event['Records'][0]['s3']['bucket']['name']

    # use boto3 library to get object from S3
    s3 = boto3.client('s3')
    s3_object = s3.get_object(Bucket=bucket, Key=key)
    file_data = s3_object['Body'].read().decode('utf-8')

    # read CSV
    csv_data = csv.reader(file_data.splitlines())
    read_data = []
    data = []

    for line in csv_data:
        read_data.append(line)

    for line in read_data:
        order = {'date_time': line[0], 'location': line[1], 'customer_name': line[2], 'products': line[3], 'payment_method': line[5], 'total': line[4], 'card_details': line[6]}
        data.append(order)

    print("we're in")
    start_transformation(data)
    print("we're out")

    return {"message": "success!!! Check the cloudwatch logs for this lambda in cloudwatch https://eu-west-1.console.aws.amazon.com/cloudwatch/home?region=eu-west-1#logsV2:log-groups"}
