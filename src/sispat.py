import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def driver():
    driver = webdriver.Chrome()
    return driver

def login(driver):
    print("Acessando o Governo Digital...")
    
    driver.get('https://www.sistemas.pa.gov.br/governodigital/public/main/index.xhtml')
    
    print("Efetuando o login...")
    with open("config.json") as file:
        login = json.load(file)
    usuario = login["usuario"]
    senha = login["senha"]
    
    WebDriverWait(driver, timeout=60)\
        .until(EC.presence_of_element_located((By.XPATH, '//*[@id="form_login:login_username"]')))\
            .send_keys(usuario)
    
    WebDriverWait(driver, timeout=60)\
        .until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="form_login:login_password"]'))
        ).send_keys(senha)
    
    WebDriverWait(driver, timeout=60)\
        .until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="form_login:button_login"]'))
        ).click()
    
    print("Login efetuado com sucesso!")

def sispatweb(driver):
    WebDriverWait(driver, timeout=60)\
        .until(EC.presence_of_element_located((By.XPATH, '//*[@id="form_sistema:submit_area"]/div/div[3]/div[1]/a/img')))
    driver.get('https://www.sistemas.pa.gov.br/sispat')
    print("Acessando o SispatWeb...")


def nao_incorporado(driver):
    entrada_por_transferencia_nao_incorporado = WebDriverWait(driver, timeout=60)\
        .until(EC.presence_of_element_located((By.XPATH, '//tr/td/a[contains(text(), "Entrada por Transferência Não Incorporado")]')))
    
    print("Acessando entrada por tranferência não incorporados...")
    
    driver.execute_script("arguments[0].click();", entrada_por_transferencia_nao_incorporado)
    sleep(3.5)
    
def dist_nao_recebido(driver):
    dist_nao_recebido = WebDriverWait(driver, timeout=60)\
        .until(EC.presence_of_element_located((By.XPATH, '//tr/td/a[contains(text(), "Distribuído Não Recebido")]')))
    
    print('Acessando distribuídos não recebidos...')
    
    driver.execute_script("arguments[0].click();", dist_nao_recebido)
    sleep(3.5)