import requests


class TorpedoClient:
    """Cliente HTTP para comunicação com Torpedo

    :param str torpedo_url: Endereço da API do serviço Torpedo
    :param str client_name: Nome do cliente requisitando o envio do email,
        esse parâmetro será usado em conjunto com o ``template_name`` para encontrar o template do email
    """

    def __init__(self, torpedo_url, client_name):

        self.torpedo_url = torpedo_url
        self.client_name = client_name

    def send_email(self, email, subject, template_name, data=None):
        """Envia email com um template pré-definido do Torpedo através da API do `Mailgun <https://www.mailgun.com/>`_.

        Exemplo:

        .. code-block:: python

            from stl_sdk.torpedo import TorpedoClient

            client = TorpedoClient('https://notifications.spacetimeanalytics.com', 'waves')
            response = client.send_email('pedro@gmail.com', 'Bem-vindo!', 'welcome', { 'name': 'Pedro' })

        :param email: Email do destinatário
        :type email: str
        :param subject: Assunto do email
        :type subject: str
        :param template_name: Nome do template do Torpedo
            (`Veja os templates disponíveis <http://notifications.spacetimeanalytics.com>`_).
        :type template_name: str
        :param data: Dicionário de dados para popular o email
        :type data: dict, optional
        :return: Resposta da requisição para o Mailgun
        :rtype: requests.Response
        """
        response = requests.post(
                '{}/api/send-email'.format(self.torpedo_url),
                json={
                    'to_email': email,
                    'subject': subject,
                    'template_name': template_name,
                    'data': data,
                    'client': self.client_name,
                }
            )
        response.raise_for_status()
        return response
