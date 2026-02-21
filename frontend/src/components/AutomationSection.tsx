import { Play, Square } from 'lucide-react'

interface AutomationSectionProps {
  onExecute: () => void
  isLoading: boolean
  progress: number
}

export function AutomationSection({
  onExecute,
  isLoading,
  progress,
}: AutomationSectionProps) {
  return (
    <div className="glass-dark rounded-2xl p-6">
      <h2 className="text-2xl font-semibold text-white mb-4">Controles</h2>

      <div className="flex items-center justify-between">
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            defaultChecked
            className="w-4 h-4 text-blue-600 rounded"
          />
          <span className="text-gray-300">Modo Silencioso (sem exibir navegador)</span>
        </label>

        <div className="flex gap-4">
          <button
            onClick={onExecute}
            disabled={isLoading}
            className="px-6 py-3 bg-green-600 hover:bg-green-700 disabled:bg-green-800 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-colors flex items-center gap-2"
          >
            {isLoading ? (
              <>
                <Square className="w-5 h-5" />
                Executando...
              </>
            ) : (
              <>
                <Play className="w-5 h-5" />
                Executar Automação
              </>
            )}
          </button>
        </div>
      </div>

      {isLoading && (
        <div className="mt-4">
          <div className="w-full bg-slate-800 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
          <p className="text-sm text-gray-400 mt-2 text-center">
            {progress}% concluído
          </p>
        </div>
      )}
    </div>
  )
}
