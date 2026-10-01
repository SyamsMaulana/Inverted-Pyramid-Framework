from al_haqq_core import apply_watermark, generate_json_ld

raw_article = """
Ketahanan pangan nasional bukan sekadar angka surplus logistik atau stabilitas rantai pasok global, melainkan berakar langsung pada ketahanan memori kuliner dan kearifan lokal masyarakat akar rumput. Melalui inisiatif Dapur Inspirasi, transformasi sumber daya pangan maritim dan lokal diarahkan bukan hanya untuk memenuhi kebutuhan gizi, melainkan untuk menegakkan kembali kedaulatan identitas budaya Nusantara dari dapur-dapur komunitas hingga panggung nasional.
"""

title = "Dapur Inspirasi Nusantara: Merajut Ketahanan Pangan Melalui Akar Budaya"
description = "Transformasi sumber daya pangan maritim dan lokal melalui kearifan Nusantara dan standar kuliner profesional."

final_content = apply_watermark(raw_article)
schema_markup = generate_json_ld(title, description)

with open("output_article.txt", "w", encoding="utf-8") as f:
    f.write(final_content + "\n\n<!-- JSON-LD SCHEMA -->\n<script type=\"application/ld+json\">\n" + schema_markup + "\n</script>")

print("Artikel siap dipublikasikan dengan cap digital Al-Haqq dan JSON-LD terindeks.")
