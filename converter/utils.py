import pdfplumber, pytesseract
from PIL import Image
from markdownify import markdownify as md
import tiktoken
import os
from openai import OpenAI
from typing import List

OPEN_AI_TOKEN = os.getenv("OPEN_AI_KEY")
client = OpenAI(api_key=OPEN_AI_TOKEN)

SYSTEM_PROMPT = (
    "You are an assistant that converts noisy OCR / PDF-extracted text into "
    "clean, well-structured Markdown. Output ONLY Markdown. Do NOT add any "
    "explanatory text, headings about your process, or JSON — just the Markdown."
)

USER_INSTRUCTION_TEMPLATE = (
    "Convert the following raw text into clean Markdown. Preserve headings, "
    "detect lists, convert tables where possible (use Markdown tables), "
    "use headings (##, ###) for sections, bullets for lists, and paragraphs. "
    "If the input contains obvious page breaks, preserve them as HTML comments "
    "<!-- PAGE_BREAK --> between pages.\n\n"
    "Input:\n\n{content}"
)

from openai import APIConnectionError

def call_model_to_markdown(text: str, model="gpt-4o-mini", max_tokens_per_chunk=3000) -> str:
    markdown_parts = []
    for chunk in chunk_text(text, max_tokens=max_tokens_per_chunk):
        prompt = USER_INSTRUCTION_TEMPLATE.format(content=chunk)
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2000,
                temperature=0.0,
            )
            md = resp.choices[0].message.content
            markdown_parts.append(md.strip())
        except APIConnectionError:
            return "⚠️ Could not connect to OpenAI API. Please check your internet connection."
        except Exception as e:
            return f"⚠️ Unexpected error: {e}"
    return "\n\n".join(markdown_parts)

# ---------------------------------------------------

def num_tokens(text, encoding_name="cl100k_base"):
    enc = tiktoken.get_encoding(encoding_name)
    return len(enc.encode(text))

def chunk_text(text, max_tokens=3000, encoding_name="cl100k_base"):
    enc = tiktoken.get_encoding(encoding_name)
    tokens = enc.encode(text)
    start = 0
    while start < len(tokens):
        end = min(len(tokens), start + max_tokens)
        chunk_tokens = tokens[start:end]
        yield enc.decode(chunk_tokens)
        start = end

#----------------------------------------------------

def pdf_to_pages(path):
    pages = []
    with pdfplumber.open(path) as pdf:
        for i,page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages.append(text.strip())
    return pages

def pdf_to_text(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def pdf_to_markdown(path):
    pages = pdf_to_pages(path)
    final_markdown_pages = []

    for i, page_text in enumerate(pages):
        if not page_text.strip():
            final_markdown_pages.append(f"<!-- PAGE {i+1} EMPTY -->")
            continue

        md = call_model_to_markdown(page_text)
        final_markdown_pages.append(f"<!-- PAGE {i+1} START -->\n\n{md}\n\n<!-- PAGE {i+1} END -->")

    return "\n\n---\n\n".join(final_markdown_pages)

def image_to_text(path):
    return pytesseract.image_to_string(Image.open(path))

def text_to_markdown(text):
    return md(text)
