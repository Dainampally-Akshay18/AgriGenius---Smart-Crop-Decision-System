import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Sidebar from '../Components/Sidebar';
import { getPredictionInput, evaluateMissing } from '../Services/predictionService';

function Missing() {
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

        const result = await evaluateMissing(storedData);
        setEvaluation(result);
        setError('');
      } catch (err) {
        setError(
          err.message || 'Failed to evaluate missing features. Please try again.'
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
              Missing Feature Evaluation
            </h1>
            <p className="text-gray-600 text-sm">
              Assess model robustness when features are missing
            </p>
          </div>

          {/* Loading State */}
          {loading && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-12">
              <div className="flex flex-col items-center justify-center space-y-4">
                <div className="w-12 h-12 border-4 border-green-200 border-t-green-600 rounded-full animate-spin"></div>
                <p className="text-gray-600">
                  Testing missing feature impact...
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
                  <p className="text-xs text-gray-600 font-medium uppercase tracking-wide mb-2">
                    Baseline Confidence
                  </p>
                  <p className="text-2xl font-bold text-gray-900">
                    {evaluation.baseline_confidence
                      ? (evaluation.baseline_confidence * 100).toFixed(1)
                      : 'N/A'}
                    %
                  </p>
                </div>

                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                  <p className="text-xs text-gray-600 font-medium uppercase tracking-wide mb-2">Stability Score</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {evaluation.stability_score
                      ? (evaluation.stability_score * 100).toFixed(1)
                      : 'N/A'}
                    %
                  </p>
                </div>

                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                  <p className="text-xs text-gray-600 font-medium uppercase tracking-wide mb-2">Total Tests</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {evaluation.total_tests || 0}
                  </p>
                </div>
              </div>

              {/* Summary */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">
                  Robustness Analysis
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="p-6 bg-orange-50 rounded-xl border border-orange-100">
                    <p className="text-xs text-gray-600 font-medium uppercase tracking-wide mb-2">
                      Prediction Changes
                    </p>
                    <p className="text-3xl font-bold text-orange-600">
                      {evaluation.prediction_changes || 0}
                    </p>
                    <p className="text-xs text-gray-600 mt-3">
                      Times prediction changed when features missing
                    </p>
                  </div>

                  <div className="p-6 bg-red-50 rounded-xl border border-red-100">
                    <p className="text-xs text-gray-600 font-medium uppercase tracking-wide mb-2">
                      Impact Severity
                    </p>
                    <p className="text-3xl font-bold text-red-600">
                      {evaluation.prediction_changes > 0
                        ? 'HIGH'
                        : 'LOW'}
                    </p>
                    <p className="text-xs text-gray-600 mt-3">
                      Model sensitivity to missing features
                    </p>
                  </div>
                </div>
              </div>

              {/* Feature Results Table */}
              {evaluation.feature_results && (
                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-6">
                    Feature Impact Analysis
                  </h2>
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead>
                        <tr className="border-b border-gray-200 bg-gray-50">
                          <th className="text-left py-4 px-4 font-semibold text-gray-900 text-sm">
                            Feature
                          </th>
                          <th className="text-left py-4 px-4 font-semibold text-gray-900 text-sm">
                            Impact
                          </th>
                          <th className="text-right py-4 px-4 font-semibold text-gray-900 text-sm">
                            Changes
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {Object.entries(evaluation.feature_results).map(
                          ([feature, data], idx) => (
                            <tr
                              key={idx}
                              className={`border-b border-gray-100 transition-colors ${
                                idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'
                              } hover:bg-gray-100`}
                            >
                              <td className="py-4 px-4 text-gray-900 font-medium text-sm">
                                {typeof data === 'object'
                                  ? data.feature || feature
                                  : feature}
                              </td>
                              <td className="py-4 px-4">
                                <span
                                  className={`px-3 py-1.5 rounded-full text-xs font-bold ${
                                    typeof data === 'object' &&
                                    data.changes > 0
                                      ? 'bg-red-100 text-red-700'
                                      : 'bg-green-100 text-green-700'
                                  }`}
                                >
                                  {typeof data === 'object' && data.changes > 0
                                    ? 'HIGH'
                                    : 'LOW'}
                                </span>
                              </td>
                              <td className="py-4 px-4 text-right text-gray-700 font-medium text-sm">
                                {typeof data === 'object'
                                  ? data.changes || 0
                                  : data}
                              </td>
                            </tr>
                          )
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Navigation Buttons */}
              <div className="flex gap-3 pt-2">
                <button
                  onClick={() => navigate('/prediction/noise')}
                  className="flex-1 px-6 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-lg transition-colors text-sm"
                >
                  ← Noise Evaluation
                </button>
                <button
                  onClick={() => navigate('/prediction/agreement')}
                  className="flex-1 px-6 py-2.5 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg transition-colors text-sm"
                >
                  Model Agreement →
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Missing;
