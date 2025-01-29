from src import sispat
from src.filtrar import filtrar
from time import sleep
from datetime import datetime as time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = sispat.driver()
sispat.login(driver)

sispat.sispatweb(driver)
sispat.nao_incorporado(driver)

origem = 'FESPDS - FUNDO ESTADUAL DE SEGURANÇA PUBLICA E DEFESA SOCIAL DO ESTADO DO PARA'
ntermo = '2024/258'
descricao = 'DISPOSITIVO ELETRICO INCAPAC.,DUPLO DISPARO,LASER DUPLO,REC.'
destino = 'SETOR DE ARMAMENTO'

xpath_root = '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[1]/div/div/div/table/tbody/tr'

xpaths = {
    "org_origem_path": xpath_root + '/td[1]/fieldset/table[1]/tbody/tr/td[2]/select',
    "n_termo_path": xpath_root + '/td[1]/fieldset/table[2]/tbody/tr[1]/td[2]/input',
    "descricao_input_path": '//*[@id="incorporar_bem_destinado_ao_orgao_form_pesq:descricaomaterial"]',
    "pesquisar_path": xpath_root + '/td[2]/table/tbody/tr/td/table/tbody/tr/td/input[1]'
}

filtrar(driver, origem, ntermo, descricao)
sleep(1.5)

log = open('relatório.log', 'a')
tasers = open('tasers.json', 'r')
for i in range(35):
    selecionar_ben_btn = WebDriverWait(driver, timeout=60)\
    .until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[1]/td[8]/a/img')))

    descricao_sistema = driver.find_element(By.XPATH, "/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[1]/td[3]").text
    
    nserie = driver.find_element(By.XPATH, "/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/div/div/table[8]/tbody/tr[4]/td[2]/span").text
    
    driver.execute_script("arguments[0].click();", selecionar_ben_btn)
    sleep(.5)    


    input_rp = WebDriverWait(driver, timeout=60)\
    .until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/div/div/table[2]/tbody/tr[2]/td[2]/input')))

    rp = tasers[nserie]

    input_rp.send_keys(rp)
    
    btn_pesquisa = WebDriverWait(driver, timeout=60)\
    .until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/div/div/fieldset/table/tbody/tr/td[2]/table/tbody/tr/td[2]/input')))
    
    driver.execute_script("arguments[0].click();", btn_pesquisa)
    sleep(.5)
    
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
        sleep(0.5)
        timestamp = time.now().strftime("%d/%m/%Y %H:%M:%S")
        msg = f'{timestamp} - Patrimônio: {rp} Descrição: {descricao_sistema} Incorporado {1}\n'
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
        sleep(1.5)

               
log.close()        
driver.quit()