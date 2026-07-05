import os
import re
from azure.identity import DefaultAzureCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
# Either set FOUNDRY_TOOLS_ENDPOINT directly:
#   https://<resource-name>.cognitiveservices.azure.com/
# ...or set FOUNDRY_PROJECT_ENDPOINT and let us derive it automatically.
PROJECT_ENDPOINT = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
EXPLICIT_TOOLS_ENDPOINT = os.environ.get("FOUNDRY_TOOLS_ENDPOINT")

credential = DefaultAzureCredential()


def _resolve_foundry_tools_endpoint() -> str:
    if EXPLICIT_TOOLS_ENDPOINT:
        return EXPLICIT_TOOLS_ENDPOINT
    if not PROJECT_ENDPOINT:
        raise ValueError("Set FOUNDRY_TOOLS_ENDPOINT or FOUNDRY_PROJECT_ENDPOINT")
    match = re.match(r"https://([^.]+)\.services\.ai\.azure\.com", PROJECT_ENDPOINT)
    if not match:
        raise ValueError(f"Could not parse resource name from {PROJECT_ENDPOINT!r}")
    resource_name = match.group(1)
    return f"https://{resource_name}.cognitiveservices.azure.com/"


def _get_document_intelligence_client() -> DocumentIntelligenceClient:
    endpoint = _resolve_foundry_tools_endpoint()
    return DocumentIntelligenceClient(endpoint=endpoint, credential=credential)


def ocr_extract_from_url(document_url: str) -> str:
    """Run OCR on a document/image available at a public URL and return extracted text."""
    client = _get_document_intelligence_client()
    poller = client.begin_analyze_document(
        "prebuilt-read",
        AnalyzeDocumentRequest(url_source=document_url),
    )
    result = poller.result()
    return _extract_text(result)


def ocr_extract_from_file(file_path: str) -> str:
    """Run OCR on a local file (PDF, PNG, JPG, TIFF, etc.) and return extracted text."""
    client = _get_document_intelligence_client()
    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-read",
            body=f,
            content_type="application/octet-stream",
        )
    result = poller.result()
    return _extract_text(result)


def _extract_text(result) -> str:
    """Pull plain text out of the analysis result, page by page."""
    lines = []
    for page in result.pages:
        for line in page.lines:
            lines.append(line.content)
    return "\n".join(lines)


def ocr_extract_with_layout(file_path: str):
    """
    Same as above, but also returns bounding boxes and confidence-adjacent
    structure (words), useful if you need positions, not just raw text.
    """
    client = _get_document_intelligence_client()
    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-read",
            body=f,
            content_type="application/octet-stream",
        )
    result = poller.result()

    pages_data = []
    for page in result.pages:
        words = [
            {"text": w.content, "confidence": w.confidence, "polygon": w.polygon}
            for w in (page.words or [])
        ]
        pages_data.append({"page_number": page.page_number, "words": words})
    return pages_data


__all__ = [
    "ocr_extract_from_url",
    "ocr_extract_from_file",
    "ocr_extract_with_layout",
]
