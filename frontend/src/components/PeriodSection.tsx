import { Plus, X } from 'lucide-react'
import type { Period, Task } from '../types'

interface PeriodSectionProps {
  isFullMonth: boolean
  setIsFullMonth: (value: boolean) => void
  month: number
  setMonth: (value: number) => void
  year: number
  setYear: (value: number) => void
  periods: Period[]
  onAddPeriod: () => void
  onRemovePeriod: (id: number) => void
  onUpdatePeriod: (id: number, updates: Partial<Period>) => void
  tasks: Task[]
}

export function PeriodSection({
  isFullMonth,
  setIsFullMonth,
  month,
  setMonth,
  year,
  setYear,
  periods,
  onAddPeriod,
  onRemovePeriod,
  onUpdatePeriod,
  tasks,
}: PeriodSectionProps) {
  return (
    <div className="glass-dark rounded-2xl p-6">
      <h2 className="text-2xl font-semibold text-white mb-4">Período</h2>

      {/* Radio buttons */}
      <div className="flex gap-6 mb-6">
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="radio"
            checked={isFullMonth}
            onChange={() => setIsFullMonth(true)}
            className="w-4 h-4 text-blue-600"
          />
          <span className="text-gray-300">Preencher mês completo</span>
        </label>
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="radio"
            checked={!isFullMonth}
            onChange={() => setIsFullMonth(false)}
            className="w-4 h-4 text-blue-600"
          />
          <span className="text-gray-300">Período específico</span>
        </label>
      </div>

      {isFullMonth ? (
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Mês
            </label>
            <select
              value={month}
              onChange={(e) => setMonth(Number(e.target.value))}
              className="w-full px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {Array.from({ length: 12 }, (_, i) => i + 1).map((m) => (
                <option key={m} value={m}>
                  {new Date(2000, m - 1).toLocaleDateString('pt-BR', { month: 'long' })}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Ano
            </label>
            <input
              type="number"
              value={year}
              onChange={(e) => setYear(Number(e.target.value))}
              min="2020"
              max="2030"
              className="w-full px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          {periods.map((period) => (
            <PeriodWidget
              key={period.id}
              period={period}
              tasks={tasks}
              onUpdate={(updates) => onUpdatePeriod(period.id, updates)}
              onRemove={() => onRemovePeriod(period.id)}
            />
          ))}
          <button
            onClick={onAddPeriod}
            className="w-full px-4 py-3 bg-blue-600/20 hover:bg-blue-600/30 border border-blue-500/50 rounded-lg text-blue-400 font-medium transition-colors flex items-center justify-center gap-2"
          >
            <Plus className="w-5 h-5" />
            Adicionar Período
          </button>
        </div>
      )}
    </div>
  )
}

function PeriodWidget({
  period,
  tasks,
  onUpdate,
  onRemove,
}: {
  period: Period
  tasks: Task[]
  onUpdate: (updates: Partial<Period>) => void
  onRemove: () => void
}) {
  const availableTasks = tasks.filter(t => {
    const saldo = parseFloat(t.saldo.replace(',', '.'))
    return saldo > 0
  })

  return (
    <div className="bg-slate-800/30 border border-slate-700 rounded-xl p-4 space-y-4">
      <div className="flex justify-between items-center mb-2">
        <h3 className="text-lg font-medium text-white">Período</h3>
        <button
          onClick={onRemove}
          className="p-1 hover:bg-red-500/20 rounded text-red-400 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            De (DD/MM/AAAA)
          </label>
          <input
            type="text"
            value={period.de}
            onChange={(e) => onUpdate({ de: e.target.value })}
            placeholder="01/01/2026"
            className="w-full px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Até (DD/MM/AAAA)
          </label>
          <input
            type="text"
            value={period.ate}
            onChange={(e) => onUpdate({ ate: e.target.value })}
            placeholder="31/01/2026"
            className="w-full px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Projeto
          </label>
          <select
            value={period.taskIndex}
            onChange={(e) => onUpdate({ taskIndex: Number(e.target.value) })}
            className="w-full px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value={-1}>Selecione um projeto...</option>
            {availableTasks.map((task, idx) => (
              <option key={idx} value={idx}>
                {task.cliente} - {task.projeto} - {task.tarefa} (Saldo: {task.saldo})
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Descrição Manhã (uma linha por dia)
          </label>
          <textarea
            value={period.descMorning}
            onChange={(e) => onUpdate({ descMorning: e.target.value })}
            placeholder="Descrição para entrada da manhã&#10;Uma linha por dia útil"
            rows={3}
            className="w-full px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Descrição Tarde (uma linha por dia)
          </label>
          <textarea
            value={period.descAfternoon}
            onChange={(e) => onUpdate({ descAfternoon: e.target.value })}
            placeholder="Descrição para entrada da tarde&#10;Uma linha por dia útil"
            rows={3}
            className="w-full px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />
        </div>
      </div>
    </div>
  )
}
