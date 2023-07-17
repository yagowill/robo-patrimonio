import PySimpleGUI as sg
from orgaos import orgaos
from time import sleep
from robo import Sistema

rps_value = []

lst = sg.Listbox(values=[''], size=(75,20), enable_events=True, select_mode='extended', k='-LIST-')

incorporar = [sg.Frame('Incorporar',[
    [sg.Text('Órgão Origem:', size=(15,1)), sg.Combo(orgaos, default_value=orgaos[0], size=(55,1), readonly=True, enable_events=True, k='-ORGAO-')],
    [sg.Text('Nº do Termo:', size=(15,1)),sg.Input(key='-NTERMO-', size=(25,1))],
    [sg.Text('Descrição do Bem:', size=(15,1)),sg.Input(key='-DESCRICAO-', size=(25,1))],
    [sg.HorizontalSeparator(pad=(10,20))],
    [sg.Text('Número do RP:', size=(15,1)),sg.Input(key='-RPS-', size=(25,1)),sg.Button('Adicionar')],
    [lst],
    [sg.Text('0 rps adicionados', k='-ADICIONADOS-'),sg.Push(), sg.Button('Limpar', button_color='gray'),sg.Button('Remover', button_color='red'),sg.Button('Incorporar', button_color='green')]
])]

receber = []
receber.append(sg.Frame('',[[sg.Text('Distribuídos não recebidos'),sg.Push(),sg.Button('Receber')]], size=(555,40) ))


layout = [
    incorporar,
    receber,
    [sg.Checkbox('Executar em segunda plano', default=True, k='-HEADLESS-'), sg.Push()]
    ]

window = sg.Window('Robô Patrimônio', layout=layout)


while True:
    event, values = window.read()
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
                        rps_value.append(i)
                except:
                    sg.popup('Não é possível gerar sequência de letras.', title='Erro')

            elif ',' in rps:
                rps = rps.split(',')
                for i in rps:
                    rp = i.strip()
                    if rp in rps_value:
                        continue
                    else:
                        rps_value.append(rp)
            
            else:
                rp = rps.strip()
                if rp in rps_value:
                    continue
                else:
                    rps_value.append(rp)
            
            window['-LIST-'].update(rps_value)
            window['-RPS-'].update('')
            window['-ADICIONADOS-'].update(f'{len(rps_value)} rps adicionados')
            
    elif event == 'Limpar':
        rps_value = []
        window['-LIST-'].update('')
        window['-ADICIONADOS-'].update(f'{len(rps_value)} rps adicionados')
        
    elif event == 'Remover':
        if lst.get() != []:
            val = lst.get()
            for i in val:
                rps_value.remove(i)
                window['-LIST-'].update(rps_value)
                window['-ADICIONADOS-'].update(f'{len(rps_value)} rps adicionados')
            
    elif event == 'Incorporar':
        sispat = Sistema(headless=values['-HEADLESS-'])
        sispat.login('operacional')
        sispat.incorporar(values['-ORGAO-'], values['-NTERMO-'], values['-DESCRICAO-'], rps_value)
        
    elif event == 'Receber':
        sispat = Sistema(headless=values['-HEADLESS-'])
        sispat.login('agente_responsavel')
        sispat.receber()
        