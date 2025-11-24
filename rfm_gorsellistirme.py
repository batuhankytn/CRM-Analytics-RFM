import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. VERİYİ OKU
# Analiz sonucu kaydettiğimiz CSV dosyasını okuyoruz
df = pd.read_csv("Musteri_Segmentleri.csv")

# 2. GRAFİK AYARLARI
plt.figure(figsize=(16, 8)) # Geniş bir tuval açalım
sns.set_style("whitegrid") # Arka plan çizgili olsun

# 3. SEGMENT SAYILARINI ÇİZDİR (Bar Chart)
# Müşteri sayılarına göre sıralayalım
order = df['segment'].value_counts().index

ax = sns.countplot(data=df, x='segment', order=order, palette='viridis')

# 4. GÖRSELLİĞİ İYİLEŞTİR
plt.title("Müşteri Segmentlerinin Dağılımı", fontsize=20, fontweight='bold')
plt.xlabel("Segmentler", fontsize=12)
plt.ylabel("Müşteri Sayısı", fontsize=12)
plt.xticks(rotation=45) # Yazılar birbirine girmesin diye eğiyoruz

# Her çubuğun üzerine sayısını yazalım (Burası işin şov kısmı)
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + 0.4, p.get_height()), 
                ha='center', va='bottom', color='black', size=12)

# 5. KAYDET VE GÖSTER
plt.tight_layout()
plt.savefig("Segment_Grafigi.png", dpi=300) # Yüksek kalitede kaydet
print("✅ Grafik 'Segment_Grafigi.png' olarak kaydedildi!")
plt.show()