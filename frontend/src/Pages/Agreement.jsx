import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Sidebar from '../Components/Sidebar';
import { getPredictionInput, evaluateAgreement } from '../Services/predictionService';

function Agreement() {
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

        const result = await evaluateAgreement(storedData);
        setEvaluation(result);
        setError('');
      } catch (err) {
        setError(
          err.message || 'Failed to evaluate model agreement. Please try again.'
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
      <div className="flex-1 ml-64 min-h-[calc(100vh-4rem)] bg-white">
        <div className="p-8 max-w-6xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Model Agreement Evaluation
            </h1>
            <p className="text-gray-600 text-sm">
              Compare predictions across different algorithms
            </p>
          </div>

          {/* Loading State */}
          {loading && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-12">
              <div className="flex flex-col items-center justify-center space-y-4">
                <div className="w-12 h-12 border-4 border-green-200 border-t-green-600 rounded-full animate-spin"></div>
                <p className="text-gray-600">
                  Comparing predictions across models...
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
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                  <p className="text-xs text-gray-600 font-medium uppercase tracking-wide mb-2">Predicted Crop</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {evaluation.predicted_crop || 'N/A'}
                  </p>
                </div>

                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                  <p className="text-xs text-gray-600 font-medium uppercase tracking-wide mb-2">Agreement Ratio</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {evaluation.agreement_ratio
                      ? (evaluation.agreement_ratio * 100).toFixed(1)
                      : 'N/A'}
                    %
                  </p>
                </div>

                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                  <p className="text-xs text-gray-600 font-medium uppercase tracking-wide mb-2">Consensus</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {evaluation.all_agree ? '✅ All Agree' : '⚠️ Divided'}
                  </p>
                </div>
              </div>

              {/* Agreement Status Card */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">
                  Model Consensus
                </h2>
                <div
                  className={`p-8 rounded-xl text-center border-2 ${
                    evaluation.all_agree
                      ? 'bg-green-50 border-green-200'
                      : 'bg-yellow-50 border-yellow-200'
                  }`}
                >
                  <div className="text-5xl mb-4">
                    {evaluation.all_agree ? '🎯' : '⚡'}
                  </div>
                  <h3
                    className={`text-2xl font-bold mb-2 ${
                      evaluation.all_agree
                        ? 'text-green-700'
                        : 'text-yellow-700'
                    }`}
                  >
                    {evaluation.all_agree
                      ? 'All Models Agree'
                      : 'Models Disagree'}
                  </h3>
                  <p
                    className={`text-sm ${
                      evaluation.all_agree
                        ? 'text-green-600'
                        : 'text-yellow-600'
                    }`}
                  >
                    {evaluation.all_agree
                      ? 'All models predict the same crop'
                      : 'Models have different predictions'}
                  </p>
                </div>
              </div>

              {/* Model Predictions Table */}
              {evaluation.predictions && (
                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-6">
                    Model Predictions Comparison
                  </h2>
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead>
                        <tr className="border-b border-gray-200 bg-gray-50">
                          <th className="text-left py-4 px-4 font-semibold text-gray-900 text-sm">
                            Model
                          </th>
                          <th className="text-left py-4 px-4 font-semibold text-gray-900 text-sm">
                            Prediction
                          </th>
                          <th className="text-center py-4 px-4 font-semibold text-gray-900 text-sm">
                            Status
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {Object.entries(evaluation.predictions).map(
                          ([model, prediction], idx) => {
                            const isConsensus =
                              prediction === evaluation.predicted_crop;
                            return (
                              <tr
                                key={idx}
                                className={`border-b border-gray-100 transition-colors ${
                                  idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'
                                } hover:bg-gray-100`}
                              >
                                <td className="py-4 px-4 text-gray-900 font-semibold text-sm">
                                  {model.toUpperCase()}
                                </td>
                                <td className="py-4 px-4 text-gray-900 text-sm">
                                  {prediction || 'N/A'}
                                </td>
                                <td className="py-4 px-4 text-center">
                                  <span
                                    className={`px-3 py-1.5 rounded-full text-xs font-bold ${
                                      isConsensus
                                        ? 'bg-green-100 text-green-700'
                                        : 'bg-orange-100 text-orange-700'
                                    }`}
                                  >
                                    {isConsensus ? '✓ Agrees' : '✗ Differs'}
                                  </span>
                                </td>
                              </tr>
                            );
                          }
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Prediction Distribution */}
              {evaluation.prediction_distribution && (
                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-6">
                    Overall Prediction Distribution
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {Object.entries(evaluation.prediction_distribution).map(
                      ([crop, count], idx) => (
                        <div
                          key={idx}
                          className="p-6 bg-blue-50 rounded-xl border border-blue-100"
                        >
                          <p className="text-sm text-gray-600 font-medium mb-2">{crop}</p>
                          <p className="text-2xl font-bold text-blue-600">
                            {count}/
                            {evaluation.total_models || 4} models
                          </p>
                        </div>
                      )
                    )}
                  </div>
                </div>
              )}

              {/* Total Models Info */}
              <div className="bg-blue-50 rounded-xl shadow-sm border border-blue-100 p-6">
                <p className="text-sm text-gray-700">
                  <span className="font-semibold">Total Models Evaluated:</span> {evaluation.total_models || 4} (Random Forest, XGBoost, SVM, MLP)
                </p>
              </div>

              {/* Navigation Buttons */}
              <div className="flex gap-3 pt-2">
                <button
                  onClick={() => navigate('/prediction/missing')}
                  className="flex-1 px-6 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-lg transition-colors text-sm"
                >
                  ← Missing Feature
                </button>
                <button
                  onClick={() => navigate('/prediction')}
                  className="flex-1 px-6 py-2.5 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg transition-colors text-sm"
                >
                  Back to Prediction
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Agreement;
