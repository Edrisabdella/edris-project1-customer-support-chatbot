import json, boto3

REGION="us-east-1"
MODEL_ARN="arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-pro-v1:0"
spec=json.load(open("flow_definition.json",encoding="utf-8"))
client=boto3.client("bedrock-agent",region_name=REGION)

# This definition is intentionally generated with native Flow nodes:
# Input -> Prompt classifier -> Condition -> 3 separate Output nodes.
# Review/adjust node coordinates in the console for a polished screenshot.
definition={
 "nodes":[
  {"name":"FlowInput","type":"Input","configuration":{"input":{}},
   "outputs":[{"name":"document","type":"String"}]},
  {"name":"Classifier","type":"Prompt",
   "inputs":[{"name":"customerMessage","type":"String","expression":"$.data"}],
   "outputs":[{"name":"modelCompletion","type":"String"}],
   "configuration":{"prompt":{"sourceConfiguration":{"inline":{"modelId":MODEL_ARN,
     "templateConfiguration":{"text":{"text":spec["classifier"]["prompt"]}}}}}}},
  {"name":"Router","type":"Condition",
   "inputs":[{"name":"category","type":"String","expression":"$.data.category"}],
   "configuration":{"condition":{"conditions":[
    {"name":"BugReport","expression":"category == \"BUG_REPORT\""},
    {"name":"PlatformQuestion","expression":"category == \"PLATFORM_QUESTION\""},
    {"name":"OtherRequest","expression":"category == \"OTHER_REQUEST\""},
    {"name":"DefaultOther","expression":"true"}
   ]}}},
  {"name":"BugReportOutput","type":"Output","inputs":[{"name":"document","type":"String","expression":"$.data"}],"configuration":{"output":{}}},
  {"name":"PlatformQuestionOutput","type":"Output","inputs":[{"name":"document","type":"String","expression":"$.data"}],"configuration":{"output":{}}},
  {"name":"OtherRequestOutput","type":"Output","inputs":[{"name":"document","type":"String","expression":"$.data"}],"configuration":{"output":{}}},
 ],
 "connections":[
  {"name":"input-classifier","type":"Data","configuration":{"data":{"source":{"node":"FlowInput","output":"document"},"target":{"node":"Classifier","input":"customerMessage"}}}},
  {"name":"classifier-router","type":"Data","configuration":{"data":{"source":{"node":"Classifier","output":"modelCompletion"},"target":{"node":"Router","input":"category"}}}},
  {"name":"route-bug","type":"Conditional","configuration":{"conditional":{"condition":"BugReport","source":{"node":"Router"},"target":{"node":"BugReportOutput","input":"document"}}}},
  {"name":"route-platform","type":"Conditional","configuration":{"conditional":{"condition":"PlatformQuestion","source":{"node":"Router"},"target":{"node":"PlatformQuestionOutput","input":"document"}}}},
  {"name":"route-other","type":"Conditional","configuration":{"conditional":{"condition":"OtherRequest","source":{"node":"Router"},"target":{"node":"OtherRequestOutput","input":"document"}}}},
  {"name":"route-default","type":"Conditional","configuration":{"conditional":{"condition":"DefaultOther","source":{"node":"Router"},"target":{"node":"OtherRequestOutput","input":"document"}}}},
 ]
}
try:
    resp=client.create_flow(
      name="customer-support-classification-routing",
      description="Customer support classifier with three explicit routed outputs.",
      executionRoleArn=None,
      definition=definition
    )
    print(json.dumps(resp,indent=2,default=str))
except Exception as e:
    print("Flow creation needs the Bedrock Flow execution role ARN in your account.")
    print("Error:",type(e).__name__,str(e))
    raise
