"""
Controlador do Playwright para automação do navegador.
Gerencia login, navegação e interações com o sistema QualiWork.
Usa API assíncrona do Playwright para compatibilidade com FastAPI.
"""
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from typing import List, Dict, Optional
import asyncio


class PlaywrightController:
    """Controla automação do navegador usando Playwright (API assíncrona)."""
    
    def __init__(self, headless: bool = True):
        """
        Inicializa o controlador do Playwright.
        
        Args:
            headless: Se True, executa sem exibir navegador
        """
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.headless = headless
        self._initialized = False
    
    async def initialize(self):
        """Inicializa o Playwright e o navegador."""
        if self._initialized:
            return
        
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled']
        )
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        self.page = await self.context.new_page()
        self._initialized = True
    
    async def login(self, email: str, password: str) -> bool:
        """
        Realiza login no sistema.
        
        Args:
            email: Email do usuário
            password: Senha do usuário
            
        Returns:
            True se login foi bem-sucedido, False caso contrário
        """
        if not self._initialized:
            await self.initialize()
        
        try:
            # Navega para página de login
            await self.page.goto("https://qualiwork.qualiit.com.br/Login", wait_until="networkidle")
            await asyncio.sleep(1)
            
            # Preenche campos de login usando XPaths específicos
            # Aguarda campos aparecerem
            email_input = self.page.locator('xpath=//*[@id="inputEmail"]')
            await email_input.wait_for(state="visible", timeout=10000)
            await email_input.fill(email)
            
            await asyncio.sleep(0.5)
            
            password_input = self.page.locator('xpath=//*[@id="inputPassword"]')
            await password_input.wait_for(state="visible", timeout=10000)
            await password_input.fill(password)
            
            await asyncio.sleep(0.5)
            
            # Clica no botão de login
            login_selectors = [
                'button:has-text("ENTRAR")',
                'button:has-text("Entrar")',
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Login")'
            ]
            
            login_clicked = False
            for selector in login_selectors:
                try:
                    login_button = self.page.locator(selector).first
                    count = await login_button.count()
                    if count > 0:
                        await login_button.click()
                        login_clicked = True
                        break
                except:
                    continue
            
            if not login_clicked:
                raise Exception("Não foi possível encontrar botão de login")
            
            # Aguarda redirecionamento ou verifica se login foi bem-sucedido
            await self.page.wait_for_load_state("networkidle", timeout=10000)
            await asyncio.sleep(2)
            
            # Verifica se está logado (URL mudou ou elemento específico apareceu)
            current_url = self.page.url
            apontamentos_locator = self.page.locator('text="Apontamentos"')
            apontamentos_count = await apontamentos_locator.count()
            if "Login" not in current_url or apontamentos_count > 0:
                return True
            
            return False
        except Exception as e:
            print(f"Erro durante login: {e}")
            return False
    
    async def navigate_to_apontamentos(self, month: int = None, year: int = None) -> bool:
        """
        Navega para a página de apontamentos.
        
        Args:
            month: Mês (1-12) - opcional, se fornecido navega direto com parâmetro
            year: Ano (ex: 2026) - opcional, se fornecido navega direto com parâmetro
        
        Returns:
            True se navegação foi bem-sucedida, False caso contrário
        """
        try:
            if month and year:
                # Navega diretamente com parâmetro mesAno na URL
                month_year_str = f"{month:02d}/{year}"
                url = f"https://qualiwork.qualiit.com.br/Apontamentos/Apontar/?mesAno={month_year_str}"
                await self.page.goto(url, wait_until="networkidle")
            else:
                # Navega para página padrão
                await self.page.goto("https://qualiwork.qualiit.com.br/Apontamentos", wait_until="networkidle")
            
            await asyncio.sleep(2)
            return True
        except Exception as e:
            print(f"Erro ao navegar para apontamentos: {e}")
            return False
    
    async def select_month_year(self, month: int, year: int) -> bool:
        """
        Seleciona mês e ano navegando diretamente pela URL.
        
        Args:
            month: Mês (1-12)
            year: Ano (ex: 2026)
            
        Returns:
            True se seleção foi bem-sucedida, False caso contrário
        """
        try:
            # Formata mês/ano como MM/AAAA
            month_year_str = f"{month:02d}/{year}"
            
            # Navega diretamente com o parâmetro na URL
            url = f"https://qualiwork.qualiit.com.br/Apontamentos/Apontar/?mesAno={month_year_str}"
            await self.page.goto(url, wait_until="networkidle")
            await asyncio.sleep(2)
            
            return True
        except Exception as e:
            print(f"Erro ao selecionar mês/ano: {e}")
            return False
    
    async def click_fazer_apontamento(self) -> bool:
        """
        Clica no botão "Fazer Apontamento".
        
        Returns:
            True se clique foi bem-sucedido, False caso contrário
        """
        try:
            # Localiza o botão pelo XPath fornecido
            button = self.page.locator('xpath=//*[@id="btnFazerApontamento"]')
            await button.click()
            await asyncio.sleep(2)  # Aguarda modal aparecer
            
            return True
        except Exception as e:
            print(f"Erro ao clicar em Fazer Apontamento: {e}")
            return False
    
    async def get_available_tasks(self) -> List[Dict[str, str]]:
        """
        Extrai lista de tarefas disponíveis da tabela no modal.
        Aguarda o modal aparecer automaticamente ao acessar a URL com mesAno.
        
        Returns:
            Lista de dicionários com informações das tarefas:
            [
                {
                    'proposta': '...',
                    'cliente': '...',
                    'projeto': '...',
                    'tarefa': '...',
                    'horas_liberadas': '...',
                    'horas_apontadas': '...',
                    'saldo': '...'
                },
                ...
            ]
        """
        tasks = []
        try:
            # Aguarda a página carregar completamente
            await self.page.wait_for_load_state("networkidle", timeout=15000)
            await asyncio.sleep(2)
            
            # Aguarda o modal aparecer usando o XPath específico
            modal_container = self.page.locator('xpath=//*[@id="zoomTarefas"]')
            await modal_container.wait_for(state="visible", timeout=15000)
            print("Modal de tarefas encontrado")
            
            # Aguarda a tabela dentro do modal aparecer
            table = self.page.locator('xpath=//*[@id="tbTarefasRecurso"]')
            await table.wait_for(state="visible", timeout=10000)
            print("Tabela de tarefas encontrada")
            
            await asyncio.sleep(1)
            
            # Extrai linhas da tabela
            rows = await table.locator('tbody tr').all()
            if len(rows) == 0:
                # Tenta sem tbody
                rows = await table.locator('tr').all()
                # Remove cabeçalho se existir
                if len(rows) > 0:
                    rows = rows[1:] if len(rows) > 1 else rows
            
            print(f"Encontradas {len(rows)} linhas na tabela")
            
            # Extrai cada linha
            for i, row in enumerate(rows, start=1):
                try:
                    cells = await row.locator('td').all()
                    
                    if len(cells) >= 7:
                        # Extrai texto de cada célula
                        proposta = (await cells[0].inner_text()).strip() if len(cells) > 0 else ""
                        cliente = (await cells[1].inner_text()).strip() if len(cells) > 1 else ""
                        projeto = (await cells[2].inner_text()).strip() if len(cells) > 2 else ""
                        tarefa = (await cells[3].inner_text()).strip() if len(cells) > 3 else ""
                        horas_liberadas = (await cells[4].inner_text()).strip() if len(cells) > 4 else ""
                        horas_apontadas = (await cells[5].inner_text()).strip() if len(cells) > 5 else ""
                        saldo = (await cells[6].inner_text()).strip() if len(cells) > 6 else ""
                        
                        # Só adiciona se tiver dados válidos
                        if proposta or cliente or projeto:
                            task_info = {
                                'proposta': proposta,
                                'cliente': cliente,
                                'projeto': projeto,
                                'tarefa': tarefa,
                                'horas_liberadas': horas_liberadas,
                                'horas_apontadas': horas_apontadas,
                                'saldo': saldo
                            }
                            tasks.append(task_info)
                            print(f"Tarefa {i} extraída: {proposta} - {cliente} - {projeto}")
                except Exception as e:
                    print(f"Erro ao extrair linha {i}: {e}")
                    import traceback
                    traceback.print_exc()
                    continue
            
            print(f"Total de tarefas extraídas: {len(tasks)}")
            return tasks
        except Exception as e:
            print(f"Erro ao extrair tarefas: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    async def select_task(self, task_index: int = 0) -> bool:
        """
        Seleciona uma tarefa da tabela pelo índice.
        Clica na coluna do projeto (td[3]) conforme especificado.
        
        Args:
            task_index: Índice da tarefa na lista (0-based, começa em 1 no XPath)
            
        Returns:
            True se seleção foi bem-sucedida, False caso contrário
        """
        try:
            # XPath usa índice baseado em 1, então adiciona 1 ao task_index
            xpath_index = task_index + 1
            
            # Clica na coluna do projeto (td[3]) conforme especificado
            task_cell = self.page.locator(f'xpath=//*[@id="tbTarefasRecurso"]/tbody/tr[{xpath_index}]/td[3]')
            
            # Aguarda célula estar visível
            await task_cell.wait_for(state="visible", timeout=10000)
            
            count = await task_cell.count()
            if count > 0:
                await task_cell.click()
                await asyncio.sleep(2)  # Aguarda página carregar após seleção
                return True
            
            return False
        except Exception as e:
            print(f"Erro ao selecionar tarefa: {e}")
            return False
    
    async def fill_time_entry(self, date: str, start: str, end: str, description: str, row_index: int = 0) -> bool:
        """
        Preenche uma entrada de horário usando XPaths específicos.
        
        Args:
            date: Data no formato DD/MM/AAAA ou DDMMAAAA
            start: Hora de início no formato HH:MM
            end: Hora de fim no formato HH:MM
            description: Descrição do apontamento
            row_index: Índice da linha (0 para linhaH0, 1 para linhaH1, etc.)
            
        Returns:
            True se preenchimento foi bem-sucedido, False caso contrário
        """
        try:
            print(f"[PlaywrightController] Preenchendo linha {row_index}: {date} {start}-{end}")
            
            # Normaliza formato da data
            if len(date) == 8 and '/' not in date:
                # Formato DDMMAAAA
                date = f"{date[:2]}/{date[2:4]}/{date[4:]}"
            
            # Determina o ID da linha baseado no índice
            # linhaH0 para primeira linha, linhaH1 para segunda, etc.
            linha_id = f"linhaH{row_index}"
            
            # XPaths específicos conforme fornecido
            date_xpath = f'xpath=//*[@id="{linha_id}"]/td[1]/input[3]'
            start_xpath = f'xpath=//*[@id="{linha_id}"]/td[2]/input'
            end_xpath = f'xpath=//*[@id="{linha_id}"]/td[3]/input'
            desc_xpath = f'xpath=//*[@id="{linha_id}"]/td[4]/textarea'
            
            # Aguarda campos aparecerem e preenche
            print(f"[PlaywrightController] Aguardando campo de data...")
            date_input = self.page.locator(date_xpath)
            await date_input.wait_for(state="visible", timeout=10000)
            await date_input.click()
            await asyncio.sleep(0.3)
            await date_input.fill(date)
            print(f"[PlaywrightController] Data preenchida: {date}")
            await asyncio.sleep(0.5)
            
            print(f"[PlaywrightController] Preenchendo horário de início...")
            start_input = self.page.locator(start_xpath)
            await start_input.wait_for(state="visible", timeout=10000)
            await start_input.click()
            await asyncio.sleep(0.3)
            await start_input.fill(start)
            print(f"[PlaywrightController] Início preenchido: {start}")
            await asyncio.sleep(0.5)
            
            print(f"[PlaywrightController] Preenchendo horário de fim...")
            end_input = self.page.locator(end_xpath)
            await end_input.wait_for(state="visible", timeout=10000)
            await end_input.click()
            await asyncio.sleep(0.3)
            await end_input.fill(end)
            print(f"[PlaywrightController] Fim preenchido: {end}")
            await asyncio.sleep(0.5)
            
            print(f"[PlaywrightController] Preenchendo descrição...")
            desc_input = self.page.locator(desc_xpath)
            await desc_input.wait_for(state="visible", timeout=10000)
            await desc_input.click()
            await asyncio.sleep(0.3)
            await desc_input.fill(description)
            print(f"[PlaywrightController] Descrição preenchida: {description[:50]}...")
            await asyncio.sleep(0.5)
            
            print(f"[PlaywrightController] ✓ Linha {row_index} preenchida com sucesso!")
            return True
        except Exception as e:
            print(f"[PlaywrightController] ERRO ao preencher entrada: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def add_new_entry_row(self) -> bool:
        """
        Adiciona uma nova linha para preenchimento (segunda entrada do dia).
        
        Returns:
            True se adicionou com sucesso, False caso contrário
        """
        try:
            # Procura por botão de adicionar linha ou similar
            # Pode ser um botão "+" ou similar
            add_button = self.page.locator('button:has-text("+"), button[title*="Adicionar"], button[aria-label*="Adicionar"]').first
            count = await add_button.count()
            if count > 0:
                await add_button.click()
                await asyncio.sleep(1)
                return True
            
            # Se não encontrar botão, pode ser que precise clicar em uma área específica
            # ou a linha seja adicionada automaticamente
            return True
        except Exception as e:
            print(f"Erro ao adicionar nova linha: {e}")
            return False
    
    async def save_entry(self) -> bool:
        """
        Salva a entrada preenchida.
        NOTA: Este método apenas localiza o botão, mas NÃO clica nele.
        O salvamento deve ser feito manualmente pelo usuário para verificação.
        
        Returns:
            True se o botão foi encontrado, False caso contrário
        """
        try:
            print("[PlaywrightController] Localizando botão de salvar...")
            # Localiza botão de salvar
            save_button = self.page.locator('button:has-text("SALVAR"), button[type="submit"], button:has-text("Salvar")').first
            count = await save_button.count()
            
            if count > 0:
                print("[PlaywrightController] ✓ Botão de salvar encontrado! (aguardando salvamento manual)")
                # NÃO clica automaticamente - deixa o usuário salvar manualmente
                # await save_button.click()
                # await asyncio.sleep(2)  # Aguarda salvamento
                return True
            else:
                print("[PlaywrightController] AVISO: Botão de salvar não encontrado")
                return False
        except Exception as e:
            print(f"[PlaywrightController] ERRO ao localizar botão de salvar: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def show_browser(self):
        """Torna o navegador visível (se estava em modo headless)."""
        if self.headless and self.browser:
            # Não é possível mudar de headless para visível em tempo de execução
            # Mas podemos garantir que não está em headless na próxima inicialização
            self.headless = False
    
    async def close(self):
        """Fecha o navegador e limpa recursos."""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            self._initialized = False
        except Exception as e:
            print(f"Erro ao fechar navegador: {e}")
