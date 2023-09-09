import PySimpleGUI as sg
from src.incorporar import incorporar
from src.receber import receber
from src.orgaos import orgaos
from src.unidades_localizacao import destinos


class Interface_grafica:
    def __init__(self):
        self.rps_value = []
        self.listbox = sg.Listbox(values=[''], size=(75,20), enable_events=True, select_mode='extended', k='-LIST-')
        self.orgaos = orgaos
        self.destinos = destinos
    def janela(self):
        layout = []
        receber = []
        
        layout.append([sg.Frame('Incorporar',[
            [sg.Text('Órgão Origem:', size=(15,1)), sg.Combo(self.orgaos, default_value=self.orgaos[0], size=(55,1), readonly=True, enable_events=True, k='-ORGAO-')],
            [sg.Text('Nº do Termo:', size=(15,1)),sg.Input(key='-NTERMO-', size=(55,1))],
            [sg.Text('Descrição:', size=(15,1)),sg.Input(key='-DESCRICAO-', size=(55,1))],
            [sg.Text('Destino:', size=(15,1)), sg.Combo(self.destinos, default_value=self.destinos[624], size=(55,1), readonly=True, enable_events=True, k='-DESTINO-')],
            [sg.HorizontalSeparator(pad=(10,20))],
            [sg.Text('Número do RP:', size=(15,1)),sg.Input(key='-RPS-', size=(25,1)),sg.Button('Adicionar')],
            [self.listbox],
            [sg.Text('0 rps adicionados', k='-ADICIONADOS-'),sg.Push(), sg.Button('Limpar', button_color='gray'),sg.Button('Remover', button_color='red'),sg.Button('Incorporar', button_color='green')]
        ])])
        
        receber.append([sg.Frame('',[[sg.Text('Distribuídos não recebidos'),sg.Push(),sg.Button('Receber')]], size=(555,40) )])
        
        layout.append(receber)
        
        layout.append([sg.Checkbox('Executar em segunda plano', default=False, k='-HEADLESS-'), sg.Push()])

        return sg.Window('Robô Patrimônio', layout=layout, finalize=True)

    def start(self):
        janela = self.janela()
        
        while True:
            event, values = janela.read()
            
            match event:
                case sg.WIN_CLOSED:
                    break
            
                case 'Adicionar':
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
                    
                case 'Limpar':
                    self.rps_value = []
                    janela['-LIST-'].update('')
                    janela['-ADICIONADOS-'].update(f'{len(self.rps_value)} rps adicionados')
                
                case 'Remover':
                    if self.listbox.get() != []:
                        val = self.listbox.get()
                        for i in val:
                            self.rps_value.remove(i)
                            janela['-LIST-'].update(self.rps_value)
                            janela['-ADICIONADOS-'].update(f'{len(self.rps_value)} rps adicionados')
                        
                case 'Incorporar':
                    incorporar(headless=values['-HEADLESS-'], cli=False, origem=values['-ORGAO-'], ntermo=values['-NTERMO-'], descricao=values['-DESCRICAO-'], patrimonios=self.rps_value, destino=values['-DESTINO-'])
                    
                case 'Receber':
                    receber(headless=values['-HEADLESS-'], cli=False)