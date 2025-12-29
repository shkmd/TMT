import { create } from 'zustand';
import { User } from '@/types/api';
import { authApi } from '@/api';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  setUser: (user: User | null) => void;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: authApi.isAuthenticated(),
  isLoading: false,
  error: null,

  setUser: (user) => set({ user, isAuthenticated: !!user }),

  login: async (username, password) => {
    set({ isLoading: true, error: null });
    try {
      await authApi.login({ username, password });
      const user = await authApi.getCurrentUser();
      set({ user, isAuthenticated: true, isLoading: false });
    } catch (error: any) {
      set({
        error: error.response?.data?.detail || 'Login failed',
        isLoading: false,
        isAuthenticated: false,
      });
      throw error;
    }
  },

  register: async (username, email, password) => {
    set({ isLoading: true, error: null });
    try {
      await authApi.register({ username, email, password });
      // After registration, automatically log in
      await authApi.login({ username, password });
      const user = await authApi.getCurrentUser();
      set({ user, isAuthenticated: true, isLoading: false });
    } catch (error: any) {
      set({
        error: error.response?.data?.detail || 'Registration failed',
        isLoading: false,
      });
      throw error;
    }
  },

  logout: () => {
    authApi.logout();
    set({ user: null, isAuthenticated: false });
  },

  checkAuth: async () => {
    if (!authApi.isAuthenticated()) {
      set({ isAuthenticated: false, user: null });
      return;
    }

    try {
      const user = await authApi.getCurrentUser();
      set({ user, isAuthenticated: true });
    } catch (error) {
      set({ user: null, isAuthenticated: false });
      authApi.logout();
    }
  },
}));
