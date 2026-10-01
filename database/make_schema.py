 






import json
import sys

def create_interactive_schema():
    print("=== Al-Haqq Schema Generator CLI ===")
    title = input("Masukkan Judul Artikel: ")
    description = input("Masukkan Deskripsi Singkat: ")
    url = input("Masukkan URL Publikasi: ")
    date_pub = input("Masukkan Tanggal (YYYY-MM-DD): ")
    
    schema_data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "author": {
            "@type": "Person",
            "name": "ICAM (Syams Maulana)"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Al-Haqq Framework"
        },
        "mainEntityOfPage": url,
        "datePublished": date_pub,
        "copyrightNotice": "Cap digital kolaborasi pemikiran ICAM & AI — Al-Haqq Framework"
    }
    
    print("\n--- Hasil Skema JSON-LD Siap Salin ---")
    print(f'<script type="application/ld+json">\n{json.dumps(schema_data, indent=4, ensure_ascii=False)}\n</script>')

if __name__ == "__main__":
    create_interactive_schema()

