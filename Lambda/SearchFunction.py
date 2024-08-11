import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    search_type = event.get('search_type')
    game_id = event.get('game_id')
    table_name = 'games'
    table = dynamodb.Table(table_name)
    if search_type == 'players':
        if not game_id:
            return {
                'statusCode': 400,
                'body': json.dumps('game_id is required for players search.')
            }

        try:
            # Convert game_id to string if ID is a string type in DynamoDB
            if not isinstance(game_id, str):
                game_id = str(game_id)

            response = table.query(
                KeyConditionExpression=Key('ID').eq(game_id)
            )

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
                'body': json.dumps(f'Error querying DynamoDB table: {str(e)}')
            }

    else:
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
