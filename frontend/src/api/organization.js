import client from './client'

export const createOrganization = (data) =>
  client.post('/api/v1/organization', data).then((r) => r.data)

export const getUserOrganizations = () =>
  client.get('/api/v1/organization').then((r) => r.data)

export const getOrganizationDetails = (orgId) =>
  client.get(`/api/v1/organization/${orgId}`).then((r) => r.data)

export const deleteOrganization = (orgId) =>
  client.delete(`/api/v1/organization/${orgId}`).then((r) => r.data)

export const createInvitation = (data) =>
  client.post('/api/v1/organization/invitation', data).then((r) => r.data)

export const checkInvitationStatus = (token) =>
  client.get(`/api/v1/organization/invitation/${token}`).then((r) => r.data)

export const acceptInvitationNewUser = (token, data) =>
  client
    .post(`/api/v1/organization/invitation/${token}/accept`, data)
    .then((r) => r.data)
