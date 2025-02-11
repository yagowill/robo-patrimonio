import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(60)
    return driver

def login(driver):
    print("Acessando o Governo Digital...")
    
    driver.get('https://www.sistemas.pa.gov.br/governodigital/public/main/index.xhtml')
    
    print("Efetuando o login...")
    with open("config.json") as file:
        login = json.load(file)
    usuario = login["usuario"]
    senha = login["senha"]
    
    login_username = driver.find_element(By.XPATH, '//*[@id="form_login:login_username"]')
    login_username.send_keys(usuario)
    
    login_password = driver.find_element(By.XPATH, '//*[@id="form_login:login_password"]')
    login_password.send_keys(senha)
    
    btn_login = driver.find_element(By.XPATH, '//*[@id="form_login:button_login"]')
    btn_login.click()
    
    print("Login efetuado com sucesso!")

def sispatweb(driver):
    driver.get('https://www.sistemas.pa.gov.br/sispat')
    print("Acessando o SispatWeb...")


def nao_incorporado(driver):
    entrada_por_transferencia_nao_incorporado = driver.find_element(By.XPATH, '//tr/td/a[contains(text(), "Entrada por Transferência Não Incorporado")]')
    
    print("Acessando entrada por tranferência não incorporados...")
    
    driver.execute_script("arguments[0].click();", entrada_por_transferencia_nao_incorporado)
    sleep(3.5)
    
def dist_nao_recebido(driver):
    driver.get("https://www.sistemas.pa.gov.br/sispat/movimentacao_bem/recebimento/recebimento_termo_bem_interno_operacional_lista.seam")
    search_btn = driver.find_element(By.XPATH, "/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[1]/div/div/div/table/tbody/tr/td[2]/table/tbody/tr/td/input")
    search_btn.click()
    print('Acessando distribuídos não recebidos...')

def manter_ocorrencia(driver):
    driver.get("https://www.sistemas.pa.gov.br/sispat/avaliacao_bem/ocorrencia/search.seam")
    novo_btn = driver.find_element(By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[1]/div/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/input')
    novo_btn.click()


wait = WebDriverWait(driver, timeout=60)