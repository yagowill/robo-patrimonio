import re
from playwright.sync_api import Page, TimeoutError
from datetime import datetime

# O prefixo comum para os 'name'/'id' dos campos dentro do formulário/modal de recebimento.
RECEIVE_FORM_PREFIX = 'entidade_form_cad2'

receive_locators = {
    # Selector para o link "Receber" na lista principal (fora do modal).
    "receive_transfer_link": 'a[title*="Receber Termo de Movimentação"]',
    
    # Seletor exato para o botão que abre o calendário (a imagem).
    "calendar_button": f'img[id="{RECEIVE_FORM_PREFIX}:dataRecebimentoPopupButton"]', 
    
    # Seletor exato para o botão "Today" dentro do calendário.
    # Lembre-se de verificar se o texto é "Today" ou "Hoje" na sua interface.
    "today_button": 'div.rich-calendar-tool-btn:has-text("Today")', 
    
    # Seletor exato para o botão "Receber" dentro do modal.
    "confirm_receive_button": f'input[id="{RECEIVE_FORM_PREFIX}:receber"][value="Receber"]',
    
    # CORRIGIDO: Seletor para a mensagem de sucesso, usando .first para resolver a strict mode violation.
    # O seletor em si é bom, mas como há múltiplos, pegamos o primeiro.
    "success_message": 'span.rich-messages-label:has-text("recebido com sucesso.")' 
}

def receber(page: Page, log_callback=None):
    _log = log_callback if log_callback else print
    _log("Iniciando processo de recebimento de distribuídos...")

    while True:
        try:
            # Esperar por qualquer link "Receber" disponível.
            page.wait_for_selector(receive_locators["receive_transfer_link"], timeout=5000) 

            # Clicar no primeiro link "Receber" encontrado.
            page.click(receive_locators["receive_transfer_link"])
            # Esperar que o modal carregue, verificando a visibilidade de um elemento dentro dele.
            page.wait_for_selector(f'input[id="{RECEIVE_FORM_PREFIX}:dataRecebimentoInputDate"]', state='visible')
            _log("Modal de recebimento aberto.")

            # Clicar no botão do calendário (imagem).
            page.click(receive_locators["calendar_button"])
            _log("Botão do calendário clicado.")
            
            # Clicar no botão "Today" dentro do calendário.
            page.wait_for_selector(receive_locators["today_button"], state='visible')
            page.click(receive_locators["today_button"])
            # Pequena pausa para garantir que a data foi selecionada.
            page.wait_for_timeout(500) 
            _log("Data 'Hoje' selecionada no calendário.")

            # Clicar no botão "Receber" dentro do modal.
            page.click(receive_locators["confirm_receive_button"])
            # Após clicar no botão "Receber" do modal, esperar por um estado de rede estável.
            page.wait_for_load_state('networkidle')
            _log("Botão 'Receber' no modal clicado.")

            # Verificar a mensagem de confirmação.
            # CORREÇÃO AQUI: Use .first para pegar o primeiro elemento correspondente.
            page.wait_for_selector(receive_locators["success_message"], state='visible')
            confirmacao_text = page.locator(receive_locators["success_message"]).first.text_content() # ADDED .first()
            
            # Usar re.search para encontrar "recebido com sucesso." em qualquer parte do texto.
            if re.search("recebido com sucesso.", confirmacao_text):
                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                msg = f'{timestamp} {confirmacao_text.strip()}'
                _log(msg)
                # A página deve ter retornado à lista de termos.
                page.wait_for_load_state('networkidle')
            else:
                _log(f"Erro inesperado no recebimento. Mensagem: {confirmacao_text.strip()}")
                break

        except TimeoutError:
            _log("Nenhum termo de transferência não recebido encontrado. Processo concluído ou sem mais itens.")
            break 
        except Exception as e:
            _log(f"Erro inesperado durante o recebimento: {e}")
            try:
                page.goto("https://www.sistemas.pa.gov.br/sispat/movimentacao_bem/recebimento/recebimento_termo_bem_interno_operacional_lista.seam")
                page.wait_for_load_state('networkidle')
                _log("Tentou retornar à lista de termos após um erro.")
            except Exception as nav_err:
                _log(f"Erro ao tentar navegar de volta para a lista: {nav_err}")
            break 

    _log("Processo de recebimento finalizado.")