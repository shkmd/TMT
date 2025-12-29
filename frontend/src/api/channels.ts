import axiosInstance from './axios';
import { TelegramChannel, TelegramChannelCreate, TelegramChannelUpdate } from '@/types/api';

export const channelsApi = {
  async list(): Promise<TelegramChannel[]> {
    const response = await axiosInstance.get<TelegramChannel[]>('/channels/');
    return response.data;
  },

  async get(id: number): Promise<TelegramChannel> {
    const response = await axiosInstance.get<TelegramChannel>(`/channels/${id}`);
    return response.data;
  },

  async create(data: TelegramChannelCreate): Promise<TelegramChannel> {
    const response = await axiosInstance.post<TelegramChannel>('/channels/', data);
    return response.data;
  },

  async update(id: number, data: TelegramChannelUpdate): Promise<TelegramChannel> {
    const response = await axiosInstance.put<TelegramChannel>(`/channels/${id}`, data);
    return response.data;
  },

  async delete(id: number): Promise<void> {
    await axiosInstance.delete(`/channels/${id}`);
  },
};
