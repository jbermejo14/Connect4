import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    # Initialize DynamoDB resource
    dynamodb = boto3.resource('dynamodb')

    # Get the table name from environment variables
    table = dynamodb.Table('games')

    # Extract game_id from the event
    game_id = event.get('game_id')
    players = event.get('players')

    if not game_id:
        logger.error('Missing game_id in the event')
        return {
            'statusCode': 400,
            'body': json.dumps('Missing game_id in the event')
        }

    # Item to be inserted
    item = {
        'ID': f'{game_id}',
        'name': f'{game_id}',
        'players': f'{players}',
    }

    try:
        # Insert the item into the DynamoDB table
        table.put_item(Item=item)
        logger.info(f'Item inserted successfully: {item}')

        return {
            'statusCode': 200,
            'body': json.dumps('Game created successfully')
        }

    except Exception as e:
        logger.error(f'Error inserting item into DynamoDB: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps('Error creating game')
        }
