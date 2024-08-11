import json
import boto3
from botocore.exceptions import ClientError

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Define the DynamoDB table
    table = dynamodb.Table('moves')

    # Extract data from the incoming event
    try:
        move_id = event.get('move_id')
        game_id = event.get('game_id')
        coords = event.get('coords')


        # Prepare the item to be inserted into DynamoDB
        item = {
            'ID': str(move_id),  # DynamoDB requires keys to be string
            'game_id': str(game_id),
            'coords': str(coords)
        }

        # Insert the item into the DynamoDB table
        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps('Move successfully stored in DynamoDB')
        }

    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Missing key: {str(e)}')
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'DynamoDB Error: {e.response["Error"]["Message"]}')
        }
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid JSON format')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Unexpected error: {str(e)}')
        }
