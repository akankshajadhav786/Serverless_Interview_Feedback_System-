# Serverless Feedback Project

## Description
A serverless feedback system built on AWS using Lambda, API Gateway, DynamoDB, and CloudWatch.  
Allows users to submit feedback and retrieve it by ID.

## AWS Services Used
- **AWS Lambda** — Runs backend code for POST/GET feedback.
- **API Gateway** — Exposes HTTP endpoints: `/feedback`, `/feedback/{feedback_id}`, `/health`.
- **DynamoDB** — Stores feedback items.
- **CloudWatch** — Logs Lambda invocations and metrics.

## Endpoints
- `POST /feedback` → Stores feedback and returns `feedback_id`.
- `GET /feedback/{feedback_id}` → Retrieves feedback by ID.
- `GET /health` → Returns simple health check.

## Usage
1. Deploy `lambda/lambda_function.py` to AWS Lambda.
2. Configure API Gateway routes:
   - POST `/feedback`
   - GET `/feedback/{feedback_id}`
   - GET `/health`
3. Create DynamoDB table: `InterviewFeedback` with Partition Key `feedback_id` (String).
4. Test endpoints with Postman or curl.
5. Check logs and metrics in CloudWatch.

## Screenshots
Include:
- POST request & response
- GET request & response
- CloudWatch logs
- CloudWatch dashboard
- DynamoDB table
