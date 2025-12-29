import axiosInstance from './axios';
import { Signal, SignalWithExecutions, SignalStats, SignalStatus } from '@/types/api';

export const signalsApi = {
  async list(params?: {
    channel_id?: number;
    status?: SignalStatus;
    symbol?: string;
    skip?: number;
    limit?: number;
  }): Promise<Signal[]> {
    const response = await axiosInstance.get<Signal[]>('/signals/', { params });
    return response.data;
  },

  async get(id: number): Promise<SignalWithExecutions> {
    const response = await axiosInstance.get<SignalWithExecutions>(`/signals/${id}`);
    return response.data;
  },

  async getStats(days: number = 7): Promise<SignalStats> {
    const response = await axiosInstance.get<SignalStats>('/signals/stats/summary', {
      params: { days },
    });
    return response.data;
  },

  async getLatest(limit: number = 10): Promise<Partial<Signal>[]> {
    const response = await axiosInstance.get<Partial<Signal>[]>('/signals/recent/latest', {
      params: { limit },
    });
    return response.data;
  },
};
