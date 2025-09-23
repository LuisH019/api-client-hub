from zeep import Plugin
import re

class ZeepDateFixer(Plugin):
    def ingress(self, envelope: str, http_headers: dict, operation: str) -> tuple[str, dict]:
        """
        Converte datas no formato DD/MM/YYYY para YYYY-MM-DD no envelope da mensagem SOAP.

        :param envelope: O envelope XML da mensagem SOAP.
        :param http_headers: Os cabeçalhos HTTP da mensagem.
        :param operation: A operação SOAP sendo processada.
        :return: O envelope e os cabeçalhos HTTP possivelmente modificados.
        """
        for elem in envelope.iter():
            if elem.text and re.match(r"\d{2}/\d{2}/\d{4}", elem.text):
                d, m, y = elem.text.split("/")
                elem.text = f"{y}-{m}-{d}"
        return envelope, http_headers