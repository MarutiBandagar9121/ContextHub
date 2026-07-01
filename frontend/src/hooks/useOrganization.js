import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  createInvitation,
  createOrganization,
  deleteOrganization,
  getOrganizationDetails,
  getUserOrganizations,
} from '../api/organization'

export function useUserOrganizations() {
  return useQuery({
    queryKey: ['organizations'],
    queryFn: getUserOrganizations,
  })
}

export function useOrganizationDetails(orgId) {
  return useQuery({
    queryKey: ['organization', orgId],
    queryFn: () => getOrganizationDetails(orgId),
    enabled: !!orgId,
  })
}

export function useCreateOrganization() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: createOrganization,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['organizations'] })
    },
  })
}

export function useDeleteOrganization() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: deleteOrganization,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['organizations'] })
    },
  })
}

export function useCreateInvitation(orgId) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: createInvitation,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['organization', orgId] })
    },
  })
}
