import json
import unittest
from unittest.mock import patch, MagicMock
import lambda_function

class TestLambdaFunction(unittest.TestCase):
    @patch('lambda_function.generate_recipe')
    def test_lambda_handler_success(self, mock_generate_recipe):
        # Mock the recipe generation
        mock_recipe = "Delicious Test Recipe"
        mock_generate_recipe.return_value = mock_recipe
        
        # Test event with keywords
        test_event = {
            'body': json.dumps({
                'keywords': ['chicken', 'pasta', 'tomatoes']
            })
        }
        
        # Call the lambda handler
        response = lambda_function.lambda_handler(test_event, {})
        
        # Verify the response
        self.assertEqual(response['statusCode'], 200)
        response_body = json.loads(response['body'])
        self.assertEqual(response_body['recipe'], mock_recipe)
        
        # Verify generate_recipe was called with the correct keywords
        mock_generate_recipe.assert_called_once_with(['chicken', 'pasta', 'tomatoes'])
    
    def test_lambda_handler_no_keywords(self):
        # Test event with no keywords
        test_event = {
            'body': json.dumps({})
        }
        
        # Call the lambda handler
        response = lambda_function.lambda_handler(test_event, {})
        
        # Verify the response
        self.assertEqual(response['statusCode'], 400)
        response_body = json.loads(response['body'])
        self.assertIn('error', response_body)
    
    @patch('boto3.client')
    def test_generate_recipe(self, mock_boto3_client):
        # Mock the Bedrock client and response
        mock_bedrock = MagicMock()
        mock_boto3_client.return_value = mock_bedrock
        
        # Mock the response from Bedrock
        mock_response_body = {
            'content': [
                {
                    'text': 'Test Recipe Content'
                }
            ]
        }
        mock_response = {
            'body': MagicMock()
        }
        mock_response['body'].read.return_value = json.dumps(mock_response_body)
        mock_bedrock.invoke_model.return_value = mock_response
        
        # Call generate_recipe
        keywords = ['chicken', 'pasta', 'tomatoes']
        result = lambda_function.generate_recipe(keywords)
        
        # Verify the result
        self.assertEqual(result, 'Test Recipe Content')
        
        # Verify Bedrock was called with the correct parameters
        mock_bedrock.invoke_model.assert_called_once()
        call_args = mock_bedrock.invoke_model.call_args[1]
        self.assertEqual(call_args['modelId'], 'anthropic.claude-3-sonnet-20240229-v1:0')
        
        # Verify the prompt contains all keywords
        request_body = json.loads(call_args['body'])
        prompt = request_body['messages'][0]['content']
        for keyword in keywords:
            self.assertIn(keyword, prompt)

if __name__ == '__main__':
    unittest.main()