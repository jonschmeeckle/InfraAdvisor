import os
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

def analyze_with_ai(knowledge_packet):
    """
    Simulates how an AI model would analyze a knowledge packet.
    This will later be replaced with a real LLM.
    """

    prompt = load_prompt()

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
