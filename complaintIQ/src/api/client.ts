import axios from 'axios'
import type {
  ClassifyRequest,
  ClassifyResponse,
  RespondRequest,
  RespondResponse,
  ClustersResponse,
  AnalyticsResponse,
  FigureMetadata,
  HistoryResponse,
  APIResponse,
} from '../types'

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ''

const api = axios.create({
  baseURL: `${BASE_URL}/api/v1`,
  headers: { 'Content-Type': 'application/json' },
  timeout: 60_000,
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    const message =
      err.response?.data?.detail ||
      err.response?.data?.error ||
      err.message ||
      'An unknown error occurred'
    return Promise.reject(new Error(message))
  }
)

export const classifyComplaint = async (
  payload: ClassifyRequest
): Promise<ClassifyResponse> => {
  const res = await api.post<ClassifyResponse>('/classify', payload)
  return res.data
}

export const generateResponse = async (
  payload: RespondRequest
): Promise<RespondResponse> => {
  const res = await api.post<RespondResponse>('/respond', payload)
  return res.data
}

export const fetchClusters = async (): Promise<ClustersResponse> => {
  const res = await api.get<APIResponse<ClustersResponse>>('/clusters')
  return res.data.data
}

export const fetchAnalytics = async (): Promise<AnalyticsResponse> => {
  const res = await api.get<APIResponse<AnalyticsResponse>>('/analytics')
  return res.data.data
}

export const fetchFigures = async (): Promise<FigureMetadata[]> => {
  const res = await api.get<APIResponse<{ figures: FigureMetadata[] }>>('/figures')
  return res.data.data.figures
}

export const fetchHistory = async (params: {
  limit?: number
  skip?: number
  cluster_id?: number
  sentiment?: string
}): Promise<HistoryResponse> => {
  const res = await api.get<APIResponse<HistoryResponse>>('/history', { params })
  return res.data.data
}

export const fetchComplaintDetail = async (id: string) => {
  const res = await api.get(`/history/${id}`)
  return res.data.data
}

export const updateResponseStatus = async (
  responseId: string,
  status: 'draft' | 'sent' | 'archived'
) => {
  const res = await api.patch(`/history/${responseId}/status`, null, {
    params: { status },
  })
  return res.data
}

export const getFigureUrl = (key: string): string =>
  `${BASE_URL}/api/v1/figures/${key}`