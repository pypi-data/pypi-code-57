import requests
import sys
import os
import pickle
import json
from urllib.parse import quote


class mlURL:
    def __init__(self):
        '''Genera la URL de la API de ML segun los criterios de busqueda configurados.

        Parametros de configuracion:
        .ml :           direccion URL base de la API de ML. Por default es: https://api.mercadolibre.com/
        .SITE_ID:       Codigo del pais donde se realiza la busqueda. Default: MLA (argentina)
        .find:          Texto a buscar en la pagina de ML
        .CATEGOTY_ID:   Codigo de la categoria donde buscar. Ver en https://api.mercadolibre.com/sites/MLA/categories
        .NICKNAME:      Nombre del vendedor sobre el cual realizar la busqueda
        .SELLER_ID:     Codigo del vendedor sobre la cual realizar la busqueda
        .limit:         Cantidad de items disponibles por offset*. El valor default es de 50.

        Metodos:
        .getURL():                  Construye la URL con los parametros seteados
        .getURL_w_offset(offset):   Construye la URL con el offset* indicado. 0: 0->limit-1 | 1: limit->2*limit-1 | etc

        *Una busqueda devuelve por default los primeros 50 items. El maximo es hasta 100 items seteando el parametro limit.
        Para obtener el resto de los items es necesario hacer un offset para el siguiente grupo 50 de items.

        Ejemplo:

        Generar la URL para buscar el texto 'Ford fiesta kinetic' en la categoria 'Autos, motos y Otros' (MLA1743):

        -------------------------------------------
        from getDataML import mlURL


        url = mlURL()
        url.CATEGORY_ID = 'MLA1743'
        url.find = 'Ford fiesta kinetic'
           
        URL = url.getURL()
        -------------------------------------------

        '''
        
        # valores predefinidos
        self.ml = 'https://api.mercadolibre.com/'
        self.SITE_ID = 'MLA'

        # valores configurables
        self.query = ''         # Texto a buscar
        self.CATEGORY_ID = ''   # Codigos en https://api.mercadolibre.com/sites/MLA/categories
        self.SELLER_ID = ''     # buscar en un vendedor segun su ID
        self.NICKNAME = ''      # buscar en un vendedor segun su NICKNAME
        self.limit = ''         # cantidad de items por busqueda u offset
        #self.offset = '0' 

        # valores almacenados
        self.totalItems = ''    # Cantida de items en la busqueda realizada
        self.url = ''           # URL base obtenida del metodo getURL()
        self.a_filters = {}     # Lista de filtros disponibles
        self.filters = {}       # Lista de filtros utilizados
        self.f = {}             # filtros aplicados a self.url

    def getURL(self):
        'Devuelve un string con la URL de la API de ML segun los parametros configurados'

        query = '&q=' + quote(self.query)               if self.query         else ''
        CATEGORY_ID = '&category=' + self.CATEGORY_ID   if self.CATEGORY_ID   else ''
        SELLER_ID = '&seller_id=' + self.SELLER_ID      if self.SELLER_ID     else ''
        NICKNAME = '&nickname=' + self.NICKNAME         if self.NICKNAME      else ''
        limit = '&limit=' + str(self.limit)             if self.limit         else ''
        
        # EH: si algunas de las opciones se quieren poner como vacias con algo distinto a ''. ej. [], None no concatena.

        URL = self.ml +'sites/' + self.SITE_ID + '/search?' + query + CATEGORY_ID + NICKNAME + SELLER_ID + limit # solo sirve para buscar
        self.url = URL

        self.a_filters = {}     # Lista de filtros disponibles
        self.filters = {}       # Lista de filtros utilizados

        return URL

    def getURL_w_offset(self, offset):
        '''Devuelve un string con la URL de la API de ML segun el offset indicado
        
        0: 0 -> 49 | 1: 50 -> 99 | etc

        '''
        #self.offset = str(offset*50)
        offset = '&offset=' + str(offset*50)
        URL = self.url + offset
        return URL

    def loadFilters(self):
        '''Almacena desde self.url la lista de filtros aplicados y filtros disponibles.

        '''

        if not self.url:
            print('No se genero la URL. Configurar url y ejecutar url.getURL().')
            return None
        
        URL = self.url
        r = get_by_key(URL)

        total = r['paging']['total']
        print('>> Hay',total,'items en esta busqueda.')

        self.filters = r["filters"]
        self.a_filters = r["available_filters"]
        return True
    
    def loadFiltersFromDict(self):
        filters = ''
        for key in self.f:
            filters = filters + '&' + key + '=' + self.f[key]
        self.url = self.url + filters
        self.a_filters = {}
        self.filters = {}

    def print_filters(self):
        '''Imprime los filtros aplicados en la busqueda.

        '''

        if not self.filters:
            print('Descargando lista de filtros disponibles...')
            if not self.loadFilters():
                return None
        print('La busqueda contiene los filtros:')
        for f in self.filters:
            print('> Filtro:',f['name'],'| ID:',f['id'])
            for v in f['values']:
                print('\t - Value:',v['name'], '| ID:',v['id'])
            #print(json.dumps(f, indent=2))

    def print_a_filters(self):
        '''Imprime los filtros disponibles para aplicar en la busqueda.

        '''

        if not self.a_filters:
            print('Descargando lista de filtros disponibles...')
            if not self.loadFilters():
                return None
        print('Se pueden incluir en la busqueda los filtros:')
        i = 0
        for f in self.a_filters:
            print('> Filtro',i,':',f['name'],'| ID:',f['id'])
            j = 0
            for v in f['values']:
                print('\t - Value', j,':',v['name'], '| ID:',v['id'],'| Items:',v['results'])
                j += 1
            i += 1
            #print(json.dumps(f, indent=2))

    def setFilter(self, idF, value, Forzar = False):
        '''Agrega un filtro 'id' con valor 'value' a self.url. 
        
        idF:    String con el id del filtro. 
        value:  valor para el filtro idF
        '''

        if not self.a_filters:
            print('Descargando lista de filtros disponibles...')
            if not self.loadFilters():
                return None
        isId = [True for f in self.a_filters if f['id'] == idF]
        if isId or Forzar:
            newFilter = '&' + idF + '=' + value
            self.url = self.url + newFilter
            self.a_filters = {}
            self.filters = {}
            self.f[idF] = value
        else:
            print(idF,'no es un filtro disponible.')
            return None

    def setFilterIdx(self, idx, valx):
        '''Agrega a self.url un filtro de la posision idx con valor de posicion valx self.a_filters. 

        idx: indice en self.a_filters del filtro a setear
        valx: indice del valor
        '''

        if not self.a_filters:
            print('Descargando lista de filtros disponibles...')
            if not self.loadFilters():
                return None
        try:
            idF = self.a_filters[idx]['id']
            value = self.a_filters[idx]['values'][valx]['id']
            self.setFilter(idF,value)
            return idF, value
        except Exception as e:
            print(repr(e))
            print(idF,'no es un filtro disponible.')
            return None

    def removeFilter(self, idF):
        '''Remuevo de self.url el filtro 'idF'.

        '''

        idx = self.url.find(idF)
        if idx > 0:
            #si hay '&' remuevo ese segmento 
            #sino remuevo todo el segmento
            idx2 = self.url[idx::].find('&')
            if idx2 > 0:
                URL = self.url[0:idx-1] + self.url[idx+idx2::]
            else:
                URL = self.url[0:idx-1]
            self.url = URL
            self.a_filters = {}
            self.filters = {}
            self.f.pop(idF)
            print('Se elimino el filtro',idF)
        else:
            print(idF,'no es un filtro aplicado.')
            return None

    def clearFilters(self):
        '''Elimina todos los filtros.

        '''

        self.getURL()
        self.f = {}
        self.a_filters = {}
        self.filters = {}

