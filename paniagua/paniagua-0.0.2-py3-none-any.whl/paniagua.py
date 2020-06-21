def hola_mundo(name="Mundo"):
   return "Librería creada e importada exitosamente. Hola, {name}".format(name = name)
   
def colored_df(pandas_df):
    return pandas_df.style.background_gradient(cmap='RdYlGn',axis=None)
    
# .format('{:,.1%}'.format)