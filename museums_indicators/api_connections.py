import requests, json
from datetime import datetime
from datetime import timedelta

class RequestMuseumRawData(object):
    def __init__(self, last_update_time):
        self._get_time = last_update_time
        self._url = 'http://museus.cultura.gov.br/api/space/find/'
        self._filters = {'@select' : 'mus_tipo, mus_tipo_tematica, En_Estado, esfera, mus_servicos_visitaGuiada, mus_arquivo_acessoPublico', 'createTimestamp' : "GT("+self._get_time.__str__()+")"}
        self._response = requests.get(self._url, self._filters)
        self._data = json.loads(self._response.text)

    @property
    def response(self):
        return self._response

    @property
    def data(self):
        return self._data

    @property
    def data_length(self):
        return len(self._data)

'''
#Código para testar o funcionamento da classe.
get_time = datetime.now() - timedelta(days=50)
museu = RequestMuseumRawData(get_time)
print(museu.data[5])
print(museu.data_length)
'''
