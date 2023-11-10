from src import sispat
from src.filtrar import filtrar
from time import sleep ,time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def incorporar(origem, ntermo, descricao, patrimonios, destino):
    driver = sispat.driver()
    sispat.login(driver,'operacional')
    
    rps = patrimonios
    cadastrados = 0  
    total = len(rps)
    
    sispat.sispatweb(driver)
    sispat.nao_incorporado(driver)
    
    print("pesquisando...")
    filtrar(driver, origem, ntermo, descricao)
    sleep(1)
    log = open('relatório.log', 'a')
    for rp in rps:
        selecionar_ben_btn = WebDriverWait(driver, timeout=60)\
        .until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[1]/td[8]/a/img')))
        selecionar_ben_btn.click()   
        
        input_rp = WebDriverWait(driver, timeout=60)\
        .until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/div/div/table[2]/tbody/tr[2]/td[2]/input')))
        input_rp.send_keys(rp)
        
        btn_pesquisa = WebDriverWait(driver, timeout=60)\
        .until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/div/div/fieldset/table/tbody/tr/td[2]/table/tbody/tr/td[2]/input')))
        btn_pesquisa.click()
        
        input_pesquisa = WebDriverWait(driver, timeout=60)\
        .until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/table[2]/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/input')))
        
        input_pesquisa.send_keys(destino)
        
        btn_pesquisar = WebDriverWait(driver, timeout=60)\
        .until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/table[2]/tbody/tr/td[2]/table/tbody/tr/td/input')))
        
        driver.execute_script("arguments[0].click();", btn_pesquisar)
        
        sleep(1)
        
        btn_destino = WebDriverWait(driver, timeout=60)\
        .until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/span/table/tbody/tr/td[3]/a')))
        
        driver.execute_script("arguments[0].click();", btn_destino)
        
        sleep(1)
        
        confirmar_btn = WebDriverWait(driver, timeout=60)\
        .until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/table/tbody/tr/td/input[1]')))
        
        driver.execute_script("arguments[0].click();", confirmar_btn)
        
        sleep(1)
        
        
        confirmacao = WebDriverWait(driver, timeout=60)\
        .until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/div[1]/table/tbody/tr/td/span[2]')))
        
        if confirmacao.text == "Bem foi incorporado ao órgão com sucesso.":
            btn_imprimir_depois = WebDriverWait(driver, timeout=60)\
                .until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/div/div[2]/input[2]')))
            driver.execute_script("arguments[0].click();", btn_imprimir_depois) 
            timestamp = time.now().strftime("%d/%m/%Y %H:%M:%S")
            cadastrados += 1
            msg = f'{timestamp} - Patrimônio: {rp} Descrição: {descricao} Incorporado {cadastrados}/{total}\n'
            print(msg)
            log.write(msg)
        else:
            aviso = WebDriverWait(driver, timeout=60)\
        .until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/span[2]')))
            print(aviso.text)
            log.write(aviso.text + '\n')
            cancelar_btn = WebDriverWait(driver, timeout=60)\
        .until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/table/tbody/tr/td/input[2]')))
            driver.execute_script("arguments[0].click();", cancelar_btn)
            
            filtrar(driver, origem, ntermo, descricao)
            
    log.close()        
    driver.quit()
    print("Finalizado")