import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const navigate = useNavigate();

  const handleStartPredicting = () => {
    navigate('/predict');
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-green-50 to-white"></div>
        <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
          <div className="text-center max-w-3xl mx-auto">
            {/* Main Heading */}
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6 leading-tight">
              Smart Crop Recommendations
            </h1>

            {/* Subheading */}
            <p className="text-lg text-gray-600 mb-10 leading-relaxed">
              Make data-driven decisions with AI-powered insights. Get personalized crop recommendations based on soil nutrients and weather conditions.
            </p>

            {/* CTA Button */}
            <button
              onClick={handleStartPredicting}
              className="inline-flex px-6 py-2.5 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition-colors duration-200"
            >
              Start Predicting Now
              <span className="ml-2">→</span>
            </button>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-3">
            Why Choose AgreeGenius?
          </h2>
          <p className="text-gray-600">Powerful tools for modern agriculture</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {/* Feature 1 */}
          <div className="p-6 bg-gray-50 rounded-xl border border-gray-100 hover:border-green-200 transition-colors">
            <div className="text-4xl mb-4">🌾</div>
            <h3 className="text-base font-semibold text-gray-900 mb-2">Smart Predictions</h3>
            <p className="text-sm text-gray-600 leading-relaxed">
              Get personalized recommendations based on your soil nutrients and local weather patterns.
            </p>
          </div>

          {/* Feature 2 */}
          <div className="p-6 bg-gray-50 rounded-xl border border-gray-100 hover:border-green-200 transition-colors">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-base font-semibold text-gray-900 mb-2">Model Evaluation</h3>
            <p className="text-sm text-gray-600 leading-relaxed">
              Understand model reliability and accuracy across multiple algorithms for confident decisions.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="p-6 bg-gray-50 rounded-xl border border-gray-100 hover:border-green-200 transition-colors">
            <div className="text-4xl mb-4">🔍</div>
            <h3 className="text-base font-semibold text-gray-900 mb-2">Deep Analysis</h3>
            <p className="text-sm text-gray-600 leading-relaxed">
              Evaluate noise stability, missing features, and model agreement for comprehensive insights.
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-3">Ready to Get Started?</h2>
          <p className="text-gray-600 mb-6">
            Join farmers and researchers making smarter decisions with AgreeGenius.
          </p>
          <button
            onClick={handleStartPredicting}
            className="inline-flex px-6 py-2.5 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition-colors"
          >
            Start Now
          </button>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
