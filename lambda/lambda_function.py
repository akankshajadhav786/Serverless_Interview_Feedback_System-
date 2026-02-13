import json
import uuid
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('InterviewFeedback')

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            if o % 1 == 0:
                return int(o)
            else:
                return float(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    try:
        http_method = event["requestContext"]["http"]["method"]
        print("=== New Lambda Invocation ===")
        print("HTTP Method:", http_method)
        print("Full Event:", json.dumps(event))

        # -------- POST /feedback --------
        if http_method == "POST":
            body = json.loads(event.get("body", "{}"))
            print("POST Request Body:", body)

            feedback_id = str(uuid.uuid4())
            print("Generated feedback_id:", feedback_id)

            item = {
                "feedback_id": feedback_id,
                "name": body.get("name"),
                "company": body.get("company"),
                "rating": body.get("rating"),
                "comments": body.get("comments")
            }

            table.put_item(Item=item)
            print("Item stored in DynamoDB:", item)

            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "message": "Feedback stored successfully",
                    "feedback_id": feedback_id
                })
            }

        # -------- GET /feedback/{feedback_id} --------
        elif http_method == "GET":
            path_params = event.get("pathParameters") or {}
            feedback_id = path_params.get("feedback_id")
            print("GET Request Path Parameters:", path_params)

            if not feedback_id:
                print("Error: feedback_id missing in path")
                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"message": "feedback_id is required in path"})
                }

            response = table.get_item(Key={"feedback_id": feedback_id})
            print("DynamoDB GET Response:", response)

            if "Item" not in response:
                print("Error: Feedback not found for ID:", feedback_id)
                return {
                    "statusCode": 404,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"message": "Feedback not found"})
                }

            print("Feedback retrieved successfully for ID:", feedback_id)
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(response["Item"], cls=DecimalEncoder)
            }

        else:
            print("Error: Method not allowed")
            return {
                "statusCode": 405,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": "Method not allowed"})
            }

    except Exception as e:
        print("Exception occurred:", str(e))
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
