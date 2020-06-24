import traceback
from opentracing.ext import tags as ext_tags
from .Base import Base
from .ErrorMs import ErrorMs
from .Util import getItemBy

class Worker(Base):
    """
        Clase que contiene la logica para el manejo de los
        worker.
    """

    def process(self, span, request, fnc, params=[]):
        """
            Metodo que se encarga de procesar, la accion
            que se asign al evento del microservicio.

            @params resquest peticion de datos
            @params fnc Funcion a ejecutar
        """
        # Parametros
        paramsInject = self.getParams(span, request, params)

        # Ejecutar la funciona final
        RESP = fnc(**paramsInject)
        # Regresar la respuesta con el formato correcto
        return self.formatResponse(request, RESP)

