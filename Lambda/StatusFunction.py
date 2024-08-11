import json
import boto3
from boto3.dynamodb.conditions import Attr

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # Extract parameters from the event
    game_id = event.get('game_id')
    table_name = 'moves'
    table = dynamodb.Table(table_name)

    try:
        # Scan the entire table
        response = table.scan()

        # Extract and process items from response
        items = response.get('Items', [])
        for i in range(len(items)):
            # Convert JSON strings to dictionaries if needed
            if isinstance(items[i], str):
                try:
                    items[i] = json.loads(items[i])
                except json.JSONDecodeError:
                    continue

        items = [{k: str(v) for k, v in item.items()} for item in items if isinstance(item, dict)]

        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error scanning DynamoDB table: {str(e)}')
        }
