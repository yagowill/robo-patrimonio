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
    message_label = driver.find_element(By.XPATH, "/html/body/div/div[1]/table/tbody/tr/td[3]/div/div[1]/table/tbody/tr/td/span[2]")
    message = message_label.text
    resultado = re.search(r'\d+', message)

    try:
        assert resultado
    except:
        print(message)
        driver.close()

    qtd_nao_recebidos = int(resultado.group())
    print(f"Quantidade de não recebidos: {qtd_nao_recebidos}")
    
                
    for i in range(qtd_nao_recebidos + 1):
        try:
            transferencia_nao_recebida_btn = driver.find_element(By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[1]/td[7]/a')
            transferencia_nao_recebida_btn.click()
            
            
            calendario_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/div/div[1]/table[3]/tbody/tr/td[2]/span/img')
            calendario_btn.click()

            
            today_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/div/div[1]/table[3]/tbody/tr/td[2]/table/tbody/tr[9]/td/table/tbody/tr/td[5]/div')
            driver.execute_script("arguments[0].click();", today_btn)
            sleep(1)
            
            receber = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/div/div[2]/input[1]')
            driver.execute_script("arguments[0].click();", receber)
            sleep(2)
            
            confirmacao = driver.find_element(By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/div[1]/table/tbody/tr/td/span[2]')
                
            assert re.search("recebido com sucesso.",confirmacao.text)
            timestamp = time.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f'{timestamp} {confirmacao.text}')
        except:
            break    
    driver.close()
    