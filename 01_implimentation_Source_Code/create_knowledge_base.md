# Optional Stand-Out Enhancement: Bedrock Knowledge Base

The source brief initially embeds the FAQ in `{{FAQ}}`. The rubric's stand-out section asks for a Knowledge Base backed by a vector index.

Recommended production architecture:

Customer → Guardrail → Bedrock Flow classifier → Condition
→ PLATFORM_QUESTION → Knowledge Base retrieval → grounded answer
→ BUG_REPORT → AgentCore harness → Gateway → Lambda → DynamoDB
→ OTHER_REQUEST → human support

Create a Bedrock Knowledge Base in `us-east-1`, upload `online_shop_faq.md` to its S3 data source, ingest/sync it, and test retrieval. Bedrock supports `Retrieve` and `RetrieveAndGenerate`; managed Knowledge Bases use managed search configuration. Keep the embedded FAQ version for the course baseline, and use the Knowledge Base as the documented stand-out enhancement.

Do not hard-code the Knowledge Base ID in source control. Put it in an environment/config file after creation.
