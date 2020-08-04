# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 11:02:01 2020

sentinentel uydu veri indirme
"""


from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import rasterio
import numpy as np
import pandas as pd
import os

#GİRİŞ
api = SentinelAPI('flavves', 'BATUhan123.', 'https://scihub.copernicus.eu/dhus')

#geojson dosyası ile hangi alanı incelemek istiyorsak o alana gidiyoruz ve seçiyoruz kaydete basarak geojson olarak almak istediğimizi söylüyoruz
footprint = geojson_to_wkt(read_geojson('map6.geojson'))
products = api.query(footprint,
                     date=('20191219', date(2019, 12, 29)),
                     platformname='Sentinel-2')

# pandas dataframe yap
products_df = api.to_dataframe(products)

# filtreleme
products_df_sorted = products_df.sort_values(['cloudcoverpercentage', 'ingestiondate'], ascending=[True, True])
products_df_sorted = products_df_sorted.head(5)

# arşiv indirmesini burada yapıyoruz
api.download_all(products_df_sorted.index)




#index verisinden kullanıcı kodu çekme

veri_cekme=products_df_sorted.index
veri_cekme1=veri_cekme[0]
veri_cekme2=veri_cekme[1]


#title çekme işlemi yaptık
"""
Bu işlem arşivden çıkarmak için gerekli arşivin adı indirdiğimiz verinin title adı oluyor

"""
arsiv_adi=api.get_product_odata(veri_cekme1)
arsiv_adi=arsiv_adi["title"]
arsiv_adi=str(arsiv_adi)

#arşivden çıkarmak için arşiv kütüphanesini ekledik


from archive import Archive
a = Archive(arsiv_adi+'.zip')
a.extract()
img_data_klasor_ismi=os.listdir((arsiv_adi+".SAFE"+'/GRANULE'))
img_data_klasor_ismi=img_data_klasor_ismi[0]
img_data_klasor_ismi=str(img_data_klasor_ismi)
dosya_yer_=(arsiv_adi+".SAFE"+'/GRANULE/'+img_data_klasor_ismi+'/IMG_DATA')
resim_isim=os.listdir(dosya_yer_)

if resim_isim == "R10m" or "R20m" or "R60m":
    dosya_yer_=(arsiv_adi+".SAFE"+'/GRANULE/'+img_data_klasor_ismi+'/IMG_DATA/R60m')
    resim_isim=os.listdir(dosya_yer_)
    resim_isim[2]
    resim_isim[3]
        
    jp2ler = [resim_isim[2],resim_isim[3]]
    bands = []
    
    #burası bizim jp2 dosyalarımızı okuyacak
    
    for jp2 in jp2ler:
        with rasterio.open(dosya_yer_+"/"+jp2) as f:
            bands.append(f.read(1))
    
    #resimlerimizi ayrıştırdık özel bantlara
    band_red=bands[0]
    band_nir=bands[1]
else:
        
    resim_isim[2]
    resim_isim[3]
    
    
    jp2ler = [resim_isim[2],resim_isim[3]]
    bands = []
    
    #burası bizim jp2 dosyalarımızı okuyacak
    
    for jp2 in jp2ler:
        with rasterio.open(dosya_yer_+"/"+jp2) as f:
            bands.append(f.read(1))
    
    #resimlerimizi ayrıştırdık özel bantlara
    band_red=bands[0]
    band_nir=bands[1]
        
        
# Klasik NDVI denklemi ile hesaplama
np.seterr(divide='ignore', invalid='ignore')

# Calculate NDVI. This is the equation at the top of this guide expressed in code
ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red)
#su için yapıyorum bu analizi
##
###
ndvi=(band_red.astype(float) - band_nir.astype(float)) / (band_red + band_nir)
###
###
np.nanmin(ndvi), np.nanmax(ndvi)
    



# görüntümüze bakalım renklerine ayrılmış bir görüntümüz var
# çizim yapacağız bunun için gerekli kütüphaneler ekleniyor

import matplotlib.pyplot as plt
import matplotlib.colors as colors

# NDVI bilindiği üzere 1 ve -1 arasındaki değerlerde sınıflandırılır.
# Biz de bu değerleri renklerle göstermek istiyoruz.
# Bunun için alınan sayısal değerleri farklı renk spektrumlarına atayarak elimizde NDVI için renklendirilmiş bir görüntümüz olacaktır
# 
# Bir orta nokta belirledik ve bu sola ve sağa olacak şekilde renklendiriyoru renk spekturumunu da aşağıda paylaşacağım

class RenkNormalizasyonu(colors.Normalize):
   
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):

        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))

min=np.nanmin(ndvi)
max=np.nanmax(ndvi)
mid=0.1

fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111)

cmap = plt.cm.RdYlGn 

cax = ax.imshow(ndvi, cmap=cmap, clim=(min, max), norm=RenkNormalizasyonu(midpoint=mid,vmin=min, vmax=max))

ax.axis('off')
ax.set_title('NDVI görüntüsü', fontsize=18, fontweight='bold')

cbar = fig.colorbar(cax, orientation='horizontal', shrink=0.65)
fig_kaydet="ndvi_sonuc/"+resim_isim[2]+".tif"
fig.savefig(fig_kaydet, dpi=200, bbox_inches='tight', pad_inches=0.7)

plt.show()




fig2 = plt.figure(figsize=(10,10))
ax = fig2.add_subplot(111)

plt.title("NDVI Histogram", fontsize=18, fontweight='bold')
plt.xlabel("NDVI values", fontsize=14)
plt.ylabel("# pixels", fontsize=14)


x = ndvi[~np.isnan(ndvi)]
numBins = 20
ax.hist(x,numBins,color='black',alpha=1)

histog_kaydet="histogram_sonuc/"+resim_isim[2]+".png"
fig2.savefig(histog_kaydet, dpi=200, bbox_inches='tight', pad_inches=0.7)

plt.show()




"""

