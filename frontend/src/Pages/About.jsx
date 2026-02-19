function About() {
  const developers = [
    {
      id: 1,
      name: 'Akshay Kireet',
      image: '👨‍💻',
      role: 'Lead Developer'
    },
    {
      id: 2,
      name: 'Selli Lavanya',
      image: '👩‍💻',
      role: 'Frontend Engineer'
    },
    {
      id: 3,
      name: 'Malvika Rayanapeta',
      image: '👨‍💼',
      role: 'ML Engineer'
    },
    {
      id: 4,
      name: 'Sagar',
      image: '👩‍🔬',
      role: 'Data Scientist'
    },
    {
      id: 5,
      name: 'Nithin',
      image: '👨‍🏫',
      role: 'Backend Developer'
    }
  ];

  return (
    <div className="bg-gray-50 min-h-screen">
      {/* Content */}
      <div className="min-h-[calc(100vh-4rem)] py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="text-center mb-16">
            <h1 className="text-5xl font-bold text-gray-900 mb-4">About AgreeGenius</h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              AgreeGenius is an innovative AI-based crop recommendation and model evaluation platform 
              built by a dedicated team of developers, data scientists, and AI engineers. Our mission 
              is to help farmers and agricultural researchers make data-driven decisions for better crop yields.
            </p>
          </div>

          {/* Mission Statement */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            <div className="bg-white rounded-lg shadow-lg p-8 text-center border-t-4 border-green-600">
              <div className="text-4xl mb-4">🌾</div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Our Mission</h3>
              <p className="text-gray-600">
                Empower farmers with AI-driven crop recommendations to maximize yields and profitability.
              </p>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-8 text-center border-t-4 border-blue-600">
              <div className="text-4xl mb-4">🤖</div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Our Vision</h3>
              <p className="text-gray-600">
                Create transparent, trustworthy AI models that farmers can understand and rely on.
              </p>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-8 text-center border-t-4 border-yellow-600">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Our Values</h3>
              <p className="text-gray-600">
                Innovation, transparency, and commitment to sustainable agricultural practices.
              </p>
            </div>
          </div>

          {/* Team Section */}
          <div>
            <h2 className="text-4xl font-bold text-gray-900 text-center mb-12">
              Meet Our Team
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
              {developers.map(dev => (
                <div
                  key={dev.id}
                  className="bg-white rounded-lg shadow-lg p-6 text-center hover:shadow-xl transition-shadow"
                >
                  {/* Profile Image */}
                  <div className="text-6xl mb-4">{dev.image}</div>

                  {/* Name */}
                  <h3 className="text-xl font-bold text-gray-900 mb-2">
                    {dev.name}
                  </h3>

                  {/* Role */}
                  <p className="text-sm text-gray-600 mb-4">
                    {dev.role}
                  </p>

                  {/* Divider */}
                  <div className="h-1 bg-gradient-to-r from-green-400 to-blue-400 rounded"></div>
                </div>
              ))}
            </div>
          </div>

          {/* Technology Stack */}
          <div className="mt-16 bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
              Technology Stack
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-xl font-semibold text-green-600 mb-4">Frontend</h3>
                <ul className="space-y-2 text-gray-700">
                  <li>✓ React + Vite</li>
                  <li>✓ Tailwind CSS</li>
                  <li>✓ React Router</li>
                  <li>✓ Modern JavaScript (ES6+)</li>
                </ul>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-blue-600 mb-4">Backend & ML</h3>
                <ul className="space-y-2 text-gray-700">
                  <li>✓ Python + FastAPI</li>
                  <li>✓ Machine Learning Models (RF, XGB, SVM, MLP)</li>
                  <li>✓ Data Processing & Analysis</li>
                  <li>✓ RESTful API Architecture</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Contact Section */}
          <div className="mt-16 text-center">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Get In Touch</h2>
            <p className="text-gray-600 mb-8">
              Interested in using AgreeGenius for your farm or agricultural research?
            </p>
            <div className="space-x-4">
              <button className="px-8 py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition-colors">
                Contact Us
              </button>
              <button className="px-8 py-3 bg-gray-200 hover:bg-gray-300 text-gray-900 font-semibold rounded-lg transition-colors">
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
