from playwright.sync_api import Page, TimeoutError
from datetime import datetime
import re


# Centralized locators for incorporation process
incorporation_locators = {
    "select_bem_link": 'a[id="incorporar_bem_destinado_ao_orgao_form_lista:patrimonios:0:incorporarbens"]',
    "description_text": 'td[id="incorporar_bem_destinado_ao_orgao_form_lista:patrimonios:0:j_id445"]',
    "serial_number_text": '//*[@id="incorporar_bem_destinado_ao_orgao_form_cad:j_id415_body"]/table[8]/tbody/tr[4]/td[2]/span',
    "rp_input": 'input[type="text"][name="incorporar_bem_destinado_ao_orgao_form_cad:j_id434"]',
    "search_ul_button": 'input[id="incorporar_bem_destinado_ao_orgao_form_cad:selecionarunidadelocalizacaodestino"][name="incorporar_bem_destinado_ao_orgao_form_cad:selecionarunidadelocalizacaodestino"][value="Pesquisar"][title="Localizar Unidade de Localização de Destino"][type="button"]',
    "destino_search_input": 'input[name="modal_searchUnidadeDestino_unidade_search_form:j_id769"]',
    "destino_search_button": 'input[id="modal_searchUnidadeDestino_unidade_search_form:j_id777"][name="modal_searchUnidadeDestino_unidade_search_form:j_id777"][value="Pesquisar"][type="submit"]',
    "select_destino_link": 'a[href="#"][id="modal_searchUnidadeDestino_unidade_search_form:unidadesearchUnidadeDestino:0:confirmacaoorigem"][name="modal_searchUnidadeDestino_unidade_search_form:unidadesearchUnidadeDestino:0:confirmacaoorigem"]',
    "confirm_button": 'input[id="incorporar_bem_destinado_ao_orgao_form_cad:Incorporar"][name="incorporar_bem_destinado_ao_orgao_form_cad:Incorporar"][value="Incorporar"][type="button"]',
    "success_message": 'span:has-text("Bem foi incorporado ao órgão com sucesso.")',
    "imprimir_depois_button": 'input[value="Imprimir depois"]',
    "error_message_span": 'table[id="j_id407"] > tbody > tr > td > span[class="rich-messages-label"]',
    "cancel_button": 'input[id="incorporar_bem_destinado_ao_orgao_form_cad:voltar"][value="Cancelar"][type="button"]'
}

