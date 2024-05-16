import json
from collections import defaultdict
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


def ilgi_alanlarini_bul(tweets):
    ilgi_alanlari = {
        'Spor ve Aktiviteler': ['futbol', 'lig', 'gol', 'basketbol', 'şampiyon'],
        'Eğitim ve Akademik': ['üniversite', 'öğrenci', 'doktora'],
        'Müzik ve Sanat': ['şarkı', 'albüm', 'konser', 'klip', 'enstrüman'],
        'Tarih ve Kültür': ['antik', 'savaş', 'medeniyet', 'imparatorluk', 'hanedan'],
        'Coğrafya ve Yerler': ['kıta', 'nehir', 'göl', 'dağ', 'deniz'],
        'Film ve Televizyon': ['aktör', 'yönetmen', 'senaryo', 'prodüksiyon', 'filmografi'],
        'Politika ve Toplum': ['milletvekili', 'hükümet', 'demokrasi', 'lider', 'siyaset'],
        'Bilim ve Teknoloji': ['bilim', 'teknoloji', 'mühendislik', 'elektronik', 'bilgisayar', 'inovasyon', 'uzay'],
        'Din ve İnanış': ['cami', 'kilise', 'müslüman', 'hristiyan', 'ibadet'],
        'Ekonomi ve Ticaret': ['şirket', 'para', 'döviz', 'şirket', 'endüstri']
    }
    kullanici_ilgi_alanlari = []
    for tweet in tweets:
        for ilgi_alani, kelimeler in ilgi_alanlari.items():
            if any(kelime.lower() in tweet.lower() for kelime in kelimeler):
                kullanici_ilgi_alanlari.append(ilgi_alani)

    return list(set(kullanici_ilgi_alanlari))

def ortak_ilgi_alanlarini_bul(username1, username2, hash_tablosu):
    kullanici1 = next((k for k in hash_tablosu if k.username == username1), None)
    kullanici2 = next((k for k in hash_tablosu if k.username == username2), None)

    if kullanici1 is not None and kullanici2 is not None:
        return set(kullanici1.ilgi_alanlari) & set(kullanici2.ilgi_alanlari)
    else:
        return set()






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

# Kullanıcı nesnelerinin ilgi alanlarını bulma
for kullanici in hash_tablosu:
    kullanici.ilgi_alanlari = ilgi_alanlarini_bul(kullanici.tweets)

# Bölgeler ve diller için en çok bulunan 3 ilgi alanı
bolge_ilgi_alanlari = defaultdict(list)
dil_ilgi_alanlari = defaultdict(list)

# Kullanıcı nesnelerini bölge ve dile göre ilgi alanlarına ekleyin
for kullanici in kullanici_listesi:
    for bolge in kullanici.region:
        bolge_ilgi_alanlari[bolge] += kullanici.ilgi_alanlari
    for dil in kullanici.language:
        dil_ilgi_alanlari[dil] += kullanici.ilgi_alanlari

# Her bir bölge için en çok bulunan 3 ilgi alanını belirleyin
for bolge, ilgi_alanlari in bolge_ilgi_alanlari.items():
    en_cok_bulunan_ilgi_alanlari = Counter(ilgi_alanlari).most_common(3)
    print(f"{bolge} Bölgesi - En Trend 3 İlgi Alanı:")
    for ilgi_alani, sayi in en_cok_bulunan_ilgi_alanlari:
        print(f"  {ilgi_alani}: {sayi} kişi")
    print()

# Her bir dil için en çok bulunan 3 ilgi alanını belirleyin
for dil, ilgi_alanlari in dil_ilgi_alanlari.items():
    en_cok_bulunan_ilgi_alanlari = Counter(ilgi_alanlari).most_common(3)
    print(f"{dil} Dili - En Trend 3 İlgi Alanı:")
    for ilgi_alani, sayi in en_cok_bulunan_ilgi_alanlari:
        print(f"  {ilgi_alani}: {sayi} kişi")
    print()