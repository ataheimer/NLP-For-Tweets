import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from collections import deque

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
        'Müzik ve Sanat': ['şarkı', 'albüm', 'konser', 'enstrüman'],
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

def ortak_followers_following_bul(username1, username2, kullanici_listesi):
    kullanici1 = next((k for k in kullanici_listesi if k.username == username1), None)
    kullanici2 = next((k for k in kullanici_listesi if k.username == username2), None)

    if kullanici1 is not None and kullanici2 is not None:
        ortak_followers = set(kullanici1.followers) & set(kullanici2.followers)
        ortak_following = set(kullanici1.following) & set(kullanici2.following)
        return ortak_followers, ortak_following
    else:
        return set(), set()

def dfs(G, start, visited=None):
    if visited is None:
        visited = set()  
    print(start) 
    visited.add(start) 
    for neighbor in G[start]: 
        if neighbor not in visited:
            dfs(G, neighbor, visited) 

def bfs(G, start):
    visited = set()
    queue = deque([start])

    while queue:
        current_node = queue.popleft()

        if current_node not in visited:
            print(current_node) 

            visited.add(current_node) 

            for neighbor in G[current_node]:
                if neighbor not in visited:
                    queue.append(neighbor)

def cizim_yap(username1, username2, ortak_ilgi_alanlari, ortak_followers, ortak_following):
    G = nx.Graph()
    kullanici1 = next((k for k in hash_tablosu if k.username == username1), None)
    kullanici2 = next((k for k in hash_tablosu if k.username == username2), None)
    # Tek bir node ekleyerek iki kullanıcıyı birleştir
    G.add_node("Ortak Kullanıcı", label=f"{kullanici1.username} ve {kullanici2.username}")

    for ilgi_alani in ortak_ilgi_alanlari:
        G.add_edge("Ortak Kullanıcı", ilgi_alani, label=ilgi_alani)

    for follower in ortak_followers:
        G.add_edge("Ortak Kullanıcı", follower, label=follower)

    for following in ortak_following:
        G.add_edge("Ortak Kullanıcı", following, label=following)
        
    start = "Ortak Kullanıcı"
    print("\n")
    dfs(G, start)
    print("\n")
    bfs(G, start)
    
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'label')

    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw_networkx_labels(G, pos, nx.get_node_attributes(G, 'label'))

    plt.show()

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
    # Kullanıcının ilgi alanlarını yazdırma
    print(f"{kullanici.username} - İlgi Alanları: {kullanici.ilgi_alanlari}")

# İlgi alanlarına göre hash tablolarını oluştur
ilgi_alani_hash_tablolari = defaultdict(list)

# Kullanıcı nesnelerini ilgi alanlarına göre hash tablolarına ekleme
for kullanici in kullanici_listesi:
    for ilgi_alani in kullanici.ilgi_alanlari:
        ilgi_alani_hash_tablolari[ilgi_alani].append(kullanici)

sporveaktiviteler_ilgi_alani_kullanicilari = ilgi_alani_hash_tablolari['Spor ve Aktiviteler']
#for kullanici in sporveaktiviteler_ilgi_alani_kullanicilari:
    #print(f"{kullanici.name} - {kullanici.username}")
print(f'"Spor ve Aktiviteler" ilgi alanına sahip kullanıcı sayısı: {len(sporveaktiviteler_ilgi_alani_kullanicilari)}')

egitimveakademik_ilgi_alani_kullanicilari = ilgi_alani_hash_tablolari['Eğitim ve Akademik']
#for kullanici in egitimveakademik_ilgi_alani_kullanicilari:
    #print(f"{kullanici.name} - {kullanici.username}")
print(f'"Eğitim ve Akademik" ilgi alanına sahip kullanıcı sayısı: {len(egitimveakademik_ilgi_alani_kullanicilari)}')

muzikvesanat_ilgi_alani_kullanicilari = ilgi_alani_hash_tablolari['Müzik ve Sanat']
#for kullanici in muzikvesanat_ilgi_alani_kullanicilari:
    #print(f"{kullanici.name} - {kullanici.username}")
print(f'"Müzik ve Sanat" ilgi alanına sahip kullanıcı sayısı: {len(muzikvesanat_ilgi_alani_kullanicilari)}')

