import { useQuery } from '@tanstack/react-query'
import { fetchAnalytics } from '../api/client'

export const useAnalytics = () =>
  useQuery({
    queryKey: ['analytics'],
    queryFn: fetchAnalytics,
    staleTime: 2 * 60 * 1000,
    refetchInterval: 2 * 60 * 1000,
  })