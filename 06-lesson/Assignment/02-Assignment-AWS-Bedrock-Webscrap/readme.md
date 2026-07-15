# Web Crawler Agent Using AWS Bedrock

## Objective

This project builds a Web Crawler Agent using AWS Bedrock Agents and AWS Lambda. A user enters a public URL through a web interface. The Bedrock Agent invokes a Lambda tool called `web_scrape`, which downloads and cleans webpage HTML before returning readable text.

## Technologies

- Python
- FastAPI
- AWS Bedrock Agents
- AWS Lambda
- Amazon Bedrock Agent Runtime
- Boto3
- HTML, CSS, JavaScript

## Architecture

Browser frontend -> FastAPI backend -> AWS Bedrock Agent -> web_scrape Action Group -> AWS Lambda -> Public Website

## Features

- Accepts public HTTP and HTTPS URLs
- Uses AWS Bedrock Agent for tool orchestration
- Lambda tool named `web_scrape`
- Handles redirects and gzip responses
- Removes HTML, scripts, styles, and extra whitespace
- Limits response size and extracted content length
- Blocks localhost and private IP addresses
- Displays final agent response in a browser UI

## Run Locally

1. Create a Python virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Add AWS Region, Agent ID, and Alias ID to `.env`.
4. Configure AWS credentials locally.
5. Start the app using `uvicorn app:app --reload`.
6. Open `http://127.0.0.1:8000`.

## Test Prompt

Crawl this URL: https://example.com