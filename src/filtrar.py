from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

xpath_root = '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[1]/div/div/div/table/tbody/tr'

xpaths = {
    "org_origem_path": xpath_root + '/td[1]/fieldset/table[1]/tbody/tr/td[2]/select',
    "n_termo_path": xpath_root + '/td[1]/fieldset/table[2]/tbody/tr[1]/td[2]/input',
    "descricao_input_path": '//*[@id="incorporar_bem_destinado_ao_orgao_form_pesq:descricaomaterial"]',
    "pesquisar_path": xpath_root + '/td[2]/table/tbody/tr/td/table/tbody/tr/td/input[1]'
}

def filtrar(driver, origem, ntermo, descricao):
        orgao_origem_selection = WebDriverWait(driver, timeout=60)\
            .until(EC.presence_of_element_located((By.XPATH, xpaths['org_origem_path'])))
        select = Select(orgao_origem_selection)
        
        select.select_by_visible_text(origem)
        
        n_termo = WebDriverWait(driver, timeout=60)\
            .until(EC.presence_of_element_located((By.XPATH, xpaths['n_termo_path'])))
        n_termo.send_keys(ntermo)
        
        descricao_input = WebDriverWait(driver, timeout=60)\
            .until(EC.presence_of_element_located((By.XPATH, xpaths['descricao_input_path'])))
        descricao_input.send_keys(descricao)
        
        pesquisar = WebDriverWait(driver, timeout=60)\
            .until(EC.presence_of_element_located((By.XPATH, xpaths['pesquisar_path'])))
        
        driver.execute_script("arguments[0].click();", pesquisar)