import { useState, useEffect } from 'react'
import { CredentialsSection } from './components/CredentialsSection'
import { PeriodSection } from './components/PeriodSection'
import { TasksSection } from './components/TasksSection'
import { AutomationSection } from './components/AutomationSection'
import { LogSection } from './components/LogSection'
import { api } from './services/api'
import type { Task, Period, LogEntry } from './types'

function App() {
  const [email, setEmail] = useState('')
  const [hasCredentials, setHasCredentials] = useState(false)
  const [tasks, setTasks] = useState<Task[]>([])
  const [periods, setPeriods] = useState<Period[]>([])
  const [month, setMonth] = useState(new Date().getMonth() + 1)
  const [year, setYear] = useState(new Date().getFullYear())
  const [isFullMonth, setIsFullMonth] = useState(true)
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    // Verifica se o backend está disponível ao iniciar
    const checkBackend = async () => {
      const health = await api.checkBackendHealth()
      if (!health.available) {
        addLog(`⚠️ ${health.error}`, 'error')
        addLog('Certifique-se de que o backend está rodando (start_backend.bat ou start.bat)', 'info')
      } else {
        addLog('✓ Backend conectado com sucesso', 'success')
        // Só verifica credenciais se o backend estiver disponível
        checkCredentials()
      }
    }
    
    checkBackend()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const checkCredentials = async () => {
    try {
      const response = await api.loadCredentials()
      if (response.has_credentials) {
        setEmail(response.email)
        setHasCredentials(true)
      }
    } catch (error: any) {
      // Não mostra erro se for apenas o backend não disponível na inicialização
      if (error.isNetworkError) {
        console.warn('Backend não disponível na inicialização:', error.message)
      } else {
        console.error('Erro ao verificar credenciais:', error)
      }
    }
  }

  const addLog = (message: string, type: 'info' | 'success' | 'error' = 'info') => {
    setLogs(prev => [...prev, {
      id: Date.now(),
      message,
      type,
      timestamp: new Date()
    }])
  }

  const handleLoadTasks = async () => {
    setIsLoading(true)
    addLog('Iniciando carregamento de tarefas...', 'info')
    
    try {
      const response = await api.loadTasks(month, year)
      setTasks(response.tasks)
      addLog(`Carregadas ${response.count} tarefas`, 'success')
    } catch (error: any) {
      let errorMessage = 'Erro desconhecido'
      
      if (error.isNetworkError) {
        errorMessage = error.message || 'Backend não está disponível. Verifique se o servidor está rodando em http://localhost:8000'
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail
      } else if (error.message) {
        errorMessage = error.message
      }
      
      addLog(`Erro: ${errorMessage}`, 'error')
      console.error('Erro ao carregar tarefas:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleAddPeriod = () => {
    setPeriods(prev => [...prev, {
      id: Date.now(),
      de: '',
      ate: '',
      taskIndex: -1,
      descMorning: '',
      descAfternoon: ''
    }])
  }

  const handleRemovePeriod = (id: number) => {
    setPeriods(prev => prev.filter(p => p.id !== id))
  }

  const handleUpdatePeriod = (id: number, updates: Partial<Period>) => {
    setPeriods(prev => prev.map(p => p.id === id ? { ...p, ...updates } : p))
  }

  const handleExecuteAutomation = async () => {
    if (isFullMonth) {
      // Validação para mês completo
      if (tasks.length === 0) {
        addLog('Por favor, carregue as tarefas primeiro', 'error')
        return
      }
    } else {
      // Validação para períodos específicos
      if (periods.length === 0) {
        addLog('Por favor, adicione pelo menos um período', 'error')
        return
      }
      
      const invalidPeriods = periods.filter(p => !p.de || !p.ate || p.taskIndex < 0)
      if (invalidPeriods.length > 0) {
        addLog('Alguns períodos estão incompletos', 'error')
        return
      }
    }

    setIsLoading(true)
    setProgress(0)
    addLog('Iniciando automação...', 'info')

    try {
      // Prepara períodos para envio
      const periodsToSend = isFullMonth 
        ? [{
            de: `01/${month.toString().padStart(2, '0')}/${year}`,
            ate: new Date(year, month, 0).toLocaleDateString('pt-BR'),
            task_index: 0, // Será selecionado na interface
            desc_morning: '',
            desc_afternoon: ''
          }]
        : periods.map(p => ({
            de: p.de,
            ate: p.ate,
            task_index: p.taskIndex,
            desc_morning: p.descMorning,
            desc_afternoon: p.descAfternoon
          }))

      const response = await api.executeAutomation(periodsToSend, true)
      
      if (response.success) {
        addLog(`Automação concluída! ${response.total_entries} entradas preenchidas`, 'success')
      } else {
        addLog(`Automação concluída com erros: ${response.errors.join(', ')}`, 'error')
      }
    } catch (error: any) {
      let errorMessage = 'Erro desconhecido'
      
      if (error.isNetworkError) {
        errorMessage = error.message || 'Backend não está disponível. Verifique se o servidor está rodando em http://localhost:8000'
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail
      } else if (error.message) {
        errorMessage = error.message
      }
      
      addLog(`Erro: ${errorMessage}`, 'error')
      console.error('Erro ao executar automação:', error)
    } finally {
      setIsLoading(false)
      setProgress(100)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-7xl mx-auto space-y-6">
          {/* Header */}
          <div className="glass-dark rounded-2xl p-6 mb-6">
            <h1 className="text-4xl font-bold text-white mb-2">
              Automação de Apontamentos
            </h1>
            <p className="text-blue-200">QualiWork - Sistema de Automação Inteligente</p>
          </div>

          {/* Credentials */}
          <CredentialsSection
            email={email}
            setEmail={setEmail}
            hasCredentials={hasCredentials}
            setHasCredentials={setHasCredentials}
            onCredentialsSaved={checkCredentials}
          />

          {/* Period Selection */}
          <PeriodSection
            isFullMonth={isFullMonth}
            setIsFullMonth={setIsFullMonth}
            month={month}
            setMonth={setMonth}
            year={year}
            setYear={setYear}
            periods={periods}
            onAddPeriod={handleAddPeriod}
            onRemovePeriod={handleRemovePeriod}
            onUpdatePeriod={handleUpdatePeriod}
            tasks={tasks}
          />

          {/* Tasks */}
          <TasksSection
            tasks={tasks}
            month={month}
            year={year}
            onLoadTasks={handleLoadTasks}
            isLoading={isLoading}
          />

          {/* Automation Controls */}
          <AutomationSection
            onExecute={handleExecuteAutomation}
            isLoading={isLoading}
            progress={progress}
          />

          {/* Logs */}
          <LogSection logs={logs} />
        </div>
      </div>
    </div>
  )
}

export default App
