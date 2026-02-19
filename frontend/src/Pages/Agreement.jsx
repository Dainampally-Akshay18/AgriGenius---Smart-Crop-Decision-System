import Sidebar from '../Components/Sidebar';

function Agreement() {
  return (
    <div className="flex">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 ml-64 min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
        <div className="p-8">
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              Model Agreement Evaluation
            </h1>
            <p className="text-gray-600">
              Compare predictions across different algorithms
            </p>
          </div>

          {/* Placeholder */}
          <div className="bg-white rounded-lg shadow-lg p-12">
            <div className="text-center">
              <div className="text-6xl mb-4">🤝</div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                Coming Soon
              </h2>
              <p className="text-gray-600">
                Model agreement evaluation will be implemented in Phase 6
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Agreement;
