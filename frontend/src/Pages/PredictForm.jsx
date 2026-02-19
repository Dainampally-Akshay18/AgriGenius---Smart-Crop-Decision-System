import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getWeather, savePredictionInput } from '../Services/predictionService';

function PredictForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    N: '',
    P: '',
    K: '',
    soilType: '',
    season: '',
    city: '',
    temperature: '',
    humidity: '',
    rainfall: ''
  });

  const [errors, setErrors] = useState({});
  const [weatherLoading, setWeatherLoading] = useState(false);
  const [weatherError, setWeatherError] = useState('');

  // List of common cities for dropdown
  const cities = [
    'Delhi',
    'Mumbai',
    'Bangalore',
    'Chennai',
    'Kolkata',
    'Hyderabad',
    'Pune',
    'Ahmedabad',
    'Jaipur',
    'Lucknow'
  ];

  const soilTypes = ['Sandy', 'Loamy', 'Clay', 'Silty'];
  const seasons = ['Kharif', 'Rabi', 'Summer'];

  // Handle input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  // Handle city input change (typing)
  const handleCityChange = (e) => {
    const city = e.target.value;
    setFormData(prev => ({
      ...prev,
      city: city
    }));
  };

  // Handle city onBlur (after user leaves field)
  const handleCityBlur = async () => {
    const city = formData.city.trim();

    if (!city) {
      setFormData(prev => ({
        ...prev,
        temperature: '',
        humidity: '',
        rainfall: ''
      }));
      setWeatherError('');
      return;
    }

    setWeatherError('');
    setWeatherLoading(true);
    try {
      const weatherData = await getWeather(city);
      setFormData(prev => ({
        ...prev,
        temperature: weatherData.temperature ?? '',
humidity: weatherData.humidity ?? '',
rainfall: weatherData.rainfall ?? ''
      }));
    } catch (error) {
      setWeatherError(`Failed to fetch weather for ${city}. Please try again.`);
      setFormData(prev => ({
        ...prev,
        temperature: '',
        humidity: '',
        rainfall: ''
      }));
    } finally {
      setWeatherLoading(false);
    }
  };

  // Validate form
  const validateForm = () => {
    const newErrors = {};

    if (!formData.N || isNaN(formData.N) || formData.N < 0) {
      newErrors.N = 'Nitrogen must be a valid number';
    }
    if (!formData.P || isNaN(formData.P) || formData.P < 0) {
      newErrors.P = 'Phosphorus must be a valid number';
    }
    if (!formData.K || isNaN(formData.K) || formData.K < 0) {
      newErrors.K = 'Potassium must be a valid number';
    }
    if (!formData.soilType) {
      newErrors.soilType = 'Soil type is required';
    }
    if (!formData.season) {
      newErrors.season = 'Season is required';
    }
    if (!formData.city || !formData.city.trim()) {
      newErrors.city = 'City is required';
    }

    return newErrors;
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();

    const newErrors = validateForm();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    // Save to localStorage and navigate
    savePredictionInput(formData);
    navigate('/prediction');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 py-8 px-4 sm:px-6 lg:px-8">
      {/* Container */}
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Soil & Location Input</h1>
          <p className="text-gray-600">Enter your soil nutrients and select a city to get weather data</p>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <form onSubmit={handleSubmit}>
            {/* Nitrogen */}
            <div className="mb-6">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Nitrogen (N) <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                name="N"
                value={formData.N}
                onChange={handleInputChange}
                placeholder="Enter nitrogen level"
                className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 ${errors.N ? 'border-red-500' : 'border-gray-300'
                  }`}
                step="0.1"
              />
              {errors.N && <p className="text-red-500 text-sm mt-1">{errors.N}</p>}
            </div>

            {/* Phosphorus */}
            <div className="mb-6">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Phosphorus (P) <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                name="P"
                value={formData.P}
                onChange={handleInputChange}
                placeholder="Enter phosphorus level"
                className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 ${errors.P ? 'border-red-500' : 'border-gray-300'
                  }`}
                step="0.1"
              />
              {errors.P && <p className="text-red-500 text-sm mt-1">{errors.P}</p>}
            </div>

            {/* Potassium */}
            <div className="mb-6">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Potassium (K) <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                name="K"
                value={formData.K}
                onChange={handleInputChange}
                placeholder="Enter potassium level"
                className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 ${errors.K ? 'border-red-500' : 'border-gray-300'
                  }`}
                step="0.1"
              />
              {errors.K && <p className="text-red-500 text-sm mt-1">{errors.K}</p>}
            </div>

            {/* Soil Type */}
            <div className="mb-6">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Soil Type <span className="text-red-500">*</span>
              </label>
              <select
                name="soilType"
                value={formData.soilType}
                onChange={handleInputChange}
                className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 ${errors.soilType ? 'border-red-500' : 'border-gray-300'
                  }`}
              >
                <option value="">Select soil type</option>
                {soilTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
              {errors.soilType && <p className="text-red-500 text-sm mt-1">{errors.soilType}</p>}
            </div>

            {/* Season */}
            <div className="mb-6">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Season <span className="text-red-500">*</span>
              </label>
              <select
                name="season"
                value={formData.season}
                onChange={handleInputChange}
                className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 ${errors.season ? 'border-red-500' : 'border-gray-300'
                  }`}
              >
                <option value="">Select season</option>
                {seasons.map(season => (
                  <option key={season} value={season}>{season}</option>
                ))}
              </select>
              {errors.season && <p className="text-red-500 text-sm mt-1">{errors.season}</p>}
            </div>

            {/* City */}
            <div className="mb-6">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                City <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="city"
                value={formData.city}
                onChange={handleCityChange}
                onBlur={handleCityBlur}
                placeholder="Type or select a city"
                list="cityList"
                className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 ${errors.city ? 'border-red-500' : 'border-gray-300'
                  }`}
              />
              <datalist id="cityList">
                {cities.map(city => (
                  <option key={city} value={city} />
                ))}
              </datalist>
              {errors.city && <p className="text-red-500 text-sm mt-1">{errors.city}</p>}
            </div>

            {/* Weather Loading Indicator */}
            {weatherLoading && (
              <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-blue-700 flex items-center">
                  <span className="inline-block w-4 h-4 border-2 border-blue-400 border-t-blue-700 rounded-full animate-spin mr-2"></span>
                  Fetching weather data...
                </p>
              </div>
            )}

            {/* Weather Error */}
            {weatherError && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-700">{weatherError}</p>
              </div>
            )}

            {/* Weather Data (Auto-filled) */}
            {formData.city && (
              formData.temperature !== '' ||
              formData.humidity !== '' ||
              formData.rainfall !== '') && (
                <div className="mb-6 bg-gray-50 p-4 rounded-lg border border-gray-200">
                  <h3 className="text-sm font-semibold text-gray-700 mb-4">Auto-Filled Weather Data</h3>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-xs font-semibold text-gray-600 mb-1">Temperature (°C)</label>
                      <input
                        type="text"
                        name="temperature"
                        value={formData.temperature}
                        readOnly
                        className="w-full px-3 py-2 border border-gray-300 rounded bg-gray-100 text-gray-700"
                        placeholder="Auto-filled"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-gray-600 mb-1">Humidity (%)</label>
                      <input
                        type="text"
                        name="humidity"
                        value={formData.humidity}
                        readOnly
                        className="w-full px-3 py-2 border border-gray-300 rounded bg-gray-100 text-gray-700"
                        placeholder="Auto-filled"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-gray-600 mb-1">Rainfall (mm)</label>
                      <input
                        type="text"
                        name="rainfall"
                        value={formData.rainfall}
                        readOnly
                        className="w-full px-3 py-2 border border-gray-300 rounded bg-gray-100 text-gray-700"
                        placeholder="Auto-filled"
                      />
                    </div>
                  </div>
                </div>
              )}

            {/* Submit Button */}
            <button
              type="submit"
              className="w-full px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg shadow-md transition-colors duration-200"
            >
              Predict
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default PredictForm;
