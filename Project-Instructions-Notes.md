Design notes mapped to Project-Instructions.md

- Input: Two policy document locations (Azure Blob SAS or local)
- Output: JSON strictly matching provided schema
- Logic: Prompted LLM via Semantic Kernel; schema validation and auto-repair of JSON
- File types: .txt, .pdf, .docx
- CLI provided for simple execution
