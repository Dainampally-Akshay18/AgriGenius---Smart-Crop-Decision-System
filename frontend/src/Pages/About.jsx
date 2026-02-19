function About() {
  const developers = [
    {
      id: 1,
      name: 'Akshay Kireet',
      image: '👨‍💻',
      role: 'Developer'
    },
    {
      id: 2,
      name: 'Selli Lavanya',
      image: '👩‍💻',
      role: 'Developer'
    },
    {
      id: 3,
      name: 'Malvika Rayanapeta',
      image: '👨‍💼',
      role: 'Developer'
    },
    {
      id: 4,
      name: 'Sagar',
      image: '👩‍🔬',
      role: 'Developer'
    },
    {
      id: 5,
      name: 'Nithin',
      image: '👨‍🏫',
      role: 'Developer'
    }
  ];

  return (
    <div className="bg-white min-h-screen">
      {/* Content */}
      <div className="min-h-[calc(100vh-4rem)] py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          {/* Header Section */}
          <div className="text-center mb-20">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">About AgreeGenius</h1>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto leading-relaxed">
              AgreeGenius is an AI-based crop recommendation and model evaluation platform built by a dedicated team. 
              We empower farmers and researchers with data-driven insights for better agricultural decisions.
            </p>
          </div>

          {/* Mission, Vision, Values */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 text-center">
              <div className="text-5xl mb-4">🌾</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Our Mission</h3>
              <p className="text-sm text-gray-600 leading-relaxed">
                Empower farmers with AI-driven crop recommendations to maximize yields and profitability.
              </p>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 text-center">
              <div className="text-5xl mb-4">🤖</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Our Vision</h3>
              <p className="text-sm text-gray-600 leading-relaxed">
                Create transparent, trustworthy AI models that farmers can understand and rely on.
              </p>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 text-center">
              <div className="text-5xl mb-4">🎯</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Our Values</h3>
              <p className="text-sm text-gray-600 leading-relaxed">
                Innovation, transparency, and commitment to sustainable agriculture.
              </p>
            </div>
          </div>

          {/* Team Section */}
          <div className="mb-20">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900">Meet the Team</h2>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-6">
              {developers.map(dev => (
                <div
                  key={dev.id}
                  className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 text-center hover:shadow-md hover:border-green-200 transition-all duration-200"
                >
                  {/* Avatar */}
                  <div className="w-20 h-20 ml-auto mr-auto mb-4 text-4xl flex items-center justify-center">
                    {dev.image}
                  </div>

                  {/* Name */}
                  <h3 className="text-sm font-semibold text-gray-900">
                    {dev.name}
                  </h3>

                  {/* Role */}
                  <p className="text-xs text-gray-500 mt-1">
                    {dev.role}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Technology Stack */}
          <div className="bg-gray-50 rounded-xl shadow-sm border border-gray-100 p-12">
            <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-10 text-center">
              Technology Stack
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
              <div>
                <h3 className="text-lg font-semibold text-green-600 mb-4">Frontend</h3>
                <ul className="space-y-2 text-sm text-gray-700">
                  <li>✓ React + Vite</li>
                  <li>✓ Tailwind CSS</li>
                  <li>✓ React Router</li>
                  <li>✓ Modern JavaScript (ES6+)</li>
                </ul>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-green-600 mb-4">Backend & ML</h3>
                <ul className="space-y-2 text-sm text-gray-700">
                  <li>✓ Python + FastAPI</li>
                  <li>✓ Machine Learning Models (RF, XGB, SVM, MLP)</li>
                  <li>✓ Data Processing & Analysis</li>
                  <li>✓ RESTful API Architecture</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Contact Section */}
          <div className="mt-20 text-center">
            <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-4">Get In Touch</h2>
            <p className="text-gray-600 mb-8">
              Interested in using AgreeGenius for your farm or agricultural research?
            </p>
            <div className="space-x-3">
              <button className="px-6 py-2.5 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg transition-colors">
                Contact Us
              </button>
              <button className="px-6 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-900 text-sm font-medium rounded-lg transition-colors">
                Learn More
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default About;