2. part burada

burada görüntü işleme ile ne durumda olduğunu bulacağız

"""
import cv2
#burası 1 kere yapılması gerekiyor
resim = cv2.imread(histog_kaydet,111)
cv2.imwrite("skysattif/donusumler//goruntu_isleme/resim_yenimis.jpg",resim)

resim_yeni="skysattif/donusumler//goruntu_isleme/resim_yenimis.jpg"
import cv2
import numpy as np

resim = cv2.imread(resim_yeni)


#bölge seçmeyi yapıyorum

#burası 1.seviye kurak alan oluyor
kesilmis_karek1= resim[0:157,0:161]
# burası 2. seviye kurak alan
kesilmis_karek2= resim[0:238,0:161]
# burası 3. seviye kurak alan
kesilmis_karek3= resim[0:422,0:161]

#burası 1.seviye az yeşil alan oluyor
kesilmis_kareaz1= resim[0:157,162:277]
# burası 2. seviye az yeşil alan
kesilmis_kareaz2= resim[0:238,162:277]
# burası 3. seviye az yeşil alan
kesilmis_kareaz3= resim[0:422,162:277]

#burası 1.seviye çok yeşil alan oluyor
kesilmis_karey1= resim[0:157,278:462]
# burası 2. seviye az yeşil alan
kesilmis_karey2= resim[0:238,278:462]
# burası 3. seviye az yeşil alan
kesilmis_karey3= resim[0:422,278:462]

#listemelemek için

listem_ort=[]

kesilmis_karek1_ort=np.mean(kesilmis_karek1)
listem_ort.append(kesilmis_karek1_ort)

kesilmis_karek2_ort=np.mean(kesilmis_karek2)
listem_ort.append(kesilmis_karek2_ort)

kesilmis_karek3_ort=np.mean(kesilmis_karek3)
listem_ort.append(kesilmis_karek3_ort)

kesilmis_kareaz1_ort=np.mean(kesilmis_kareaz1)
listem_ort.append(kesilmis_kareaz1_ort)

kesilmis_kareaz2_ort=np.mean(kesilmis_kareaz2) 
listem_ort.append(kesilmis_kareaz2_ort)

kesilmis_kareaz3_ort=np.mean(kesilmis_kareaz3) 
listem_ort.append(kesilmis_kareaz3_ort)

kesilmis_karey1_ort=np.mean(kesilmis_karey1)
listem_ort.append(kesilmis_karey1_ort)

kesilmis_karey2_ort=np.mean(kesilmis_karey2)
listem_ort.append(kesilmis_karey2_ort)

kesilmis_karey3_ort=np.mean(kesilmis_karey3)
listem_ort.append(kesilmis_karey3_ort)




# yoğunluk hesaplandı
listem_ort.sort()
en_kucuk=listem_ort[0]
if en_kucuk==kesilmis_karek1_ort:
    toprak_turu="kuraklık seviyesi 1"
elif en_kucuk==kesilmis_karek2_ort:
   toprak_turu="kuraklık seviyesi 2"
elif en_kucuk==kesilmis_karek3_ort:
    toprak_turu="kuraklık seviyesi 3"
elif en_kucuk==kesilmis_kareaz1_ort:
    toprak_turu="Az yeşil 1"
elif en_kucuk==kesilmis_kareaz2_ort:
    toprak_turu="Az yeşil 2"
elif en_kucuk==kesilmis_kareaz3_ort:
    toprak_turu="Az yeşil 3"
elif en_kucuk==kesilmis_karey1_ort:
    toprak_turu="Yeşil 1"
elif en_kucuk==kesilmis_karey2_ort:
    toprak_turu="Yeşil 2"
elif en_kucuk==kesilmis_karey3_ort:
    toprak_turu="Yeşil 3"
print("1 en yüksek değeri ifade eder yeşil 1 en fazla yeşillik, kuraklık 1 en kurak alan anlamına gelir")
print("yoğunluk olarak: %s"%toprak_turu)
    

#ortalama hesaplanıyor
#burda en yakın komşuyu buluyoruz
from heapq import nsmallest
ortalama_yogunluk=nsmallest(1, listem_ort, key=lambda x: abs(x-(np.sum(listem_ort)/9)))

if ortalama_yogunluk==kesilmis_karek1_ort:
    yogunluk_tipi="kuraklık seviyesi 1"
elif ortalama_yogunluk==kesilmis_karek2_ort:
   yogunluk_tipi="kuraklık seviyesi 2"
elif ortalama_yogunluk==kesilmis_karek3_ort:
    yogunluk_tipi="kuraklık seviyesi 3"
elif ortalama_yogunluk==kesilmis_kareaz1_ort:
    yogunluk_tipi="Az yeşil 1"
elif ortalama_yogunluk==kesilmis_kareaz2_ort:
    yogunluk_tipi="Az yeşil 2"
elif ortalama_yogunluk==kesilmis_kareaz3_ort:
    yogunluk_tipi="Az yeşil 3"
elif ortalama_yogunluk==kesilmis_karey1_ort:
    yogunluk_tipi="Yeşil 1"
elif ortalama_yogunluk==kesilmis_karey2_ort:
    yogunluk_tipi="Yeşil 2"
elif ortalama_yogunluk==kesilmis_karey3_ort:
    yogunluk_tipi="Yeşil 3"
print("1 en yüksek değeri ifade eder yeşil 1 en fazla yeşillik, kuraklık 1 en kurak alan anlamına gelir")
print("ortalama olarak: %s"%yogunluk_tipi)
print("yoğunluk olarak: %s"%toprak_turu)




"""
Burası bölünen alanları görmek için var yok sayılabilir

