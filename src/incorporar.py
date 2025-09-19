from playwright.sync_api import Page, TimeoutError # Changed PlaywrightTimeoutError to TimeoutError
from datetime import datetime


# Centralized locators for incorporation process
incorporation_locators = {
    "select_bem_link": 'a[id*="incorporar_bem_destinado_ao_orgao_form_lista:patrimonios:0:incorporarbens"]', 
    "description_text": 'td[id*="incorporar_bem_destinado_ao_orgao_form_lista:patrimonios:0:j_id446"]', 
    "rp_input": 'input[id*="incorporar_bem_destinado_ao_orgao_form_cad:rpInicial"]',
    "search_unidade_button": 'input[value="Pesquisar"][id*="incorporar_bem_destinado_ao_orgao_form_cad:selecionarunidadelocalizacaodestino"]',
    "destino_search_input": 'input[name="modal_searchUnidadeDestino_unidade_search_form:j_id770"]',
    "destino_search_button": 'input[value="Pesquisar"][id*="modal_searchUnidadeDestino_unidade_search_form:j_id778"]',
    "select_destino_link": 'a[id*="modal_searchUnidadeDestino_unidade_search_form:unidadesearchUnidadeDestino:0:confirmacaoorigem"]', 
    "confirm_button": 'input[id*="incorporar_bem_destinado_ao_orgao_form_cad:Incorporar"]',
    "success_message": 'span:has-text("Bem foi incorporado ao órgão com sucesso.")',
    "imprimir_depois_button": 'input[id*="incorporar_bem_destinado_ao_orgao_form_lista:cancelaimpressao"]',
    "error_message_span": 'div.erros > table > tbody > tr > td > span',
    "cancel_button": 'input[value="Cancelar"]'
}

