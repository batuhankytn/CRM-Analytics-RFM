/*
  RFM Analizi için SQL Sorgusu
  Amaç: Ham satış verisinden her müşterinin Recency, Frequency ve Monetary değerlerini hesaplamak.
  
  Filtreler:
  - İade işlemleri (Quantity < 0) çıkarıldı.
  - Müşteri ID'si olmayan kayıtlar çıkarıldı.
  - Birim fiyatı 0 olan hatalı kayıtlar çıkarıldı.
*/

WITH clean_data AS (
    SELECT * FROM retail_sales
    WHERE customer_id IS NOT NULL 
      AND quantity > 0 
      AND price > 0
)
SELECT 
    customer_id,
    
    -- RECENCY: Analiz tarihinden (2012-01-01) son alışveriş tarihini çıkar
    ('2012-01-01'::date - MAX(invoicedate)::date) as recency,
    
    -- FREQUENCY: Eşsiz fatura sayısı
    COUNT(DISTINCT invoice) as frequency,
    
    -- MONETARY: Toplam Harcama (Adet * Birim Fiyat)
    SUM(quantity * price) as monetary
FROM 
    clean_data
GROUP BY 
    customer_id
ORDER BY 
    monetary DESC;