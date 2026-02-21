import { AlertCircle, CheckCircle, Info } from 'lucide-react'
import type { LogEntry } from '../types'

interface LogSectionProps {
  logs: LogEntry[]
}

export function LogSection({ logs }: LogSectionProps) {
  const getIcon = (type: LogEntry['type']) => {
    switch (type) {
      case 'success':
        return <CheckCircle className="w-4 h-4 text-green-400" />
      case 'error':
        return <AlertCircle className="w-4 h-4 text-red-400" />
      default:
        return <Info className="w-4 h-4 text-blue-400" />
    }
  }

  const getTextColor = (type: LogEntry['type']) => {
    switch (type) {
      case 'success':
        return 'text-green-400'
      case 'error':
        return 'text-red-400'
      default:
        return 'text-gray-300'
    }
  }

  return (
    <div className="glass-dark rounded-2xl p-6">
      <h2 className="text-2xl font-semibold text-white mb-4">Log / Status</h2>

      <div className="bg-slate-900/50 rounded-lg p-4 max-h-64 overflow-y-auto space-y-2">
        {logs.length === 0 ? (
          <p className="text-gray-500 text-center py-4">Nenhum log ainda</p>
        ) : (
          logs.map((log) => (
            <div
              key={log.id}
              className="flex items-start gap-3 p-2 rounded hover:bg-slate-800/30 transition-colors"
            >
              {getIcon(log.type)}
              <div className="flex-1">
                <p className={`text-sm ${getTextColor(log.type)}`}>
                  {log.message}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  {log.timestamp.toLocaleTimeString('pt-BR')}
                </p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
