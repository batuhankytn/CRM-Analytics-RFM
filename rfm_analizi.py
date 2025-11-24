import pandas as pd
from sqlalchemy import create_engine
import sys

# 1. BAĞLANTI AYARLARI
# ---------------------------------------------------------
# NOT: GitHub'a yüklemeden önce buradaki şifreyi silip 'xxxxx' yaptık.
# Bu kodu çalıştıracak kişi kendi yerel veritabanı şifresini girmelidir.
DB_USER = 'postgres'
DB_PASS = 'BURAYA_SIFRENIZI_YAZIN'  # <--- Güvenlik için şifre gizlendi
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'eticaret_db'

conn_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(conn_string)

# 2. SQL SORGUSU (Veriyi Özetleme)
# ---------------------------------------------------------
print("SQL ile 1+ Milyon satır analiz ediliyor...")

sql_query = """
WITH clean_data AS (
    SELECT * FROM retail_sales
    WHERE customer_id IS NOT NULL 
      AND quantity > 0 
      AND price > 0
)
SELECT 
    customer_id,
    ('2012-01-01'::date - MAX(invoicedate)::date) as recency,
    COUNT(DISTINCT invoice) as frequency,
    SUM(quantity * price) as monetary
FROM 
    clean_data
GROUP BY 
    customer_id
"""

try:
    rfm = pd.read_sql(sql_query, engine)
    print(f"✅ Veriler çekildi! {len(rfm)} eşsiz müşteri analiz ediliyor.")
except Exception as e:
    print("❌ Hata:", e)
    sys.exit()

# 3. PUANLAMA (Scoring) - Python'un Gücü
# ---------------------------------------------------------
# Veriyi 5 parçaya bölüyoruz (qcut fonksiyonu)

# RECENCY: Düşük olması İYİDİR (Az gün geçmiş). O yüzden etiketler [5, 4, 3, 2, 1]
# (Yani en küçük değerler 5 puan alır)
rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])

# FREQUENCY: Yüksek olması İYİDİR. Etiketler [1, 2, 3, 4, 5]
# Not: Aynı sayıda çok fazla işlem varsa qcut hata verebilir, o yüzden .rank(method="first") kullanıyoruz.
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

# MONETARY: Yüksek olması İYİDİR.
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

# Puanları yanyana yazıp (Örn: "53") tek bir skor oluşturuyoruz
rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))

# 4. SEGMENTASYON (Müşteriyi Etiketleme)
# ---------------------------------------------------------
# Bu harita standart RFM analizinde kullanılır
seg_map = {
    r'[1-2][1-2]': 'Hibernating (Uykuda)',
    r'[1-2][3-4]': 'At_Risk (Riskli)',
    r'[1-2]5': 'Cant_Loose (Kaybedilemez)',
    r'3[1-2]': 'About_to_Sleep (Uykuya Dalmak Üzere)',
    r'33': 'Need_Attention (Dikkat Gerektirir)',
    r'[3-4][4-5]': 'Loyal_Customers (Sadık Müşteriler)',
    r'41': 'Promising (Umut Vaat Eden)',
    r'51': 'New_Customers (Yeni Müşteriler)',
    r'[4-5][2-3]': 'Potential_Loyalists (Potansiyel Sadık)',
    r'5[4-5]': 'Champions (Şampiyonlar)'
}

# Regex ile haritayı uyguluyoruz
rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)

# 5. SONUÇLARI GÖSTER VE KAYDET
# ---------------------------------------------------------
print("-" * 50)
print("SEGMENTLERE GÖRE MÜŞTERİ SAYILARI:")
print(rfm["segment"].value_counts()) # Hangi grupta kaç kişi var?
print("-" * 50)

# Ortalamalara bakalım: Şampiyonlar ortalama kaç TL harcamış?
print("\nSEGMENT ORTALAMALARI:")
print(rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"]))

# Dosyayı kaydet (İşte bu dosya Pazarlama departmanına gidecek olandır)
rfm.to_csv("Musteri_Segmentleri.csv")
print("\n✅ Dosya 'Musteri_Segmentleri.csv' olarak kaydedildi!")