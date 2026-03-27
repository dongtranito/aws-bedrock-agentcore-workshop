# Lab 1 - Implementation Notes (English)

## Official References

- Workshop: https://catalog.workshops.aws/workshops/850fcd5c-fd1f-48d7-932c-ad9babede979/en-US
- Lab 1: https://catalog.workshops.aws/workshops/850fcd5c-fd1f-48d7-932c-ad9babede979/en-US/20-create-an-agent

## Purpose of This Variant

This repository follows the Lab 1 workflow and customizes the implementation for local learning and portfolio evidence.

## What Was Customized

- Main script: `index.py`
- Framework: Strands
- Model: BedrockModel (Amazon Nova Lite)
- Tool set changed to arithmetic tools:
  - `add(a, b)`
  - `subtract(a, b)`
  - `multiply(a, b)`
  - `divide(a, b)`
- System prompt tuned for Vietnamese responses and explicit tool usage.

## Prerequisites

- Python 3.10+
- AWS CLI configured
- Bedrock model access enabled in your AWS account

## Setup and Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python index.py
```

## IAM and Security Notes

For quick testing, broad permissions can work, but least privilege is strongly recommended.

Suggested baseline policies (adjust to your real scope):

- AmazonBedrockFullAccess
- AWSCloudFormationFullAccess (only if your lab flow needs stack deployment)
- AmazonS3FullAccess or a bucket-scoped custom policy
- CloudWatchLogsFullAccess

## How the Agent Works

1. The user provides a request.
2. The agent decides which tool to call.
3. Strands builds tool schemas from functions decorated with `@tool`.
4. The model synthesizes a final response from tool output.

## Current Lab 1 Limitations

- No long-term memory
- Local tools only
- No production observability
- No user identity layer
- Local runtime only (not production-scaled)


