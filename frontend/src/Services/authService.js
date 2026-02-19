import apiRequest from './api';

export const register = async (name, email, password) => {
  const data = await apiRequest('/api/auth/register', {
    method: 'POST',
    skipAuth: true,
    body: JSON.stringify({ name, email, password })
  });
  
  if (data.token) {
    localStorage.setItem('token', data.token);
  }
  
  return data;
};

export const login = async (email, password) => {
  const data = await apiRequest('/api/auth/login', {
    method: 'POST',
    skipAuth: true,
    body: JSON.stringify({ email, password })
  });
  
  if (data.token) {
    localStorage.setItem('token', data.token);
  }
  
  return data;
};

export const logout = () => {
  localStorage.removeItem('token');
};

export const isAuthenticated = () => {
  return !!localStorage.getItem('token');
};
