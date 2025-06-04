# Recipe Suggestion API

This project implements a serverless API that generates recipe suggestions based on provided keywords. It uses AWS API Gateway, AWS Lambda, and Amazon Bedrock with Anthropic Claude 3.

## Architecture

The solution consists of:

1. **API Gateway**: Receives HTTP requests with recipe keywords
2. **Lambda Function**: Processes the request and calls Amazon Bedrock
3. **Amazon Bedrock**: Uses Claude 3 to generate recipe suggestions

## Prerequisites

- AWS Account with access to Amazon Bedrock
- AWS CLI configured
- Python 3.9 or later
- SAM CLI (for deployment)

## Deployment

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Deploy using SAM:
   ```
   sam build
   sam deploy --guided
   ```

## Usage

Send a POST request to the API endpoint with recipe keywords:

```bash
curl -X POST \
  https://your-api-id.execute-api.region.amazonaws.com/Prod/recipe \
  -H 'Content-Type: application/json' \
  -d '{"keywords": ["chicken", "pasta", "tomatoes"]}'
```

### Example Request

```json
{
  "keywords": ["chicken", "pasta", "tomatoes"]
}
```

### Example Response

```json
{
  "recipe": "# Chicken Tomato Pasta\n\n## Ingredients\n- 2 boneless, skinless chicken breasts, diced\n- 8 oz pasta (penne or fusilli work well)\n- 2 cups cherry tomatoes, halved\n- ..."
}
```

## Testing

Run the unit tests:

```bash
python -m unittest test_lambda_function.py
```

## IAM Permissions

The Lambda function requires permissions to invoke Amazon Bedrock models. These permissions are defined in the CloudFormation template.

## Cost Considerations

This solution uses Amazon Bedrock, which incurs costs based on the number of tokens processed. Monitor your usage to avoid unexpected charges.
