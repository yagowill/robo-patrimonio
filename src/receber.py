import re
from src import sispat
from time import sleep
from selenium.webdriver.common.by import By
from datetime import datetime as time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def receber(strategy='TUDO'):
    driver = sispat.driver()
    
    sispat.login(driver, "agente_responsavel")
    sispat.sispatweb(driver)
    nao_recebidos =  WebDriverWait(driver, timeout=60)\
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, '#form_pendencias\:panel > table > tbody > tr:nth-child(2) > td.col_quantidade > span')))
    qtd_nao_recebidos = int(nao_recebidos.text)
    print(f"Quantidade de não recebidos: {qtd_nao_recebidos}")
    sispat.dist_nao_recebido(driver)
    
    match strategy:
        case 'DIME':
            while True:
                termos = WebDriverWait(driver, timeout=60).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="movimentacao_interna_form_lista:movimentacoes:tb"]/tr')))
                for i in range(1, len(termos) + 1):
                    unidade_origem = WebDriverWait(driver, timeout=60)\
                        .until(EC.presence_of_element_located((By.XPATH, f'/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[{i}]/td[3]'))).text
                        
                    while unidade_origem != "UNIDADE DE PATRIMONIO":
                        transferencia_nao_recebida_btn = WebDriverWait(driver, timeout=60)\
                            .until(EC.presence_of_element_located((By.XPATH, f'/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[{i}]/td[7]')))
                        transferencia_nao_recebida_btn.click()
                        
                        calendario_btn = WebDriverWait(driver, timeout=60)\
                            .until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/fieldset/div/table/tbody/tr[4]/td[2]/span/img')))
                        calendario_btn.click()
                        
                        data_btn = WebDriverWait(driver, timeout=60)\
                            .until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/fieldset/div/table/tbody/tr[4]/td[2]/table/tbody/tr[9]/td/table/tbody/tr/td[5]/div')))
                        data_btn.click()
                        
                        receber = WebDriverWait(driver, timeout=60)\
                            .until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/div/input[1]')))
                        receber.click()
                        
                        confirmacao = WebDriverWait(driver, timeout=60)\
                            .until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/div[1]/table/tbody/tr/td/span[2]')))
                            
                        assert re.search("recebido com sucesso.",confirmacao.text) != None
                        timestamp = time.now().strftime("%d/%m/%Y %H:%M:%S")
                        print(f'{timestamp} {unidade_origem} {confirmacao.text}')
                        
                        unidade_origem = WebDriverWait(driver, timeout=60)\
                            .until(EC.presence_of_element_located((By.XPATH, f'/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[{i}]/td[3]'))).text
                        
                avançar = WebDriverWait(driver, timeout=60)\
                    .until(EC.presence_of_element_located((By.XPATH, '//*[@id="movimentacao_interna_form_lista:paginador_table"]/tbody/tr/td[contains(text(), "»")]')))
                    
                if(WebDriverWait(driver, timeout=60).until(EC.element_attribute_to_include((By.XPATH, '//*[@id="movimentacao_interna_form_lista:paginador_table"]/tbody/tr/td[contains(text(), "»")]'), "onclick"))):
                    driver.execute_script("arguments[0].click();", avançar)
                    sleep(2)
                else: break
                
        case 'TUDO':
            for i in range(qtd_nao_recebidos + 1):
                transferencia_nao_recebida_btn = WebDriverWait(driver, timeout=60)\
                    .until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[1]/td[7]')))
                transferencia_nao_recebida_btn.click()
                
                calendario_btn = WebDriverWait(driver, timeout=60)\
                    .until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/fieldset/div/table/tbody/tr[4]/td[2]/span/img')))
                calendario_btn.click()
                
                data_btn = WebDriverWait(driver, timeout=60)\
                    .until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/fieldset/div/table/tbody/tr[4]/td[2]/table/tbody/tr[9]/td/table/tbody/tr/td[5]/div')))
                data_btn.click()
                
                receber = WebDriverWait(driver, timeout=60)\
                    .until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/div/input[1]')))
                receber.click()
                
                confirmacao = WebDriverWait(driver, timeout=60)\
                    .until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/div[1]/table/tbody/tr/td/span[2]')))
                    
                assert re.search("recebido com sucesso.",confirmacao.text) != None
                timestamp = time.now().strftime("%d/%m/%Y %H:%M:%S")
                print(f'{timestamp} {confirmacao.text}')
            driver.quit()
    