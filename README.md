# MSFoundryOCR

A lightweight Python wrapper around Azure AI Foundry / Azure AI Document Intelligence for extracting text (OCR) from documents and images.

It handles authentication (via `DefaultAzureCredential`), endpoint resolution, and result parsing, so you can call one function and get back plain text — or structured, word-level layout data with bounding boxes and confidence scores.

## Features

- 📄 Extract text from local files (PDF, PNG, JPG, TIFF, etc.)
- 🌐 Extract text from documents hosted at a public URL
- 📐 Optional word-level layout output (bounding boxes, confidence)
- 🔐 Auth via `DefaultAzureCredential` (Azure CLI login, managed identity, or service principal env vars)
- ⚙️ Works with either a Document Intelligence resource endpoint or an Azure AI Foundry project endpoint

## Prerequisites

- Python 3.8+
- An Azure subscription with an **Azure AI Document Intelligence** resource (or an **Azure AI Foundry** project) provisioned
- Azure credentials available in your environment (see [Configuration](#configuration))

## Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/praveen11singh/MSFoundryOCR.git
cd MSFoundryOCR
python -m pip install -r requirements.txt
```

## Configuration

Set **one** of the following environment variables (e.g. in a `.env` file at the project root):

| Variable | Description |
|---|---|
| `FOUNDRY_TOOLS_ENDPOINT` | Direct Document Intelligence endpoint, e.g. `https://<resource-name>.cognitiveservices.azure.com/` |
| `FOUNDRY_PROJECT_ENDPOINT` | Azure AI Foundry project endpoint, e.g. `https://<resource-name>.services.ai.azure.com/api/projects/<project>` — the underlying Document Intelligence endpoint is derived automatically |

Authentication is handled by [`DefaultAzureCredential`](https://learn.microsoft.com/python/api/overview/azure/identity-readme?view=azure-python#defaultazurecredential), which will try (in order) environment variables, managed identity, and the Azure CLI login. Make sure one of these is configured for your environment, for example:

```bash
az login
```

## Quick Usage

Run the included CLI example, which OCRs the sample PDF in the repo:

```bash
python foundry_ocr.py
```

Or import the package directly in your own code:

```python
from foundry_ocr import (
    ocr_extract_from_file,
    ocr_extract_from_url,
    ocr_extract_with_layout,
)

# Extract plain text from a local file
text = ocr_extract_from_file("sample.pdf")
print(text)

# Extract plain text from a document at a public URL
text = ocr_extract_from_url("https://example.com/sample-invoice.png")
print(text)

# Extract word-level layout data (bounding boxes + confidence)
layout = ocr_extract_with_layout("sample.pdf")
print(layout)
```

### API Reference

| Function | Description |
|---|---|
| `ocr_extract_from_file(file_path: str) -> str` | Runs OCR on a local file and returns extracted text. |
| `ocr_extract_from_url(document_url: str) -> str` | Runs OCR on a document at a public URL and returns extracted text. |
| `ocr_extract_with_layout(file_path: str) -> list` | Runs OCR on a local file and returns per-page word data (text, confidence, bounding polygon). |

All functions use Azure Document Intelligence's `prebuilt-read` model under the hood.

## Project Structure

```
MSFoundryOCR/
├── foundry_ocr/
│   └── api.py          # Core OCR functions (client setup, extraction, parsing)
├── foundry_ocr.py       # CLI wrapper / usage examples
├── tests/                # Test suite
├── run_test.py           # Test runner
├── requirements.txt
├── sample.pdf            # Sample file for quick testing
└── .env                  # Environment variables (not committed with secrets)
```

## Running Tests

```bash
python -m pip install -r requirements.txt
pytest
```

or

```bash
python run_test.py
```

## Troubleshooting

- **`ValueError: Set FOUNDRY_TOOLS_ENDPOINT or FOUNDRY_PROJECT_ENDPOINT`** — make sure one of the two environment variables is set and loaded (check your `.env` file and that `python-dotenv` is finding it).
- **Authentication errors** — confirm you're logged in via `az login`, or that the appropriate service principal environment variables (`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_SECRET`) are set.
- **Could not parse resource name from endpoint** — double-check the format of `FOUNDRY_PROJECT_ENDPOINT`; it must match `https://<resource-name>.services.ai.azure.com/...`.

## Contributing

Issues and pull requests are welcome. If you're adding a new extraction mode or model, please include a corresponding test in `tests/`.

## License

No license has been specified for this repository yet. Until one is added, all rights are reserved by the author.
