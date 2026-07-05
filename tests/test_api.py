import os
import importlib

import pytest


def test_import_package():
    # package should import
    mod = importlib.import_module("foundry_ocr")
    assert hasattr(mod, "ocr_extract_from_file")


def test_functions_raise_without_endpoint(monkeypatch):
    # ensure no endpoints are set
    monkeypatch.delenv("FOUNDRY_TOOLS_ENDPOINT", raising=False)
    monkeypatch.delenv("FOUNDRY_PROJECT_ENDPOINT", raising=False)

    from foundry_ocr import (
        ocr_extract_from_file,
        ocr_extract_from_url,
        ocr_extract_with_layout,
    )

    with pytest.raises(ValueError):
        ocr_extract_from_file("nonexistent.pdf")

    with pytest.raises(ValueError):
        ocr_extract_from_url("https://example.com/doc.png")

    with pytest.raises(ValueError):
        ocr_extract_with_layout("nonexistent.pdf")
