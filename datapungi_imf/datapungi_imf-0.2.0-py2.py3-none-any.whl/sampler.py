'''
  summary tables
'''
import datapungi_imf as dpi
import pandas as pd 


data = dpi.data()


def countryList():
    countries = data.params('IFS')['codes']['CL_AREA_IFS']
    return(countries)

def sna(country):
    '''
      Given a country, returns SA Deflated GDP and components
    '''
    variables = [
        ["Y",     "NGDP_SA_XDC"],
        ["C",     "NCP_SA_XDC"],
        ["G",     "NCGG_SA_XDC"],
        ["I",     "NFI_SA_XDC"],
        ["INV",   "NINV_SA_XDC"],
        ["X",     "NX_SA_XDC"],
        ["M",     "NM_SA_XDC"],
        ["DEF",   "NGDP_D_SA_IX"],
    ]
    
    query = lambda dbName : f'IFS/A.{country}.{dbName}'
    table = [data.data( query(x[1]) ) for x in variables  ]
    tab = pd.concat(table,axis=1)
    names = [x[0] for x in variables]
    nondef = list(filter(lambda x: x != 'DEF', names))
    tab.columns = names
    tab['DEF'] = tab['DEF']/100
    tab[nondef] = tab[nondef]/(1000)  #all in billions
    tab[nondef] = tab[nondef].div(tab['DEF'], axis=0)
    return(tab)

## Balance of Payments: Current Accounts | Capital and Financial Accounts %%%%%%%%%%%%%%%%%%%
def CurAcct(country):
   vars = {'BGS_BP6_USD':'Net Exports', 'BG_BP6_USD':"-Net Exports of Goods",'BS_BP6_USD':'-Net Exports of Services','BIP_BP6_USD':'Primary Income','BIS_BP6_USD':'Secondary Income'}
   fetch = [data.data(f'BOP/A.{country}.'+var).rename({'value':name},axis='columns').drop('@OFFICIAL_BPM',axis=1) for var, name in vars.items()]
   tab = pd.concat(fetch,axis=1)/1000
   return(tab)

def FinAcct(country,Freq='Q'):
    vars = {
      'BFD'  : 'Direct Investment, net',
      'BFDL' : '-Direct Investment, liability',
      'BFP'  : 'Portfolio Investment, net',
      'BFPL' : '-Portfolio Investment, liability',
      'BFF'  :  'Derivatives',
      'BFO'  : 'Other Investment, net',
      'BFOL' : '-Other Investment, liability',
    }
    fetch = []
    for var, name in vars.items():
      fetch.append(data.data(f'BOP/{Freq}.{country}.'+var+'_BP6_USD').rename({'value':name},axis='columns').drop('@OFFICIAL_BPM',axis=1) )
    tab = pd.concat(fetch,axis=1)/1000
    #insert assets:
    tab.insert(1,'-Direct Investment, assets', tab['Direct Investment, net'] + tab['-Direct Investment, liability'])
    tab.insert(4,'-Portfolio Investment, assets', tab['Portfolio Investment, net'] + tab['-Portfolio Investment, liability'])
    tab.insert(8,'-Other Investment, assets', tab['Other Investment, net'] + tab['-Other Investment, liability'])
    
    return(tab)

def CapitalAcct(country):
    vars = {
      'BK_CD_BP6'  : '-Capital Account, Credit',
      'BK_DB_BP6' : '-Capital Account, Debit',
    }
    fetch = []
    for var, name in vars.items():
      fetch.append(data.data(f'BOP/A.{country}.'+var+'_BP6_USD').rename({'value':name},axis='columns').drop('@OFFICIAL_BPM',axis=1) )
    tab = pd.concat(fetch,axis=1)/1000
    tab.insert(0, 'Capital Account', tab[])
    return(tab)


def ReserveAcct(country):
    vars = {
      'BTRUE_BP6_USD' : 'Reserve Assets',
      'BIMF_CD_BP6_USD' : 'Reserve Assets IMF',
      'BEF' : 'Exceptional Financing',
    }
    fetch = []
    for var, name in vars.items():
      fetch.append(data.data(f'BOP/A.{country}.'+var+'_BP6_USD').rename({'value':name},axis='columns').drop('@OFFICIAL_BPM',axis=1) )
    tab = pd.concat(fetch,axis=1)/1000
    return(tab)


## examples
def FDI(countryList):
  ''' liabilities = purchases - sales by foreigners to acquire, establish expand business'''
  output = {country : FinAcct(code).iloc[:,0:3] for code, country in countryList.items()}
  return(output)

if __name__ == '__main__':
    import pypungi
    pp = pypungi.link()
    pp.plot(nsi('SG'))
    
    
    #countries = countryList()
    southAm = {'AR':'Argentina','BR':'Brazil','BO':'Bolivia','CL':'Chile','CO':'Colombia','EC':'Ecuador','PE':'Peru','UY':'Uruguay','VE':'Venezuela','SR':'Suriname','GY':'Guyana'}
    SAfdi = FDI(southAm)
    