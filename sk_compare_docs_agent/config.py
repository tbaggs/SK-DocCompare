import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class ModelConfig:
    temperature: float
    max_tokens: int
    use_json_mode: bool
    azure_endpoint: str | None
    azure_api_key: str | None
    azure_deployment: str | None


load_dotenv(override=False)


def get_model_config() -> ModelConfig:

    return ModelConfig(
        temperature = float(os.getenv("MODEL_TEMPERATURE")),
        max_tokens = int(os.getenv("MODEL_MAX_TOKENS")),
        use_json_mode = os.getenv("USE_JSON_MODE"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT")
    )
