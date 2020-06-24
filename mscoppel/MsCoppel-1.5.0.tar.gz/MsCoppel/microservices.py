import sys
import inspect
import json
import os
import socket
import copy
import base64
import datetime
import traceback
import uuid
import _thread
import asyncio  # Requerido
from jaeger_client import Config
from opentracing import Format
from opentracing.ext import tags as ext_tags
from abc import abstractmethod, ABC
from .options import Options
from .Worker import Worker
from .Fork import Fork
from .ErrorMs import ErrorMs
from .Util import validForksConf, getItemBy
from .version_framework import version
from http.server import BaseHTTPRequestHandler, HTTPServer
from .types import TypesActions

if os.environ.get('KAFKA', None):
    from .ms_base import KafkaBase as BaseClass
elif os.environ.get('NATS', None):
    from .NatsBase import NatsBase as BaseClass
else:
    # En caso que se no indique por variable de entorno
    from .ms_base import KafkaBase as BaseClass


class Microservices(BaseClass, ABC):
    """
        Clase con la logica necesaria para utilizar sobre los
        microservicios, se debe implementar los metodos segun
        como se requiera.
    """
    # Datos de configuracion
    __OPT = {}
    # Acciones del microservicio
    __ACTIONS = {}
    # Lista de errores definidos por el usuario
    __ERRORS = {
        '-97': 'No existe la accion que esta tratando de llamar',
        '-98': 'Ocurrio una error, favor de intentar de nuevo.',
        '-99': 'Ocurrio una excepcion, favor de intentar de nuevo.',
        '0': 'Smoke Test',
        '-1': 'Este servicio no puede ser consumido de forma externa'
    }
    # Logica de la aplicacion
    __APP = None

    # Topico
    __TOPIC__ = ''

    # Hostname
    __HOSTNAME = ''

    # Fork Configurados en la clase
    __FORKS = None

    # Indicar si es el servicio es una bifurcacion
    ___isForks = False

    # OpenTracing Jaeger
    ___Tracer = None

    # Indicar si se usara los logs de fluentd
    __fluentd_logs = False

    """
        Clase que contiene la logica del microservicio.
    """

    def __init__(self, opt):
        # Validar que se pase un objeto de configuracion correcto
        if not isinstance(opt, Options):
            self.logs.error('No se proporciono una configuracion correcta')
            sys.exit(-1)

        # Asignar los datos de la configuracion para su acceso
        self.__OPT = opt

        # Construccion del topico
        if opt.App == 'appcoppel' and opt.Version == 'v1':
            topico = opt.Name
        else:
            topico = "{}_{}_{}".format(opt.App, opt.Version, opt.Name)

        # Asignar el topico
        self.__TOPIC__ = topico

        # Recuperar el hostname del servidor
        self.__HOSTNAME = socket.gethostname()

        # Inicializacion del tracer
        self.initilizeTracer()

        # Inicializacion de HealthCheck
        _thread.start_new_thread(
            self.startHttpHealthCheck, (self.HealthCheck, self.smoketest))

        # Buscar las acciones
        self.__initActions()

        # Validar si es Productivo o si se activaron los logs a fluent
        if not os.environ.get('LOGS_FLUENT', None) is None:
            self.__fluentd_logs = True
            # Enviar la configuracion necesaria
            self.logs.set_conf(opt.App, opt.Name,
                               opt.Version, opt.Hosts, version)

        # Crear el administrador de la logica de la aplicacion.
        if self.__FORKS is None:
            self.__APP = Worker(self.__TOPIC__)
        else:
            self.logs.info(
                'Se Inicia el servicio con soporte para bifurcaciones')
            self.__APP = Fork(self.__TOPIC__)
            self.___isForks = True

        # llamar el constructor padre
        BaseClass.__init__(self, topico, opt.Hosts, topico)

        if opt.isNats:
            # iniciar la aplicacion
            """
                NOTA:
                    Ninguna instruccion debajo del etodo run_forever()
                    se ejecutara.
            """
            self.loop = asyncio.get_event_loop()
            self.loop.run_until_complete(asyncio.wait([self.run()]))
            # self.loop.run_until_complete(self.run())
            try:
                self.loop.run_forever()
            finally:
                self.loop.close()

    def initilizeTracer(self):
        config = Config(
            config={
                'sampler': {
                    'type': 'const',
                    'param': 1,
                },
                'local_agent': {
                    'reporting_host': os.environ.get('JAEGER_AGENT_HOST', 'jaeger-agent.logging'),
                    'reporting_port': os.environ.get('JAEGER_AGENT_PORT', 6831),
                },
                'logging': True if os.environ.get('PRODUCTION', False) else False,
                'tags': {
                    '@coppel-py-version': version
                }
            },
            service_name=self.__TOPIC__,
            validate=True,
        )
        self.___Tracer = config.initialize_tracer()

    def send(self, topic, msj, idTransaction=""):
        """
            Metodo para el envio de datos a Nats

            @params reply Elemento al que se le responde
            @params msj Mensaje que enviara
            @params idTransaction Id de la transaccion
        """
        self._send(topic, msj, idTransaction)

    def HealthCheck(self):
        return self.validateConnection()

    def startHttpHealthCheck(self, healthcheck, smoketest):
        if os.environ.get('PRODUCTION', False):
            class myHandler(BaseHTTPRequestHandler):
                def do_GET(self):
                    message_parts = []
                    code = 0
                    try:
                        if healthcheck() and smoketest():
                            code = 200
                            message_parts.append("OK")
                    except:
                        code = 500

                    if code < 100:
                        code = 500
                        message_parts.append("ERROR")

                    message = '\r\n'.join(message_parts)
                    self.send_response(code)
                    self.send_header(
                        'Content-Type', 'text/plain; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(message.encode('utf-8'))

            self.logs.info('[HealthCheck] listening on 0.0.0.0:80')

            server = HTTPServer(('', 80), myHandler)
            server.serve_forever()
        else:
            self.logs.warn('HttpHealthCheck is Disabled')

    def coro_manager(self, coro):
        """
            Metodo para poder hacer el llamado de la funcion Async
            sin necesidad de usar await.

            @params coro Metodo async a llamar
        """
        try:
            coro.send(None)
        except StopIteration as stop:
            return stop.value

    def json_to_b64(self, json_in):
        """
            Metodo para convertir un diccionaro al formato
            correcto de los mensajes.

            @param json_in Dict de entrada
        """
        return base64.b64encode(str.encode(json.dumps(json_in)))

    def without_response(self, topic, data):
        """
            Metodo para el envio de una peticion a un topico, sin esperar
            una respuesta del mismo.
        """
        self._send(topic, {
            "metadata": {
                "uuid": None,
                "id_operacion": str(uuid.uuid4()),
                "id_transaction": str(uuid.uuid4()),
                "intents": 1,
                "callback": None,
                "callbacks": [],
                "owner": self.__TOPIC__,
                "uowner": self.__TOPIC__,
                "uworker": "{}_WITHOUT_RESPONSE".format(self.__TOPIC__),
                "worker": self.__TOPIC__,
                "asynchronous": False,
                "mtype": "WITHOUT_RESPONSE",
                "bifurcacion": False,
                "time": "",
                "from": socket.gethostname(),
                "method": "GET",
                "deviceType": "",
                "span": None,
                "filters": None,
            },
            "data": data,
            "headers": {}
        }, str(uuid.uuid4()))

    def _message(self, msg):
        """
            Metodo que se encagra de procesar todos los
            mensajes que llegas desde Kafka.
        """
        # metodo que se ejecutara
        mth = None

        # Recuperar los datos de otro modo regresar
        data = msg.get('data', {})

        # Recuperar la metadata
        meta = msg.get('metadata', {})

        # Configuracion del worker
        confForks = None

        # Parametros solicitados
        paramsConf = []

        # Recuperar el rootSpan
        rootSpan = msg['metadata']['span'] if 'span' in msg['metadata'] else None

        # Validar si es un smoktest
        if 'smoketest' in list(data):
            span = self.___Tracer.start_span(
                operation_name='smoketest', child_of=rootSpan)

            span.set_tag(ext_tags.HTTP_METHOD, msg['metadata']['method'])

            # Ejecutar la funcion del smoketest
            if self.smoketest():
                # Todo esta bien
                self.__response(msg, 0, True, msg.get('uuid', None), span=span)
            else:
                # Algo salio mal
                self.__response(
                    msg, -1, True, msg.get('uuid', None), span=span)

            span.finish()
            return

        # Solo actualizar los datos si e el servicio original
        if self.__TOPIC__ == msg['metadata']['callback']:
            if not msg['metadata'].get('data_inicial', None) is None:
                # Recuperar el metodo original
                if not msg['metadata'].get('original_method', None) is None:
                    msg['metadata']['method'] = msg['metadata']['original_method']

                # Recuperar el metodo original
                if not msg['metadata'].get('data_inicial', None) is None:
                    msg['data'] = msg['metadata']['data_inicial']

        # Validar si se encuentra en modo Debug
        if self.__OPT.Debug and self.__fluentd_logs:
            _data_ = {}
            _data_.update({'owner': meta.get('owner')})
            _data_.update({'method': meta.get('method')})
            _data_.update({'headers': msg.get('headers', {})})
            _data_.update({'data': msg.get('data', {})})
            self.logs.info('ENTRADA {}'.format(json.dumps(_data_)))
        elif self.__OPT.Debug:
            self.logs.info("\n ENTRADA: {} \n METODO: {} \n HEADERS: {} \n DATA: {}".format(
                meta.get('owner'),
                meta.get('method'),
                json.dumps(msg.get('headers', {})),
                msg.get('data', {})
            ))

        try:
            if msg['metadata']['time'].index('Z') > -1:
                date = datetime.datetime.strptime(
                    msg['metadata']['time'], '%Y-%m-%dT%H:%M:%SZ')
                currDate = datetime.datetime.utcnow()
                elapsedTime = currDate - date
                diff = divmod(elapsedTime.total_seconds(), 60)[0]
                if diff >= 5:
                    # print('EXIT TIME : ', msg['metadata']['time'], ' ', diff)
                    pass
        except:
            self.logs.warn(
                'Ocurrior un error al momento de procesar el tiempo del mensaje')

        # Procesar el mensaje
        try:
            mth = self.__getMethod(msg.get('metadata'))
        except Exception as identifier:
            # No fue posible recuperar una accion para el evento
            self.logs.error(
                'No fue posible recuperar una accion para el evento {}'.format(identifier))

        # Validar que exista
        try:
            if hasattr(mth, '__CONF_FORKS__'):
                methodConfFork = getattr(mth, '__CONF_FORKS__')
                # Recuperar la configuracion
                confForks = self.__getConfServiceFork(methodConfFork)
        except Exception as e:
            self.logs.error(
                'Ocurrio un error al recuperar la configuracion del servicio: {}'.format(e))

        # Buscar los parametros
        try:
            if hasattr(mth, '__CONF_PARAMS__'):
                paramsConf = getattr(mth, '__CONF_PARAMS__')
        except Exception as e:
            self.logs.error(e)

        if rootSpan is not None:
            rootSpan = self.___Tracer.extract(Format.TEXT_MAP, rootSpan)

        span = self.___Tracer.start_span(operation_name=getattr(
            mth, '__FUNC_NAME__'), child_of=rootSpan)

        span.set_tag(ext_tags.HTTP_METHOD, msg['metadata']['method'])

        RESP = {}

        # Enviar el mensaje al que procesa [Worker, Fork]
        try:
            # Configuracion de los forks
            if confForks is None:
                self.__APP = Worker(self.__TOPIC__)
            else:
                self.__APP = Fork(self.__TOPIC__)
                self.__APP.confForks(confForks)

            # Indicar si es una bifurcacion
            msg['metadata']['bifurcacion'] = True if confForks else False

            # ejecutar el proceso
            RESP = self.__APP.process(span, msg, mth, paramsConf)

            # Ruta [SOLO NATST]
            id_route_nats = getItemBy('response.uuid', RESP)

            if not msg['metadata']['mtype'] == 'WITHOUT_RESPONSE':
                # Enviar la respuesta
                self.__response(
                    RESP.get('response', {}),
                    RESP.get('errorCode'),
                    span=span,
                    nats_route=id_route_nats,
                    errorResp=RESP.get('errorWorker', None),
                )

        except ErrorMs as error:
            span.set_tag(ext_tags.ERROR, True)
            span.log_kv({'event': 'error', 'error.code': error.errorCode, 'error.message': self.___getErrorId(
                error.errorCode), 'error.stack': traceback.format_exc()})
            self.logs.error(self.___getErrorId(error.errorCode))
            # Validar si es async
            if not msg['metadata']['mtype'] == 'WITHOUT_RESPONSE':
                self.__response(
                    msg, error.errorCode, span=span, nats_route=msg.get(
                        'uuid', None), errorResp=RESP.get('errorWorker', None),
                )  # Enviar el error

        except Exception as e:
            span.set_tag(ext_tags.ERROR, True)
            span.log_kv({'event': 'error', 'error.message': str(
                e), 'error.stack': traceback.format_exc()})
            self.logs.error(e)
            # Enviar el error
            if not msg['metadata']['mtype'] == 'WITHOUT_RESPONSE':
                self.__response(
                    msg, -99, span=span, nats_route=msg.get('uuid', None),
                    errorResp=RESP.get('errorWorker', None),
                )

        span.finish()

    def __response(self, data, errorCode, isSmokeTest=False, nats_route=None, span=None, errorResp=None):
        """
            Metodo para enviar la respuesta a kafka
        """

        # Diccionario de la respuesta
        Resp = {}

        # Crear una copia de la respuesta
        dataResponse = data

        # Topico de respuesta
        TOPIC_RESP = None

        # Comprobar si contiene un error heredado
        if not errorResp is None:
            errorCode = errorResp.get('errorCode', -99)  # Error generico

        try:
            errorCodeBk = errorCode
            # Prevenir el paso de string como error
            errorCode = int(errorCode)
        except:
            self.logs.error(
                'Ocurrio une error al realizar el CAST del error code: {}'.format(errorCodeBk))
            errorCode = -99

        # Validar si ocurrio un error
        if errorCode < 0 or errorCode > 0:
            # Estructura del mensaje de error
            dataResponse['response'] = {
                "data": {
                    "response": {
                        "hostname": self.__HOSTNAME,
                        "code": errorCode,
                        "errorCode": errorCode,
                        # Regresar el mensaje que se proporciono desde el worker que se consumio
                        "userMessage": self.___getErrorId(errorCode) if errorResp is None else errorResp.get('userMessage')
                    }
                },
                "meta": {
                    "id_transaction": dataResponse['metadata']['id_transaction'],
                    "status": 'ERROR' if errorCode < 0 or errorCode > 0 else 'SUCCESS'
                }
            }

        # Asignar el tiempo
        dataResponse['metadata']['time'] = datetime.datetime.utcnow().isoformat()

        # Indicar el worker
        # dataResponse['metadata']['worker'] = data['metadata']['owner']

        # Topico
        dataResponse['metadata']['owner'] = self.__TOPIC__

        # Tipo de salida
        dataResponse['metadata']['mtype'] = 'output'

        # Indicar Hostname
        dataResponse['metadata']['hostname'] = self.__HOSTNAME

        # Indicar version del framework
        dataResponse['metadata']['framework'] = version

        # Validar que tenga un uowner
        if dataResponse['metadata'].get("uowner", None) is not None:
            dataResponse['metadata']['uworker'] = data['metadata']['uowner']

        # Validar si tiene asignado un uworker
        if dataResponse['metadata'].get("uworker", None) is not None:
            dataResponse['metadata']['uowner'] = data['metadata']['uworker']

        if span:
            carrier = {}
            self.___Tracer.inject(span, Format.TEXT_MAP, carrier)
            dataResponse['metadata']['span'] = carrier

        # Ver si es un Worker
        if isinstance(self.__APP, Worker):
            dataResponse['metadata']['bifurcacion'] = False

        # Ver si es bifurcacion
        is_forks = getItemBy('metadata.bifurcacion', dataResponse)

        # Metodo original
        original_method = getItemBy('metadata.original_method', dataResponse)

        '''
            Validacion del Callback
        '''

        if is_forks:
            if getItemBy('metadata.callbacks', dataResponse) is None:
                # Agregar
                dataResponse['metadata'].update({'callbacks': []})
                # Validar que sea NATS
                if not nats_route is None or len(nats_route) > 0:
                    # Agregar el Nats_UUID
                    dataResponse['metadata']['callbacks'].append({
                        "method": 'ENDPOINT',
                        "name": nats_route,
                    })

            # Recuperar los callbacks
            callbacks = getItemBy('metadata.callbacks',
                                  copy.deepcopy(dataResponse))

            if len(callbacks) > 0:
                cllbs = callbacks.pop()

                tp = cllbs.get('name')
                mt = cllbs.get('method')

                if self.__TOPIC__ == tp and original_method == mt:
                    self.logs.warn('Repetition event prevented')
                else:
                    # Agregar al arreglo
                    dataResponse['metadata']['callbacks'].append({
                        "method": original_method,
                        "name": self.__TOPIC__,
                    })
            else:
                # Agregar al arreglo
                dataResponse['metadata']['callbacks'].append({
                    "method": original_method,
                    "name": self.__TOPIC__,
                })

            # TOPIC_RESP = dataResponse['metadata']['worker']
        else:
            callbacks = getItemBy('metadata.callbacks', dataResponse)
            # Se obtiene el ultimo elemento agregado para responder a el
            if callbacks and len(callbacks) > 0:
                cllbs = callbacks.pop()
                sizeCllbs = len(callbacks)
                mthd = original_method
                find = True
                counter = 0
                if self.__TOPIC__ == cllbs.get('name') and mthd == cllbs.get('method'):
                    while find and counter < sizeCllbs:
                        cllbs = callbacks.pop()
                        if self.__TOPIC__ != cllbs.get('name') or mthd != cllbs.get('method'):
                            TOPIC_RESP = cllbs.get('name')
                            dataResponse['metadata']['method'] = cllbs.get(
                                'method')
                            find = False
                        counter += 1
                else:
                    TOPIC_RESP = cllbs.get('name')
                    dataResponse['metadata']['method'] = cllbs.get('method')

            else:
                pass

            # Eliminamos elemento (Este es agregado cuando es una bifurcacion)
            if not dataResponse['metadata'].get('original_method', None) is None:
                del dataResponse['metadata']['original_method']
            else:
                pass

        # Ver si es utilizado Nats
        if nats_route is None:
            # Topico de respuesta
            TOPIC_RESP = TOPIC_RESP if TOPIC_RESP else "respuesta_{}".format(
                dataResponse['metadata']['owner'])
        else:
            # Asignar el id de ruta que proviene del reply
            TOPIC_RESP = TOPIC_RESP if TOPIC_RESP else nats_route

        # Consultar quien es el callback
        cllb = getItemBy('metadata.callback', dataResponse)

        # Datos requeridos para seleccion de topic
        req_worker = getItemBy('metadata.worker', dataResponse)
        req_owner = getItemBy('metadata.owner', dataResponse)
        req_bifurcacion = getItemBy('metadata.bifurcacion', dataResponse)

        if req_worker != req_owner and req_bifurcacion:
            TOPIC_RESP = req_worker
            dataResponse['metadata']['worker'] = req_owner
            Resp = dataResponse
        elif self.__TOPIC__ != cllb and req_bifurcacion:
            TOPIC_RESP = TOPIC_RESP if TOPIC_RESP else cllb
            dataResponse['data'] = dataResponse['response']['data']
            Resp = dataResponse
        else:
            # Asignar la respuesta
            Resp = {
                "_id": dataResponse['metadata']['id_transaction'],
                "data": getItemBy('metadata.data_inicial', dataResponse),
                "headers": dataResponse.get('headers', {}),
                "metadata": dataResponse.get('metadata', {}),
                "response": dataResponse.get('response', {})
            }

        callbacksTop = getItemBy('metadata.callbacks', dataResponse)

        if callbacksTop and len(callbacksTop) == 0:
            del Resp['metadata']['metadata_inicial']
            del Resp['metadata']['data_inicial']

        # Revisar si es un smoketest
        if isSmokeTest:
            # respuesta generica
            Resp.update(
                {
                    'response': {
                        "data": {
                            "response": {
                                "code": errorCode,
                                "framework": version,
                                "hostname": self.__HOSTNAME,
                                "userMessage": "Smoke test"
                            }
                        },
                        "meta": {
                            "id_transaction": dataResponse['metadata']['id_transaction'],
                            "status": 'ERROR' if errorCode < 0 or errorCode > 0 else 'SUCCESS'
                        }
                    }
                }
            )

        span.log_kv({'event': 'output', 'response': Resp['response']})

        # Validar si es modeo DEBUG
        if self.__OPT.Debug and self.__fluentd_logs:
            self.logs.info("SALIDA [{}]".format(TOPIC_RESP), Resp)
        elif self.__OPT.Debug:
            self.logs.info("SALIDA [{}]: {}".format(
                TOPIC_RESP, json.dumps(Resp)))

        # Publicar la respuesta
        self._send(TOPIC_RESP, Resp,
                   dataResponse['metadata']['id_transaction'])

    def ___getErrorId(self, id_error):
        """
            Metodo apra recuperar los datos de un error registrado
        """
        try:
            if self.__ERRORS.get(str(id_error), None):
                return self.__ERRORS.get(str(id_error))
            else:
                return self.__ERRORS.get('-99')
        except:
            self.logs.error(
                'Ocurrio un excepcion al recuperar los datos del error')
            return 'Ocurrio un error generico'

    def __getListener(self):
        """
            Metodo para recuperar la accion registrada
            en el Listener, de no contar con dicha accion
            se lanza una excepcion.
        """
        if self.__ACTIONS.get(TypesActions.LISTENER, None):
            return self.__caller(self.__ACTIONS.get(TypesActions.LISTENER))
        else:
            raise Exception('No existe un metodo para el evento solicitado')

    def __getMethod(self, meta):
        """
            Metodo para recuperar el metodo que se
            ejecutara, segun los datos pasados en
            el metada.
        """
        if meta.get('method', None) and (meta.get('uuid', None) and len(meta.get('uuid', '')) > 0):
            if meta.get('method', None) == 'GET':  # Consultar un elemento
                return self.__caller(self.__ACTIONS.get(TypesActions.GET))
            elif meta.get('method', None) == 'DELETE':  # Eliminar el elemento
                return self.__caller(self.__ACTIONS.get(TypesActions.DELETE))
            elif meta.get('method', None) == 'PUT':  # Actualizar el elemento
                return self.__caller(self.__ACTIONS.get(TypesActions.UPDATE))
        elif meta.get('method', None) == 'GET':  # Lista de servicios
            if self.__ACTIONS.get(TypesActions.LIST, None):
                return self.__caller(self.__ACTIONS.get(TypesActions.LIST))

        elif meta.get('method') == 'POST':  # Creacion de un nuevo elemento
            if self.__ACTIONS.get(TypesActions.CREATE, None):
                return self.__caller(self.__ACTIONS.get(TypesActions.CREATE))

        # Regresar el Listener por default
        return self.__getListener()

    def __initActions(self):
        """
            Metodo que se encarga de recuperar todas las
            acciones registradas, para su implementacion
            durante su llamado.
        """
        for f in inspect.getmembers(self):
            # Validar que tenga el atributo minimo
            if hasattr(f[1], '__MICROSERVICE_ACTION__'):
                # Recuperar el tipo de accion
                typeAction = getattr(f[1], '__TYPE__')
                # Validar si es el de errores
                if typeAction == TypesActions.ERRORS:
                    # Recuperar la funcion para ejecutarla
                    errorFNC = self.__caller(f[0])
                    # Ejecutar la funcion para recuperar los errores definidos
                    errores_definidos = errorFNC()
                    # Validar que sea el tipo correcto
                    if not isinstance(errores_definidos, dict):
                        self.logs.error(
                            'No se proporciono un formato correcto para los errores definidos')
                        sys.exit(-1)
                    # Ejecutar y asignar los errores
                    self.__ERRORS = self.__merge_dicts(
                        self.__ERRORS, errores_definidos)
                elif typeAction == TypesActions.FORKS:
                    # Recuperar la funcion para ejecutarla
                    forksFNC = self.__caller(f[0])
                    # Ejecutar la funcion para recuperar la configuracion
                    forks_conf = forksFNC()
                    # Validar que sea el tipo correcto
                    if not isinstance(forks_conf, dict):
                        self.logs.error(
                            'No se proporciono un formato correcto para los Forks definidos')
                        sys.exit(-1)
                    # Validar que cuente con el forma correcto
                    valid, error = validForksConf(forks_conf)
                    if valid:
                        self.__FORKS = forks_conf
                    else:
                        self.logs.error(error)
                        sys.exit(-1)
                else:
                    # Almacenar la accion
                    self.__ACTIONS.update({typeAction: f[0]})

    def __caller(self, name):
        """
            Metodo para recuperar una propiedad que sera utilizada
            como metodo
        """
        if hasattr(self, name):
            return getattr(self, name)

    @abstractmethod
    def smoketest(self):
        """
            Metodo que es llamado para validar los
            servicios desde su consumo por REST/Kafka
        """
        pass

    def __merge_dicts(self, *dict_args):
        """
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in latter dicts.
        """
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result

    def __getConfServiceFork(self, conf):
        """
            Metodo para iniciar la configuracion de los Forks a ejecutar
        """
        forks = []

        # Recorrer las configuraciones
        for item in conf:
            # Verificar que existe en las configuraciones
            if self.__FORKS.get(item.get('fork'), None) is None:
                self.logs.error(
                    'No se encuentra configurado el Fork {}'.format(item.get('fork')))
                raise Exception(
                    'No se encuentra configurado el Fork {}'.format(item.get('fork')))

            # Actualizar el item con la configuracion inicial
            item.update({"conf": self.__FORKS.get(item.get('fork', ''), None)})

            # Validar si es necesario recuperar una funcion
            if not item.get('fnc', None) is None:
                item.update({'fnc_call': self.__caller(item.get('fnc'))})

            # Agregar a la coleccion
            forks.append(item)

        # Regresar la coleccion
        return forks
