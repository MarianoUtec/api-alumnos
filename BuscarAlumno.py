import boto3
import json
from decimal import Decimal

def convertir(obj):
    # DynamoDB devuelve números como Decimal, que json no puede serializar
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    alumno_id = event['body']['alumno_id']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    response = table.get_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        }
    )
    if 'Item' not in response:
        return {
            'statusCode': 404,
            'status': 'Alumno no existe'
        }
    alumno = json.loads(json.dumps(response['Item'], default=convertir))
    # Salida (json)
    return {
        'statusCode': 200,
        'alumno': alumno
    }