tarihvekultur_ilgi_alani_kullanicilari = ilgi_alani_hash_tablolari['Tarih ve Kültür']
#for kullanici in tarihvekultur_ilgi_alani_kullanicilari:
    #print(f"{kullanici.name} - {kullanici.username}")
print(f'"Tarih ve Kültür" ilgi alanına sahip kullanıcı sayısı: {len(tarihvekultur_ilgi_alani_kullanicilari)}')

cografyaveyerler_ilgi_alani_kullanicilari = ilgi_alani_hash_tablolari['Coğrafya ve Yerler']
#for kullanici in cografyaveyerler_ilgi_alani_kullanicilari:
    #print(f"{kullanici.name} - {kullanici.username}")
print(f'"Coğrafya ve Yerler" ilgi alanına sahip kullanıcı sayısı: {len(cografyaveyerler_ilgi_alani_kullanicilari)}')

filmvetelevizyon_ilgi_alani_kullanicilari = ilgi_alani_hash_tablolari['Film ve Televizyon']
#for kullanici in filmvetelevizyon_ilgi_alani_kullanicilari:
    #print(f"{kullanici.name} - {kullanici.username}")
print(f'"Film ve Televizyon" ilgi alanına sahip kullanıcı sayısı: {len(filmvetelevizyon_ilgi_alani_kullanicilari)}')

politikavetoplum_ilgi_alani_kullanicilari = ilgi_alani_hash_tablolari['Politika ve Toplum']
#for kullanici in politikavetoplum_ilgi_alani_kullanicilari:
    #print(f"{kullanici.name} - {kullanici.username}")
print(f'"Politika ve Toplum" ilgi alanına sahip kullanıcı sayısı: {len(politikavetoplum_ilgi_alani_kullanicilari)}')

bilimveteknoloji_ilgi_alani_kullanicilari = ilgi_alani_hash_tablolari['Bilim ve Teknoloji']
#for kullanici in bilimveteknoloji_ilgi_alani_kullanicilari:
    #print(f"{kullanici.name} - {kullanici.username}")
print(f'"Bilim ve Teknoloji" ilgi alanına sahip kullanıcı sayısı: {len(bilimveteknoloji_ilgi_alani_kullanicilari)}')

dinveinanis_ilgi_alani_kullanicilari = ilgi_alani_hash_tablolari['Din ve İnanış']
#for kullanici in dinveinanis_ilgi_alani_kullanicilari:
    #print(f"{kullanici.name} - {kullanici.username}")
print(f'"Din ve İnanış" ilgi alanına sahip kullanıcı sayısı: {len(dinveinanis_ilgi_alani_kullanicilari)}')

ekonomiveticaret_ilgi_alani_kullanicilari = ilgi_alani_hash_tablolari['Ekonomi ve Ticaret']
#for kullanici in ekonomiveticaret_ilgi_alani_kullanicilari:
    #print(f"{kullanici.name} - {kullanici.username}")
print(f'"Ekonomi ve Ticaret" ilgi alanına sahip kullanıcı sayısı: {len(ekonomiveticaret_ilgi_alani_kullanicilari)}')

# Kullanıcının girdiği iki username'i al
username1 = input("İlk kullanıcı username'i: ")
username2 = input("İkinci kullanıcı username'i: ")

ortak_ilgi_alanlari = ortak_ilgi_alanlarini_bul(username1, username2, hash_tablosu)

if ortak_ilgi_alanlari:
    print(f"{username1} ve {username2} arasında ortak ilgi alanları: {ortak_ilgi_alanlari}")
else:
    print(f"{username1} ve {username2} arasında ortak ilgi alanı bulunmuyor.")

ortak_followers, ortak_following = ortak_followers_following_bul(username1, username2, kullanici_listesi)

if ortak_followers:
    print(f"{username1} ve {username2} arasında ortak takipçi: {ortak_followers}")
else:
    print(f"{username1} ve {username2} arasında ortak takipçi bulunmuyor.")

if ortak_following:
    print(f"{username1} ve {username2} arasında ortak takip edilen: {ortak_following}")
else:
    print(f"{username1} ve {username2} arasında ortak takip edilen bulunmuyor.")

cizim_yap(username1, username2, ortak_ilgi_alanlari, ortak_followers, ortak_following)