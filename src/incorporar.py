from src.Sispat import Sispat
from time import sleep ,time


def incorporar(cli, origem, ntermo, descricao, patrimonios, destino):
    sispat = Sispat(tipo='operacional', cli=cli)
    rps = patrimonios
    cadastrados = 0  
    total = len(rps)
    
    sispat.login()
    sispat.acessar_sispatweb()
                
    sispat.acessar_entrada_por_transferencia_nao_incorporado()
    
    sispat.mensagem("pesquisando...")
    sispat.filtrar(origem, ntermo, descricao)
    sleep(1)
    log = open('relatório.log', 'a')
    for rp in rps:
        selecionar_ben_btn = sispat.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[1]/td[8]/a/img')
        selecionar_ben_btn.click()   
        
        input_rp = sispat.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/div/div/table[2]/tbody/tr[2]/td[2]/input')
        input_rp.send_keys(rp)
        
        btn_pesquisa = sispat.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/div/div/fieldset/table/tbody/tr/td[2]/table/tbody/tr/td[2]/input')
        btn_pesquisa.click()
        
        input_pesquisa = '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/table[2]/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/input'
        
        input_pesquisa.send_keys(destino)
        
        btn_pesquisar = '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/table[2]/tbody/tr/td[2]/table/tbody/tr/td/input'
        
        sispat.navegador.execute_script("arguments[0].click();", btn_pesquisar)
        
        sleep(1)
        
        btn_destino = '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/span/table/tbody/tr/td[3]/a'
        
        sispat.navegador.execute_script("arguments[0].click();", btn_destino)
        
        sleep(1)
        
        confirmar_btn = sispat.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/table/tbody/tr/td/input[1]')
        
        sispat.navegador.execute_script("arguments[0].click();", confirmar_btn)
        
        sleep(1)
        
        
        confirmacao = sispat.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/div[1]/table/tbody/tr/td/span[2]')
        
        if confirmacao.text == "Bem foi incorporado ao órgão com sucesso.":
            btn_imprimir_depois = '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/div/div[2]/input[2]'
            sispat.navegador.execute_script("arguments[0].click();", btn_imprimir_depois) 
            timestamp = time.now().strftime("%d/%m/%Y %H:%M:%S")
            cadastrados += 1
            msg = f'{timestamp} - Patrimônio: {rp} Descrição: {descricao} Incorporado {cadastrados}/{total}\n'
            sispat.mensagem(msg, 'green')
            log.write(msg)
        else:
            aviso = sispat.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/span[2]')
            sispat.mensagem(aviso.text, text_color='red')
            log.write(aviso.text + '\n')
            cancelar_btn = sispat.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/table/tbody/tr/td/input[2]')
            sispat.navegador.execute_script("arguments[0].click();", cancelar_btn)
            
            sispat.filtrar(origem, ntermo, descricao)
            
    log.close()        
    sispat.navegador.quit()
    sispat.mensagem("Finalizado", text_color='green')