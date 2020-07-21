# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 13:59:23 2020

@author: yazılım
"""


from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date


#GİRİŞ
api = SentinelAPI('flavves', 'BATUhan123.', 'https://scihub.copernicus.eu/dhus')

#dosyamızı indiriyoruz
api.download("cc40b640-151e-44ad-a114-41a592e75bf2")

#indirilen dosyayı rardan çıkarıyoruz
#dosyanın ismini buradan çekeceğiz
arsiv_adi=api.get_product_odata("bed2d688-746d-4c87-b905-92d581502067")
arsiv_adi=arsiv_adi["title"]
from pyunpack import Archive
Archive(arsiv_adi+'.zip').extractall('indirilen_dosya')

jp2s = ["T36SVG_20200717T082611_B11.jp2","T36SVG_20200717T082611_B11.jp2"]
arrs = []
#burası bizim jp2 dosyalarımızı okuyacak
for jp2 in jp2s:
    with rasterio.open(jp2) as f:
        arrs.append(f.read(1))

data = np.array(arrs, dtype=arrs[0].dtype)
data

#geojson dosyamızı okuyoruz
footprint = geojson_to_wkt(read_geojson('map.geojson'))
#filtreleme yapıyoruz
products = api.query(footprint,
                     date = ('20151219', date(2015, 12, 29)),
                     platformname = 'Sentinel-2',
                     cloudcoverpercentage = (0, 30))
#indirme yapılıyor
api.download_all(products)

api.to_geojson(products)
#çalışmıyor
api.to_geodataframe(products)
#verilerimizi çekiyoruz
api.get_product_odata("S2A_MSIL1C_20200717T064631_N0209_R020_T41UNT_20200717T084758", full=True)


SentinelAPI("flavves", "BATUhan123.",api_url='https://scihub.copernicus.eu/apihub',show_progressbars=True)

api.get_product_odata("S2A_MSIL1C_20200717T064631_N0209_R020_T41UMT_20200717T084758")



api = SentinelAPI('flavves', 'BATUhan123.')
footprint = geojson_to_wkt(read_geojson('map.geojson'))
products = api.query(footprint,
                     producttype='SLC',
                     orbitdirection='ASCENDING')
api.download_all(products, max_attempts=1)



from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date

api = SentinelAPI('flavves', 'BATUhan123.', 'https://scihub.copernicus.eu/dhus')

# download single scene by known product id
#göz simgesine bas ordan yukardan al bunu linkin içinde
api.download("cc40b640-151e-44ad-a114-41a592e75bf2")

# search by polygon, time, and SciHub query keywords
footprint = geojson_to_wkt(read_geojson('map.geojson'))
products = api.query(footprint,
                     date=('20151219', date(2020, 7, 14)),
                     platformname='Sentinel-2',
                     cloudcoverpercentage=(0, 30))

# download all results from the search
api.download_all(products)

# convert to Pandas DataFrame
products_df = api.to_dataframe(products)

# GeoJSON FeatureCollection containing footprints and metadata of the scenes
api.to_geojson(products)

# GeoPandas GeoDataFrame with the metadata of the scenes and the footprints as geometries
api.to_geodataframe(products)

# Get basic information about the product: its title, file size, MD5 sum, date, footprint and
# its download url
api.get_product_odata("bed2d688-746d-4c87-b905-92d581502067")

# Get the product's full metadata available on the server
api.get_product_odata("cc40b640-151e-44ad-a114-41a592e75bf2", full=True)


# convert to Pandas DataFrame
products_df = api.to_dataframe(products)

# sort and limit to first 5 sorted products
products_df_sorted = products_df.sort_values(['cloudcoverpercentage', 'ingestiondate'], ascending=[True, True])
products_df_sorted = products_df_sorted.head(5)

# download sorted and reduced products
api.download_all(products_df_sorted.index)


