import api from './api';

export interface User {
  id: string;
  email: string;
  username: string;
  first_name?: string;
  last_name?: string;
  work_address?: string;
  work_lat?: number;
  work_lng?: number;
  max_commute_time?: number;
  budget_min?: number;
  budget_max?: number;
  preferred_areas?: string[];
}

export interface LoginResponse {
  user: User;
  access_token: string;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
  first_name?: string;
  last_name?: string;
}

class AuthService {
  async login(email: string, password: string): Promise<LoginResponse> {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  }

  async register(userData: RegisterData): Promise<LoginResponse> {
    const response = await api.post('/auth/register', userData);
    return response.data;
  }

  async getProfile(): Promise<User> {
    const response = await api.get('/auth/profile');
    return response.data;
  }

  async updateProfile(data: Partial<User>): Promise<User> {
    const response = await api.put('/auth/profile', data);
    return response.data.user;
  }

  async googleOAuth(token: string, email: string, name: string, googleId: string): Promise<LoginResponse> {
    const response = await api.post('/auth/oauth/google', {
      token,
      email,
      name,
      google_id: googleId,
    });
    return response.data;
  }
}

export const authService = new AuthService();
