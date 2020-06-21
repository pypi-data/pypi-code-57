def hola_mundo(name="Mundo"):
   return "Librería creada e importada exitosamente. Hola, {name}".format(name = name)
   
def colored_df(pandas_df, cmap='RdYlGn',axis=None):
   return pandas_df.style.background_gradient(cmap=cmap,axis=axis)
    
# .format('{:,.1%}'.format)