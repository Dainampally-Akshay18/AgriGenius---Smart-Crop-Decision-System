import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Sidebar from '../Components/Sidebar';
import { getPredictionInput, evaluateNoise } from '../Services/predictionService';

function Noise() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState(null);
  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Load form data and fetch evaluation on mount
  useEffect(() => {
    const loadEvaluation = async () => {
      try {
        const storedData = getPredictionInput();
        if (!storedData) {
          navigate('/predict');
          return;
        }

        setFormData(storedData);
        setLoading(true);

        const result = await evaluateNoise(storedData);
        setEvaluation(result);
        setError('');
      } catch (err) {
        setError(
          err.message || 'Failed to evaluate noise stability. Please try again.'
        );
        setEvaluation(null);
      } finally {
        setLoading(false);
      }
    };

    loadEvaluation();
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
              Noise Stability Evaluation
            </h1>
            <p className="text-gray-600 text-sm">
              Test model robustness with noisy input data
            </p>
          </div>

          {/* Loading State */}
          {loading && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-12">
              <div className="flex flex-col items-center justify-center space-y-4">
                <div className="w-12 h-12 border-4 border-green-200 border-t-green-600 rounded-full animate-spin"></div>
                <p className="text-gray-600">
                  Running noise stability tests...
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
                    Evaluation Error
                  </h3>
                  <p className="text-gray-700 text-sm mb-4">{error}</p>
                  <button
                    onClick={() => navigate('/prediction')}
                    className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm rounded-lg transition-colors"
                  >
                    Back to Prediction
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Results */}
          {evaluation && !loading && (
            <div className="space-y-6">
              {/* Key Metrics */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                  <p className="text-xs text-gray-600 font-medium uppercase tracking-wide mb-2">Predicted Crop</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {evaluation.predicted_crop || 'N/A'}
                  </p>
                </div>

                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                  <p className="text-xs text-gray-600 font-medium uppercase tracking-wide mb-2">RSS Score</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {evaluation.rss ? evaluation.rss.toFixed(4) : 'N/A'}
                  </p>
                </div>

                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                  <p className="text-xs text-gray-600 font-medium uppercase tracking-wide mb-2">Prediction Changes</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {evaluation.prediction_changes || 0}
                  </p>
                </div>

                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                  <p className="text-xs text-gray-600 font-medium uppercase tracking-wide mb-2">Total Runs</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {evaluation.total_runs || 0}
                  </p>
                </div>
              </div>

              {/* Noise Percentage */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">
                  Noise Impact Summary
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="p-6 bg-blue-50 rounded-xl border border-blue-100">
                    <p className="text-xs text-gray-600 font-medium uppercase tracking-wide mb-2">Noise Percentage</p>
                    <p className="text-3xl font-bold text-blue-600">
                      {evaluation.noise_percentage
                        ? evaluation.noise_percentage.toFixed(2)
                        : 'N/A'}
                      %
                    </p>
                    <p className="text-xs text-gray-600 mt-3">
                      Percentage of inputs with noise applied
                    </p>
                  </div>

                  <div className="p-6 bg-green-50 rounded-xl border border-green-100">
                    <p className="text-xs text-gray-600 font-medium uppercase tracking-wide mb-2">Stability</p>
                    <p className="text-3xl font-bold text-green-600">
                      {((100 -
                        (evaluation.prediction_changes || 0) /
                          (evaluation.total_runs || 1)) *
                        100).toFixed(1)}
                      %
                    </p>
                    <p className="text-xs text-gray-600 mt-3">
                      Model prediction consistency
                    </p>
                  </div>
                </div>
              </div>

              {/* Prediction Distribution Table */}
              {evaluation.prediction_distribution && (
                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-6">
                    Prediction Distribution
                  </h2>
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead>
                        <tr className="border-b border-gray-200 bg-gray-50">
                          <th className="text-left py-4 px-4 font-semibold text-gray-900 text-sm">
                            Crop
                          </th>
                          <th className="text-right py-4 px-4 font-semibold text-gray-900 text-sm">
                            Count
                          </th>
                          <th className="text-right py-4 px-4 font-semibold text-gray-900 text-sm">
                            Percentage
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {Object.entries(
                          evaluation.prediction_distribution
                        ).map(([crop, count], idx) => (
                          <tr
                            key={idx}
                            className={`border-b border-gray-100 transition-colors ${
                              idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'
                            } hover:bg-gray-100`}
                          >
                            <td className="py-4 px-4 text-gray-900 font-medium text-sm">
                              {crop}
                            </td>
                            <td className="py-4 px-4 text-right text-gray-700 text-sm">
                              {count}
                            </td>
                            <td className="py-4 px-4 text-right text-gray-700 text-sm font-medium">
                              {(
                                (count /
                                  (evaluation.total_runs || 1)) *
                                100
                              ).toFixed(1)}
                              %
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Navigation Buttons */}
              <div className="flex gap-3 pt-2">
                <button
                  onClick={() => navigate('/prediction')}
                  className="flex-1 px-6 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-lg transition-colors text-sm"
                >
                  ← Crop Prediction
                </button>
                <button
                  onClick={() => navigate('/prediction/missing')}
                  className="flex-1 px-6 py-2.5 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg transition-colors text-sm"
                >
                  Missing Feature →
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Noise;
