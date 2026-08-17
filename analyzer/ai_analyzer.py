import os
import json
from openai import OpenAI


def get_api_key():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable not found."
        )

    return api_key


def get_openai_client():
    return OpenAI(api_key=get_api_key())


def test_openai_connection():
    client = get_openai_client()

    response = client.responses.create(
        model="gpt-5.6",
        input="Reply with exactly: InfraAdvisor AI connection successful."
    )

    print(response.output_text)


def load_prompt():
    with open("prompts/network_analysis_prompt.txt", "r") as prompt_file:
        return prompt_file.read()

def analyze_with_rules(knowledge_packet):
    """
    Performs deterministic rule-based analysis of the knowledge packet.
    Used to compare traditional automation with AI reasoning.
    """

    prompt = load_prompt()
    client = get_openai_client()

    analysis = []

    # Temporary placeholder until we connect a real LLM.
    analysis.append("=== AI PROMPT ===")
    analysis.append(prompt)
    analysis.append("")
    analysis.append("=== KNOWLEDGE PACKET RECEIVED ===")

    for interface in knowledge_packet["interfaces"]["details"]:

        if interface["admin_status"] == "down":

            analysis.append(
                f"{interface['name']} appears to be administratively down. "
                f"Description: {interface['description']}. "
                f"If this interface is expected to be active, verify whether the shutdown is intentional."
            )

    if not analysis:
        analysis.append("No issues detected.")

    return analysis


def analyze_with_ai(knowledge_packet):
    """
    Sends the knowledge packet to GPT for AI analysis.
    """

    prompt = load_prompt()
    client = get_openai_client()

    knowledge_json = json.dumps(knowledge_packet, indent=2)

    response = client.responses.create(
        model="gpt-5.6",
        input=f"""
{prompt}

Knowledge Packet:
{knowledge_json}
""",
        text={
            "format": {
                "type": "json_schema",
                "name": "network_analysis",
                "schema": {
                    "type": "object",
                    "properties": {
                        "findings": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "interface": {"type": "string"},
                                    "severity": {
                                        "type": "string",
                                        "enum": ["HIGH", "MEDIUM", "LOW"]
                                    },
                                    "severity_reason": {
                                        "type": "string"
                                    },
                                    "observed_facts": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "inferences": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "possible_impact": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "recommended_actions": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "additional_data_needed": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                },
                                "required": [
                                    "interface",
                                    "severity",
                                    "severity_reason",
                                    "observed_facts",
                                    "inferences",
                                    "possible_impact",
                                    "recommended_actions",
                                    "additional_data_needed"
                                ],
                                "additionalProperties": False
                            }
                        },
                        "overall_priority_summary": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["findings", "overall_priority_summary"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    )
    return json.loads(response.output_text)
