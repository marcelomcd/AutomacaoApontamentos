import { Download, Loader2 } from 'lucide-react'
import type { Task } from '../types'

interface TasksSectionProps {
  tasks: Task[]
  month: number
  year: number
  onLoadTasks: () => void
  isLoading: boolean
}

export function TasksSection({
  tasks,
  month,
  year,
  onLoadTasks,
  isLoading,
}: TasksSectionProps) {
  return (
    <div className="glass-dark rounded-2xl p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-semibold text-white">Tarefas Disponíveis</h2>
        <button
          onClick={onLoadTasks}
          disabled={isLoading}
          className="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-colors flex items-center gap-2"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              Carregando...
            </>
          ) : (
            <>
              <Download className="w-4 h-4" />
              Carregar Tarefas ({month.toString().padStart(2, '0')}/{year})
            </>
          )}
        </button>
      </div>

      {tasks.length === 0 ? (
        <div className="text-center py-12 text-gray-400">
          <p>Nenhuma tarefa carregada</p>
          <p className="text-sm mt-2">Clique em "Carregar Tarefas" para buscar projetos disponíveis</p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-700">
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-300">Proposta</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-300">Cliente</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-300">Projeto</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-300">Tarefa</th>
                <th className="px-4 py-3 text-right text-sm font-semibold text-gray-300">H. Liberadas</th>
                <th className="px-4 py-3 text-right text-sm font-semibold text-gray-300">H. Apontadas</th>
                <th className="px-4 py-3 text-right text-sm font-semibold text-gray-300">Saldo</th>
              </tr>
            </thead>
            <tbody>
              {tasks.map((task, idx) => (
                <tr
                  key={idx}
                  className="border-b border-slate-800 hover:bg-slate-800/30 transition-colors"
                >
                  <td className="px-4 py-3 text-white">{task.proposta}</td>
                  <td className="px-4 py-3 text-gray-300">{task.cliente}</td>
                  <td className="px-4 py-3 text-gray-300">{task.projeto}</td>
                  <td className="px-4 py-3 text-gray-300">{task.tarefa}</td>
                  <td className="px-4 py-3 text-right text-gray-300">{task.horas_liberadas}</td>
                  <td className="px-4 py-3 text-right text-gray-300">{task.horas_apontadas}</td>
                  <td className={`px-4 py-3 text-right font-medium ${
                    parseFloat(task.saldo.replace(',', '.')) > 0 
                      ? 'text-green-400' 
                      : 'text-gray-400'
                  }`}>
                    {task.saldo}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
