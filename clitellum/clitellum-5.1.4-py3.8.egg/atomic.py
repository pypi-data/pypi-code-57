import json
from clitellum.channels.channel import Channel, ChannelConfiguration
from clitellum import logger_manager
from clitellum.channels.amqp import AmqpMessage, AmqpMessageProperties


class Quark:

  def __init__(self, headers, routing_key):
    self._headers = headers
    self._message = ''
    self._routing_key = routing_key
    self._encoding = 'utf-8'

  def get_headers(self):
    return self._headers

  def get_routing_key(self):
    return self._routing_key

  def set_encoding(self, encoding):
    self._encoding = encoding

  def get_encoding(self):
    return self._encoding

  def get_bytes(self):
    return bytes(self._message, self._encoding)

  def set_message(self, message: bytes, encoding="utf-8"):
    self._message = message
    self._encoding = encoding

  def get_message(self):
    return str(self._message, encoding=self._encoding)


class QuarkCreator():

  @classmethod
  def create_empty(cls, headers: dict, routing_key: str) -> Quark:
    q = Quark(headers, routing_key)
    return q

  @classmethod
  def create_from_str(cls, headers: dict, routing_key: str, message: str, encoding: str = 'utf-8') -> Quark:
    q = Quark(headers, routing_key)
    b = bytes(message, encoding=encoding)
    q.set_message(message=message, encoding=encoding)
    return q

  @classmethod
  def create_from_bytes(cls, headers: dict, routing_key: str, message: bytes, encoding: str = 'utf-8') -> Quark:
    q = Quark(headers, routing_key)
    q.set_message(message=message, encoding=encoding)
    return q


class Router:

  def __init__(self):
    self._router = dict()

  def add_route(self, routing_key: str, handler_func):
    self._router[routing_key] = handler_func

  def get_handler(self, routing_key):
    if routing_key in self._router:
      return self._router[routing_key]

    return None

  def get_keys(self):
    return self._router.keys()


class Accelerator:

  def publish(self, quark: Quark):
    pass


class Particle(Accelerator):

  def __init__(self, name: str, sender: Channel, receiver: Channel, router: Router):
    self._sender = sender
    self._receiver = receiver
    self._receiver.on_message_received = self._on_message_received
    self._name = name
    self._router = router

  def get_router(self) -> Router:
    return self._router

  def get_name(self) -> str:
    return self._name

  def connect(self):
    logger_manager.get_logger().debug("Particle %s - Realizando conexion", self._name)

    for key in self._router.get_keys():
      self._receiver.add_binding(key)

    self._sender.connect()
    self._receiver.connect()

  def disconnect(self):
    self._receiver.close()
    self._sender.close()

  def run(self):
    logger_manager.get_logger().debug("Particle %s - Iniciando Runner", self._name)
    self._receiver.consume()

  def stop(self):
    logger_manager.get_logger().debug("Particle %s - Stop Runner", self._name)
    self._receiver.stop_consuming()

  def publish(self, quark: Quark):
    logger_manager.get_logger().debug("Service - Publicando Mensaje")

    properties = AmqpMessageProperties.create()
    properties.headers = quark.get_headers()
    encoding = quark.get_encoding()

    self._channel.publish(quark.get_bytes(), quark.get_routing_key(), properties)

  def _on_message_received(self, message: AmqpMessage):
    try:
      logger_manager.get_logger().debug("Service - Received Message")
      encoding = message.properties.content_encoding \
          if message.properties.content_encoding is not None else 'utf-8'

      handler_func = self._router.get_handler(message.frame.routing_key)

      if handler_func is not None:
        quark = QuarkCreator.create_from_bytes(message.properties.headers, message.routing_key, message.body, encoding)
        err = handler_func(quark, self)
        if err is not None and err > 0:
          self._send_error_code(message, err)

    except Exception as exception:
      logger_manager.get_logger().error("Service - Error al procesar el mensaje", exception)
      self._send_error(message.body, exception)
    finally:
      self._receiver.ack(message)

  def _send_error(self, message: bytes, exception: Exception):
    message_error = dict()
    message_error['description'] = str(exception)
    message_error['message'] = message
    str_error = json.dumps(message_error)
    self._sender.publish(bytes(str_error, 'utf-8'), 'Message.Error', AmqpMessageProperties.create())

  def _send_error_code(self, message: bytes, err_code: int):
    message_error = dict()
    message_error['description'] = "Error Code: %d" % err_code
    message_error['message'] = message
    str_error = json.dumps(message_error)
    self._sender.publish(bytes(str_error, 'utf-8'), 'Message.Error', AmqpMessageProperties.create())


class Atom:

  def __init__(self, name: str):
    self._particles = list()
    self._name = name

  def add_particle(self, particle: Particle):
    self._particles.append(particle)

  def run(self):
    for particle in self._particles:
      particle.connect()
      particle.run()

  def stop(self):
    for particle in self._particles:
      particle.stop()
      particle.disconnect()

  def get_router(self, particle_name: str) -> Router:
    for particle in self._particles:
      if particle.get_name() == particle_name:
        return particle.get_router()
    return None

  def add_route(self, particle, routing_key, handler_func):
    self.get_router(particle).add_route(routing_key, handler_func)


def create_atom(name: str, particles: list, amqp_uri: str, output: str, prefix: str = None) -> Atom:
  atom = Atom(name)
  for particle in particles:
    ch_sender_config = ChannelConfiguration()
    ch_sender_config.uri = amqp_uri
    ch_sender_config.exchange.name = output

    ch_receiver_config = ChannelConfiguration()
    ch_receiver_config.uri = amqp_uri
    if prefix is not None:
      ch_receiver_config.exchange.name = "%s.%s" % (prefix, name)
      ch_receiver_config.queue.name = str.format("%s.%s.%s", prefix, name, particle)
    else:
      ch_receiver_config.exchange.name = name
      ch_receiver_config.queue.name = "%s.%s" % (name, particle)

    sender = Channel.create(ch_sender_config)
    receiver = Channel.create(ch_receiver_config)
    router = Router()
    part_obj = Particle(particle, sender, receiver, router)
    atom.add_particle(part_obj)
  return atom
