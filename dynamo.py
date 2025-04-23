import boto3
from creds import aws_access_key_id, aws_secret_access_key

# Connect to DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id = aws_access_key_id,
    aws_secret_access_key = aws_secret_access_key
)
def get_all_users():
    try:
        table = dynamodb.Table('Favorite_Food_Type')
        response = table.scan()
        return response.get('Items', [])
    except Exception as e:
        print("🔴 Error in get_all_users():", str(e))  # Print to terminal
        return {'error': str(e)}


# ADD new user
def insert_user_dynamo(data):
    try:
        table = dynamodb.Table('Favorite_Food_Type')
        if 'Name' not in data or 'Food Type' not in data:
            return {'error': 'Missing Name or Food Type'}
        table.put_item(Item=data)
        return {'message': 'User added to Favorite_Food_Type'}
    except Exception as e:
        return {'error': str(e)}

# DELETE user
def delete_user_dynamo(name):
    try:
        table = dynamodb.Table('Favorite_Food_Type')
        table.delete_item(Key={'Name': name})
        return {'message': 'User deleted from Favorite_Food_Type'}
    except Exception as e:
        return {'error': str(e)}
    
def update_user_dynamo(name, data):
    try:
        table = dynamodb.Table('Favorite_Food_Type')
        print(f"🔄 Updating user: {name} with data: {data}")

        # Use safe placeholders like "#attr0", "#attr1", etc.
        expression_names = {}
        expression_values = {}
        update_parts = []

        for idx, (key, value) in enumerate(data.items()):
            placeholder = f"#attr{idx}"
            value_placeholder = f":val{idx}"
            update_parts.append(f"{placeholder} = {value_placeholder}")
            expression_names[placeholder] = key
            expression_values[value_placeholder] = value

        update_expression = "SET " + ", ".join(update_parts)

        response = table.update_item(
            Key={'Name': name},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values,
            ReturnValues="UPDATED_NEW"
        )

        print("✅ Update response:", response)
        return {'message': 'User updated successfully'}

    except Exception as e:
        print("❌ Error in update_user_dynamo:", str(e))
        return {'error': str(e)}
