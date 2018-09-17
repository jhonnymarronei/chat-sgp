# -*- coding: utf-8 -*-

import re
import requests
import json
import sys


class WebService:

    def __init__(self):
        self.TOKEN = 'TOKEN_AQUI'
        self.APP = 'whatsapp'
        self.WS_HOST = 'http://10.10.10.10:8000'
        self.WS_PATH = '/ws/ura/verificaacesso/'
        self.WS_URL = '%s%s' %(self.WS_HOST,self.WS_PATH)

    def updatews(self,data_json):
        if data_json.get('TOKEN'):
            self.TOKEN = data_json.get('TOKEN')
        if data_json.get('APP'):
            self.APP = data_json.get('APP')
        if data_json.get('WS_URL'):
            self.WS_URL = data_json.get('WS_URL')
        if data_json.get('WS_HOST'):
            self.WS_URL = '%s%s' %(data_json.get('WS_HOST'),self.WS_PATH)

    def run(self, q, **kwargs):

        reload(sys)
        sys.setdefaultencoding('utf-8')

        query = re.sub('[^0-9 ]', '', ' '.join(q.strip().split()))

        if query:
            datareq = {}
            data_json = {}
            try:
                data = kwargs.get('data')
                data_json = json.loads(data)
            except:
                pass
            if data_json:
                datareq['cpfcnpj'] = data_json.get('cpfCnpj')
                datareq['contrato'] = data_json.get('contratoId')
                resposta = ''

                self.updatews(data_json)
                datareq['token'] = self.TOKEN
                datareq['app'] = self.APP

                r = requests.post(self.WS_URL, data=datareq)
                rws = r.json()
                if rws.get('msg'):
                    if rws.get('status') == 1:
                        resposta = 'Detectamos seu equipamento conectado no nosso concentrador. \
Favor desligue e ligue o equipamento e verifique se o acesso encontra-se normalizado. \
Caso problema ainda persista, favor selecionar a opção abertura de chamado.'

                    elif rws.get('status') == 2:
                        resposta = 'Não detectamos seu equipamento conexão no nosso concentrador.'

                    elif rws.get('status') == 9:

                        resposta = 'No momento sua região encontra-se em manutenção.'
                        if rws.get('tempo'):
                            resposta += 'Prazo para normalização é %s' % rws.get(
                                'tempo')

                    if rws.get('protocolo'):
                        resposta += '\nChamado aberto com sucesso. Protocolo: %s' % (
                            rws.get('protocolo'))
                    else:
                        resposta += rws.get('msg')
                return {'message': resposta}
            else:
                return {'message': 'Erro no processamento. Favor identifique-se novamente digitando a opção #ajuda'}
