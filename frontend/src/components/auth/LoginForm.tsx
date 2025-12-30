import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { Zap, User, Lock } from 'lucide-react';
import toast from 'react-hot-toast';

export const LoginForm: React.FC = () => {
  const navigate = useNavigate();
  const { login, isLoading } = useAuthStore();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(formData.username, formData.password);
      toast.success('Login successful!');
      navigate('/dashboard');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Login failed');
    }
  };

  const handleDemoLogin = async () => {
    try {
      await login('demo', 'demo123');
      toast.success('Demo login successful!');
      navigate('/dashboard');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Demo login failed');
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-dark-bg px-4">
      <div className="max-w-md w-full">
        {/* Card */}
        <div className="bg-dark-surface border border-dark-border rounded-2xl p-8 shadow-2xl">
          {/* Icon */}
          <div className="flex justify-center mb-6">
            <div className="w-16 h-16 bg-gradient-to-br from-primary-400 to-primary-600 rounded-2xl flex items-center justify-center">
              <Zap className="w-8 h-8 text-white" />
            </div>
          </div>

          {/* Title */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-white mb-2">Trading Signals</h1>
            <p className="text-gray-400">Telegram to Broker Automation</p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Username */}
            <div>
              <label className="flex items-center gap-2 text-sm font-medium text-white mb-2">
                <User className="w-4 h-4" />
                Username
              </label>
              <input
                name="username"
                type="text"
                required
                value={formData.username}
                onChange={handleChange}
                placeholder="Enter username"
                className="w-full px-4 py-3 bg-dark-card border border-dark-border rounded-lg text-gray-200 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all"
              />
            </div>

            {/* Password */}
            <div>
              <label className="flex items-center gap-2 text-sm font-medium text-white mb-2">
                <Lock className="w-4 h-4" />
                Password
              </label>
              <input
                name="password"
                type="password"
                required
                value={formData.password}
                onChange={handleChange}
                placeholder="Enter password"
                className="w-full px-4 py-3 bg-dark-card border border-dark-border rounded-lg text-gray-200 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all"
              />
            </div>

            {/* Login Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 bg-primary-500 hover:bg-primary-600 text-white font-semibold rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Logging in...' : 'Login'}
            </button>
          </form>

          {/* Divider */}
          <div className="my-6 text-center">
            <span className="text-gray-500 text-sm">or try demo</span>
          </div>

          {/* Demo Login Button */}
          <button
            type="button"
            onClick={handleDemoLogin}
            disabled={isLoading}
            className="w-full py-3 bg-transparent border border-gray-600 hover:border-primary-500 text-white font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Demo Login (demo / demo123)
          </button>

          {/* Demo Credentials Info */}
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-500">
              Demo credentials: username:{' '}
              <span className="text-gray-400 bg-dark-card px-2 py-1 rounded">demo</span>{' '}
              password:{' '}
              <span className="text-gray-400 bg-dark-card px-2 py-1 rounded">demo123</span>
            </p>
          </div>
        </div>

        {/* Sign Up Link */}
        <div className="mt-6 text-center">
          <p className="text-gray-400 text-sm">
            Don't have an account?{' '}
            <Link to="/register" className="text-primary-400 hover:text-primary-300 font-medium transition-colors">
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};
