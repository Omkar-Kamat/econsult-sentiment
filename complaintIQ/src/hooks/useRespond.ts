import { useMutation } from '@tanstack/react-query'
import { generateResponse } from '../api/client'

export const useRespond = () =>
  useMutation({
    mutationFn: generateResponse,
  })