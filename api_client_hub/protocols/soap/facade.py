from zeep import Client
from .client import AuthSoapClient

import re

class SoapApiFacade:
    def __init__(self, client: Client):
        """
        Classe para operar com um cliente SOAP.

        :param client: Instância do cliente SOAP.
        """
        self.client = client

    def getAllClientOperations(self) -> dict:
        """
        Retorna todas as operações disponíveis no cliente SOAP.

        :return: Dicionário com os nomes das operações disponíveis e seus detalhes.
        """

        try:
            operations = {}

            targetNamespace = self.client.namespaces.get('ns0', '') # Obtém o namespace padrão

            operationsDict = list(self.client.wsdl.bindings.values())[0]._operations # Obtém o dicionário de operações

            for opName, opObject in operationsDict.items():
                inputSignatureStr = (opObject.input.body.type._element.signature()) # Obtém a assinatura de entrada

                match = re.search(r'(\w+): {.*?}(\w+)', inputSignatureStr) # Extrai o nome do tipo complexo dos parâmetros de entrada

                formattedParams = {}

                if match:
                    paramTypeName = match.group(2)

                    paramTypeQname = f'{{{targetNamespace}}}{paramTypeName}' # Cria o QName completo do tipo complexo
                    paramDefinition = self.client.get_type(paramTypeQname) # Obtém a definição do tipo complexo
                    
                    if hasattr(paramDefinition, 'elements'):
                        for fieldName, fieldElement in paramDefinition.elements:
                            typeName = fieldElement.type.name
                            formattedParams.update(
                                {fieldName: typeName}
                            )

                else:
                    formattedParams = ['Parâmetros não encontrados']

                outputSignatureStr = opObject.output.body.type._element.signature()
                match = re.search(r'{.*?}(\w+)', outputSignatureStr)
                returnType = match.group(1) if match else 'void'

                operations.update({
                    opName: {
                        'parameters': formattedParams,
                        'returnType': returnType
                    }
                })

            return operations
        except Exception as e:
            raise ValueError(f"Erro ao listar as operações do cliente SOAP: {e}")

    def runClientOperation(self, operationName: str, parameters: dict) -> any:
        """
        Executa uma operação específica no cliente SOAP com os parâmetros fornecidos,
        criando o objeto de parâmetro complexo quando necessário.

        :param operationName: Nome da operação a ser executada.
        :param parameters: Dicionário de parâmetros para a operação.
        :return: Resultado da operação.
        """

        try:
            operation = getattr(self.client.service, operationName) # Obtém a operação do cliente SOAP

            result = operation(parameters) # Executa a operação com os parâmetros fornecidos

            return result
        except Exception as e:
            raise ValueError(f"Erro ao executar a operação '{operationName}': {e}")
        
    @staticmethod
    def createClient(wsdlUrl: str, username: str = None, password: str = None, plugins: list = None) -> 'SoapApiFacade':
        """
        Método de fábrica para criar uma instância do cliente SOAP com autenticação opcional.

        :param wsdlUrl: URL do WSDL do serviço SOAP.
        :param username: Nome de usuário para autenticação (opcional).
        :param password: Senha para autenticação (opcional).
        :param plugins: Lista de plugins para o cliente SOAP (opcional).
        :return: Instância do cliente SOAP.
        """

        try:
            client = (
                AuthSoapClient(
                    wsdl=wsdlUrl, 
                    username=username, 
                    password=password, 
                    plugins=plugins
                ) 

                if username and password 
                else 

                Client(
                    wsdl=wsdlUrl, 
                    plugins=plugins
                )
            )
            return SoapApiFacade(client)
        except Exception as e:
            raise ValueError(f"Erro ao criar o cliente SOAP: {e}")
