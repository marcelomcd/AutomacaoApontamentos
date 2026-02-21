/**
 * Serviço de API para comunicação com backend.
 * Seguindo princípios de separação de responsabilidades.
 */
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 segundos de timeout
})

// Interceptor para tratar erros de rede
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED' || error.message === 'Network Error') {
      // Backend não está disponível
      const customError = new Error(
        'Backend não está disponível. Verifique se o servidor está rodando em http://localhost:8000'
      ) as any
      customError.isNetworkError = true
      customError.originalError = error
      return Promise.reject(customError)
    }
    
    if (!error.response) {
      // Erro de conexão
      const customError = new Error(
        'Não foi possível conectar ao servidor. Verifique se o backend está rodando.'
      ) as any
      customError.isNetworkError = true
      customError.originalError = error
      return Promise.reject(customError)
    }
    
    return Promise.reject(error)
  }
)

export const api = {
  async saveCredentials(email: string, password: string) {
    const response = await apiClient.post('/api/credentials/save', {
      email,
      password,
    })
    return response.data
  },

  async loadCredentials() {
    const response = await apiClient.get('/api/credentials/load')
    return response.data
  },

  async loadTasks(month: number, year: number) {
    const response = await apiClient.post('/api/tasks/load', {
      month,
      year,
    })
    return response.data
  },

  async executeAutomation(periods: any[], headless: boolean = true) {
    const response = await apiClient.post('/api/automation/execute', {
      periods,
      headless,
    })
    return response.data
  },

  async getAutomationStatus() {
    const response = await apiClient.get('/api/automation/status')
    return response.data
  },

  async checkBackendHealth() {
    try {
      const response = await apiClient.get('/api/health', { timeout: 5000 })
      return { available: true, data: response.data }
    } catch (error: any) {
      return { 
        available: false, 
        error: error.isNetworkError 
          ? 'Backend não está disponível. Verifique se o servidor está rodando em http://localhost:8000'
          : error.message || 'Erro desconhecido'
      }
    }
  },
}
