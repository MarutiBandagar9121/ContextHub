import { useState } from 'react'
import { useLocation, Navigate } from 'react-router-dom'
import { useVerifyOtp } from '../../hooks/useAuth'
import { useMutation } from '@tanstack/react-query'
import { resendOtp } from '../../api/auth'
import Button from '../../components/ui/Button'
import Input from '../../components/ui/Input'

export default function VerifyOtpPage() {
  const { state } = useLocation()
  const [otp, setOtp] = useState('')
  const verifyOtp = useVerifyOtp()

  const resend = useMutation({
    mutationFn: () => resendOtp({ id: state?.userId }),
  })

  if (!state?.userId) {
    return <Navigate to="/register" replace />
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    verifyOtp.mutate({ id: state.userId, otp })
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-2">Verify your email</h2>
      <p className="text-sm text-gray-500 mb-6">
        We sent a code to your email. Enter it below to activate your account.
      </p>

      {verifyOtp.error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md text-sm text-red-700">
          {verifyOtp.error.response?.data?.detail ?? 'Invalid OTP. Please try again.'}
        </div>
      )}

      {resend.isSuccess && (
        <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-md text-sm text-green-700">
          A new code has been sent to your email.
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Verification code"
          type="text"
          required
          placeholder="Enter OTP"
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
        />
        <Button type="submit" className="w-full" isLoading={verifyOtp.isPending}>
          Verify
        </Button>
      </form>

      <p className="mt-4 text-sm text-center text-gray-600">
        Didn't receive a code?{' '}
        <button
          onClick={() => resend.mutate()}
          disabled={resend.isPending}
          className="text-indigo-600 hover:text-indigo-500 font-medium disabled:opacity-50"
        >
          Resend
        </button>
      </p>
    </div>
  )
}
