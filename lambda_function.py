import json
import boto3
import base64

s3_client = boto3.client('s3')
bucket_name = 'lokesh-poc-s3'

def lambda_handler(event, context):
    
    if event['httpMethod'] == 'POST':
        try:
            body = json.loads(event['body'])
            
            if 'file_based_64' in body:
                file_content_base64 = body['file_based_64']
                file_content = base64.b64decode(file_content_base64)

                if 'file_name' in body:
                    file_name = body['file_name']
                    file_path = f"{file_name}"

                    s3_client.put_object(Body=file_content, Bucket=bucket_name, Key=file_path)
                    s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_path}"

                    return {
                        'statusCode': 201,
                        'body': json.dumps({
                            'data': {
                                'statusCode': 201,
                                's3_url': s3_url
                            }
                        })
                    }
                else:
                    return {
                        'statusCode': 400,
                        'body': json.dumps({
                            'error': 'Missing required File name: file_name'
                        })
                    }

            elif 'file_name' in body:
                file_name = body['file_name']
                file_path = f'{file_name}'

                presigned_url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': bucket_name,
                        'Key': file_path
                    },
                    ExpiresIn=300
                )

                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'file-url': presigned_url
                    })
                }
            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'error': 'Missing required parameters: file_based_64 or file_name'
                    })
                }

        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': f'Error: {str(e)}'
                })
            }
    elif event['httpMethod'] == 'GET':
        try:
            response = s3_client.list_objects_v2(Bucket=bucket_name)
            files = [obj['Key'] for obj in response.get('Contents', [])]
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'data': {
                        'files': files
                    }
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': 'Error'
                })
            }
    elif event['httpMethod'] == 'DELETE':
        try:
            body = json.loads(event['body'])
            file_name = body['file_name']
            file_path = f'{file_name}' 

            s3_client.delete_object(Bucket=bucket_name, Key=file_path)

            return {
                'statusCode': 201,
                'body': json.dumps({
                    'message': f'File {file_name} deleted successfully'
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': 'Error'
                })
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid method')
        }
