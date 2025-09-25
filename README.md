## SK-CompareDocsAgent

A Python Semantic Kernel agent that reads two policy documents (via Azure Blob SAS URLs or local files), analyzes whether they are related, identifies differences, and proposes integration steps. Outputs strict JSON matching the given schema.

### Features
- Python + Semantic Kernel prompts to produce structured JSON
- Reads .txt, .pdf, and .docx from Azure Blob SAS URLs or local files
- CLI via Typer; saves result to file or prints to stdout
- Pydantic schema validation and light output repair

### Prerequisites
- Python 3.10+
- An LLM: Azure OpenAI (recommended) or OpenAI

### Setup
1) Create and activate a virtual environment.
2) Install dependencies.
3) Configure environment variables.

#### Environment variables (Azure OpenAI only)
- AZURE_OPENAI_ENDPOINT
- AZURE_OPENAI_API_KEY
- AZURE_OPENAI_DEPLOYMENT (chat model deployment name)

Optional tuning:
- MODEL_TEMPERATURE (default 0.1)
- MODEL_MAX_TOKENS (default 1200)
- USE_JSON_MODE (true/false, attempt JSON mode output)

You can copy `.env.example` to `.env` and fill values.

### How to run

```powershell
# 1) Install deps
pip install -r requirements.txt

# 2) Set env (or put them in .env)
$env:AZURE_OPENAI_ENDPOINT = "https://<your-endpoint>.openai.azure.com/"
$env:AZURE_OPENAI_API_KEY = "<key>"
$env:AZURE_OPENAI_DEPLOYMENT = "<deployment-name>"

# 3) Run comparison (SAS URLs)
python -m sk_compare_docs_agent `
  "https://<account>.blob.core.windows.net/<container>/<file1>.pdf?<SAS>" `
  "https://<account>.blob.core.windows.net/<container>/<file2>.docx?<SAS>" `
  --output result.json --pretty

# Local files
python -m sk_compare_docs_agent .\samples\primary.txt .\samples\secondary.txt --output result.json
```

The project now uses only the standard `main.py` entrypoint; the previous Typer CLI has been removed.

### Output schema
The output strictly matches:

```
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "PolicyDocumentComparison",
  "type": "object",
  "properties": {
    "documentSimilarity": { "type": "boolean" },
    "documentDifferences": { "type": "array", "items": { "type": "string" } },
    "documentIntegrationSteps": { "type": "array", "items": { "type": "string" } }
  },
  "required": [
    "documentSimilarity",
    "documentDifferences",
    "documentIntegrationSteps"
  ],
  "additionalProperties": false
}
```

### Notes
- PDFs and DOCX extraction are best-effort. For complex documents, consider preprocessing to text.
- If the LLM returns non-JSON, the agent attempts repair once and validates again.