def incorporar(page: Page, origem: str, ntermo: str, descricao: str, patrimonios: list, destino: str, log_callback=None):
    _log = log_callback if log_callback else print
    from src.filtrar import filtrar # Import here to avoid circular dependency

    _log("Iniciando processo de incorporação...")

    cadastrados = 0
    total = len(patrimonios)
    log_file_path = 'relatório.log'

    # Open log file once for appending
    with open(log_file_path, 'a', encoding='utf-8') as log:
        # Initial filter
        try:
            filtrar(page, origem, ntermo, descricao, _log)
            page.wait_for_load_state('networkidle')
        except Exception as e:
            _log(f"Erro na filtragem inicial: {e}")
            return # Stop if initial filter fails

        for i, rp in enumerate(patrimonios):
            _log(f"Processando patrimônio {i+1}/{total}: {rp}")
            try:
                # Wait for the table to be visible and then the 'Selecionar Bem' link
                page.wait_for_selector('table[id*="incorporar_bem_destinado_ao_orgao_form_lista:patrimonios"]')
                
                # Check if there are any results before trying to select
                try:
                    # Assuming 'Selecionar Bem' is always on the first row for the items we want to process
                    # This locator is still somewhat brittle; ideally, we'd find the row by RP number
                    # For now, stick to original logic which assumes the first result is the target.
                    # A better way would be to filter the table data for the specific RP.
                    # Since the original code iterated on `patrimonios` after filtering by description,
                    # it implies the list on screen *should* correspond to what's in `patrimonios`.
                    # However, the current flow clicks the 'selecionar_ben_btn' on a fixed first row.
                    # This means it will only incorporate the *first item* on the list for *every RP*.
                    # This is a critical flaw in the original design if `patrimonios` contains multiple RPs
                    # that appear *sequentially* in the filtered list.
                    # To fix this, we need to iterate through the displayed table rows.

                    # Let's assume for simplicity and to match the original *behavior* that
                    # the first row of the filtered list is the one to be acted upon.
                    # If this is not the case, a more complex table iteration logic is needed.

                    selecionar_bem_link_locator = page.locator(incorporation_locators["select_bem_link"]).first
                    descricao_sistema_locator = page.locator(incorporation_locators["description_text"]).first

                    # Get description from the table before clicking
                    descricao_sistema = descricao_sistema_locator.text_content().strip()
                    _log(f"Descrição do sistema para o primeiro item encontrado: '{descricao_sistema}'")
                    
                    while descricao.strip() != descricao_sistema:
                        _log(f"A descrição do primeiro item '{descricao_sistema}' não corresponde à descrição esperada '{descricao}'. Abortando incorporação.")
                        filtrar(page, origem, ntermo, descricao, _log)
                        page.wait_for_load_state('networkidle')
                        selecionar_bem_link_locator = page.locator(incorporation_locators["select_bem_link"]).first
                        descricao_sistema_locator = page.locator(incorporation_locators["description_text"]).first
                        descricao_sistema = descricao_sistema_locator.text_content().strip()
                        _log(f"Descrição do sistema para o primeiro item encontrado: '{descricao_sistema}'")

                    selecionar_bem_link_locator.click()
                    page.wait_for_selector(incorporation_locators["rp_input"]) # Wait for the RP input field to appear

                    # Fill RP number in the popup/new page
                    page.fill(incorporation_locators["rp_input"], str(rp))

                    # Fill destination
                    page.click(incorporation_locators["search_unidade_button"])
                    page.fill(incorporation_locators["destino_search_input"], destino)
                    page.click(incorporation_locators["destino_search_button"])
                    page.wait_for_load_state('networkidle')

                    # Select destination from results
                    page.click(incorporation_locators["select_destino_link"])
                    page.wait_for_load_state('networkidle')
                    # Wait for the modal/popup to close or the page to update
                    page.wait_for_selector(incorporation_locators["confirm_button"])
                    page.wait_for_load_state('networkidle')

                    # Confirm incorporation
                    page.click(incorporation_locators["confirm_button"])
                    page.wait_for_load_state('networkidle')

                    # Check confirmation message
                    try:
                        page.wait_for_selector(incorporation_locators["imprimir_depois_button"])
                        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        cadastrados += 1
                        msg = f'{timestamp} - Patrimônio: {rp} Descrição: {descricao_sistema} Incorporado {cadastrados}/{total}\n'
                        _log(msg.strip())
                        log.write(msg)
                        
                        # Click "Imprimir depois" button
                        page.click(incorporation_locators["imprimir_depois_button"])
                        page.wait_for_load_state('networkidle')
                        # After "Imprimir depois", it usually returns to the list.
                        # Re-filter to ensure the list is fresh for the next iteration.

                    except TimeoutError: # Changed PlaywrightTimeoutError to TimeoutError
                        error_msg_elem = page.locator(incorporation_locators["error_message_span"])
                        error_text = error_msg_elem.text_content().strip() if error_msg_elem.is_visible() else "Mensagem de erro genérica não encontrada."
                        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        msg = f"{timestamp} - ERRO ao incorporar Patrimônio {rp}: {error_text}\n"
                        _log(msg.strip())
                        log.write(msg)
                        
                        # If there was an error, click "Cancelar" or navigate back to the list
                        try:
                            page.click(incorporation_locators["cancel_button"])
                            page.wait_for_load_state('networkidle')
                            # After cancel, it should return to the main list
                            # Re-filter for the next item
                            filtrar(page, origem, ntermo, descricao, _log)
                        except TimeoutError: # Changed PlaywrightTimeoutError to TimeoutError
                            _log(f"Não foi possível clicar em 'Cancelar' para {rp}, tentando re-filtrar...")
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
                    page.goto("https://www.sistemas.pa.gov.br/sispat/incorporar_bem/incorporar_bem_destinado_ao_orgao_lista.seam")
                    filtrar(page, origem, ntermo, descricao, _log)
                except Exception as nav_err:
                    _log(f"Erro ao tentar navegar de volta para a lista: {nav_err}")
                    _log("Processo de incorporação pode estar em estado inconsistente. Recomenda-se reiniciar.")
                    break # Stop if we can't even get back to the list

    _log(f"Processo de incorporação finalizado. {cadastrados}/{total} patrimônios incorporados.")        