def incorporar(page: Page, origem: str, ntermo: str, descricao: str, patrimonios: list, destino: str, log_callback=None, usar_serial=False, serial_regex=''):
    _log = print #log_callback if log_callback else print
    from src.filtrar import filtrar # Import here to avoid circular dependency

    _log("Iniciando processo de incorporação...")

    cadastrados = 0
    resultados = page.locator('//*[@id="j_id407"]/tbody/tr/td/span[2]').text_content().split()[3]
    total = len(patrimonios) if not usar_serial else int(resultados)
    log_file_path = 'relatório.log'

    # Open log file once for appending
    with open(log_file_path, 'a', encoding='utf-8') as log:
        # Initial filter
        try:
            filtrar(page, origem, ntermo, descricao, _log)
        except Exception as e:
            _log(f"Erro na filtragem inicial: {e}")
            return # Stop if initial filter fails
        if not usar_serial:
            for i, rp in enumerate(patrimonios):
                _log(f"Processando patrimônio {i+1}/{total}: {rp}")
                try:
                    try:
                        selecionar_bem_link_locator = page.locator(incorporation_locators["select_bem_link"])
                        descricao_sistema_locator = page.locator(incorporation_locators["description_text"])

                        # Get description from the table before clicking
                        descricao_sistema = descricao_sistema_locator.text_content().strip()
                        _log(f"Descrição do sistema encontrado: '{descricao_sistema}'")

                        selecionar_bem_link_locator.click()
                        serial_number = page.locator(incorporation_locators["serial_number_text"]).text_content().strip()
                        _log(f"Número de serie do sistema encontrado: '{serial_number}'")

                        

                        # Preenche o campo RP com o serial tratado ou original
                        page.locator(incorporation_locators["rp_input"]).fill(str(rp))
                        page.locator(incorporation_locators["search_ul_button"]).click()

                        # Fill destination
                        page.locator(incorporation_locators["destino_search_input"]).fill(destino)
                        page.locator(incorporation_locators["destino_search_button"]).click()
                        

                        # Select destination from results
                        page.locator(incorporation_locators["select_destino_link"]).click()
                        # Wait for the modal/popup to close or the page to update
                        page.wait_for_selector(incorporation_locators["confirm_button"])

                        # Confirm incorporation
                        page.locator(incorporation_locators["confirm_button"]).click()
                        

                        # Check confirmation message
                        if page.locator(incorporation_locators["success_message"]).is_visible():
                            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            cadastrados += 1
                            msg = f'{timestamp} - Patrimônio: {rp} Descrição: {descricao_sistema} Incorporado {cadastrados}/{total}\n'
                            _log(msg.strip())
                            log.write(msg)
                            
                            # Click "Imprimir depois" button
                            page.click(incorporation_locators["imprimir_depois_button"])
                            
                            # After "Imprimir depois", it usually returns to the list.
                            # Re-filter to ensure the list is fresh for the next iteration.
                            filtrar(page, origem, ntermo, descricao, _log)

                        else:
                            error_msg_elem = page.locator(incorporation_locators["error_message_span"])
                            error_text = error_msg_elem.text_content().strip()
                            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            msg = f"{timestamp} - ERRO ao incorporar Patrimônio {rp}: {error_text}\n"
                            _log(msg.strip())
                            log.write(msg)
                            
                            # If there was an error, click "Cancelar" or navigate back to the list
                            try:
                                page.click(incorporation_locators["cancel_button"])
                                
                                # After cancel, it should return to the main list
                                # Re-filter for the next item
                                filtrar(page, origem, ntermo, descricao, _log)
                            except TimeoutError: # Changed PlaywrightTimeoutError to TimeoutError
                                _log(f"Não foi possível clicar em 'Cancelar' para {rp}, tentando re-filtrar...")
                                page.goto('https://www.sistemas.pa.gov.br/sispat')
                                page.click('text="Entrada por Transferência Não Incorporado"')
                                filtrar(page, origem, ntermo, descricao, _log)


                    except TimeoutError: # Changed PlaywrightTimeoutError to TimeoutError
                        msg = f"Patrimônio {rp} (ou link 'Selecionar Bem' para ele) não encontrado na lista filtrada. Verifique os filtros ou se o item já foi incorporado.\n"
                        _log(msg.strip())
                        log.write(msg)
                        # No need to filter again, just continue to next RP
                        # If this happens consistently, the filter might be wrong or the item isn't there.
                        # We continue to avoid stopping the entire batch.

                except Exception as e:
                    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    msg = f"{timestamp} - ERRO crítico ao processar Patrimônio {rp}: {e}\n"
                    _log(msg.strip())
                    log.write(msg)
                    # Attempt to return to the list for the next item, might fail
                    try:
                        page.goto('https://www.sistemas.pa.gov.br/sispat')
                        page.click('text="Entrada por Transferência Não Incorporado"')
                        filtrar(page, origem, ntermo, descricao, _log)
                    except Exception as nav_err:
                        _log(f"Erro ao tentar navegar de volta para a lista: {nav_err}")
                        _log("Processo de incorporação pode estar em estado inconsistente. Recomenda-se reiniciar.")
                        break # Stop if we can't even get back to the list
        else:
            while True:
                try:
                    # Tenta localizar o primeiro bem da lista filtrada
                    selecionar_bem_link_locator = page.locator(incorporation_locators["select_bem_link"])
                    if not selecionar_bem_link_locator.is_visible():
                        _log("Nenhum bem restante para incorporar na lista filtrada.")
                        break

                    descricao_sistema_locator = page.locator(incorporation_locators["description_text"])
                    descricao_sistema = descricao_sistema_locator.text_content().strip()
                    _log(f"Descrição do sistema encontrado: '{descricao_sistema}'")

                    selecionar_bem_link_locator.click()
                    serial_number = page.locator(incorporation_locators["serial_number_text"]).text_content().strip()
                    _log(f"Número de série do sistema encontrado: '{serial_number}'")
                    
                    # Aplica regex se fornecida
                    serial_para_usar = serial_number
                    if usar_serial and serial_regex:
                        match = re.search(serial_regex, serial_number.replace("\\", "\\\\"))  # Escape backslashes for regex
                        _log(f"Aplicando regex '{serial_regex}' no número de série: '{serial_number}'")
                        if match:
                            serial_para_usar = match.group(1)
                            _log(f"Número de série tratado pela regex: '{serial_para_usar}'")
                        else:
                            _log(f"Regex '{serial_regex}' não encontrou correspondência. Usando número de série original.")

                    # Preenche o campo RP com o serial_number
                    page.locator(incorporation_locators["rp_input"]).fill(serial_para_usar)
                    page.locator(incorporation_locators["search_ul_button"]).click()

                    # Preenche destino
                    page.locator(incorporation_locators["destino_search_input"]).fill(destino)
                    page.locator(incorporation_locators["destino_search_button"]).click()

                    # Seleciona destino e confirma
                    page.locator(incorporation_locators["select_destino_link"]).click()
                    page.wait_for_selector(incorporation_locators["confirm_button"])
                    page.locator(incorporation_locators["confirm_button"]).click()

                    # Confirma sucesso
                    if page.locator(incorporation_locators["success_message"]).is_visible():
                        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        cadastrados += 1
                        msg = f'{timestamp} - Serial: {serial_number} Descrição: {descricao_sistema} Incorporado {cadastrados}\n'
                        _log(msg.strip())
                        log.write(msg)
                        page.click(incorporation_locators["imprimir_depois_button"])
                        filtrar(page, origem, ntermo, descricao, _log)
                    else:
                        error_msg_elem = page.locator(incorporation_locators["error_message_span"])
                        error_text = error_msg_elem.text_content().strip()
                        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        msg = f"{timestamp} - ERRO ao incorporar Serial {serial_number}: {error_text}\n"
                        _log(msg.strip())
                        log.write(msg)
                        try:
                            page.click(incorporation_locators["cancel_button"])
                            filtrar(page, origem, ntermo, descricao, _log)
                        except TimeoutError:
                            _log(f"Não foi possível clicar em 'Cancelar' para {serial_number}, tentando re-filtrar...")
                            page.goto('https://www.sistemas.pa.gov.br/sispat')
                            page.click('text=\"Entrada por Transferência Não Incorporado\"')
                            filtrar(page, origem, ntermo, descricao, _log)
                except TimeoutError:
                    _log("Nenhum bem encontrado na lista filtrada ou erro de timeout.")
                    break
                except Exception as e:
                    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    msg = f"{timestamp} - ERRO crítico ao processar Serial: {e}\n"
                    _log(msg.strip())
                    log.write(msg)
                    try:
                        page.goto('https://www.sistemas.pa.gov.br/sispat')
                        page.click('text=\"Entrada por Transferência Não Incorporado\"')
                        filtrar(page, origem, ntermo, descricao, _log)
                    except Exception as nav_err:
                        _log(f"Erro ao tentar navegar de volta para a lista: {nav_err}")
                        _log("Processo de incorporação pode estar em estado inconsistente. Recomenda-se reiniciar.")
                        break    
    _log(f"Processo de incorporação finalizado. {cadastrados}/{total} patrimônios incorporados.")
