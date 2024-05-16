import json
import re
from nltk.corpus import stopwords
from collections import Counter


#json dosyasını veriye atayan fonksiyon
def json_oku(json_dosya_adı):
    with open(json_dosya_adı, 'r', encoding='utf-8') as dosya:
        veri = json.load(dosya)
    return veri


#kullanıcı sınıfı
class Kullanici:
    def __init__(self, username, name, followers_count, following_count, language, region, tweets, following, followers):
        self.username = username
        self.name = name
        self.followers_count = followers_count
        self.following_count = following_count
        self.language = language
        self.region = region
        self.tweets = tweets
        self.following = following
        self.followers = followers


#kullanıcı sınıfından nesne türeten fonksiyon
def kullanici_nesnesi_olustur(veri):
    kullanici_listesi = []
    for kullanici_verisi in veri:
        kullanici = Kullanici(
            kullanici_verisi['username'],
            kullanici_verisi['name'],
            kullanici_verisi['followers_count'],
            kullanici_verisi['following_count'],
            kullanici_verisi['language'],
            kullanici_verisi['region'],
            kullanici_verisi['tweets'],
            kullanici_verisi['following'],
            kullanici_verisi['followers']
        )
        kullanici_listesi.append(kullanici)
    return kullanici_listesi


#fonksiyonları gerçekleştiren kısım
if __name__ == "__main__":
    json_dosya_adı = '50k_data.json'  #Burada içinde daha az kullanıcı olan bir veriseti kullandık
    veri = json_oku(json_dosya_adı)
    kullanici_listesi = kullanici_nesnesi_olustur(veri)

#verileri kendi oluşturduğumuz veri yapısına (hash tablosuna) dönüştüren kısım
    hash_tablosu = {}
    for kullanici in kullanici_listesi:
        hash_tablosu[kullanici] = {
        "username": kullanici.username,
        "name": kullanici.name,
        "followers_count": kullanici.followers_count,
        "following_count": kullanici.following_count,
        "language": kullanici.language,
        "region": kullanici.region,
        "tweets": kullanici.tweets,
        "following": kullanici.following,
        "followers": kullanici.followers,
    }

# Tüm kullanıcıların tweets'lerini birleştirme
tum_tweetler = ' '.join([tweet for kullanici in hash_tablosu for tweet in kullanici.tweets])

# Tweet'lerden gereksiz karakterleri temizleme
tum_tweetler = re.sub(r'[^a-zA-ZğüşöçıĞÜŞÖÇİ\s]', '', tum_tweetler)

# Küçük harfe dönüştürme6
tum_tweetler = tum_tweetler.lower()

