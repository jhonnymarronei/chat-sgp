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
        self.WS_PATH = '/ws/ura/liberacaopromessa/'
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

            if rws.get('liberado') == 1:
                return {'redirect_menu': True, 
                         'message': u'Acesso liberado com sucesso. Protocolo gerado: %s. Em alguns minutos a conexão estará normalizada. Caso não normalize o acesso em 5 minutos, favor desligar e ligar o equipamento.' %rws.get('protocolo')}
            else:
                return {'redirect_menu':True,
                        'message': rws.get('msg') or u'Erro Interno, tente novamente posteriormente.'}
        else:
            return {'message': u'Erro no processamento. Favor identifique-se novamente digitando a opção #ajuda'}
