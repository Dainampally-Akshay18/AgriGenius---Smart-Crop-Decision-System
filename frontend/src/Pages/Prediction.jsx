import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Sidebar from '../Components/Sidebar';
import { getPredictionInput, predictCrop } from '../Services/predictionService';

function Prediction() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Load form data and fetch prediction on mount
  useEffect(() => {
    const loadPrediction = async () => {
      try {
        // Get form data from localStorage
        const storedData = getPredictionInput();
        if (!storedData) {
          navigate('/predict');
          return;
        }

        setFormData(storedData);
        setLoading(true);

        // Call crop prediction API
        const result = await predictCrop(storedData);
        setPrediction(result);
        setError('');
      } catch (err) {
        setError(
          err.message || 'Failed to fetch prediction. Please try again.'
        );
        setPrediction(null);
      } finally {
        setLoading(false);
      }
    };

    loadPrediction();
  }, [navigate]);

  return (
    <div className="flex">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 ml-64 min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
        <div className="p-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              Crop Prediction
            </h1>
            <p className="text-gray-600">
              Based on your soil nutrients and location
            </p>
          </div>

          {/* Loading State */}
          {loading && (
            <div className="bg-white rounded-lg shadow-lg p-12">
              <div className="flex flex-col items-center justify-center space-y-4">
                <div className="w-12 h-12 border-4 border-green-200 border-t-green-600 rounded-full animate-spin"></div>
                <p className="text-lg text-gray-600">
                  Analyzing soil data and generating prediction...
                </p>
              </div>
            </div>
          )}

          {/* Error State */}
          {error && !loading && (
            <div className="bg-white rounded-lg shadow-lg p-8 border-l-4 border-red-500">
              <div className="flex items-start space-x-4">
                <span className="text-3xl">❌</span>
                <div>
                  <h3 className="text-xl font-semibold text-red-700 mb-2">
                    Prediction Error
                  </h3>
                  <p className="text-gray-700 mb-4">{error}</p>
                  <button
                    onClick={() => navigate('/predict')}
                    className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
                  >
                    Back to Form
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Prediction Results */}
          {prediction && !loading && (
            <div className="space-y-6">
              {/* Main Prediction Card */}
              <div className="bg-white rounded-lg shadow-lg p-8 border-t-4 border-green-600">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">
                  Recommended Crop
                </h2>

                {prediction.recommendedCrops &&
                  prediction.recommendedCrops.length > 0 ? (
                  <div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      {prediction.recommendedCrops.map((crop, index) => (
                        <div
                          key={index}
                          className={`p-6 rounded-lg border-2 transition-all ${
                            index === 0
                              ? 'bg-green-50 border-green-500 ring-2 ring-green-200'
                              : 'bg-gray-50 border-gray-300'
                          }`}
                        >
                          <div className="text-center">
                            <div className="text-4xl mb-3">🌾</div>
                            <h3
                              className={`text-2xl font-bold mb-4 ${
                                index === 0
                                  ? 'text-green-700'
                                  : 'text-gray-800'
                              }`}
                            >
                              {crop.crop}
                            </h3>

                            <div className="space-y-3">
                              <div className="bg-white rounded p-3">
                                <p className="text-sm text-gray-600 mb-1">
                                  Yield
                                </p>
                                <p className="text-xl font-semibold text-gray-900">
                                  {crop.yield || 'N/A'} units
                                </p>
                              </div>

                              <div className="bg-white rounded p-3">
                                <p className="text-sm text-gray-600 mb-1">
                                  Price
                                </p>
                                <p className="text-xl font-semibold text-gray-900">
                                  ₹{crop.price || 'N/A'} per unit
                                </p>
                              </div>
                            </div>

                            {index === 0 && (
                              <div className="mt-4 inline-block bg-green-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
                                ⭐ Top Recommendation
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <p className="text-gray-600 text-lg">
                      No crops found for the given conditions.
                    </p>
                  </div>
                )}
              </div>

              {/* Input Summary Card */}
              <div className="bg-white rounded-lg shadow-lg p-8">
                <h3 className="text-xl font-bold text-gray-900 mb-6">
                  Input Parameters
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600 mb-1">Nitrogen (N)</p>
                    <p className="text-lg font-semibold text-gray-900">
                      {formData?.N}
                    </p>
                  </div>
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600 mb-1">
                      Phosphorus (P)
                    </p>
                    <p className="text-lg font-semibold text-gray-900">
                      {formData?.P}
                    </p>
                  </div>
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600 mb-1">Potassium (K)</p>
                    <p className="text-lg font-semibold text-gray-900">
                      {formData?.K}
                    </p>
                  </div>
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600 mb-1">Soil Type</p>
                    <p className="text-lg font-semibold text-gray-900">
                      {formData?.soilType}
                    </p>
                  </div>
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600 mb-1">Season</p>
                    <p className="text-lg font-semibold text-gray-900">
                      {formData?.season}
                    </p>
                  </div>
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600 mb-1">Location</p>
                    <p className="text-lg font-semibold text-gray-900">
                      {formData?.city}
                    </p>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-4">
                <button
                  onClick={() => navigate('/predict')}
                  className="flex-1 px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white font-semibold rounded-lg transition-colors"
                >
                  ← Back to Form
                </button>
                <button
                  onClick={() => navigate('/prediction/noise')}
                  className="flex-1 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors"
                >
                  Noise Evaluation →
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Prediction;
