from zeep import Client
from zeep.transports import Transport
from requests import Session
from requests.auth import HTTPBasicAuth

class AuthSoapClient(Client):
    def __init__(self, wsdl: str, username: str, password: str, plugins: list = []):
        """
        Inicializa o cliente SOAP autenticado usando Zeep.

        :param wsdl: URL do WSDL da API SOAP.
        :param username: Nome de usuário para autenticação.
        :param password: Senha para autenticação.
        :param plugins: Lista de plugins Zeep a serem usados (opcional).
        """
        session = Session()
        session.auth = HTTPBasicAuth(username, password)

        transportWithAuth = Transport(session=session)

        maxRetries = 3
        attempt = 0
        while attempt < maxRetries:
            try:
                super().__init__(wsdl=wsdl, transport=transportWithAuth, plugins=plugins)
                break  # Se a inicialização for bem-sucedida, sai do loop
            except Exception as e:
                print(f"Error initializing AuthSoapClient: {e}")
                attempt += 1
                if attempt < maxRetries:
                    print(f"Retrying... (Attempt {attempt + 1}/{maxRetries})")