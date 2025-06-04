import json
import os
import boto3
from typing import Dict, Any

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function handler that processes API Gateway requests,
    extracts recipe keywords, and uses Amazon Bedrock with Claude 3
    to generate recipe suggestions.
    
    Args:
        event: API Gateway event containing recipe keywords
        context: Lambda context
        
    Returns:
        API Gateway response with the generated recipe
    """
    try:
        # Extract keywords from the request
        body = json.loads(event.get('body', '{}'))
        keywords = body.get('keywords', [])
        
        if not keywords:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'No keywords provided'})
            }
        
        # Generate recipe using Amazon Bedrock
        recipe = generate_recipe(keywords)
        
        # Return the recipe as response
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'recipe': recipe})
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Internal server error: {str(e)}'})
        }

def generate_recipe(keywords: list) -> str:
    """
    Generate a recipe suggestion using Amazon Bedrock with Claude 3.
    
    Args:
        keywords: List of keywords relevant for recipe creation
        
    Returns:
        Generated recipe as a string
    """
    # Initialize Bedrock client
    bedrock_runtime = boto3.client(
        service_name='bedrock-runtime',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )
    
    # Prepare the prompt for Claude 3
    prompt = f"""
    Create a detailed recipe based on the following ingredients or themes: {', '.join(keywords)}.
    
    Please include:
    - Recipe name
    - Ingredients list with measurements
    - Step-by-step cooking instructions
    - Estimated preparation and cooking time
    - Serving size
    - Any tips or variations
    
    Format the recipe in a clear, easy-to-follow structure.
    """
    
    # Prepare the request payload for Claude 3
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4000,
        "temperature": 0.7,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    # Invoke Claude 3 through Amazon Bedrock
    response = bedrock_runtime.invoke_model(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',  # Claude 3 Sonnet model
        body=json.dumps(request_body)
    )
    
    # Parse and extract the generated recipe
    response_body = json.loads(response.get('body').read())
    recipe_text = response_body.get('content', [{}])[0].get('text', '')
    
    return recipe_text