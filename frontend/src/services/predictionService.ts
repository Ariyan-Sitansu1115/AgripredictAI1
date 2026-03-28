import api from './api';
import { API_ENDPOINTS } from '../utils/constants';
import { PricePrediction, PriceHistoryPoint } from '../types';

export const getPricePredictions = async (crop?: string): Promise<PricePrediction[]> => {
  const params = crop ? { crop } : {};
  const response = await api.get(API_ENDPOINTS.PREDICTION, { params });
  return response.data;
};

export const getPriceHistory = async (crop: string, days = 30): Promise<PriceHistoryPoint[]> => {
  const response = await api.get(`${API_ENDPOINTS.PREDICTION}/history`, { params: { crop, days } });
  return response.data;
};
