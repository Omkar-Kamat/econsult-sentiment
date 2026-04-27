import { useQuery } from '@tanstack/react-query'
import { fetchFigures } from '../api/client'

export const useFigures = () =>
  useQuery({
    queryKey: ['figures'],
    queryFn: fetchFigures,
    staleTime: Infinity,
  })