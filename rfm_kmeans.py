import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# 1. VERİYİ ÇEK (Aynı SQL Sorgusu)
# ---------------------------------------------------------
# Veritabanı bağlantı bilgileri (Güvenlik nedeniyle şifre gizlenmiştir)
DB_USER = 'postgres'
DB_PASS = 'BURAYA_SIFRENIZI_YAZIN' # <--- Kendi şifrenizi giriniz
conn_string = f"postgresql://{DB_USER}:{DB_PASS}@localhost:5432/eticaret_db"
engine = create_engine(conn_string)

sql_query = """
WITH clean_data AS (
    SELECT * FROM retail_sales
    WHERE customer_id IS NOT NULL AND quantity > 0 AND price > 0
)
SELECT 
    customer_id,
    ('2012-01-01'::date - MAX(invoicedate)::date) as recency,
    COUNT(DISTINCT invoice) as frequency,
    SUM(quantity * price) as monetary
FROM clean_data
GROUP BY customer_id
"""
rfm = pd.read_sql(sql_query, engine)

# 2. VERİYİ HAZIRLA (Log Transformation & Scaling)
# ---------------------------------------------------------
# Makine öğrenmesi algoritmaları uç değerleri (çok zenginleri) sevmez.
# O yüzden veriyi sıkıştırıyoruz (Log alma) ve standartlaştırıyoruz.

# Negatif veya sıfır değerler log almada hata verir, filtreleyelim
rfm_ml = rfm[(rfm['monetary'] > 0) & (rfm['frequency'] > 0)]

# Standartlaştırma (Herkesi eşit şartlara getirme - 0 ile 1 arasına sıkıştırma gibi düşün)
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_ml[['recency', 'frequency', 'monetary']])

# 3. K-MEANS ALGORİTMASINI ÇALIŞTIR
# ---------------------------------------------------------
# Müşterileri 4 ana kümeye ayırmasını istiyoruz
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans.fit(rfm_scaled)

# Etiketleri ana veriye yapıştır
rfm_ml['Cluster'] = kmeans.labels_

# 4. SONUÇLARI YORUMLA
# ---------------------------------------------------------
print("-" * 50)
print("MAKİNE ÖĞRENMESİ İLE AYRILAN KÜMELERİN ORTALAMALARI:")
print("-" * 50)
summary = rfm_ml.groupby('Cluster')[['recency', 'frequency', 'monetary']].mean()
print(summary)

# Kümeleri isimlendirme (Sonuçlara bakıp manuel karar veririz)
# Örn: Hangi kümenin harcaması (Monetary) en yüksekse o "VIP"dir.

# 5. GÖRSELLEŞTİRME (Scatter Plot)
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))
sns.scatterplot(data=rfm_ml, x='recency', y='monetary', hue='Cluster', palette='viridis', s=50)
plt.title('K-Means Kümeleme Sonuçları (Recency vs Monetary)')
plt.savefig("KMeans_Cluster_Grafigi.png")
print("\n✅ Grafik 'KMeans_Cluster_Grafigi.png' olarak kaydedildi.")