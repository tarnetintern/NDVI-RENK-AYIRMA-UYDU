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
api = SentinelAPI('flavves', 'sifre.', 'https://scihub.copernicus.eu/dhus')

footprint = geojson_to_wkt(read_geojson('map.geojson'))
products = api.query(footprint,
                     date=('20151219', date(2015, 12, 29)),
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
arsiv_adi=api.get_product_odata(veri_cekme2)
arsiv_adi=arsiv_adi["title"]
arsiv_adi=str(arsiv_adi)

#arşivden çıkarmak için arşiv kütüphanesini ekledik
from pyunpack import Archive

Archive(arsiv_adi+'.zip').extractall('indirilen_dosya')

dosya_yer_=('indirilen_dosya/'+arsiv_adi+".SAFE"+'/GRANULE/L1C_T35TPE_A002678_20151227T085356/IMG_DATA')
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
    







