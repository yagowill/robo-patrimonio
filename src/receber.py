import re
from src import sispat
from time import sleep
from selenium.webdriver.common.by import By
from datetime import datetime as time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def receber():
    driver = sispat.driver()
    
    sispat.login(driver)
    sispat.sispatweb(driver)
    sispat.dist_nao_recebido(driver)
    mensagem_label = WebDriverWait(driver, timeout=60).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[2]/div[1]/table/tbody/tr/td[3]/div/div[1]/table/tbody/tr/td/span[2]')))
    mensagem = mensagem_label.text
    
    try:
        assert re.search("A busca não retornou resultados.",confirmacao.text) == None
        print(mensagem)
    except:
        print(mensagem)
        driver.quit()
    
                
        case 'TUDO':
            while True:
                try:
                    transferencia_nao_recebida_btn = WebDriverWait(driver, timeout=60)\
                        .until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[1]/td[7]')))
                
                    transferencia_nao_recebida_btn.click()
                    
                    calendario_btn = WebDriverWait(driver, timeout=60)\
                        .until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/div/div[1]/table[3]/tbody/tr/td[2]/span/img')))
                    calendario_btn.click()
                    
                    data_btn = WebDriverWait(driver, timeout=60)\
                        .until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/div/div[1]/table[3]/tbody/tr/td[2]/table/tbody/tr[9]/td/table/tbody/tr/td[5]/div')))
                    data_btn.click()
                    
                    receber = WebDriverWait(driver, timeout=60)\
                        .until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/div/div[2]/input[1]')))
                    receber.click()
                    
                    confirmacao = WebDriverWait(driver, timeout=60)\
                        .until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/table/tbody/tr/td[3]/div/div[1]/table/tbody/tr/td/span[2]')))
                        
                    assert re.search("recebido com sucesso.",confirmacao.text) != None
                    timestamp = time.now().strftime("%d/%m/%Y %H:%M:%S")
                    print(f'{timestamp} {confirmacao.text}')
                except: driver.quit()
    