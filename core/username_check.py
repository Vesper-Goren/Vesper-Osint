import requests
import json
import time
import random
from bs4 import BeautifulSoup
import concurrent.futures

user = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/115.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
]

wafsignal = ["cloudflare", "verify you are a human", "incapsula", "captcha", "attention required!"]

def check_waf(html_content, status_code):
    if status_code in [403, 429]: 
        return True
    for signature in wafsignal:
        if signature.lower() in html_content.lower():
            return True
    return False

def extract_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.find('title')
    title_text = title.text.strip() if title else "Başlık bulunamadı"
    
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    og_desc = soup.find('meta', attrs={'property': 'og:description'})
    
    if meta_desc and meta_desc.has_attr('content'):
        desc_text = meta_desc['content'].strip()
    elif og_desc and og_desc.has_attr('content'):
        desc_text = og_desc['content'].strip()
    else:
        desc_text = "Açıklama bulunamadı veya WAF tarafından gizlendi"
        
    return {"title": title_text, "description": desc_text}

def check_single_site(site, data, username, proxies):
    
    target_url = data['url'].format(username)
    headers = {
        'User-Agent': random.choice(user),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none'
    }
    
    time.sleep(random.uniform(0.1, 0.8)) 
    
    try:
        response = requests.get(target_url, headers=headers, proxies=proxies, timeout=10)
        html_content = response.text
        status_code = response.status_code
        
        is_waf_blocked = check_waf(html_content, status_code)
        
        account_exists = False
        if data['errorType'] == "status_code" and status_code == 200:
            account_exists = True
        elif data['errorType'] == "message" and 'errorMsg' in data:
            error_msgs = data['errorMsg']
            if isinstance(error_msgs, str):
                error_msgs = [error_msgs]
                
            is_missing = any(msg in html_content for msg in error_msgs)
            if not is_missing:
                account_exists = True
                
        if account_exists:
            scraped_data = extract_info(html_content) if not is_waf_blocked else {"title": "WAF Engeli", "description": "İçerik güvenlik duvarı tarafından gizlendi."}
            return site, {
                "url": target_url,
                "waf_warning": is_waf_blocked,
                "scraped_info": scraped_data
            }
            
    except requests.exceptions.RequestException:
        pass
        
    return site, None

def scan_user(username, use_proxy=False, proxy_url="socks5://127.0.0.1:9050"):
    with open('wordlists/sites.json', 'r', encoding='utf-8') as file:
        sites = json.load(file)
    
    found_accounts = {}
    proxies = {"http": proxy_url, "https": proxy_url} if use_proxy else {}

    print(f"[*] '{username}' için tarama başlatılıyor (Proxy: {use_proxy})...")
    print(f"[*] {len(sites)} site eşzamanlı taranıyor, lütfen 30-60 saniye bekleyin...\n")

   
    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
       
        futures = [executor.submit(check_single_site, site, data, username, proxies) for site, data in sites.items()]
       
        for future in concurrent.futures.as_completed(futures):
            site, result = future.result()
            if result:
                found_accounts[site] = result
                
    return found_accounts