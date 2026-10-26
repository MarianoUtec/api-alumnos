import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    alumno_id = event['body']['alumno_id']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    try:
        table.delete_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            },
            # Solo elimina si el alumno existe
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
        'status': 'Alumno eliminado',
        'tenant_id': tenant_id,
        'alumno_id': alumno_id
    }
