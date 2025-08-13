import fitz  # PyMuPDF
import re
from typing import List, Dict
from PIL import Image
import pytesseract

def pdf_pages_to_text_bytes(fileobj) -> List[str]:
    doc = fitz.open(stream=fileobj.read(), filetype="pdf")
    texts = []
    for page in doc:
        txt = page.get_text("text")
        if txt and txt.strip():
            texts.append(txt)
        else:
            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            ocr_text = pytesseract.image_to_string(img, lang='jpn')
            texts.append(ocr_text)
    return texts

def parse_text_for_orders(text: str) -> List[Dict]:
    orders = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.search(r"(?P<item>[\u3000-\u30FF\u4E00-\u9FFF\w\-\s]+?)\s+(?P<qty>[0-9,]+)\s+(?P<unit_price>[0-9,]+)\s+(?P<amount>[0-9,]+)\s+(?P<due>\d{4}[\-/]??\d{1,2}[\-/]??\d{1,2})", line)
        if m:
            orders.append({
                "item": m.group("item").strip(),
                "qty": m.group("qty").replace(",", ""),
                "unit_price": m.group("unit_price").replace(",", ""),
                "amount": m.group("amount").replace(",", ""),
                "due": m.group("due")
            })
            continue
        parts = re.split(r"[\t,]+", line)
        if len(parts) >= 3:
            item = parts[0].strip()
            nums = re.findall(r"[0-9,]+", line)
            qty = nums[0].replace(',', '') if nums else None
            unit_price = nums[1].replace(',', '') if len(nums) > 1 else None
            date_m = re.search(r"(\d{4}[\-/]\d{1,2}[\-/]\d{1,2})", line)
            due = date_m.group(1) if date_m else None
            if item and qty:
                orders.append({
                    "item": item,
                    "qty": qty,
                    "unit_price": unit_price,
                    "amount": None,
                    "due": due
                })
                continue
    return orders

def extract_order_info_from_file(fileobj) -> List[Dict]:
    try:
        fileobj.seek(0)
    except Exception:
        pass
    page_texts = pdf_pages_to_text_bytes(fileobj)
    all_text = "\n".join(page_texts)
    all_text = all_text.replace('\u3000', ' ')
    orders = parse_text_for_orders(all_text)
    return orders
