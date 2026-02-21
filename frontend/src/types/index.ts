export interface Task {
  proposta: string
  cliente: string
  projeto: string
  tarefa: string
  horas_liberadas: string
  horas_apontadas: string
  saldo: string
}

export interface Period {
  id: number
  de: string
  ate: string
  taskIndex: number
  descMorning: string
  descAfternoon: string
}

export interface LogEntry {
  id: number
  message: string
  type: 'info' | 'success' | 'error'
  timestamp: Date
}
