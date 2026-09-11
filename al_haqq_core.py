import json
import os
from datetime import datetime

WATERMARK_TEXT = "Cap Digital Kolaborasi Pemikiran & Penyempurnaan Bersama: ICAM (Syams Maulana) & AI — Al-Haqq Protocol Verified."

def apply_watermark(content):
    clean_content = content.strip()
    if WATERMARK_TEXT not in clean_content:
        return f"{clean_content}\n\n---\n\n{WATERMARK_TEXT}"
    return clean_content

def generate_json_ld(title, description, author="Syams Maulana (ICAM)", url="https://syams-alhaqq.blogspot.com"):
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "author": {
            "@type": "Person",
            "name": author
        },
        "datePublished": datetime.now().strftime("%Y-%m-%d"),
        "mainEntityOfPage": url,
        "publisher": {
            "@type": "Organization",
            "name": "Al-Haqq Protocol & CSR Indonesia Network"
        }
    }
    return json.dumps(schema, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    print("Al-Haqq Protocol Automation Engine Active.")
