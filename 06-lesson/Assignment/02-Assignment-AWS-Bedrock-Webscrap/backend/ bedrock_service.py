import os
import uuid

import boto3
from botocore.exceptions import ClientError


class BedrockAgentService:
    def __init__(self):
        self.region = os.getenv("AWS_REGION", "us-east-1")
        self.agent_id = os.getenv("BEDROCK_AGENT_ID")
        self.agent_alias_id = os.getenv("BEDROCK_AGENT_ALIAS_ID")

        if not self.agent_id:
            raise ValueError("BEDROCK_AGENT_ID is missing in environment variables.")

        if not self.agent_alias_id:
            raise ValueError(
                "BEDROCK_AGENT_ALIAS_ID is missing in environment variables."
            )

        self.client = boto3.client(
            service_name="bedrock-agent-runtime",
            region_name=self.region
        )

    def invoke_agent(self, user_message, session_id=None):
        if not session_id:
            session_id = str(uuid.uuid4())

        try:
            response = self.client.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=self.agent_alias_id,
                sessionId=session_id,
                inputText=user_message,
                enableTrace=False
            )

            completion_text = ""

            for event in response.get("completion", []):
                if "chunk" in event:
                    completion_text += event["chunk"]["bytes"].decode("utf-8")

            return {
                "success": True,
                "session_id": session_id,
                "answer": completion_text.strip()
            }

        except ClientError as error:
            return {
                "success": False,
                "session_id": session_id,
                "answer": "",
                "error": error.response["Error"]["Message"]
            }

        except Exception as error:
            return {
                "success": False,
                "session_id": session_id,
                "answer": "",
                "error": str(error)
            }