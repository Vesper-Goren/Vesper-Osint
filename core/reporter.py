import json
import os
from datetime import datetime

def save_results(username, data, format_type="json"):
    if not os.path.exists("output"):
        os.makedirs("output")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format_type == "json":
        filename = f"output/{username}_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
    elif format_type == "txt":
        filename = f"output/{username}_{timestamp}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"--- {username} İÇİN OSİNT RAPORU ---\n")
            f.write(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for site, info in data.items():
                f.write(f"[+] {site}: {info['url']}\n")
                if info['waf_warning']:
                    f.write("    UYARI: WAF / Güvenlik Duvarı Tespit Edildi\n")
                else:
                    f.write(f"    Başlık: {info['scraped_info'].get('title', '')}\n")
                    f.write(f"    Açıklama: {info['scraped_info'].get('description', '')}\n")
                f.write("-" * 40 + "\n")
                
    return filename