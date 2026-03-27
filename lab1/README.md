# Lab 1 - Create the Agent Prototype

This directory contains the Lab 1 implementation for the AWS Bedrock AgentCore workshop, with local customizations for learning and demonstration.

## References

- Official workshop: https://catalog.workshops.aws/workshops/850fcd5c-fd1f-48d7-932c-ad9babede979/en-US
- Lab 1 page: https://catalog.workshops.aws/workshops/850fcd5c-fd1f-48d7-932c-ad9babede979/en-US/20-create-an-agent

## Documentation

- English step-by-step: `ReadmeEN.md`
- Vietnamese step-by-step: `ReadmeVN.md`

## Current Implementation in This Repo

- Main code: `index.py`
- Agent framework: Strands
- Model: Amazon Nova Lite via Bedrock
- Tools: `add`, `subtract`, `multiply`, `divide`

## Quick Start

```powershell
cd lab1
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python index.py
```

## Notes

- This is a customized Lab 1 variant for tool-calling behavior.
- Full production capabilities (memory, gateway, observability, identity) are expected in later labs.
