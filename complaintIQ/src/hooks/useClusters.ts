import { useQuery } from '@tanstack/react-query'
import { fetchClusters } from '../api/client'

export const useClusters = () =>
  useQuery({
    queryKey: ['clusters'],
    queryFn: fetchClusters,
    staleTime: 5 * 60 * 1000,
  })