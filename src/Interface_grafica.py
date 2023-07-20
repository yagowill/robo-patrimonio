import PySimpleGUI as sg
from src.Robo import Robo


class Interface_grafica:
    def __init__(self):
        self.rps_value = []
        self.listbox = sg.Listbox(values=[''], size=(75,20), enable_events=True, select_mode='extended', k='-LIST-')
        self.orgaos = [
            'Todos',
            '10º CRS - 10º CENTRO REGIONAL DE SAÚDE - ALTAMIRA',
            '11º CRS - 11º CENTRO REGIONAL DE SAÚDE - MARABÁ',
            '12º CRS - 12º CENTRO REGIONAL DE SAÚDE - CONCEIÇÃO DO ARAGUAIA',
            '13º CRS - 13º CENTRO REGIONAL DE SAÚDE - CAMETÁ',
            '1º CRS - 1º CENTRO REGIONAL DE SAÚDE - BELÉM',
            '2º CRS - 2º CENTRO REGIONAL DE SAÚDE - SANTA IZABEL DO PARÁ',
            '3º CRS - 3º CENTRO REGIONAL DE SAÚDE - CASTANHAL',
            '4º CRS - 4º CENTRO REGIONAL DE SAÚDE - CAPANEMA',
            '5º CRS - 5º CENTRO REGIONAL DE SAÚDE - SÃO MIGUEL DO GUAMÁ',
            '6º CRS - 6º CENTRO REGIONAL DE SAÚDE - BARCARENA',
            '7º CRS - 7º CENTRO REGIONAL DE SAÚDE - MARAJÓ',
            '8º CRS - 8º CENTRO REGIONAL DE SAÚDE - BREVES',
            '9º CRS - 9º CENTRO REGIONAL DE SAÚDE - SANTARÉM',
            'ADEPARA - AGÊNCIA DE DEFESA AGROPECUÁRIA DO ESTADO DO PARÁ',
            'AGE - AUDITORIA GERAL DO ESTADO',
            'AGTRAN - AGENCIA DE TRANSPORTE METROPOLITANO',
            'ARCON - AGÊNCIA ESTADUAL DE REGULAÇÃO  E CONTROLE DE SERVIÇOS PÚBLICOS DO ESTADO',
            'ASIPAG - AÇÃO SOCIAL INTEGRADA DO PALÁCIO DO GOVERNO',
            'CAF/NDB - CAF/NDB',
            'CBM - CORPO DE BOMBEIROS MILITAR DO PARÁ',
            'CC - CASA CIVIL',
            'CEASA - CENTRAIS DE ABASTECIMENTO DO PARA S.A.',
            'CGE - CONSULTORIA GERAL DO ESTADO',
            'CIIR-INDSH - CENTRO INTEGRADO DE INCLUSÃO E REABILITAÇÃO - CIIR/INDSH',
            'CM - CASA MILITAR',
            'CODEC - COMPANHIA DE DESENVOLVIMENTO ECONÔMICO DO PARÁ',
            'COHAB - COMPANHIA DE HABITAÇÃO DO ESTADO DO PARÁ',
            'COSANPA - COMPANHIA DE SANEAMENTO DO PARÁ',
            'CPH - COMPANHIA DE PORTOS E HIDROVIAS DO ESTADO DO PARÁ',
            'DEFPUB - DEFENSORIA PUBLICA DO ESTADO DO PARÁ',
            'DETRAN - DEPARTAMENTO DE TRÂNSITO DO ESTADO DO PARÁ',
            'EGPA - ESCOLA DE GOVERNANÇA PÚBLICA DO ESTADO DO PARÁ',
            'EMATER - EMPRESA DE ASSISTÊNCIA TÉCNICA E EXTENSÃO RURAL DO ESTADO DO PARÁ',
            'ETSUS - ESCOLA TÉCNICA DO SUS DO PARÁ "DR.MANUEL AYRES"',
            'FAPESPA - FUNDAÇÃO AMAZÔNIA DE AMPARO A ESTUDOS E PESQUISAS',
            'FASEPA - FUNDAÇÃO DE ATENDIMENTO SOCIOEDUCATIVO DO PARÁ',
            'FASPM - FUNDO DE ASSISTÊNCIA SOCIAL DA POLÍCIA MILITAR',
            'FCA - FUNDO DE COMPENSAÇÃO AMBIENTAL DO ESTADO DO PARÁ',
            'FCG - FUNDAÇÃO CARLOS GOMES',
            'FCP - FUNDAÇÃO CULTURAL DO PARÁ',
            'FCV - FUNDAÇÃO CURRO VELHO',
            'FEAS - FUNDO ESTADUAL DE ASSISTÊNCIA SOCIAL',
            'FEBOM - FUNDO ESPECIAL DOS BOMBEIROS',
            'FEDD - FUNDO ESTADUAL DE DIREITOS DIFUSOS',
            'FEMA - FUNDO ESTADUAL DO MEIO AMBIENTE',
            'FESPDS - FUNDO ESTADUAL DE SEGURANÇA PUBLICA E DEFESA SOCIAL DO ESTADO DO PARA',
            'FHCGV - FUNDAÇÃO PÚBLICA ESTADUAL HOSPITAL DE CLÍNICAS GASPAR VIANA',
            'FIPAT - FUNDO DE INVESTIMENTO PERMANENTE DA ADMINISTRAÇÃO TRIBUTÁRIA DO ESTADO DO PARÁ',
            'FISP - FUNDO DE INVESTIMENTO EM SEGURANÇA PÚBLICA',
            'FSCMP - FUNDAÇÃO SANTA CASA DE MISERICÓRDIA DO PARÁ',
            'FUNDEFLOR - FUNDO ESTADUAL DE DESENVOLVIMENTO FLORESTAL',
            'FUNPGE - FUNDO DA PROCURADORIA GERAL DO ESTADO',
            'FUNSAU - FUNDO DE SAUDE DOS SERVIDORES MILITARES',
            'FUNTELPA - FUNDAÇÃO PARAENSE DE RADIODIFUSÃO',
            'GESTOR - Diretoria de Gestao de Patrimonio do Estado',
            'HEMOPA - FUNDAÇÃO CENTRO DE HEMOTERAPIA E HEMATOLOGIA DO PARÁ',
            'HGI-IPIXUNA - HOSPITAL GERAL DE IPIXUNA',
            'HGPCS-ALTAMIRA - HOSPITAL GERAL PUBLICO CASTELO DOS SONHOS',
            'HGT - TAILANDIA - HOSPITAL GERAL DE TAILANDIA',
            'HJB - JEAN BITAR - HOSPITAL JEAN BITAR',
            'HMIB - BARCARENA - HOSPITAL MATERNO INFANTIL DE BARCARENA DRA.ANNA TURAN',
            'HMUE - ANANINDEUA - HOSPITAL METROPOLITANO DE URGENCIA E EMERGENCIA',
            'HOIOL - OCTAVIO LOBO - HOSPITAL ONCOLOGICO INFANTIL OCTAVIO LOBO',
            'HOL - OPHIR LOIOLA - HOSPITAL OPHIR LOYOLA',
            'HPEG - GALILEU - HOSPITAL PUBLICO ESTADUAL GALILEU',
            'HRAS- ABELARDO SANTOS - HOSPITAL REGIONAL ABELARDO SANTOS',
            'HRBA - SANTARÉM - HOSPITAL REGIONAL DO BAIXO AMAZONAS - SANTARÉM',
            'HRCA - CONCEIÇÃO - HOSPITAL REGIONAL DE CONCEIÇÃO DO ARAGUAIA',
            'HRC - CAMETÁ - HOSPITAL REGIONAL DE CAMETÁ',
            'HRPA-REDENÇÃO - HOSPITAL REGIONAL PUBLICO ARAGUAIA',
            'HRPC - CAETES - CAPANEMA - HOSPITAL PÚBLICO REGIONAL DOS CAETES',
            'HRPC - CASTANHAL - HOSPITAL REGIONAL PUBLICO DE CASTANHAL',
            'HRPL-PARAGOMINAS - HOSPITAL REGIONAL PUBLICO DO LESTE',
            'HRPM - BREVES - HOSPITAL REGIONAL PUBLICO DO MARAJO',
            'HRPT - ALTAMIRA - HOSPITAL REGIONAL PÚBLICO DA TRANSAMAZONICA',
            'HRPT-ITAITUBA - HOSPITAL REGIONAL PUBLICO DO TAPAJOS - ITAITUBA',
            'HRSP - MARABA - HOSPITAL REGIONAL DO SUDESTE DO PARA - DR. GERALDO VELOSO',
            'HRS - SALINAS - HOSPITAL REGIONAL DE SALINÓPOLIS',
            'HRT - TUCURUÍ - HOSPITAL REGIONAL DE TUCURUÍ',
            'HSR-ABAETETUBA - HOSPITAL SANTA ROSA',
            'IAP - INSTITUTO DE ARTES DO PARÁ',
            'IASEP - INSTITUTO DE ASSISTÊNCIA DOS SERVIDORES DO ESTADO DO PARÁ',
            'IDEFLOR-BIO - INSTITUTO DE DESENVOLVIMENTO FLORESTAL E DA BIODIVERSIDADE DO ESTADO DO PARÁ',
            'IDESP - INSTITUTO DE DESENVOLVIMENTO ECONÔMICO, SOCIAL E AMBIENTAL DO PARÁ',
            'IGEPREV - INSTITUTO DE GESTAO PREVIDENCIÁRIA DO ESTADO DO PARÁ',
            'IMETROPARÁ - INSTITUTO DE METROLOGIA DO ESTADO DO PARA',
            'IOE - IMPRENSA OFICIAL DO ESTADO',
            'ITERPA - INSTITUTO DE TERRAS DO PARÁ',
            'JUCEPA - JUNTA COMERCIAL DO ESTADO DO PARA',
            'LACEN - LABORATÓRIO CENTRAL',
            'LOTERPA - LOTERIA DO ESTADO DO PARÁ',
            'NAC - NÚCLEO DE ARTICULAÇÃO E CIDADANIA',
            'NAF - NÚCLEO ADMINISTRATIVO E FINANCEIRO',
            'NEPMV - NÚCLEO EXECUTOR DO PROGRAMA MUNÍCIPIOS VERDES',
            'NEPMV - FA - NÚCLEO EXECUTOR DO PROGRAMA MUNICÍPIOS VERDES - FUNDO AMAZÔNIA',
            'NGPM-CREDCIDADÃO - NÚCLEO DE GERENCIAMENTO DO PROGRAMA DE MICROCRÉDITO-CREDCIDADÃO',
            'NGPR - NÚCLEO DE GERENCIAMENTO DO PARÁ RURAL',
            'NGTM - NÚCLEO DE GERENCIAMENTO DE TRANSPORTE METROPOLITANO',
            'PARAPAZ - FUNDAÇÃO PARAPAZ',
            'PARATUR - COMPANHIA PARAENSE DE TURISMO',
            'PCEPA - POLICIA CIENTÍFICA DO PARÁ ',
            'PGE - PROCURADORIA GERAL DO ESTADO',
            'PM-PA - POLÍCIA MILITAR DO PARÁ',
            'PNAGE - PNAGE',
            'POLICLINICA DE TUCURUI - ISSAA-INSTITUTO DE SAUDE SOCIAL E AMBIENTAL DA AMAZONIA',
            'POLIM -  POLICLINICA  METROPOLITANA',
            'POLITUCU - TUCURUI - POLICLINICA DE TUCURUI',
            'PRODEPA - EMPRESA DE TECNOLOGIA DA INFORMAÇÃO E COMUNICAÇÃO DO ESTADO DO PARÁ',
            'PROFISCO II - PROFISCO II',
            'PROGEFAZ - PROGRAMA DE APOIO À MODERNIZAÇÃO E À TRANSPARÊNCIA DA GESTÃO FISCAL DO ESTADO DO PARÁ',
            'SEAC - SECRETARIA ESTRATEGICA DE ESTADO DE  ARTICULAÇÃO DA CIDADANIA',
            'SEAD - SECRETARIA DE ESTADO DE ADMINISTRAÇÃO',
            'SEAP - SECRETARIA DE ESTADO DE ADMINISTRAÇÃO PENITENCIÁRIA',
            'SEASTER - SECRETARIA DE ESTADO DE ASSISTÊNCIA SOCIAL, TRABALHO, EMPREGO E RENDA',
            'SECIR - SECRETARIA DE ESTADO DAS CIDADES E INTEGRAÇÃO REGIONAL',
            'SECOM - SECRETARIA DE ESTADO DE COMUNICAÇÃO',
            'SECTET - SECRETARIA DE ESTADO DE CIÊNCIA, TECNOLOGIA E EDUCAÇÃO TÉCNICA E TECNOLÓGICA',
            'SECULT - SECRETARIA DE ESTADO DE CULTURA',
            'SEDAP - SECRETARIA DE ESTADO DE DESENVOLVIMENTO AGROPECUÁRIO E DA PESCA',
            'SEDEME - SECRETARIA DE ESTADO DE DESENVOLVIMENTO ECONÔMICO, MINERAÇÃO E ENERGIA',
            'SEDUC - SECRETARIA DE ESTADO DE EDUCAÇÃO',
            'SEEL - SECRETARIA DE ESTADO DE ESPORTE E LAZER',
            'SEFA - SECRETARIA DE ESTADO DA FAZENDA',
            'SEGUP - SECRETARIA DE ESTADO DE SEGURANÇA PÚBLICA E DEFESA SOCIAL',
            'SEIRDH - SECRETARIA DE IGUALDADE RACIAL E DIREITOS HUMANOS',
            'SEJU - SECRETARIA DE ESTADO DE JUSTIÇA',
            'SEMAS - SECRETARIA DE ESTADO DE MEIO AMBIENTE E SUSTENTABILIDADE',
            'SEMU - SECRETARIA DE ESTADO DAS MULHERES',
            'SEOP - SECRETARIA DE ESTADO DE OBRAS PÚBLICAS',
            'SEPAQ - SECRETARIA DE ESTADO DE PESCA E AQUICULTURA',
            'SEPLAD - SECRETARIA DE ESTADO DE PLANEJAMENTO E ADMINISTRAÇÃO',
            'SEPLAN - SECRETARIA DE ESTADO DE PLANEJAMENTO',
            'SESPA - SECRETARIA DE ESTADO DE SAÚDE PUBLICA',
            'SETER - SECRETARIA DE ESTADO DE TRABALHO, EMPREGO E RENDA',
            'SETRAN - SECRETARIA DE ESTADO DE TRANSPORTE',
            'SETUR - SECRETARIA DE ESTADO DE TURISMO',
            'TCE - TRIBUNAL DE CONTAS DO ESTADO DO PARÁ',
            'UEPA - UNIVERSIDADE DO ESTADO DO PARÁ',
            'UMS-SÃO CAETANO DE ODIVELAS - UNIDADE MISTA DE SAUDE DE SÃO CAETANO DE ODIVELAS',
            'VICEGOV - VICE GOVERNADORIA'
        ]

    def janela(self):
        layout = []
        receber = []
        
        layout.append([sg.Frame('Incorporar',[
            [sg.Text('Órgão Origem:', size=(15,1)), sg.Combo(self.orgaos, default_value=self.orgaos[0], size=(55,1), readonly=True, enable_events=True, k='-ORGAO-')],
            [sg.Text('Nº do Termo:', size=(15,1)),sg.Input(key='-NTERMO-', size=(25,1))],
            [sg.Text('Descrição do Bem:', size=(15,1)),sg.Input(key='-DESCRICAO-', size=(25,1))],
            [sg.HorizontalSeparator(pad=(10,20))],
            [sg.Text('Número do RP:', size=(15,1)),sg.Input(key='-RPS-', size=(25,1)),sg.Button('Adicionar')],
            [self.listbox],
            [sg.Text('0 rps adicionados', k='-ADICIONADOS-'),sg.Push(), sg.Button('Limpar', button_color='gray'),sg.Button('Remover', button_color='red'),sg.Button('Incorporar', button_color='green')]
        ])])
        
        receber.append([sg.Frame('',[[sg.Text('Distribuídos não recebidos'),sg.Push(),sg.Button('Receber')]], size=(555,40) )])
        
        layout.append(receber)
        
        layout.append([sg.Checkbox('Executar em segunda plano', default=True, k='-HEADLESS-'), sg.Push()])

        return sg.Window('Robô Patrimônio', layout=layout, finalize=True)

    def start(self):
        janela = self.janela()
        
        while True:
            event, values = janela.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == 'Adicionar':
                rps = values['-RPS-']
                if rps != '' and rps != ' ':
                    if ':' in rps:
                        rps = rps.split(':')
                        try:
                            rps = range(int(rps[0]), (int(rps[1])+1))
                            for i in rps:
                                self.rps_value.append(i)
                        except:
                            sg.popup('Não é possível gerar sequência de letras.', title='Erro')

                    elif ',' in rps:
                        rps = rps.split(',')
                        for i in rps:
                            rp = i.strip()
                            if rp in self.rps_value:
                                continue
                            else:
                                self.rps_value.append(rp)
                    
                    else:
                        rp = rps.strip()
                        if rp in self.rps_value:
                            continue
                        else:
                            self.rps_value.append(rp)
                    
                    janela['-LIST-'].update(self.rps_value)
                    janela['-RPS-'].update('')
                    janela['-ADICIONADOS-'].update(f'{len(self.rps_value)} rps adicionados')
                    
            elif event == 'Limpar':
                self.rps_value = []
                janela['-LIST-'].update('')
                janela['-ADICIONADOS-'].update(f'{len(self.rps_value)} rps adicionados')
                
            elif event == 'Remover':
                if self.listbox.get() != []:
                    val = self.listbox.get()
                    for i in val:
                        self.rps_value.remove(i)
                        janela['-LIST-'].update(self.rps_value)
                        janela['-ADICIONADOS-'].update(f'{len(self.rps_value)} rps adicionados')
                    
            elif event == 'Incorporar':
                sispat = Robo(headless=values['-HEADLESS-'])
                sispat.login('operacional')
                sispat.incorporar(values['-ORGAO-'], values['-NTERMO-'], values['-DESCRICAO-'], self.rps_value)
                
            elif event == 'Receber':
                sispat = Robo(headless=values['-HEADLESS-'])
                sispat.login('agente_responsavel')
                sispat.receber()
        