def getData(url):
    '''Generador que devuelve progresivamente un diccionario con el resultado de la busqueda.

    La variable url es la clase mlURL() instanciada y configurada con la busqueda a realizar.

    Ejemplos:

    -------------------------------------------

    from getData import mlURL
    from getData import getData

    url = mlURL()
    url.CATEGORY_ID = 'MLA1743'
    url.query = 'Ford fiesta kinetic 2011'
        
    prices = [item['price'] for item in getData(url)] # devuelve todos los precios de la busqueda
    print(prices)

    -------------------------------------------

    from getDataML import getData
    from getDataML import mlURL

    url = mlURL()
    url.CATEGORY_ID = 'MLA1743'
    url.query = 'Ford fiesta kinetic'

    items = getData(url)

    item = next(items) # 1er item de la busqueda
    print(url.totalItems) # cantidad de items en la busqueda
    print(item['price']) # precio del item

    item = next(items) # 2do item de la busqueda
    item = next(items) # 3er item de la busqueda
    ...
    -------------------------------------------

    '''
    maxItems = 1000

    r = requests.get(url.url)
    totalItems = r.json()['paging']['total']
    limit = r.json()['paging']['limit']
    url.totalItems = totalItems
    print(' - Se encontraron',totalItems,'resultados.')
    
    if totalItems > maxItems:
        print ('El maximo permitido de publicaciones a descargar es de',maxItems)
        totalItems = maxItems

    offsets = int((totalItems-1)/limit + 1)
    n_offsets = 0

    bar = toolbar(int(totalItems))
    # recorro cada bloque de 50 publicaciones
    next(bar)
    while n_offsets < offsets:
        
        URL = url.getURL_w_offset(n_offsets)
        r = requests.get(URL)
        # recorro cada publicacion del bloque
        for item in r.json()['results']:
            #price = item['price']
            #yield price
            next(bar)
            yield item
        
        #print (n_offsets)
        n_offsets += 1
    
