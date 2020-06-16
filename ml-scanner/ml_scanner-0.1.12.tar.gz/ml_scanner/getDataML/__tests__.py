from ml_scanner.getDataML import getDataML

url = getDataML.mlURL()
url.query = 'nescafe dolce gusto piccolo xs'
URL = url.getURL()

# filtros disponibles para aplicar
url.print_a_filters()
url.setFilterIdx(14,0)
url.setFilterIdx(8,0)
url.setFilterIdx(11,0)
url.setFilterIdx(0,1)
url.setFilter('price','*-12500.0',Forzar= True)

url.f



