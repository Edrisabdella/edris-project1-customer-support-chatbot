# Final Submission Package

**Project:** Customer Support Chatbot with Amazon Bedrock AgentCore
**Candidate:** Edris Abdella Nuure
**Email:** edrisabdella178@gmail.com / engineeredrisabdella@gmail.com
**Phone:** +251905131051 / +251944676746
**LinkedIn:** https://www.linkedin.com/in/edris-abdella-7aa521177

## Package structure

- `01_Source_Code/` — application source, infrastructure, prompt, FAQ, tests, and dependencies.
- `02_Documentation/` — README, project manifest, and project summary.
- `03_Architecture/` — high-resolution professional architecture diagrams.
- `04_Final_Deliverables/` — final PPTX presentation and final PDF report.
- `05_Evidence_Templates/` — submission checklist and evaluation-observation template.

## Architecture

Customer Message → Amazon Bedrock AgentCore Managed Harness → routing in system prompt →

- Bug report → AgentCore Gateway → `create_bug_report` Lambda → DynamoDB
- Platform question → embedded FAQ → grounded answer
- Other / unsupported request → human support hand-off

## Evidence note

The package includes the implementation and documentation assets. Actual AWS console screenshots (Gateway, tool call, DynamoDB item, and Bedrock Evaluation results) should be added after running the project in the AWS environment.
