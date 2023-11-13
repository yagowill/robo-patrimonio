import PySimpleGUI as sg
from src.incorporar import incorporar
from src.receber import receber
from src.orgaos import orgaos
from src.unidades_localizacao import destinos

sg.theme('DarkBlue')

class Interface_grafica:
    def __init__(self):
        self.rps_value = []
        self.listbox = sg.Listbox(values=[''], size=(36,25), enable_events=True, select_mode='extended', k='-LIST-')
        self.orgaos = orgaos
        self.destinos = destinos
    def janela(self):
        layout = []
        receber = []
        
        col_left = [
            [sg.Text('Órgão Origem:')],
            [sg.Combo(self.orgaos, default_value=self.orgaos[0], readonly=True, enable_events=True, k='-ORGAO-', size=(78,1))],
            [sg.Text('Nº do Termo:')],
            [sg.Input(key='-NTERMO-', size=(78,1))],
            [sg.Text('Descrição:')],
            [sg.Input(key='-DESCRICAO-', size=(78,1))],
            [sg.Text('Destino:')],
            [sg.Combo(self.destinos, default_value=self.destinos[624], readonly=True, enable_events=True, k='-DESTINO-', size=(78,1))],
            [sg.VPush()],
            [sg.Push(), sg.Button('Limpar', button_color='gray'),sg.Button('Remover', button_color='red'),sg.Button('Incorporar', button_color='green')]]
        
        col_right = [
            [sg.Text('Número do RP:')],
            [sg.Input(key='-RPS-', size=(25,1)),sg.Button('Adicionar')],
            [self.listbox],
            [sg.Text('0 rps adicionados', k='-ADICIONADOS-')]]
        
        
        layout.append([sg.Column(col_left, vertical_alignment='top'), sg.Column(col_right)])
        
        receber.append([sg.Frame('Receber',[[sg.Text('Distribuídos não recebidos'),sg.Push(),sg.Button('Receber')]], size=(857,50) )])
        
        layout.append(receber)

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
                    
                    elif '\n' in rps:
                        rps = rps.strip()
                        rps = rps.split('\n')
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
                incorporar(origem=values['-ORGAO-'], ntermo=values['-NTERMO-'], descricao=values['-DESCRICAO-'], patrimonios=self.rps_value, destino=values['-DESTINO-'])
                
            elif event == 'Receber':
                receber(strategy='TUDO')