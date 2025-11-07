import os
import fitz  # PyMuPDF – best for accurate text extraction
import docx2txt
import re

# Optional OCR imports
try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


def extract_text(file_path):
    """
    Extract text from a resume (PDF or DOCX) with high accuracy.
    Automatically handles:
      - normal PDFs
      - scanned PDFs (OCR fallback)
      - Word files (.docx)
    """

    text = ""

    # -----------------------------------------------------------
    # 1️⃣ PDF Extraction (Primary: PyMuPDF)
    # -----------------------------------------------------------
    if file_path.lower().endswith(".pdf"):
        try:
            with fitz.open(file_path) as doc:
                for page_num, page in enumerate(doc, start=1):
                    try:
                        page_text = page.get_text("text") or ""

                        # If the page has no selectable text (scanned image)
                        if not page_text.strip() and OCR_AVAILABLE:
                            pix = page.get_pixmap()
                            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                            ocr_text = pytesseract.image_to_string(img)
                            text += ocr_text + "\n"
                            img.close()
                            del pix
                        else:
                            text += page_text + "\n"

                    except Exception as inner_e:
                        print(f"[WARN] Failed to read page {page_num}: {inner_e}")

        except Exception as e:
            print(f"[ERROR] Error reading PDF: {e}")
            raise ValueError(f"Error reading PDF file: {file_path}\n{e}")

    # -----------------------------------------------------------
    # 2️⃣ DOCX Extraction (Simple + Safe)
    # -----------------------------------------------------------
    elif file_path.lower().endswith(".docx"):
        try:
            text = docx2txt.process(file_path)
        except Exception as e:
            print(f"[ERROR] Error reading DOCX: {e}")
            raise ValueError(f"Error reading DOCX file: {file_path}\n{e}")

    # -----------------------------------------------------------
    # 3️⃣ Unsupported File Type
    # -----------------------------------------------------------
    else:
        raise ValueError("Unsupported file format. Please upload PDF or DOCX files only.")

    # -----------------------------------------------------------
    # 4️⃣ Final Cleanup
    # -----------------------------------------------------------
    # Normalize whitespace, remove hidden characters
    text = " ".join(text.split())
    text = text.replace("\x00", "").strip()

    if not text:
        print(f"[WARN] No text extracted from file: {file_path}")
        if file_path.lower().endswith(".pdf") and not OCR_AVAILABLE:
            print("[INFO] You can enable OCR by installing pytesseract and pillow.")

    return text


def validate_email(email):
    """
    Validates that email matches strict email pattern and has no invalid prefixes or suffixes.
    """
    valid_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if re.match(valid_pattern, email):
        # Additional cleanup for common noise (e.g. remove leading - or trailing anything after .com)
        cleaned_email = re.sub(r"^[-]+", "", email)
        cleaned_email = re.sub(r"\.?(linkedin\.com|facebook\.com|twitter\.com|instagram\.com|phone|india|[0-9]+)$", "", cleaned_email)
        return cleaned_email
    return None


def extract_email(text):
    """
    Extracts valid email address(es) from given text using strict regex and validation.
    Returns a list of cleaned valid emails.
    """
    # Regex to fetch candidate emails
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    candidate_emails = re.findall(pattern, text)

    valid_emails = []
    for email in candidate_emails:
        clean_email = validate_email(email)
        if clean_email and clean_email not in valid_emails:
            valid_emails.append(clean_email)

    return valid_emails
