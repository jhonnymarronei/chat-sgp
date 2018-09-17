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
        self.WS_PATH = '/ws/ura/consultacliente/'
        self.WS_URL = '%s%s' %(self.WS_HOST,self.WS_PATH)

    def responseContrato(self,rws,**kwargs):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        response = {}
        response['contratoId'] = str(rws.get('contratoId'))
        response['razaoSocial'] = str(rws.get('razaoSocial'))
        response['cpfCnpj'] = str(rws.get('cpfCnpj'))
        response['contratoStatus'] = str(rws.get('contratoStatus'))
        response['contratoStatusDisplay'] = str(rws.get('contratoStatusDisplay'))
        response['contratoStatusModo'] = str(rws.get('contratoStatusModo'))
        response['message'] = u'Olá %s, seja bem-vindo ao autoatendimento. Seguem as opções.' %response['razaoSocial']
        response['customer'] = response['razaoSocial']
        response['doc'] = response['cpfCnpj']

        if kwargs.get('next_ws'):
            response['TOKEN'] = self.TOKEN
            response['WS_HOST'] = self.WS_HOST
            response['APP'] = self.APP

        return response

    def run(self,q,**kwargs):

        query = re.sub('[^0-9 ]','',' '.join(q.strip().split()))

        if query:
            datareq={}
            datareq['token'] = self.TOKEN
            datareq['app'] = self.APP
            try:
                datareq['cpfcnpj'] = query.split()[0]
            except:
                datareq['cpfcnpj'] = ''

            r = requests.post(self.WS_URL,data=datareq)
            rws = r.json()
            contrato = None
            if rws.get('contratos'):
                if len(rws.get('contratos')) == 1:
                    return self.responseContrato(rws.get('contratos')[0])
                else:
                    if len(query.split()) > 1:
                        for c1 in rws.get('contratos'):
                            if query.split()[1].strip() == str(c1.get('contratoId')):
                                return self.responseContrato(c1,**kwargs)

                    mensagem = u"Olá %s, verificamos que há mais de 1 contrato." %(rws.get('contratos')[0].get('razaoSocial'))
                    for c1 in rws.get('contratos'):
                        mensagem += "\n Digite %s %s para selecionar contrato %s" %(query.split()[0],c1.get('contratoId'),c1.get('contratoId'))
                    return {'message': mensagem}
            else:
                # descomentar abaixo se quiser consultar outros sistemas caso nao encontre o cliente
                #if not kwargs.get('next_ws'):
                #    # consultar outra empresa 
                #    self.TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxx'
                #    self.WS_HOST = 'http://XXX.XXX.XXX.XXX:8000'
                #    kwargs['next_ws'] = True
                #    return self.run(q,**kwargs)
                return {'message': 'Não localizamos o cliente com as informações informadas'}

        return {'message': 'Digite CPF/CNPJ do Assinante'}
