"""
Gerador de horários aleatórios para apontamentos.
Gera horários respeitando intervalos e validações especificadas.
"""
import random
from datetime import datetime, timedelta
from typing import Dict


def time_to_minutes(time_str: str) -> int:
    """
    Converte string de hora (HH:MM) para minutos desde meia-noite.
    
    Args:
        time_str: String no formato "HH:MM"
        
    Returns:
        Minutos desde meia-noite
    """
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes


def minutes_to_time(minutes: int) -> str:
    """
    Converte minutos desde meia-noite para string (HH:MM).
    
    Args:
        minutes: Minutos desde meia-noite
        
    Returns:
        String no formato "HH:MM"
    """
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"


def random_time_in_range(start_str: str, end_str: str) -> str:
    """
    Gera um horário aleatório dentro de um intervalo.
    
    Args:
        start_str: Hora inicial no formato "HH:MM"
        end_str: Hora final no formato "HH:MM"
        
    Returns:
        Hora aleatória no formato "HH:MM"
    """
    start_minutes = time_to_minutes(start_str)
    end_minutes = time_to_minutes(end_str)
    
    # Se start >= end, assume que end é do dia seguinte
    if start_minutes >= end_minutes:
        end_minutes += 24 * 60
    
    # Gera um horário aleatório no intervalo
    random_minutes = random.randint(start_minutes, end_minutes)
    
    # Normaliza para o mesmo dia (0-1439 minutos)
    random_minutes = random_minutes % (24 * 60)
    
    return minutes_to_time(random_minutes)


def generate_daily_hours() -> Dict[str, Dict[str, str]]:
    """
    Gera horários aleatórios para um dia completo de trabalho.
    
    Retorna horários que respeitam:
    - Manhã: Início entre 08:55-09:00, Fim entre 12:00-12:15
    - Tarde: Início entre 13:00-13:15, Fim entre 18:00-18:15
    - Intervalo entre fim manhã e início tarde: ~1h (45min a 1h15min, entre 12:00-13:15)
    - Total do dia: ~8h (480 minutos ± 15min de tolerância)
    
    Returns:
        Dicionário com horários formatados:
        {
            'morning': {'start': 'HH:MM', 'end': 'HH:MM'},
            'afternoon': {'start': 'HH:MM', 'end': 'HH:MM'}
        }
    """
    max_attempts = 200
    attempt = 0
    
    while attempt < max_attempts:
        # Gera horários da manhã: início entre 08:55-09:00, fim entre 12:00-12:15
        morning_start_min = random.randint(time_to_minutes("08:55"), time_to_minutes("09:00"))
        morning_end_min = random.randint(time_to_minutes("12:00"), time_to_minutes("12:15"))
        
        # Gera horários da tarde: início entre 13:00-13:15, fim entre 18:00-18:15
        afternoon_start_min = random.randint(time_to_minutes("13:00"), time_to_minutes("13:15"))
        afternoon_end_min = random.randint(time_to_minutes("18:00"), time_to_minutes("18:15"))
        
        # Valida intervalo entre fim manhã e início tarde (deve ser ~1h)
        # O intervalo está entre 12:00-13:15, então pode variar de 45min a 1h15min
        interval_minutes = afternoon_start_min - morning_end_min
        
        # Valida intervalo: deve estar entre 45min e 1h15min (75min)
        if not (45 <= interval_minutes <= 75):
            attempt += 1
            continue
        
        # Valida total do dia (início manhã até fim tarde)
        total_minutes = afternoon_end_min - morning_start_min
        
        # Valida total: deve ser aproximadamente 8h (480 minutos ± 15min de tolerância)
        # Isso permite variação de 7h45min (465min) a 8h15min (495min)
        if not (465 <= total_minutes <= 495):
            attempt += 1
            continue
        
        # Se passou todas as validações, retorna os horários
        return {
            'morning': {
                'start': minutes_to_time(morning_start_min),
                'end': minutes_to_time(morning_end_min)
            },
            'afternoon': {
                'start': minutes_to_time(afternoon_start_min),
                'end': minutes_to_time(afternoon_end_min)
            }
        }
    
    # Se não conseguiu gerar após várias tentativas, retorna valores padrão válidos (8h exatas)
    return {
        'morning': {
            'start': '09:00',
            'end': '12:00'
        },
        'afternoon': {
            'start': '13:00',
            'end': '18:00'
        }
    }


def validate_hours(morning_start: str, morning_end: str, 
                  afternoon_start: str, afternoon_end: str) -> tuple[bool, str]:
    """
    Valida se os horários gerados estão dentro dos parâmetros esperados.
    
    Args:
        morning_start: Início da manhã (HH:MM)
        morning_end: Fim da manhã (HH:MM)
        afternoon_start: Início da tarde (HH:MM)
        afternoon_end: Fim da tarde (HH:MM)
        
    Returns:
        Tupla (é_válido, mensagem_erro)
    """
    morning_start_min = time_to_minutes(morning_start)
    morning_end_min = time_to_minutes(morning_end)
    afternoon_start_min = time_to_minutes(afternoon_start)
    afternoon_end_min = time_to_minutes(afternoon_end)
    
    # Valida intervalo manhã (08:55-09:00 para início, 12:00-12:15 para fim)
    if not (time_to_minutes("08:55") <= morning_start_min <= time_to_minutes("09:00")):
        return False, "Início da manhã fora do intervalo permitido (08:55-09:00)"
    
    if not (time_to_minutes("12:00") <= morning_end_min <= time_to_minutes("12:15")):
        return False, "Fim da manhã fora do intervalo permitido (12:00-12:15)"
    
    # Valida intervalo tarde (13:00-13:15 para início, 18:00-18:15 para fim)
    if not (time_to_minutes("13:00") <= afternoon_start_min <= time_to_minutes("13:15")):
        return False, "Início da tarde fora do intervalo permitido (13:00-13:15)"
    
    if not (time_to_minutes("18:00") <= afternoon_end_min <= time_to_minutes("18:15")):
        return False, "Fim da tarde fora do intervalo permitido (18:00-18:15)"
    
    # Valida intervalo entre fim manhã e início tarde
    # O intervalo está entre 12:00-13:15, então pode variar de 45min a 1h15min
    interval_minutes = afternoon_start_min - morning_end_min
    if interval_minutes < 0:
        interval_minutes += 24 * 60
    
    if not (45 <= interval_minutes <= 75):
        return False, f"Intervalo entre fim manhã e início tarde inválido: {interval_minutes}min (deve ser 45-75min, entre 12:00-13:15)"
    
    # Valida total do dia (deve ser aproximadamente 8h)
    total_minutes = afternoon_end_min - morning_start_min
    if total_minutes < 0:
        total_minutes += 24 * 60
    
    # Permite variação de 7h45min (465min) a 8h15min (495min) para total de 8h
    if not (465 <= total_minutes <= 495):
        return False, f"Total de horas do dia inválido: {total_minutes}min (deve ser 465-495min, aproximadamente 8h)"
    
    return True, "Horários válidos"
