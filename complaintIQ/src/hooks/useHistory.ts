import { useQuery } from '@tanstack/react-query'
import { fetchHistory } from '../api/client'

export const useHistory = (params: {
  limit?: number
  skip?: number
  cluster_id?: number
  sentiment?: string
}) =>
  useQuery({
    queryKey: ['history', params],
    queryFn: () => fetchHistory(params),
    staleTime: 30 * 1000,
  })