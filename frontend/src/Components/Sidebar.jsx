import { useLocation, useNavigate } from 'react-router-dom';

function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();

  const navItems = [
    { path: '/prediction', label: 'Crop Prediction', icon: '🌾' },
    { path: '/prediction/noise', label: 'Noise Evaluation', icon: '📊' },
    { path: '/prediction/missing', label: 'Missing Feature', icon: '⚠️' },
    { path: '/prediction/agreement', label: 'Model Agreement', icon: '🤝' }
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <aside className="w-64 bg-green-700 text-white h-screen fixed left-0 top-0 pt-6 shadow-lg overflow-y-auto">
      {/* Logo/Title */}
      <div className="px-6 mb-8">
        <h2 className="text-2xl font-bold">AgreeGenius</h2>
        <p className="text-green-100 text-sm mt-1">Evaluation Workspace</p>
      </div>

      {/* Navigation */}
      <nav className="space-y-2">
        {navItems.map((item) => (
          <button
            key={item.path}
            onClick={() => navigate(item.path)}
            className={`w-full text-left px-6 py-3 transition-colors duration-200 flex items-center space-x-3 ${
              isActive(item.path)
                ? 'bg-green-600 border-l-4 border-white'
                : 'hover:bg-green-600'
            }`}
          >
            <span className="text-xl">{item.icon}</span>
            <span className="font-semibold">{item.label}</span>
          </button>
        ))}
      </nav>

      {/* Info Section */}
      <div className="absolute bottom-6 left-6 right-6 bg-green-600 rounded-lg p-4">
        <h3 className="font-semibold text-sm mb-2">💡 Tip</h3>
        <p className="text-xs text-green-100">
          Navigate between different evaluation modules using the menu above.
        </p>
      </div>
    </aside>
  );
}

export default Sidebar;
