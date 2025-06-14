import PySide6.QtWidgets as QtWidgets
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
from src.sispat import GovernoDigital
from src.incorporar import incorporar
from src.receber import receber
from src import db_manager # Import the new database manager
import sys

class AutomationWorker(QtCore.QThread):
    """Worker thread to run automation tasks without freezing the GUI."""
    log_signal = QtCore.Signal(str)
    finished_signal = QtCore.Signal()
    error_signal = QtCore.Signal(str)

    def __init__(self, sispat_automation, task_type, **kwargs):
        super().__init__()
        self.sispat_automation = sispat_automation
        self.task_type = task_type
        self.kwargs = kwargs
        self.running = False

    def run(self):
        self.running = True
        try:
            # Start browser and login only once per worker run
            if not self.sispat_automation.page:
                self.sispat_automation.start_browser()
                self.sispat_automation.login()

            if self.task_type == "incorporar":
                self.sispat_automation.navigate_to_nao_incorporado()
                incorporar(
                    page=self.sispat_automation.page,
                    origem=self.kwargs['origem'],
                    ntermo=self.kwargs['ntermo'],
                    descricao=self.kwargs['descricao'],
                    patrimonios=self.kwargs['patrimonios'],
                    destino=self.kwargs['destino'],
                    log_callback=self.log_signal.emit
                )
            elif self.task_type == "receber":
                self.sispat_automation.navigate_to_dist_nao_recebido()
                receber(
                    page=self.sispat_automation.page,
                    log_callback=self.log_signal.emit
                )
            else:
                self.error_signal.emit(f"Tipo de tarefa desconhecido: {self.task_type}")

        except Exception as e:
            error_message = f"Erro na automação: {e}"
            self.log_signal.emit(error_message)
            self.error_signal.emit(error_message)
        finally:
            self.sispat_automation.stop_browser()
            self.running = False
            self.finished_signal.emit()

class PatrimonyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Robô Patrimônio')
        self.setGeometry(100, 100, 1000, 700) # Increased size for log output

        self.rps_value = []
        
        # Load data from database
        self.orgaos = db_manager.get_orgaos()
        self.destinos = db_manager.get_unidades_localizacao()
        
        self.worker = None
        self.sispat_automation = GovernoDigital(log_callback=self.append_log)

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QtWidgets.QHBoxLayout(main_widget)

        # Left Column (Form Inputs)
        left_column = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()

        self.origem_combo = QtWidgets.QComboBox()
        self.origem_combo.addItems(self.orgaos)
        # Set default value by text, safer than index if DB order changes
        if 'Todos' in self.orgaos:
            self.origem_combo.setCurrentText('Todos')
        else:
            self.origem_combo.setCurrentIndex(0) # Fallback

        form_layout.addRow('Órgão Origem:', self.origem_combo)

        self.ntermo_input = QtWidgets.QLineEdit()
        form_layout.addRow('Nº do Termo:', self.ntermo_input)

        self.descricao_input = QtWidgets.QLineEdit()
        form_layout.addRow('Descrição:', self.descricao_input)

        self.destino_combo = QtWidgets.QComboBox()
        self.destino_combo.addItems(self.destinos)
        # Set default value by text for 'UNIDADE DE PATRIMONIO'
        if 'UNIDADE DE PATRIMONIO' in self.destinos:
            self.destino_combo.setCurrentText('UNIDADE DE PATRIMONIO')
        else:
            self.destino_combo.setCurrentIndex(0) # Fallback

        form_layout.addRow('Destino:', self.destino_combo)

        left_column.addLayout(form_layout)
        left_column.addStretch() # Push buttons to bottom

        button_layout = QtWidgets.QHBoxLayout()
        self.clear_button = QtWidgets.QPushButton('Limpar')
        self.clear_button.setStyleSheet("background-color: gray; color: white;")
        self.remove_button = QtWidgets.QPushButton('Remover')
        self.remove_button.setStyleSheet("background-color: red; color: white;")
        self.incorporar_button = QtWidgets.QPushButton('Incorporar')
        self.incorporar_button.setStyleSheet("background-color: green; color: white;")

        button_layout.addStretch()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.incorporar_button)
        left_column.addLayout(button_layout)

        main_layout.addLayout(left_column)

        # Right Column (RPS List)
        right_column = QtWidgets.QVBoxLayout()

        rp_input_layout = QtWidgets.QHBoxLayout()
        self.rp_input = QtWidgets.QLineEdit()
        self.add_rp_button = QtWidgets.QPushButton('Adicionar')
        rp_input_layout.addWidget(self.rp_input)
        rp_input_layout.addWidget(self.add_rp_button)
        right_column.addLayout(rp_input_layout)

        self.rps_listbox = QtWidgets.QListWidget()
        self.rps_listbox.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        right_column.addWidget(self.rps_listbox)

        self.added_rps_label = QtWidgets.QLabel('0 rps adicionados')
        right_column.addWidget(self.added_rps_label)

        main_layout.addLayout(right_column)
        
        # Log Output (Below both columns)
        bottom_layout = QtWidgets.QVBoxLayout()
        
        self.log_text_edit = QtWidgets.QTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setMinimumHeight(150)
        bottom_layout.addWidget(QtWidgets.QLabel('Log de Operações:'))
        bottom_layout.addWidget(self.log_text_edit)

        # Receive Section
        receive_group_box = QtWidgets.QGroupBox('Receber')
        receive_layout = QtWidgets.QHBoxLayout(receive_group_box)
        receive_layout.addWidget(QtWidgets.QLabel('Distribuídos não recebidos:'))
        receive_layout.addStretch()
        self.receive_button = QtWidgets.QPushButton('Receber')
        receive_layout.addWidget(self.receive_button)
        bottom_layout.addWidget(receive_group_box)
        
        # Add bottom layout to main layout
        main_layout.addLayout(bottom_layout)


    def _connect_signals(self):
        self.add_rp_button.clicked.connect(self._add_rp)
        self.clear_button.clicked.connect(self._clear_rps)
        self.remove_button.clicked.connect(self._remove_rps)
        self.incorporar_button.clicked.connect(self._start_incorporar_task)
        self.receive_button.clicked.connect(self._start_receber_task)

    def _add_rp(self):
        rps_input_text = self.rp_input.text()
        if not rps_input_text.strip():
            return

        added_count = 0
        if ':' in rps_input_text:
            try:
                start, end = map(int, rps_input_text.split(':'))
                for i in range(start, end + 1):
                    rp_str = str(i)
                    if rp_str not in self.rps_value:
                        self.rps_value.append(rp_str)
                        added_count += 1
            except ValueError:
                QtWidgets.QMessageBox.warning(self, 'Erro', 'Formato de sequência inválido. Use "inicio:fim" com números.')
        elif ',' in rps_input_text:
            for rps_part in rps_input_text.split(','):
                rp = rps_part.strip()
                if rp and rp not in self.rps_value:
                    self.rps_value.append(rp)
                    added_count += 1
        elif '\n' in rps_input_text: # Handle pasted multiline input
            for rps_line in rps_input_text.split('\n'):
                rp = rps_line.strip()
                if rp and rp not in self.rps_value:
                    self.rps_value.append(rp)
                    added_count += 1
        else:
            rp = rps_input_text.strip()
            if rp and rp not in self.rps_value:
                self.rps_value.append(rp)
                added_count += 1
        
        if added_count > 0:
            self._update_rps_list()
            self.rp_input.clear()

    def _remove_rps(self):
        selected_items = self.rps_listbox.selectedItems()
        if not selected_items:
            return

        items_to_remove = [item.text() for item in selected_items]
        self.rps_value = [rp for rp in self.rps_value if rp not in items_to_remove]
        self._update_rps_list()

    def _clear_rps(self):
        self.rps_value = []
        self._update_rps_list()
        self.rp_input.clear()
        self.append_log("Lista de RPs limpa.")

    def _update_rps_list(self):
        self.rps_listbox.clear()
        self.rps_listbox.addItems(sorted(self.rps_value))
        self.added_rps_label.setText(f'{len(self.rps_value)} rps adicionados')

    def append_log(self, message):
        """Appends a message to the log QTextEdit."""
        self.log_text_edit.append(message)
        # Scroll to bottom automatically
        self.log_text_edit.verticalScrollBar().setValue(self.log_text_edit.verticalScrollBar().maximum())

    def _disable_ui(self):
        self.incorporar_button.setEnabled(False)
        self.receive_button.setEnabled(False)
        self.add_rp_button.setEnabled(False)
        self.remove_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.append_log("Automação iniciada. UI desabilitada temporariamente.")

    def _enable_ui(self):
        self.incorporar_button.setEnabled(True)
        self.receive_button.setEnabled(True)
        self.add_rp_button.setEnabled(True)
        self.remove_button.setEnabled(True)
        self.clear_button.setEnabled(True)
        self.append_log("Automação finalizada. UI habilitada.")

    def _on_automation_finished(self):
        self.worker = None # Clear worker reference
        self._enable_ui()
        self.append_log("--- Fim da Tarefa de Automação ---")

    def _on_automation_error(self, message):
        self.append_log(f"ERRO CRÍTICO NA AUTOMAÇÃO: {message}")
        QtWidgets.QMessageBox.critical(self, "Erro de Automação", f"Ocorreu um erro crítico na automação: {message}\nVerifique o log para detalhes.")

    def _start_incorporar_task(self):
        if self.worker and self.worker.isRunning():
            QtWidgets.QMessageBox.warning(self, "Aviso", "Uma tarefa de automação já está em execução.")
            return

        if not self.rps_value:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Nenhum RP adicionado para incorporar.")
            return

        self.append_log("--- Iniciando Tarefa de Incorporação ---")
        self._disable_ui()

        self.worker = AutomationWorker(
            self.sispat_automation,
            "incorporar",
            origem=self.origem_combo.currentText(),
            ntermo=self.ntermo_input.text(),
            descricao=self.descricao_input.text(),
            patrimonios=self.rps_value,
            destino=self.destino_combo.currentText()
        )
        self.worker.log_signal.connect(self.append_log)
        self.worker.finished_signal.connect(self._on_automation_finished)
        self.worker.error_signal.connect(self._on_automation_error)
        self.worker.start()

    def _start_receber_task(self):
        if self.worker and self.worker.isRunning():
            QtWidgets.QMessageBox.warning(self, "Aviso", "Uma tarefa de automação já está em execução.")
            return

        self.append_log("--- Iniciando Tarefa de Recebimento ---")
        self._disable_ui()

        self.worker = AutomationWorker(
            self.sispat_automation,
            "receber"
        )
        self.worker.log_signal.connect(self.append_log)
        self.worker.finished_signal.connect(self._on_automation_finished)
        self.worker.error_signal.connect(self._on_automation_error)
        self.worker.start()

    def closeEvent(self, event):
        """Handle window close event to stop the worker thread if running."""
        if self.worker and self.worker.isRunning():
            reply = QtWidgets.QMessageBox.question(self, 'Confirmação',
                                                   "A automação está em andamento. Deseja realmente fechar e interromper?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.worker.terminate() # Force terminate the thread (use with caution)
                self.worker.wait()      # Wait for it to finish (or timeout)
                self.sispat_automation.stop_browser() # Ensure browser is closed
                event.accept()
            else:
                event.ignore()
        else:
            self.sispat_automation.stop_browser() # Ensure browser is closed
            event.accept()


if __name__ == '__main__':
    # This block allows testing the GUI directly
    app = QtWidgets.QApplication(sys.argv)
    window = PatrimonyApp()
    window.show()
    sys.exit(app.exec())