# Kelimeleri ayırma ve stop word'leri filtreleme
stop_words = set(stopwords.words('turkish'))
turkish_stopwords = set(['özellikle','edilir','değildir','sahiptir','ardından','almaktadır','sadece','üzerinde''almıştır','sırasında','yoktur','bulunur','üzerine','yapmıştır','devam','boyunca','birlikte','üzerine''yapmıştır','genellikle','farklı','sonraları','olduktan','durumdadır','öne','olmaya','katılmıştır','olmuştur','ilk','bulunmaktadır','arasında','çeşitli','yer','büyük','aldı','önemli','başladı','aynı','vardır','a', 'acaba', 'altı', 'altmış', 'ama', 'ancak', 'arada', 'artık', 'asla', 'aslında', 'aslında', 'ayrıca', 'az', 'bana', 'bazen', 'bazı', 'bazıları', 'belki', 'ben', 'benden', 'beni', 'benim', 'beri', 'beş', 'bile', 'bilhassa', 'bin', 'bir', 'biraz', 'birçoğu', 'birçok', 'biri', 'birisi', 'birkaç', 'birşey', 'biz', 'bizden', 'bize', 'bizi', 'bizim', 'böyle', 'böylece', 'bu', 'buna', 'bunda', 'bundan', 'bunlar', 'bunları', 'bunların', 'bunu', 'bunun', 'burada', 'bütün', 'çoğu', 'çoğunu', 'çok', 'çünkü', 'da', 'daha', 'dahi', 'dan', 'de', 'defa', 'değil', 'diğer', 'diğeri', 'diğerleri', 'diye', 'doksan', 'dokuz', 'dolayı', 'dolayısıyla', 'dört', 'e', 'edecek', 'eden', 'ederek', 'edilecek', 'ediliyor', 'edilmesi', 'ediyor', 'eğer', 'elbette', 'elli', 'en', 'etmesi', 'etti', 'ettiği', 'ettiğini', 'fakat', 'falan', 'filan', 'gene', 'gereği', 'gerek', 'gibi', 'göre', 'hala', 'halde', 'halen', 'hangi', 'hangisi', 'hani', 'hatta', 'hem', 'henüz', 'hep', 'hepsi', 'her', 'herhangi', 'herkes', 'herkese', 'herkesi', 'herkesin', 'hiç', 'hiçbir', 'hiçbiri', 'i', 'ı', 'için', 'içinde', 'iki', 'ile', 'ilgili', 'ise', 'işte', 'itibaren', 'itibariyle', 'kaç', 'kadar', 'karşın', 'kendi', 'kendilerine', 'kendine', 'kendini', 'kendisi', 'kendisine', 'kendisini', 'kez', 'ki', 'kim', 'kime', 'kimi', 'kimin', 'kimisi', 'kimse', 'kırk', 'madem', 'mi', 'mı', 'milyar', 'milyon', 'mu', 'mü', 'nasıl', 'ne', 'neden', 'nedenle', 'nerde', 'nerede', 'nereye', 'neyse', 'niçin', 'nin', 'nın', 'niye', 'nun', 'nün', 'o', 'öbür', 'olan', 'olarak', 'oldu', 'olduğu', 'olduğunu', 'olduklarını', 'olmadı', 'olmadığı', 'olmak', 'olması', 'olmayan', 'olmaz', 'olsa', 'olsun', 'olup', 'olur', 'olur', 'olursa', 'oluyor', 'on', 'ön', 'ona', 'önce', 'ondan', 'onlar', 'onlara', 'onlardan', 'onları', 'onların', 'onu', 'onun', 'orada', 'öte', 'ötürü', 'otuz', 'öyle', 'oysa', 'pek', 'rağmen', 'sana', 'sanki', 'sanki', 'şayet', 'şekilde', 'sekiz', 'seksen', 'sen', 'senden', 'seni', 'senin', 'şey', 'şeyden', 'şeye', 'şeyi', 'şeyler', 'şimdi', 'siz', 'siz', 'sizden', 'sizden', 'size', 'sizi', 'sizi', 'sizin', 'sizin', 'sonra', 'şöyle', 'şu', 'şuna', 'şunları', 'şunu', 'ta', 'tabii', 'tam', 'tamam', 'tamamen', 'tarafından', 'trilyon', 'tüm', 'tümü', 'u', 'ü', 'üç', 'un', 'ün', 'üzere', 'var', 'vardı', 've', 'veya', 'ya', 'yani', 'yapacak', 'yapılan', 'yapılması', 'yapıyor', 'yapmak', 'yaptı', 'yaptığı', 'yaptığını', 'yaptıkları', 'ye', 'yedi', 'yerine', 'yetmiş', 'yi', 'yı', 'yine', 'yirmi', 'yoksa', 'yu', 'yüz', 'zaten', 'zira', 'zxtest'])
kelimeler = [word for word in tum_tweetler.split() if word not in stop_words]
kelimeler = [word for word in kelimeler if word not in turkish_stopwords]

# Kelime frekanslarını bulma
kelime_frekanslari = Counter(kelimeler)

# En çok kullanılan kelimeleri bulma
frekanslar = kelime_frekanslari.most_common(1000)

# Sonuçları yazdırma
for i, (kelime, frekans) in enumerate(frekanslar, 1):
    print(f"{kelime}: {frekans} defa")