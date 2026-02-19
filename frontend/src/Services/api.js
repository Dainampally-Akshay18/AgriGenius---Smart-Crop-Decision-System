const API_BASE_URL = 'http://127.0.0.1:5000';

export const apiRequest = async (endpoint, options = {}) => {
  const token = localStorage.getItem('token');
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  if (token && !options.skipAuth) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const config = {
    ...options,
    headers,
  };
  
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
    const data = await response.json();
    
    if (!response.ok) {
      throw {
        status: response.status,
        message: data.detail || data.message || 'Request failed',
        data
      };
    }
    
    return data;
  } catch (error) {
    if (error.status) {
      throw error;
    }
    throw {
      status: 500,
      message: 'Network error',
      data: null
    };
  }
};

export default apiRequest;
