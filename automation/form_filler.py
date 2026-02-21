"""
Orquestrador de preenchimento de formulários.
Gerencia o preenchimento de múltiplas datas com validações.
Usa API assíncrona do Playwright.
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import asyncio
from automation.playwright_controller import PlaywrightController
from utils.time_generator import generate_daily_hours, validate_hours


class FormFiller:
    """Orquestra o preenchimento de apontamentos."""
    
    def __init__(self, controller: PlaywrightController):
        """
        Inicializa o preenchedor de formulários.
        
        Args:
            controller: Instância do PlaywrightController
        """
        self.controller = controller
    
    async def fill_date_range(self, start_date: datetime, end_date: datetime,
                       task_index: int, description_morning: str,
                       description_afternoon: str, 
                       callback=None,
                       description_morning_by_date=None,
                       description_afternoon_by_date=None) -> Dict[str, any]:
        """
        Preenche apontamentos para um intervalo de datas.
        
        Args:
            start_date: Data inicial
            end_date: Data final
            task_index: Índice da tarefa selecionada
            description_morning: Descrição para entrada da manhã
            description_afternoon: Descrição para entrada da tarde
            callback: Função de callback para atualizar progresso (opcional)
            
        Returns:
            Dicionário com resultados:
            {
                'success': bool,
                'filled_dates': List[str],
                'errors': List[str],
                'total_entries': int
            }
        """
        results = {
            'success': True,
            'filled_dates': [],
            'errors': [],
            'total_entries': 0
        }
        
        # Gera lista de datas
        current_date = start_date
        dates_to_fill = []
        
        while current_date <= end_date:
            # Pula finais de semana (sábado=5, domingo=6)
            if current_date.weekday() < 5:  # Segunda a sexta
                dates_to_fill.append(current_date)
            current_date += timedelta(days=1)
        
        total_dates = len(dates_to_fill)
        
        try:
            # Navega para apontamentos com mês/ano (usa a primeira data)
            if dates_to_fill:
                first_date = dates_to_fill[0]
                if not await self.controller.navigate_to_apontamentos(first_date.month, first_date.year):
                    results['success'] = False
                    results['errors'].append(f"Erro ao navegar para mês/ano {first_date.month:02d}/{first_date.year}")
                    return results
            else:
                # Se não há datas, apenas navega
                if not await self.controller.navigate_to_apontamentos():
                    results['success'] = False
                    results['errors'].append("Erro ao navegar para página de apontamentos")
                    return results
            
            # Seleciona tarefa diretamente da tabela (não precisa clicar em "Fazer Apontamento")
            # A navegação já carregou as tarefas
            if not await self.controller.select_task(task_index):
                results['success'] = False
                results['errors'].append(f"Erro ao selecionar tarefa no índice {task_index}")
                return results
            
            # Após selecionar a tarefa, pode ser necessário clicar em "Fazer Apontamento" 
            # ou a página já redireciona. Vamos tentar clicar se o botão existir
            try:
                fazer_apontamento_btn = self.controller.page.locator('xpath=//*[@id="btnFazerApontamento"]')
                count = await fazer_apontamento_btn.count()
                if count > 0:
                    await fazer_apontamento_btn.click()
                    await asyncio.sleep(2)
            except:
                # Se não encontrar o botão, continua (pode já estar na página correta)
                pass
            
            # Preenche cada data
            for idx, date in enumerate(dates_to_fill):
                try:
                    print(f"\n[FormFiller] Processando data: {date.strftime('%d/%m/%Y')}")
                    
                    # Gera horários para o dia
                    daily_hours = generate_daily_hours()
                    print(f"[FormFiller] Horários gerados - Manhã: {daily_hours['morning']['start']}-{daily_hours['morning']['end']}, Tarde: {daily_hours['afternoon']['start']}-{daily_hours['afternoon']['end']}")
                    
                    # Valida horários gerados
                    is_valid, error_msg = validate_hours(
                        daily_hours['morning']['start'],
                        daily_hours['morning']['end'],
                        daily_hours['afternoon']['start'],
                        daily_hours['afternoon']['end']
                    )
                    
                    if not is_valid:
                        print(f"[FormFiller] AVISO: {error_msg}, usando horários padrão")
                        # Usa horários padrão válidos (8h exatas) se a validação falhar
                        daily_hours = {
                            'morning': {'start': '09:00', 'end': '12:00'},
                            'afternoon': {'start': '13:00', 'end': '18:00'}
                        }
                        results['errors'].append(f"Data {date.strftime('%d/%m/%Y')}: {error_msg} (usando horários padrão)")
                    
                    # Formata data como DD/MM/AAAA
                    date_str = date.strftime('%d/%m/%Y')
                    
                    # Obtém descrições para este dia específico
                    # Se description_by_date é uma lista de linhas, pega a linha correspondente ao índice
                    day_index = idx
                    desc_morning = description_morning
                    desc_afternoon = description_afternoon
                    
                    if description_morning_by_date:
                        # Se é uma string com múltiplas linhas, pega a linha do dia
                        lines = description_morning_by_date.split('\n')
                        if day_index < len(lines) and lines[day_index].strip():
                            desc_morning = lines[day_index].strip()
                    
                    if description_afternoon_by_date:
                        lines = description_afternoon_by_date.split('\n')
                        if day_index < len(lines) and lines[day_index].strip():
                            desc_afternoon = lines[day_index].strip()
                    
                    # Se descrições estão vazias, usa as padrão
                    if not desc_morning:
                        desc_morning = description_morning
                    if not desc_afternoon:
                        desc_afternoon = description_afternoon
                    
                    # Preenche primeira entrada (manhã) - linha 0 (linhaH0)
                    print(f"[FormFiller] Preenchendo entrada da manhã para {date_str}")
                    if not await self.controller.fill_time_entry(
                        date_str,
                        daily_hours['morning']['start'],
                        daily_hours['morning']['end'],
                        desc_morning,
                        row_index=0
                    ):
                        error_msg = f"Erro ao preencher entrada da manhã para {date_str}"
                        print(f"[FormFiller] ERRO: {error_msg}")
                        results['errors'].append(error_msg)
                        continue
                    print(f"[FormFiller] Entrada da manhã preenchida com sucesso")
                    
                    # Aguarda segunda linha aparecer automaticamente após preencher a primeira
                    # O sistema cria automaticamente uma nova linha quando preenchemos linhaH0
                    await asyncio.sleep(2)  # Aguarda linha ser criada automaticamente
                    
                    # Verifica se a segunda linha (linhaH1) apareceu
                    try:
                        segunda_linha = self.controller.page.locator('xpath=//*[@id="linhaH1"]')
                        await segunda_linha.wait_for(state="visible", timeout=10000)
                    except:
                        # Se não apareceu, tenta adicionar manualmente
                        await self.controller.add_new_entry_row()
                        await asyncio.sleep(1)
                    
                    # Preenche segunda entrada (tarde) - linha 1 (linhaH1)
                    print(f"[FormFiller] Preenchendo entrada da tarde para {date_str}")
                    if not await self.controller.fill_time_entry(
                        date_str,
                        daily_hours['afternoon']['start'],
                        daily_hours['afternoon']['end'],
                        desc_afternoon,
                        row_index=1
                    ):
                        error_msg = f"Erro ao preencher entrada da tarde para {date_str}"
                        print(f"[FormFiller] ERRO: {error_msg}")
                        results['errors'].append(error_msg)
                        continue
                    print(f"[FormFiller] Entrada da tarde preenchida com sucesso")
                    
                    # Verifica se botão de salvar está disponível (salvamento será manual)
                    print(f"[FormFiller] Verificando botão de salvar para {date_str}")
                    save_available = await self.controller.save_entry()
                    if not save_available:
                        print(f"[FormFiller] AVISO: Botão de salvar não encontrado para {date_str}")
                        # Não falha, apenas avisa - o usuário pode salvar manualmente
                    else:
                        print(f"[FormFiller] Botão de salvar disponível - aguardando salvamento manual para {date_str}")
                    
                    # Aguarda um pouco para o usuário verificar e salvar manualmente
                    print(f"[FormFiller] Aguardando 3 segundos para verificação manual...")
                    await asyncio.sleep(3)
                    
                    results['filled_dates'].append(date_str)
                    results['total_entries'] += 2
                    print(f"[FormFiller] ✓ Data {date_str} processada com sucesso!")
                    
                    # Chama callback se fornecido
                    if callback:
                        progress = ((idx + 1) / total_dates) * 100
                        callback(progress, f"Preenchido: {date_str}")
                    
                except Exception as e:
                    error_msg = f"Erro ao processar data {date.strftime('%d/%m/%Y')}: {str(e)}"
                    print(f"[FormFiller] EXCEÇÃO: {error_msg}")
                    import traceback
                    traceback.print_exc()
                    results['errors'].append(error_msg)
                    continue
            
            if results['errors']:
                results['success'] = False
            
            return results
            
        except Exception as e:
            results['success'] = False
            results['errors'].append(f"Erro geral: {str(e)}")
            return results
    
    async def fill_single_date(self, date: datetime, task_index: int,
                        description_morning: str, description_afternoon: str) -> bool:
        """
        Preenche apontamento para uma única data.
        
        Args:
            date: Data a preencher
            task_index: Índice da tarefa selecionada
            description_morning: Descrição para entrada da manhã
            description_afternoon: Descrição para entrada da tarde
            
        Returns:
            True se preenchimento foi bem-sucedido, False caso contrário
        """
        result = await self.fill_date_range(
            date, date, task_index, description_morning, description_afternoon
        )
        return result['success']
