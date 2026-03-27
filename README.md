# AWS Bedrock AgentCore Workshop Guide

Hands-on implementation and study notes for the AWS Bedrock AgentCore workshop.

## Official Workshop Links

- Main page: https://catalog.workshops.aws/workshops/850fcd5c-fd1f-48d7-932c-ad9babede979/en-US
- Lab 1: https://catalog.workshops.aws/workshops/850fcd5c-fd1f-48d7-932c-ad9babede979/en-US/20-create-an-agent

## Repository Purpose

This repository is organized as a practical learning path:

- Follow the official workshop flow.
- Implement code locally and test each lab.
- Keep bilingual documentation for easier review and sharing.

## Repository Structure

```text
aws-bedrock-agentcore-workshop/
├─ README.md                # You are here (overview and navigation)
├─ lab1/
│  ├─ README.md             # Lab 1 entry and quick start
│  ├─ ReadmeEN.md           # Detailed Lab 1 notes in English
│  ├─ ReadmeVN.md           # Detailed Lab 1 notes in Vietnamese
│  ├─ index.py              # Main Lab 1 implementation
│  ├─ requirements.txt      # Python dependencies
│  ├─ .env.sample           # Environment variable template
│  └─ images/               # Screenshots and evidence
└─ .gitignore
```

## How To Use This Repository

1. Start from this file for overall context.
2. Open `lab1/README.md` to run the lab quickly.
3. Read one detailed guide:
	- English: `lab1/ReadmeEN.md`
	- Vietnamese: `lab1/ReadmeVN.md`
4. Review screenshots in `lab1/images/` for setup and run evidence.

## Quick Start (Lab 1)

```powershell
cd lab1
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python index.py
```

## Prerequisites

- Python 3.10+
- AWS account with Bedrock model access
- AWS CLI configured for local execution

## Current Status

- Lab 1: Implemented and documented
- Lab 2+: Planned

## Notes

- The current implementation is a customized Lab 1 variant for learning tool-calling behavior.
- Production concerns such as memory, identity, observability, and runtime scaling are expected in later labs.
