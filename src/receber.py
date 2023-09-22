import re
from time import sleep
from datetime import datetime as time
from src.Sispat import Sispat
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
    

def receber(cli, strategy):
    sispat = Sispat(tipo='agente_responsavel', cli=cli)
    
    sispat.login()
    sispat.acessar_sispatweb()
    nao_recebidos =  sispat.espera_elemento_selector('#form_pendencias\:panel > table > tbody > tr:nth-child(2) > td.col_quantidade > span')
    qtd_nao_recebidos = int(nao_recebidos.text)
    print(f"Quantidade de não recebidos: {qtd_nao_recebidos}")
    sispat.acessar_dist_nao_recebido()
    
    match strategy:
        case 'DIME':
            while True:
                termos = WebDriverWait(sispat.navegador, timeout=60).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="movimentacao_interna_form_lista:movimentacoes:tb"]/tr')))
                for i in range(1, len(termos) + 1):
                    unidade_origem = sispat.espera_elemento(f'/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[{i}]/td[3]').text
                    while unidade_origem != "UNIDADE DE PATRIMONIO":
                        transferencia_nao_recebida_btn = sispat.espera_elemento(f'/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[{i}]/td[7]')
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
                        sispat.mensagem(f'{timestamp} {unidade_origem} {confirmacao.text}')
                        unidade_origem = sispat.espera_elemento(f'/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[{i}]/td[3]').text
                        
                avançar = sispat.espera_elemento('//*[@id="movimentacao_interna_form_lista:paginador_table"]/tbody/tr/td[contains(text(), "»")]')
                if(WebDriverWait(sispat.navegador, timeout=60).until(EC.element_attribute_to_include((By.XPATH, '//*[@id="movimentacao_interna_form_lista:paginador_table"]/tbody/tr/td[contains(text(), "»")]'), "onclick"))):
                    sispat.navegador.execute_script("arguments[0].click();", avançar)
                    sleep(2)
                else: break
        case 'TUDO':
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
    