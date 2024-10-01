import json
import boto3
from botocore.exceptions import ClientError

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    table_moves = 'moves'
    table_games = 'games'
    game_id = event['game_id']

    # Initialize table object
    table1 = dynamodb.Table(table_moves)
    table2 = dynamodb.Table(table_games)

    # Scan the table to find all moves with the game_id substring
    # Move ID -> 'yp1432', get the game_id from the string ('yp1'-'432')

    try:
        scan_params = {
            'TableName': table_moves,
            'FilterExpression': 'contains(#id, :game_id)',
            'ExpressionAttributeNames': {'#id': 'ID'},
            'ExpressionAttributeValues': {':game_id': game_id}
        }

        response = table1.scan(**scan_params)
        items_to_delete = response['Items']

        # Delete each move with the game_id
        for item in items_to_delete:
            table1.delete_item(
                Key={
                    'ID': item['ID']
                }
            )

        # Deletes the game from games table
        table2.delete_item(
            Key={
                'ID': f'{game_id}',
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"Deleted {len(items_to_delete)} moves and game: {game_id}")
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting items: {str(e)}")
        }