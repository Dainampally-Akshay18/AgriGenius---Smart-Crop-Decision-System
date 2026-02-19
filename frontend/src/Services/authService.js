import apiRequest from './api';

export const register = async (name, email, password) => {
  const data = await apiRequest('/api/auth/register', {
    method: 'POST',
    skipAuth: true,
    body: JSON.stringify({ name, email, password })
  });
  
  if (data.token) {
    localStorage.setItem('token', data.token);
    localStorage.setItem('userName', name);
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
    // Store user name if available in response, otherwise use email
    if (data.name) {
      localStorage.setItem('userName', data.name);
    } else if (data.user && data.user.name) {
      localStorage.setItem('userName', data.user.name);
    } else {
      localStorage.setItem('userName', email.split('@')[0]);
    }
  }
  
  return data;
};

export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('userName');
};

export const isAuthenticated = () => {
  return !!localStorage.getItem('token');
};
