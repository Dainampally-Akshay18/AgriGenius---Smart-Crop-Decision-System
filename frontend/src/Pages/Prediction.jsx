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
      <div className="flex-1 md:ml-64 min-h-[calc(100vh-4rem)] bg-white w-full md:w-auto">
        <div className="p-8 max-w-6xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Crop Prediction
            </h1>
            <p className="text-gray-600 text-sm">
              Based on your soil nutrients and location
            </p>
          </div>

          {/* Loading State */}
          {loading && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-12">
              <div className="flex flex-col items-center justify-center space-y-4">
                <div className="w-12 h-12 border-4 border-green-200 border-t-green-600 rounded-full animate-spin"></div>
                <p className="text-gray-600">
                  Analyzing soil data and generating prediction...
                </p>
              </div>
            </div>
          )}

          {/* Error State */}
          {error && !loading && (
            <div className="bg-white rounded-xl shadow-sm border border-red-100 p-8">
              <div className="flex items-start space-x-4">
                <span className="text-3xl">❌</span>
                <div>
                  <h3 className="text-lg font-semibold text-red-700 mb-2">
                    Prediction Error
                  </h3>
                  <p className="text-gray-700 text-sm mb-4">{error}</p>
                  <button
                    onClick={() => navigate('/predict')}
                    className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm rounded-lg transition-colors"
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
              <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-8">
                  Recommended Crops
                </h2>

                {prediction.recommendedCrops &&
                  prediction.recommendedCrops.length > 0 ? (
                  <div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      {prediction.recommendedCrops.map((crop, index) => (
                        <div
                          key={index}
                          className={`h-full p-6 rounded-xl border-2 transition-all duration-200 flex flex-col ${
                            index === 0
                              ? 'bg-green-50 border-green-200 ring-2 ring-green-100'
                              : 'bg-gray-50 border-gray-100 hover:border-gray-200'
                          }`}
                        >
                          <div className="text-center flex-1 flex flex-col justify-center">
                            <div className="text-5xl mb-4">🌾</div>
                            <h3
                              className={`text-xl font-bold mb-6 ${
                                index === 0
                                  ? 'text-green-700'
                                  : 'text-gray-800'
                              }`}
                            >
                              {crop.crop}
                            </h3>

                            <div className="space-y-4">
                              <div className={`rounded-lg p-4 ${
                                index === 0
                                  ? 'bg-white/60'
                                  : 'bg-white'
                              }`}>
                                <p className="text-xs text-gray-600 font-medium mb-1 uppercase tracking-wide">
                                  Yield
                                </p>
                                <p className="text-2xl font-bold text-gray-900">
                                  {crop.yield || 'N/A'}
                                </p>
                                <p className="text-xs text-gray-500 mt-1">Units</p>
                              </div>

                              <div className={`rounded-lg p-4 ${
                                index === 0
                                  ? 'bg-white/60'
                                  : 'bg-white'
                              }`}>
                                <p className="text-xs text-gray-600 font-medium mb-1 uppercase tracking-wide">
                                  Price
                                </p>
                                <p className="text-2xl font-bold text-gray-900">
                                  ₹{crop.price || 'N/A'}
                                </p>
                                <p className="text-xs text-gray-500 mt-1">Per unit</p>
                              </div>
                            </div>

                            {index === 0 && (
                              <div className="mt-6 inline-block bg-green-600 text-white px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-wide mx-auto">
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
              <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8">
                <h3 className="text-xl font-bold text-gray-900 mb-6">
                  Input Parameters
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div className="p-4 bg-gray-50 rounded-lg border border-gray-100">
                    <p className="text-xs text-gray-600 font-medium uppercase tracking-wide mb-2">Nitrogen (N)</p>
                    <p className="text-lg font-bold text-gray-900">
                      {formData?.N}
                    </p>
                  </div>
                  <div className="p-4 bg-gray-50 rounded-lg border border-gray-100">
                    <p className="text-xs text-gray-600 font-medium uppercase tracking-wide mb-2">
                      Phosphorus (P)
                    </p>
                    <p className="text-lg font-bold text-gray-900">
                      {formData?.P}
                    </p>
                  </div>
                  <div className="p-4 bg-gray-50 rounded-lg border border-gray-100">
                    <p className="text-xs text-gray-600 font-medium uppercase tracking-wide mb-2">Potassium (K)</p>
                    <p className="text-lg font-bold text-gray-900">
                      {formData?.K}
                    </p>
                  </div>
                  <div className="p-4 bg-gray-50 rounded-lg border border-gray-100">
                    <p className="text-xs text-gray-600 font-medium uppercase tracking-wide mb-2">Soil Type</p>
                    <p className="text-lg font-bold text-gray-900">
                      {formData?.soilType}
                    </p>
                  </div>
                  <div className="p-4 bg-gray-50 rounded-lg border border-gray-100">
                    <p className="text-xs text-gray-600 font-medium uppercase tracking-wide mb-2">Season</p>
                    <p className="text-lg font-bold text-gray-900">
                      {formData?.season}
                    </p>
                  </div>
                  <div className="p-4 bg-gray-50 rounded-lg border border-gray-100">
                    <p className="text-xs text-gray-600 font-medium uppercase tracking-wide mb-2">Location</p>
                    <p className="text-lg font-bold text-gray-900">
                      {formData?.city}
                    </p>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3 pt-2">
                <button
                  onClick={() => navigate('/predict')}
                  className="flex-1 px-6 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-lg transition-colors text-sm"
                >
                  ← Back to Form
                </button>
                <button
                  onClick={() => navigate('/prediction/noise')}
                  className="flex-1 px-6 py-2.5 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg transition-colors text-sm"
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
