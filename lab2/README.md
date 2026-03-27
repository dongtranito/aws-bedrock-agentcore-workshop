# Lab 2 - Enhance Agent with Memory

This folder contains a complete local implementation of Workshop Lab 2 for Amazon Bedrock AgentCore Memory.

## References

- Workshop lab page: https://catalog.workshops.aws/workshops/850fcd5c-fd1f-48d7-932c-ad9babede979/en-US/30-add-memory
- Official notebook: https://github.com/awslabs/amazon-bedrock-agentcore-samples/blob/main/01-tutorials/09-AgentCore-E2E/strands-agents/lab-02-agentcore-memory.ipynb

## Documentation

- Vietnamese guide: ReadmeVN.md
- English guide: ReadmeEN.md

## What This Lab 2 Code Does

The main script `index.py` follows the Lab 2 journey end-to-end:

1. Create (or reuse) an AgentCore Memory resource with two long-term memory strategies:
	- USER_PREFERENCE (`support/customer/{actorId}/preferences/`)
	- SEMANTIC (`support/customer/{actorId}/semantic/`)
2. Seed historical customer conversations into Short-Term Memory via `create_event`.
3. Wait and retrieve processed Long-Term Memories from both namespaces.
4. Build a Strands Agent using `AgentCoreMemorySessionManager`.
5. Run personalization tests to verify memory-aware responses.

## Quick Start (PowerShell)

```powershell
cd lab2
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python index.py
```

## Prerequisites

- Python 3.10+
- AWS CLI configured (`aws configure`)
- Access to Bedrock model `amazon.nova-lite-v1:0` (or set `BEDROCK_MODEL_ID`)
- Required AgentCore permissions in your AWS account

## Expected Output Highlights

- Successful AWS region detection
- Existing/new Memory resource ID
- Validation of USER_PREFERENCE and SEMANTIC strategies
- Retrieved preference and semantic memories
- Two test prompts executed on a memory-enabled support agent

## Model Configuration

The script uses:

- `BEDROCK_MODEL_ID` environment variable if provided
- Otherwise defaults to `amazon.nova-lite-v1:0`

Example (PowerShell):

```powershell
$env:BEDROCK_MODEL_ID="amazon.nova-lite-v1:0"
python index.py
```
