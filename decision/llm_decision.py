from typing import TypedDict
from openai import OpenAI
import json
import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config" / "llm.yaml"
CONFIG = yaml.safe_load(CONFIG_PATH.read_text())

MODEL_NAME = CONFIG["model_name"]
TEMPERATURE = CONFIG["temperature"]
MAX_TOKENS = CONFIG["max_tokens"]
TIMEOUT = CONFIG["timeout"]
SYSTEM_PROMPT = CONFIG["prompt"]

class DecisionInput(TypedDict):
    ok_count: int
    error_count: int
    timeout_count: int
    last_status: str
    latency_ms: float

class DecisionOutput(TypedDict):
    decision: str
    incident_type: str
    confidence: float

def llm_decide(state: DecisionInput) -> DecisionOutput:
    print(">>> LLM CALLED <<<")
    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL_NAME,
        response_format={"type": "json_object"},
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(state)},
        ],
        timeout=TIMEOUT,
    )
    raw = response.choices[0].message.content
    print(">>> LLM RESPONSE RECEIVED <<<")
    try:
        data = json.loads(raw)
    except Exception:
        raise ValueError("LLM did not return valid JSON")
    required = ["decision", "incident_type", "confidence"]
    for field in required:
        if field not in data:
            raise ValueError(f"Missing field: {field}")
    if not isinstance(data["confidence"], (float, int)):
        raise ValueError("confidence must be a float")
    return data