import argparse
from colorama import Fore, Style, init
from core.username_check import scan_user
from core.reporter import save_results


init(autoreset=True)

def print_banner():
    
    banner = rf"""
{Fore.RED}
 __      __        _____            ____       _       _   
 \ \    / /       |  __ \          / __ \     (_)     | |  
  \ \  / /__  ___ | |__) |__ _ __ | |  | |___  _ _ __ | |_ 
   \ \/ / _ \/ __||  ___/ _ \ '__|| |  | / __|| | '_ \| __|
    \  /  __/\__ \| |  |  __/ |   | |__| \__ \| | | | | |_ 
     \/ \___||___/|_|   \___|_|    \____/|___/|_|_| |_|\__| 
{Style.RESET_ALL}
    {Fore.YELLOW} OSINT ve Profil Toplama Aracı - vesper{Style.RESET_ALL}
    """
    print(banner)

def main():
    print_banner()
    
    
    parser = argparse.ArgumentParser(description="Hedef kullanıcı adını açık kaynaklarda arar.")
    parser.add_argument("-u", "--username", required=True, help="Taranacak hedef kullanıcı adı (Örn: ahmet123)")
    parser.add_argument("--proxy", action="store_true", help="İz gizlemek için yerel Proxy/TOR ağını kullan")
    
    
    args = parser.parse_args()
    
    username = args.username
    use_proxy = args.proxy
    
    print(f"{Fore.CYAN}[+] Hedef: {username}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[+] Proxy Kullanımı: {'Aktif' if use_proxy else 'Pasif'}{Style.RESET_ALL}\n")
    
    
    results = scan_user(username, use_proxy=use_proxy)
    
    print(f"\n{Fore.CYAN}[+] Tarama Tamamlandı. Sonuçlar:{Style.RESET_ALL}")
    print("-" * 60)
    
    if not results:
        print(f"{Fore.RED}[+] Hiçbir platformda hesap bulunamadı.{Style.RESET_ALL}")
    else:
        for site, data in results.items():
           
            waf_alert = f" {Fore.YELLOW}[WAF TESPİT EDİLDİ - Manuel Kontrol Gerekli]{Style.RESET_ALL}" if data['waf_warning'] else ""
            
            
            print(f"{Fore.GREEN}[+] {site}:{Style.RESET_ALL} {data['url']}{waf_alert}")
            
            
            if not data['waf_warning']:
                title = data['scraped_info'].get('title', 'Bulunamadı')
                desc = data['scraped_info'].get('description', 'Bulunamadı')
                
               
                if len(desc) > 80:
                    desc = desc[:80] + "..."
                    
                print(f"    {Fore.LIGHTBLACK_EX}└─ Başlık: {title}{Style.RESET_ALL}")
                print(f"    {Fore.LIGHTBLACK_EX}└─ Açıklama: {desc}{Style.RESET_ALL}")
            print()
            
        
        print(f"{Fore.YELLOW}[+] Rapor kaydediliyor...{Style.RESET_ALL}")
        
        
        json_file = save_results(username, results, format_type="json")
        txt_file = save_results(username, results, format_type="txt")
        
        print(f"{Fore.GREEN}[+] Raporlar başarıyla oluşturuldu!{Style.RESET_ALL}")
        print(f"    {Fore.LIGHTBLACK_EX}└─ {json_file}{Style.RESET_ALL}")
        print(f"    {Fore.LIGHTBLACK_EX}└─ {txt_file}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()