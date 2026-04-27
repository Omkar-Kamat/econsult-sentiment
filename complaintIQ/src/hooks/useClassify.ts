import { useMutation } from '@tanstack/react-query'
import { classifyComplaint } from '../api/client'

export const useClassify = () =>
  useMutation({
    mutationFn: classifyComplaint,
  })