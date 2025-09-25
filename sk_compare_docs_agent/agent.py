import json
from typing import Any

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIPromptExecutionSettings


from config import get_model_config
from schema import PolicyDocumentComparison


PROMPT_PATH = "prompts/compare_policy_documents.skprompt.txt"


def _build_kernel() -> Kernel:
    cfg = get_model_config()
    kernel = Kernel()

    if not (cfg.azure_endpoint and cfg.azure_api_key and cfg.azure_deployment):
        raise RuntimeError("Missing Azure OpenAI configuration.")
    kernel.add_service(
        AzureChatCompletion(
            service_id="chat",
            deployment_name=cfg.azure_deployment,
            endpoint=cfg.azure_endpoint,
            api_key=cfg.azure_api_key,
        )
    )

    return kernel


async def run_comparison(primary_text: str, secondary_text: str) -> PolicyDocumentComparison:
    kernel = _build_kernel()

    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    # Compose the final prompt using SK template variables
    rendered_prompt = prompt_template.replace("{{$input}}", "Analyze and return only valid JSON per the schema.")
    rendered_prompt = rendered_prompt.replace("{{$primary}}", primary_text)
    rendered_prompt = rendered_prompt.replace("{{$secondary}}", secondary_text)

    # Invoke the model directly with the rendered prompt. If JSON mode requested,
    # we pass a hint via function_call / response_format (provider-dependent). Semantic Kernel
    # currently surfaces limited native JSON-mode control; we emulate by strongly constraining the prompt
    # and (optionally) attaching an expected response format object where supported.

    cfg = get_model_config()
    if cfg.use_json_mode:
        # Attempt structured invocation (future-proof: Semantic Kernel may accept response_format kwarg)
        try:
            settings = OpenAIPromptExecutionSettings(
                max_tokens=cfg.max_tokens,
                temperature=cfg.temperature,
                response_format={"type": "json_object"}  # guarantees valid JSON
            )

            result = await kernel.invoke_prompt(rendered_prompt, service_id="chat", settings=settings)
        except TypeError:
            # Fallback if response_format unsupported
            result = await kernel.invoke_prompt(rendered_prompt, service_id="chat")
    else:
        settings = OpenAIPromptExecutionSettings(
            max_tokens=cfg.max_tokens,
            temperature=cfg.temperature,
        )

        result = await kernel.invoke_prompt(rendered_prompt, service_id="chat", settings=settings)

    raw = str(result)

    def _try_parse(text: str) -> PolicyDocumentComparison:
        data: Any = json.loads(text)
        return PolicyDocumentComparison.model_validate(data)

    try:
        return _try_parse(raw)
    except Exception:
        # Light repair: find first and last braces
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            snippet = raw[start : end + 1]
            try:
                return _try_parse(snippet)
            except Exception:
                pass
        raise
