from intake_dal.dal_catalog import DalCatalog
from intake_dal.dal_online import DalOnlineSource

if __name__ == "__main__":
    serving_cat = DalCatalog('https://dataset-catalog-service.dev.zo.zillow.net/catalog/latest/dev', storage_mode="serving")
    print(serving_cat.entity.property.geo_etl(key=[62994016, 200, 62994016]).read())
    print(serving_cat.entity.property.geo_etl(key=62994016).read())
