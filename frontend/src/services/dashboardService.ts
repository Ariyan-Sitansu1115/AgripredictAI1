import api from './api';
import { API_ENDPOINTS } from '../utils/constants';
import { DashboardData, MetricCard } from '../types';

export const getDashboardData = async (): Promise<DashboardData> => {
  const response = await api.get(API_ENDPOINTS.DASHBOARD);
  return response.data;
};

export const getMetrics = async (): Promise<MetricCard[]> => {
  const response = await api.get(`${API_ENDPOINTS.DASHBOARD}/metrics`);
  return response.data;
};