def get_by_key(URL, key = ''):
    '''Devuelve el diccionario bajo el key. Sin key, devuelve todo el request

    '''
    r = requests.get(URL)
    dic = r.json()[key] if key else r.json()
    return dic

def get_by_keys(URL, keys = []):
    '''Generador que devuelve el diccionario bajo los keys. Sin keys, devuelve todo el request

    '''
    r = requests.get(URL)
    for key in keys:
        dic = r.json()[key] if key else r.json()
        yield dic

def getCategories(CATEGORY_ID = '', key = ''):
    '''Devuelve el diccionario con las categorias disponibles.

    Si no se especifican argumentos, devuelve todas las categorias
    Sino para una URL de categorias, devuelve las categorias de la key indicada

    Ejemplo:

    # Obtener todas las categorias disponibles
    -----------------------------------
    allCat = getCategories()
    -----------------------------------

    # Obtener las categorias de raiz y las hijas de una categoria
    -----------------------------------
    CATEGORY_ID = 'MLA5725'

    rootCat = getCategories(CATEGORY_ID, key = 'root')
    childCat = getCategories(CATEGORY_ID, key = 'child')
    -----------------------------------

    '''
    URL = 'https://api.mercadolibre.com/categories/'
    URL = URL+CATEGORY_ID if CATEGORY_ID else 'https://api.mercadolibre.com/sites/MLA/categories'

    if key == 'child':
        cat = get_by_key(URL, key = 'children_categories')
    elif key == 'root':
        cat = get_by_key(URL, key = 'path_from_root')
    else:
        cat = get_by_key(URL)

    return cat



def toolbar(toolbar_width = 40):
    '''Imprime una barra de progreso: [##########].

    # Variables:

    toolbar_width:  Ancho total de la barra.

    # Uso:
    ------------------------------------
    progressTotal = 8
    bar = toolbar(progressTotal)

    next(bar)
    for i in range(progressTotal):
        #cosas del programa
        next(bar)
    ------------------------------------

    '''
    max_toolbar_width = 80
    toolbar_step = 1
    stop = max_toolbar_width
    toolbar_width_real = toolbar_width

    # si excedo el ancho maximo, comprimo en toolbar_step veces cada paso. Lo que sobra lo paso uno a uno despues del stop
    # ej. si max_toolbar_width = 10 y toolbar_width = 15, hago que cada paso equivalnga a 2 hasta completar 10. los restantes 5 los hago 1 a 1.
    if toolbar_width > max_toolbar_width:
        toolbar_step = round(toolbar_width/max_toolbar_width)
        stop = toolbar_width_real - toolbar_width_real//max_toolbar_width  #2*toolbar_width - toolbar_step*max_toolbar_width
        toolbar_width_real = toolbar_width
        toolbar_width = max_toolbar_width
        
    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

    i = 0
    while i < toolbar_width_real:
        # update the bar
        j = toolbar_step - 1 if i >= stop else 0
        while j < toolbar_step:
            yield
            i += 1
            j += 1
        sys.stdout.write("|")
        sys.stdout.flush()
    sys.stdout.write("]\n") # this ends the progress bar
    yield
#crear una clase para los filtros


#ejemplos        
#https://api.mercadolibre.com/sites/MLA/search?q=Motorola%20G6&category=MLA1743
#https://api.mercadolibre.com/sites/$SITE_ID/search?seller_id=$SELLER_ID&category=$CATEGORY_ID
#https://api.mercadolibre.com/sites/$SITE_ID/search?seller_id=$SELLER_ID&sort=price_asc
#https://api.mercadolibre.com/sites/$SITE_ID/search?nickname=$NICKNAME
#https://api.mercadolibre.com/sites/$SITE_ID/search?seller_id=$SELLER_ID
#https://api.mercadolibre.com/sites/MLA/search?q=Ford%20fiesta%20kinetic&VEHICLE_YEAR=2011-2011

#with vcr.use_cassette('fixtures/vcr_cassettes/ML.yaml', record_mode='new_episodes'):
    #url =mlURL()
    
    #url.CATEGORY_ID = 'MLA90998'
    #url.CATEGORY_ID = ''
    #url.find = 'Ford fiesta kinetic 2011'
           
    #CATEGORY_ID = 'MLA1743' # Autos, motos y Otros
    #CATEGORY_ID = "MLA90998" # Ford Fiesta KD
    #CATEGORY_ID = ''

    #url.getURL()
    #url.getURL_w_offset(1)

    #r = requests.get(url.getURL())

    #n_item = 0
    #totalItems = r.json()['paging']['total']
    #r.json()['results'][n_item]['price']
    #r.json()['results'][0]['attributes'][10]['value_name'] # year
    #r.json()['results'][0]['attributes'][6]['value_struct']['number'] #km
    #r.json()['total']

    #[print(item['attributes'][10]['value_name']) for item in r.json()['results']]
  
    #prices = [a for a in getData(url)]
    #print(prices)
