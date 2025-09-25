import json
from typing import Any

from jsonschema import Draft202012Validator

SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "PolicyDocumentComparison",
    "type": "object",
    "properties": {
        "documentSimilarity": {
            "type": "boolean",
            "description": "Indicates whether the two documents are considered similar (true) or not (false).",
        },
        "documentDifferences": {
            "type": "array",
            "description": "List of differences between the two documents.",
            "items": {"type": "string"},
        },
        "documentIntegrationSteps": {
            "type": "array",
            "description": "Step-by-step actions to integrate or reconcile the two documents.",
            "items": {"type": "string"},
        },
    },
    "required": [
        "documentSimilarity",
        "documentDifferences",
        "documentIntegrationSteps",
    ],
    "additionalProperties": False,
}

_validator = Draft202012Validator(SCHEMA)


def validate_or_raise(data: Any) -> None:
    errors = sorted(_validator.iter_errors(data), key=lambda e: e.path)
    if errors:
        msgs = [f"{list(e.path)}: {e.message}" for e in errors]
        raise ValueError("Invalid JSON per schema: \n" + "\n".join(msgs))
