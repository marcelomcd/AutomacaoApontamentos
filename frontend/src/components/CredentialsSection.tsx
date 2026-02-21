import { useState } from 'react'
import { Save, Key, Mail } from 'lucide-react'
import { api } from '../services/api'

interface CredentialsSectionProps {
  email: string
  setEmail: (email: string) => void
  hasCredentials: boolean
  setHasCredentials: (has: boolean) => void
  onCredentialsSaved: () => void
}

export function CredentialsSection({
  email,
  setEmail,
  hasCredentials,
  setHasCredentials,
  onCredentialsSaved,
}: CredentialsSectionProps) {
  const [password, setPassword] = useState('')
  const [isSaving, setIsSaving] = useState(false)

  const handleSave = async () => {
    if (!email || !password) {
      alert('Por favor, preencha email e senha')
      return
    }

    setIsSaving(true)
    try {
      await api.saveCredentials(email, password)
      setHasCredentials(true)
      setPassword('')
      onCredentialsSaved()
      alert('Credenciais salvas com sucesso!')
    } catch (error: any) {
      let errorMessage = 'Erro desconhecido'
      
      if (error.isNetworkError) {
        errorMessage = error.message || 'Backend não está disponível. Verifique se o servidor está rodando em http://localhost:8000'
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail
      } else if (error.message) {
        errorMessage = error.message
      }
      
      alert(`Erro ao salvar: ${errorMessage}`)
      console.error('Erro ao salvar credenciais:', error)
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="glass-dark rounded-2xl p-6">
      <h2 className="text-2xl font-semibold text-white mb-4 flex items-center gap-2">
        <Key className="w-6 h-6 text-blue-400" />
        Credenciais
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-300 flex items-center gap-2">
            <Mail className="w-4 h-4" />
            Email
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="seu.email@qualiit.com.br"
            className="w-full px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-300">
            Senha
          </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder={hasCredentials ? "Preencha para atualizar" : "Sua senha"}
            className="w-full px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div className="flex items-end">
          <button
            onClick={handleSave}
            disabled={isSaving}
            className="w-full px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            <Save className="w-4 h-4" />
            {isSaving ? 'Salvando...' : 'Salvar Credenciais'}
          </button>
        </div>
      </div>

      {hasCredentials && (
        <div className="mt-4 p-3 bg-green-500/10 border border-green-500/20 rounded-lg">
          <p className="text-green-400 text-sm">
            ✓ Credenciais salvas e criptografadas
          </p>
        </div>
      )}
    </div>
  )
}
