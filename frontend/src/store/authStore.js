import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const useAuthStore = create(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      isAuthenticated: false,

      setAuth: (user, accessToken) =>
        set({ user, accessToken, isAuthenticated: true }),

      setAccessToken: (accessToken) =>
        set({ accessToken }),

      clearAuth: () =>
        set({ user: null, accessToken: null, isAuthenticated: false }),
    }),
    {
      name: 'contexthub-auth',
      // Only persist user info — access token is short-lived and re-fetched
      // via the refresh cookie on app boot, so no need to persist it.
      partialize: (state) => ({ user: state.user }),
    }
  )
)

export default useAuthStore
