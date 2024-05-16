import json
import networkx as nx
import matplotlib.pyplot as plt

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

json_dosya_adı = '350_data.json'  #Burada içinde daha az kullanıcı olan bir veriseti kullandık
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
        
# Boş bir yönlendirilmiş graf oluştur
graf = nx.DiGraph()

# Followers-following ilişkilerini grafa ekle
for kullanici in hash_tablosu:
    for follower_username in kullanici.followers:
        follower = next((k for k in hash_tablosu if k.username == follower_username), None)
        if follower:
            graf.add_node(kullanici.username, label=kullanici.username)
            graf.add_edge(follower.username, kullanici.username)

# Grafı çizdikten sonra kenarı olmayan düğümleri kaldır
#isolated_nodes = [node for node, degree in graf.degree() if degree == 0]
#graf.remove_nodes_from(isolated_nodes)

# Grafiği dosyaya yaz
nx.write_gexf(graf, 'graf1.gexf')

# Grafi çiz
pos = nx.spring_layout(graf)  # Grafın düzenini belirle
nx.draw(graf, pos, with_labels=True, node_size=700, node_color="turquoise", font_size=8, font_color="black", font_weight="bold", arrowsize=10)

# Düğüm etiketlerini göster
labels = nx.get_edge_attributes(graf, 'label')
nx.draw_networkx_edge_labels(graf, pos, edge_labels=labels, font_color='red', font_size=8)

plt.title("Followers-Following İlişkileri Grafi")
plt.show()

#Çalışıp çalışmadığını kontrol etmek amaçlı
print(f"{len(kullanici_listesi)}")