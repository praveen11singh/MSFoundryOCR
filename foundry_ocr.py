from foundry_ocr import (
    ocr_extract_from_file,
    ocr_extract_from_url,
    ocr_extract_with_layout,
)


if __name__ == "__main__":
    # Example 1: OCR from a local file
    text = ocr_extract_from_file("sample.pdf")
    print("Extracted text:\n", text)

    # Example 2: OCR from a URL
    # text = ocr_extract_from_url("https://example.com/sample-invoice.png")
    # print(text)

    # Example 3: With word-level layout/confidence data
    # layout = ocr_extract_with_layout("sample.pdf")
    # print(layout)