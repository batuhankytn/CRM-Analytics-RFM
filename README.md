CRM Analitiği ve Müşteri Yaşam Boyu Değeri Optimizasyonu

Yönetici Özeti (Executive Summary)

Bu proje, 1 milyonun üzerinde işlem verisine sahip bir e-ticaret platformunun karlılığını artırmak ve müşteri kaybını (Churn) önlemek amacıyla geliştirilmiş uçtan uca bir veri analitiği çözümüdür. Sıradan bir analizden farklı olarak; Veri Mühendisliği (SQL Pipeline), İstatistiksel Analiz (RFM) ve Makine Öğrenmesi (K-Means Clustering) disiplinleri birleştirilerek hibrit bir segmentasyon modeli kurulmuştur.

Çözülen İş Problemleri
Bir işletme için en pahalı aksiyon "yeni müşteri bulmaktır". Bu proje şu sorulara matematiksel yanıtlar üretmiştir:

Müşteri Kaybı: "Hangi müşterilerimizi kaybetmek üzereyiz ve onları nasıl tutabiliriz?"

Pazarlama Bütçesi: "Reklam bütçemizi kime harcamalıyız?" (Herkese aynı reklamı göstermek bütçe israfıdır).

VIP Yönetimi: "Pareto İlkesi'ne göre ciromuzun %80'ini getiren %20'lik kitle kim?"

Teknik Mimari ve Zorluklar
Bu proje, basit bir veri setinin analizi değil, ölçeklenebilir bir veri hattı simülasyonudur.

Aşama

Kullanılan Teknoloji

Karşılaşılan Zorluk & Çözüm

1. Veri Depolama
PostgreSQL tercih edildi. Excel'in açamadığı 1.000.000+ satırlık ham veri, ilişkisel veritabanında modellendi.

2. Veri İşleme
SQL (Window Functions)
Python RAM'ini şişirmemek için toplama (Aggregation) işlemleri veritabanı seviyesinde optimize edildi.

3. Modelleme
Python & Scikit-Learn
Geleneksel RFM analizi, K-Means (Unsupervised Learning) algoritması ile desteklenerek insan yanlılığı (bias) elimine edildi.

Kritik İş Çıkarımları (Business Insights)
Analiz sonucunda müşteriler davranışsal özelliklerine göre segmente edilmiş ve aşağıdaki kritik gruplar tespit edilmiştir:

Acil Aksiyon Gerektiren Tespitler:
"Hibernating" (Uykuda) Tehlikesi: Müşteri tabanının en büyük kısmı (%30+) eskiden alışveriş yapmış ama son 1.5 yıldır uğramamış. Finansal Risk: Bu kitlenin tamamen kaybedilmesi, potansiyel ciroda tahmini %25 kayıp demektir."Champions" kısmı yani gelirin çoğunluğunu sağlayan azınlık sadece 850 kişi olmasına rağmen, toplam cironun çok büyük bir kısmını domine ediyorlar. Bu kitleye yapılacak "Özel Müşteri Temsilcisi" ataması, sadakati %40 artırabilir.

Projenin Kurulumu
Bu repo, yerel makinenizde bir SQL veritabanı simülasyonu kurar.
Gereksinimler:
pip install pandas sqlalchemy psycopg2-binary matplotlib seaborn scikit-learn
Veri Hattını (Pipeline) Çalıştırma:
analiz_sorgusu.sql: Veritabanı mimarisini ve sorgu mantığını incelemek için.
rfm_analizi.py: Kural tabanlı segmentasyonu başlatmak için.
rfm_kmeans.py: Yapay zeka modelini eğitmek ve çalıştırmak için.


Bu çalışma, veri odaklı karar alma (Data-Driven Decision Making) süreçlerini optimize etmek için @batuhankytn tarafından geliştirilmiştir.

