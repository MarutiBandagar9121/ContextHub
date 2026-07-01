import { useMutation } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import useAuthStore from '../store/authStore'
import { loginUser, logoutUser, registerUser, verifyOtp } from '../api/auth'

export function useLogin() {
  const { setAuth } = useAuthStore()
  const navigate = useNavigate()

  return useMutation({
    mutationFn: loginUser,
    onSuccess: (data) => {
      setAuth(
        { id: data.id, first_name: data.first_name, last_name: data.last_name, email: data.email },
        data.access_token
      )
      navigate('/dashboard')
    },
  })
}

export function useRegister() {
  const navigate = useNavigate()

  return useMutation({
    mutationFn: registerUser,
    onSuccess: (data) => {
      // Navigate to OTP verification, passing the new user's id
      navigate('/verify-otp', { state: { userId: data.id } })
    },
  })
}

export function useVerifyOtp() {
  const { setAuth } = useAuthStore()
  const navigate = useNavigate()

  return useMutation({
    mutationFn: verifyOtp,
    onSuccess: (data) => {
      // After OTP verified, auth service returns an access token.
      // User info isn't in this response, so we only store the token here;
      // the user object will be populated on the next authenticated request.
      useAuthStore.getState().setAccessToken(data.access_token)
      navigate('/dashboard')
    },
  })
}

export function useLogout() {
  const { clearAuth } = useAuthStore()
  const navigate = useNavigate()

  return useMutation({
    mutationFn: logoutUser,
    onSuccess: () => {
      clearAuth()
      navigate('/login')
    },
    onError: () => {
      // Clear local state even if the server call fails
      clearAuth()
      navigate('/login')
    },
  })
}
