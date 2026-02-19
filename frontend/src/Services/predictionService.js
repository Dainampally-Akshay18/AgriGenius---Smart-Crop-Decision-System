import apiRequest from './api';

// Get weather data for a given city (No auth required)
export const getWeather = async (location) => {
  try {
    const data = await apiRequest(`/api/weather?location=${encodeURIComponent(location)}`, {
      method: 'GET',
      skipAuth: true
    });
    return data;
  } catch (error) {
    throw error;
  }
};

// Store prediction input form data in localStorage
export const savePredictionInput = (formData) => {
  localStorage.setItem('predictionInput', JSON.stringify(formData));
};

// Retrieve prediction input from localStorage
export const getPredictionInput = () => {
  const data = localStorage.getItem('predictionInput');
  return data ? JSON.parse(data) : null;
};

// Clear prediction input from localStorage
export const clearPredictionInput = () => {
  localStorage.removeItem('predictionInput');
};

// Call crop prediction API
export const predictCrop = async (formData) => {
  try {
    const requestBody = {
      N: parseFloat(formData.N),
      P: parseFloat(formData.P),
      K: parseFloat(formData.K),
      soilType: formData.soilType,
      season: formData.season,
      location: formData.city
    };

    const data = await apiRequest('/api/predict/crop', {
      method: 'POST',
      body: JSON.stringify(requestBody)
    });

    return data;
  } catch (error) {
    throw error;
  }
};
