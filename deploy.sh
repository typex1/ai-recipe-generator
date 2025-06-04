#!/bin/bash

# Exit on error
set -e

echo "Installing dependencies..."
pip install -r requirements.txt -t ./package

echo "Creating deployment package..."
cd package
zip -r ../deployment.zip .
cd ..
zip -g deployment.zip lambda_function.py

echo "Building with SAM..."
sam build

echo "Deploying with SAM..."
sam deploy --guided

echo "Deployment complete!"