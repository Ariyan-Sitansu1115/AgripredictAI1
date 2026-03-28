import api from './api';
import { API_ENDPOINTS } from '../utils/constants';
import { LoginCredentials, RegisterCredentials, User } from '../types';

export const loginUser = async (credentials: LoginCredentials): Promise<{ user: User; token: string }> => {
  const response = await api.post(API_ENDPOINTS.LOGIN, credentials);
  return response.data;
};

export const registerUser = async (credentials: RegisterCredentials): Promise<{ user: User; token: string }> => {
  const response = await api.post(API_ENDPOINTS.REGISTER, credentials);
  return response.data;
};

export const refreshToken = async (): Promise<{ token: string }> => {
  const response = await api.post(API_ENDPOINTS.REFRESH);
  return response.data;
};

export const logoutUser = (): void => {
  localStorage.removeItem('agripredict_token');
  localStorage.removeItem('agripredict_user');
};
