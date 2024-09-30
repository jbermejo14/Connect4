import json
import boto3
from botocore.exceptions import ClientError

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    table_name = 'moves'
    game_id_substring = event['game_id']
    table = dynamodb.Table(table_name)
    try:
        scan_params = {
            'TableName': table_name,
            'FilterExpression': 'contains(#id, :game_id_substring)',
            'ExpressionAttributeNames': {'#id': 'ID'},
            'ExpressionAttributeValues': {':game_id_substring': game_id_substring}
        }

        response = table.scan(**scan_params)
        items_to_delete = response['Items']

        for item in items_to_delete:
            table.delete_item(
                Key={
                    'ID': item['ID']
                }
            )

        return {
            'statusCode': 200,
            'body': json.dumps(f"Deleted {len(items_to_delete)} items containing game_id {game_id_substring}")
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting items: {str(e)}")
        }