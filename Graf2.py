import json
import networkx as nx
import matplotlib.pyplot as plt

# json dosyasını veriye atayan fonksiyon
def json_oku(json_dosya_adı):
    with open(json_dosya_adı, 'r', encoding='utf-8') as dosya:
        veri = json.load(dosya)
    return veri


# kullanıcı sınıfı
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


# kullanıcı sınıfından nesne türeten fonksiyon
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


# fonksiyonları gerçekleştiren kısım

json_dosya_adı = '50k_data.json'
veri = json_oku(json_dosya_adı)
kullanici_listesi = kullanici_nesnesi_olustur(veri)
hedef_kullanici_adi = input("İlişki grafi oluşturmak istediğiniz kullanıcının adını girin: ")

# verileri kendi oluşturduğumuz veri yapısına (hash tablosuna) dönüştüren kısım
hash_tablosu = {}
for kullanici in kullanici_listesi:
    hash_tablosu[kullanici.username] = kullanici

# Boş bir yönlendirilmiş graf oluştur
graf = nx.DiGraph()

# Hedef kullanıcının takipçi ve takip ettikleri ile ilişkiyi grafa ekle
if hedef_kullanici_adi in hash_tablosu:
    hedef_kullanici = hash_tablosu[hedef_kullanici_adi]

    for follower_username in hedef_kullanici.followers:
        follower = hash_tablosu.get(follower_username)
        if follower:
            graf.add_node(hedef_kullanici.username, label=hedef_kullanici.username)
            graf.add_edge(follower.username, hedef_kullanici.username)

    for following_username in hedef_kullanici.following:
        following = hash_tablosu.get(following_username)
        if following:
            graf.add_node(hedef_kullanici.username, label=hedef_kullanici.username)
            graf.add_edge(hedef_kullanici.username, following.username)

    # Grafiği çiz
    pos = nx.spring_layout(graf)  # Grafın düzenini belirle
    nx.draw(graf, pos, with_labels=True, node_size=700, node_color="turquoise", font_size=8, font_color="black",
            font_weight="bold", arrowsize=10)

    # Düğüm etiketlerini göster
    labels = nx.get_edge_attributes(graf, 'label')
    nx.draw_networkx_edge_labels(graf, pos, edge_labels=labels, font_color='red', font_size=8)

    plt.title(f"{hedef_kullanici.username}'in Followers-Following İlişkileri Grafi")
    plt.show()

    # Çalışıp çalışmadığını kontrol etmek amaçlı
    print(f"{hedef_kullanici.username}'in ilişki grafi oluşturuldu.")
else:
    print(f"{hedef_kullanici_adi} adlı kullanıcı bulunamadı.")
