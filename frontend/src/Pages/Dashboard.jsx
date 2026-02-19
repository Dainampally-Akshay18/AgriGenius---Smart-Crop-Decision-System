import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const navigate = useNavigate();

  const handleStartPredicting = () => {
    navigate('/predict');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      {/* Header */}
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h2 className="text-2xl font-bold text-green-700">AgreeGenius</h2>
        </div>
      </nav>

      {/* Main Content */}
      <div className="flex items-center justify-center min-h-[calc(100vh-80px)]">
        <div className="text-center px-4 sm:px-6 lg:px-8 max-w-2xl">
          {/* Title */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
            Welcome to <span className="text-green-600">AgreeGenius</span>
          </h1>

          {/* Description */}
          <p className="text-lg sm:text-xl text-gray-600 mb-8 leading-relaxed">
            An AI-Powered Crop Recommendation & Model Evaluation Platform. 
            Discover the best crops for your farm based on soil nutrients, weather conditions, 
            and advanced machine learning models.
          </p>

          {/* CTA Button */}
          <button
            onClick={handleStartPredicting}
            className="px-8 py-4 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg shadow-md transition-colors duration-200 text-lg sm:text-xl"
          >
            Start Predicting
          </button>

          {/* Additional Info */}
          <div className="mt-12 grid grid-cols-1 sm:grid-cols-3 gap-6">
            <div className="p-4">
              <div className="text-3xl mb-2">🌾</div>
              <h3 className="font-semibold text-gray-800 mb-2">Smart Predictions</h3>
              <p className="text-sm text-gray-600">Get personalized crop recommendations</p>
            </div>
            <div className="p-4">
              <div className="text-3xl mb-2">📊</div>
              <h3 className="font-semibold text-gray-800 mb-2">Model Evaluation</h3>
              <p className="text-sm text-gray-600">Understand model reliability and accuracy</p>
            </div>
            <div className="p-4">
              <div className="text-3xl mb-2">🔍</div>
              <h3 className="font-semibold text-gray-800 mb-2">Deep Analysis</h3>
              <p className="text-sm text-gray-600">Evaluate noise, missing features & more</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
