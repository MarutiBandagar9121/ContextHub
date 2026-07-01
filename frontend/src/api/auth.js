import axios from 'axios'
import client from './client'

export const registerUser = (data) =>
  client.post('/api/v1/auth/register', data).then((r) => r.data)

export const verifyOtp = (data) =>
  client.post('/api/v1/auth/verify_otp', data).then((r) => r.data)

export const resendOtp = (data) =>
  client.post('/api/v1/auth/resend_otp', data).then((r) => r.data)

export const loginUser = (data) =>
  client.post('/api/v1/auth/login', data).then((r) => r.data)

export const logoutUser = () =>
  client.post('/api/v1/auth/logout').then((r) => r.data)

// Called on app boot to restore session from the httpOnly refresh cookie.
// Uses raw axios (not the intercepted client) to avoid an infinite retry loop.
export const refreshAccessToken = () =>
  axios
    .post('/api/v1/auth/refresh', {}, { withCredentials: true })
    .then((r) => r.data)
