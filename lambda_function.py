#It is Working 
import json
import boto3

ses_client = boto3.client('ses')

def send_email(template, recipient, subject):
    try:
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [recipient]
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': template
                    }
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject
                }
            },
            Source='sanjog.k@shikhartech.com'
        )
        return response

    except Exception as e:
        raise e

def lambda_handler(event, context):
    print(json.dumps({"event": event}))
    
    try:
        if event['httpMethod'] == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Origin': "*"
                }
            }
        
        body = json.loads(event['body'])
        template = body.get('template')
        recipients = body.get('recipients')
        subject = body.get('subject')

        if not template or not recipients or not subject:
            error_response = {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': json.dumps({'message': 'Missing required parameters'})
            }
            print(json.dumps({"response": error_response}))
            return error_response

        responses = []
        for recipient in recipients:
            response = send_email(template, recipient, subject)
            responses.append(response)

        print(json.dumps({"email_responses": responses}))
        
        # Constructing the success response
        success_response = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({'message': 'Emails sent successfully', 'responses': responses})
        }
        print(json.dumps({"response": success_response}))
        return success_response

    except Exception as e:
        error_response = {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({'message': str(e)})
        }
        print(json.dumps({"response": error_response}))
        return error_response



# import json

# # Importing the necessary AWS SDK
# import boto3

# # Create an SES client
# ses_client = boto3.client('ses')

# def send_email(template, recipient, subject):
#     try:
#         # Send email using Amazon SES
#         response = ses_client.send_email(
#             Destination={
#                 'ToAddresses': [recipient]
#             },
#             Message={
#                 'Body': {
#                     'Html': {
#                         'Charset': 'UTF-8',
#                         'Data': template
#                     }
#                 },
#                 'Subject': {
#                     'Charset': 'UTF-8',
#                     'Data': subject
#                 }
#             },
#             Source='sanjog.k@shikhartech.com'
#         )
#         return response

#     except Exception as e:
#         raise e


# def lambda_handler(event, context):
#     # Log the incoming event
#     print(json.dumps({"event": event}))
    
#     try:
#         # Check if it's an OPTIONS request
#         if event['httpMethod'] == 'OPTIONS':
#             # Return a response without attempting to parse the body
#             return {
#                 'statusCode': 200,
#                 'headers': {
#                     'Access-Control-Allow-Headers': 'Content-Type',  # Allow Content-Type header
#                     'Access-Control-Allow-Methods': 'POST, OPTIONS',
#                     'Access-Control-Allow-Origin' : "*"# Allow POST and OPTIONS methods
#                 }
#             }
        
#         # Parse payload from event
#         body = json.loads(event['body'])
#         template = body.get('template')
#         recipient = body.get('recipient')
#         subject = body.get('subject')

#         if not template or not recipient or not subject:
#             error_response = {
#                 'statusCode': 400,
#                 'headers': {
#                     'Access-Control-Allow-Headers': 'Content-Type',  # Allow Content-Type header
#                     'Access-Control-Allow-Methods': 'POST, OPTIONS'  # Allow POST and OPTIONS methods
#                 },
#                 'body': json.dumps({'message': 'Missing required parameters'})
#             }
#             # Log the error response
#             print(json.dumps({"response": error_response}))
#             return error_response

#         # Send email
#         response = send_email(template, recipient, subject)
#         # Log the email response
#         print(json.dumps({"email_response": response}))
#         return {
#             'statusCode': 200,
#             'headers': {
#                 'Access-Control-Allow-Headers': 'Content-Type',  # Allow Content-Type header
#                 'Access-Control-Allow-Methods': 'POST, OPTIONS'  # Allow POST and OPTIONS methods
#             },
#             'body': json.dumps({'message': 'Email sent successfully', 'response': response})
#         }

#     except Exception as e:
#         error_response = {
#             'statusCode': 500,
#             'headers': {
#                 'Access-Control-Allow-Headers': 'Content-Type',  # Allow Content-Type header
#                 'Access-Control-Allow-Methods': 'POST, OPTIONS'  # Allow POST and OPTIONS methods
#             },
#             'body': json.dumps({'message': str(e)})
#         }
#         # Log the error response
#         print(json.dumps({"response": error_response}))
#         return error_response
