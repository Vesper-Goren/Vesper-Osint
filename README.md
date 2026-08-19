















__      __        _____            ____       _       _   
 \ \    / /       |  __ \          / __ \     (_)     | |  
  \ \  / /__  ___ | |__) |__ _ __ | |  | |___  _ _ __ | |_ 
   \ \/ / _ \/ __||  ___/ _ \ '__|| |  | / __|| | '_ \| __|
    \  /  __/\__ \| |  |  __/ |   | |__| \__ \| | | | | |_ 
     \/ \___||___/|_|   \___|_|    \____/|___/|_|_| |_|\__| 

Merhaba, ben Berat. Üzerinde uzun süredir çalıştığım bir aracı sizinle paylaşmak istiyorum.

Son zamanlarda siber güvenlik alanına yoğunlaştığım için eksik kaldığımı hissettiğim bir konu vardı: Yazılım dili öğrenmek. Bu alanda kendimi geliştirmek amacıyla bir süredir Python çalışıyorum. Öğrenme sürecimi teorikte bırakmayıp siber güvenlik uygulamaları geliştirerek pratik bir hale getirmeye çalıştım ve bu çabalarımın sonucunda kendi OSINT aracımı ortaya çıkardım.

İlk olarak, bu OSINT aracını piyasadaki diğer araçlardan ayıran özelliklerden bahsetmek istiyorum. Çünkü bu projeyi geliştirirken aklımda hep "Diğerlerinden nasıl daha farklı ve etkili bir şey yapabilirim?" sorusu vardı.

1) Yanlış Pozitif (False Positive) Koruması: Daha önce kullandığım birçok araçta, aslında hesap olmayan sayfalar için "bulundu" hatası (False Positive) almak gerçekten can sıkıcıydı. Buna önlem olarak; aracın gelen HTML sayfasını okuyup WAF (Güvenlik Duvarı veya CAPTCHA) tespiti yapmasını ve sahte bir sonuç vermek yerine kullanıcıyı uyarmasını sağlayan bir sistem ekledim.

2) Derin Veri Çekme (Scraping): Diğer araçlar genellikle sadece hedefin profil URL'sini verirken, bu araç sayfanın içine girerek açıklama (biyografi) kısmını ve sayfa başlıklarını da çeker. Bu sayede profilleri tek tek manuel ziyaret etme zahmetinden ve zaman kaybından kurtulmuş oluruz.

3) Yüksek Hız (Multithreading): Araç, asenkron mimarisiyle aynı anda birden fazla siteye eşzamanlı istek atar. Bu sayede yüzlerce sitenin taranması dakikalar değil, saniyeler sürer ve sonuçlar çok daha hızlı gelir.

4) Gizlilik ve Ban Koruması (Stealth): Yüksek hızda tarama yapmanın kaçınılmaz sonlarından biri sunucular tarafından engellenmektir (ban). Bunu önlemek için araç, havuzunda bulunan dinamik HTTP Headers (User-Agent) bilgileriyle her siteye farklı bir tarayıcı/cihazmış gibi istek gönderiyor. Ayrıca Proxy/TOR desteği sayesinde trafiği gizleyerek tamamen gerçek bir insan (robot olmayan) davranışı sergileyebiliyor.

Kullanımı oldukça basittir. Terminal üzerinden aşağıdaki komutla taramayı başlatabilirsiniz:
python main.py -u <KULLANICI_ADI>

Araç, elde ettiği sonuçları hem okunabilir şekilde terminale basar hem de ileride analiz edilebilmesi için 'output' klasörüne JSON ve TXT formatlarında otomatik olarak kaydeder.