"""


"""
#gösterme kesilmiş kare kurak alan 
cv2.imshow("kesilmis_karek1",kesilmis_karek1)
cv2.imshow("kesilmis_karek2",kesilmis_karek2)
cv2.imshow("kesilmis_karek3",kesilmis_karek3)

#gösterme kesilmiş az yeşil alan 
cv2.imshow("kesilmis_kareaz1",kesilmis_kareaz1)
cv2.imshow("kesilmis_kareaz2",kesilmis_kareaz2)
cv2.imshow("kesilmis_kareaz3",kesilmis_kareaz3)

#gösterme kesilmiş çok yeşil alan
cv2.imshow("kesilmis_karey1",kesilmis_karey1)
cv2.imshow("kesilmis_karey2",kesilmis_karey2)
cv2.imshow("kesilmis_karey3",kesilmis_karey3)

cv2.waitKey(0)
cv2. destroyAllWindows()
type(resim)
"""


# pasta grafiğine dönüştürüyoruz 

import matplotlib.pyplot as plt

%matplotlib inline


labels="kuraklık seviyesi 1","kuraklık seviyesi 2","kuraklık seviyesi 3","Az yeşil 1","Az yeşil 2","Az yeşil 3","Yeşil 1","Yeşil 2","Yeşil 3"
sizes=[kesilmis_karek1_ort,kesilmis_karek2_ort,kesilmis_karek3_ort,kesilmis_kareaz1_ort,kesilmis_kareaz2_ort,kesilmis_kareaz3_ort,kesilmis_karey1_ort,kesilmis_karey2_ort,kesilmis_karey3_ort]
explode = (0,0,0,0.2,0.2,0.2,0,0.1,0)

figl, axl = plt.subplots()

axl.pie(sizes,explode=explode,labels=labels,autopct="%1.1f%%", shadow=True, startangle=90)
axl.axis("equal")
figl.savefig("pasta_grafik.png")
plt.show()







