from src.Sispat import Sispat
import re
import time


def receber(headless, cli):
    sispat = Sispat(headless=headless, tipo='agente_responsavel', cli=cli)
    
    sispat.login()
    sispat.acessar_sispatweb()
    nao_recebidos =  sispat.espera_elemento_selector('#form_pendencias\:panel > table > tbody > tr:nth-child(3) > td.col_quantidade > span')
    qtd_nao_recebidos = int(nao_recebidos.text)
    print(qtd_nao_recebidos, type(qtd_nao_recebidos))
    sispat.acessar_dist_nao_recebido()
                    

    for i in range(qtd_nao_recebidos + 1):
        transferencia_nao_recebida_btn = sispat.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[1]/td[7]')
        transferencia_nao_recebida_btn.click()
        calendario_btn = sispat.espera_elemento('/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/fieldset/div/table/tbody/tr[4]/td[2]/span/img')
        calendario_btn.click()
        data_btn = sispat.espera_elemento('/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/fieldset/div/table/tbody/tr[4]/td[2]/table/tbody/tr[9]/td/table/tbody/tr/td[5]/div')
        data_btn.click()
        receber = sispat.espera_elemento('/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/div/input[1]')
        receber.click()
        confirmacao = sispat.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/div[1]/table/tbody/tr/td/span[2]')
        assert re.search("recebido com sucesso.",confirmacao.text) != None
        timestamp = time.now().strftime("%d/%m/%Y %H:%M:%S")
        sispat.mensagem(f'{timestamp} {confirmacao.text}')
    sispat.navegador.quit()