import os

from foundry_ocr import (
    ocr_extract_from_file,
    ocr_extract_from_url,
    ocr_extract_with_layout,
)


def expect_value_error(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except ValueError as e:
        print(f"PASS: {func.__name__} raised ValueError as expected: {e}")
        return True
    except Exception as e:
        print(f"FAIL: {func.__name__} raised unexpected {type(e).__name__}: {e}")
        return False
    else:
        print(f"FAIL: {func.__name__} did not raise ValueError")
        return False


def main():
    # Temporarily remove endpoint env vars to exercise the ValueError behavior
    original_tools = os.environ.pop("FOUNDRY_TOOLS_ENDPOINT", None)
    original_project = os.environ.pop("FOUNDRY_PROJECT_ENDPOINT", None)

    print("Running dry/unit tests (expect ValueError when endpoints aren't configured)...")
    expect_value_error(ocr_extract_from_file, "nonexistent.pdf")
    expect_value_error(ocr_extract_from_url, "https://example.com/doc.png")
    expect_value_error(ocr_extract_with_layout, "nonexistent.pdf")

    # restore env
    if original_tools is not None:
        os.environ["FOUNDRY_TOOLS_ENDPOINT"] = original_tools
    if original_project is not None:
        os.environ["FOUNDRY_PROJECT_ENDPOINT"] = original_project

    if os.environ.get("RUN_INTEGRATION") == "1":
        print("\nRunning integration tests (RUN_INTEGRATION=1)...")
        sample_file = os.environ.get("SAMPLE_FILE")
        sample_url = os.environ.get("SAMPLE_URL")
        if sample_file:
            try:
                text = ocr_extract_from_file(sample_file)
                print("Integration file result (first 200 chars):\n", text[:200])
            except Exception as e:
                print("Integration file test failed:", e)
        if sample_url:
            try:
                text = ocr_extract_from_url(sample_url)
                print("Integration URL result (first 200 chars):\n", text[:200])
            except Exception as e:
                print("Integration URL test failed:", e)
        if not sample_file and not sample_url:
            print("No SAMPLE_FILE or SAMPLE_URL provided; skipping integration tests.")


if __name__ == "__main__":
    main()
