# Foundry OCR

Small wrapper and package for running Azure Foundry / Document Intelligence OCR.

Installation
------------

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Configuration
-------------

Set either `FOUNDRY_TOOLS_ENDPOINT` (e.g. https://<name>.cognitiveservices.azure.com/) or
`FOUNDRY_PROJECT_ENDPOINT` (e.g. https://<name>.services.ai.azure.com/api/projects/<project>)
in the environment. `DefaultAzureCredential` is used; ensure your Azure auth is configured
for the environment (CLI login, managed identity, or service principal variables).

Quick usage
-----------

Run the CLI wrapper:

```bash
python foundry_ocr.py
```

Import from the package in Python:

```python
from foundry_ocr import ocr_extract_from_file

text = ocr_extract_from_file("sample.pdf")
print(text)
```

Files
-----

- [foundry_ocr/api.py](foundry_ocr/api.py) — core functions
- [foundry_ocr.py](foundry_ocr.py) — CLI wrapper that imports the package
