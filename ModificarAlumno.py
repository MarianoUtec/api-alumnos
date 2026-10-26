import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    alumno_id = event['body']['alumno_id']
    alumno_datos = event['body']['alumno_datos']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    try:
        response = table.update_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            },
            UpdateExpression='SET alumno_datos = :datos',
            ExpressionAttributeValues={
                ':datos': alumno_datos
            },
            # Solo modifica si el alumno ya existe (evita crear uno nuevo)
            ConditionExpression='attribute_exists(tenant_id)'
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {
                'statusCode': 404,
                'status': 'Alumno no existe'
            }
        raise
    # Salida (json)
    return {
        'statusCode': 200,
        'status': 'Alumno modificado',
        'tenant_id': tenant_id,
        'alumno_id': alumno_id
    }
