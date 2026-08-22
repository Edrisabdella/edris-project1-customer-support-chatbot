# Project Summary

## Customer Support Chatbot with Amazon Bedrock AgentCore

This project demonstrates prompt-driven customer support routing with a stateful Amazon Bedrock AgentCore managed harness.

### Core design

The chatbot receives a customer message and selects exactly one behavior:

**Bug Report**
- Gather description
- Gather reproduction steps
- Gather environment
- Invoke `create_bug_report`
- Return the real ticket ID

**Platform Question**
- Answer only from the embedded FAQ
- Hand off if the FAQ does not contain the answer

**Other Request**
- Politely redirect to human support

### AWS service chain

**Amazon Bedrock AgentCore Managed Harness**
→ **Amazon Bedrock AgentCore Gateway**
→ **AWS Lambda**
→ **Amazon DynamoDB**

The FAQ is embedded directly into the system prompt through the `{{FAQ}}` placeholder.

### Evaluation

The test suite includes normal requests plus edge cases for ambiguity, minimal input, and prompt injection. Bedrock Evaluations with an LLM-as-a-judge are used to assess response correctness.

### Author

Edris Abdella Nuure  
edrisabdella178@gmail.com  
https://www.linkedin.com/in/edris-abdella-7aa521177
