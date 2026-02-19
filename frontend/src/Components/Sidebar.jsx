import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useSidebar } from '../Context/SidebarContext';

function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { sidebarOpen, closeSidebar } = useSidebar();
  const [expanded, setExpanded] = useState(true);

  const navItems = [
    { path: '/prediction', label: 'Crop Prediction', icon: '🌾' },
    { path: '/prediction/noise', label: 'Noise Evaluation', icon: '📊' },
    { path: '/prediction/missing', label: 'Missing Feature', icon: '⚠️' },
    { path: '/prediction/agreement', label: 'Model Agreement', icon: '🤝' }
  ];

  const isActive = (path) => location.pathname === path;

  // Mobile overlay background
  const mobileOverlay = (
    <div
      className="fixed inset-0 bg-black/40 md:hidden z-30 transition-opacity duration-300"
      onClick={closeSidebar}
    />
  );

  return (
    <>
      {/* Mobile Overlay */}
      {sidebarOpen && mobileOverlay}

      {/* Sidebar */}
      <aside
        className={`bg-gradient-to-b from-gray-900 to-gray-800 border-r border-gray-700/50 transition-all duration-300 shadow-xl overflow-y-auto scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800
          ${/* Desktop: Fixed */ 'hidden md:block fixed left-0 top-16 h-[calc(100vh-4rem)]'}
          ${/* Mobile: Overlay Drawer */ sidebarOpen ? 'fixed left-0 top-16 h-[calc(100vh-4rem)] w-64 z-40' : 'fixed -left-64 top-16 h-[calc(100vh-4rem)] w-64 z-40'}
          ${/* Expanded state */ expanded ? 'md:w-64' : 'md:w-20'}`}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-6 border-b border-gray-700/50">
          {expanded && (
            <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Navigation</h3>
          )}
          <button
            onClick={() => setExpanded(!expanded)}
            className={`p-1.5 hover:bg-gray-700/50 rounded-lg transition-all duration-200 text-gray-400 hover:text-white hidden md:block ${
              !expanded && 'mx-auto'
            }`}
            title={expanded ? 'Collapse sidebar' : 'Expand sidebar'}
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11 19l-7-7 7-7m8 14l-7-7 7-7"
              />
            </svg>
          </button>
          {/* Mobile Close Button */}
          <button
            onClick={closeSidebar}
            className="md:hidden p-1.5 hover:bg-gray-700/50 rounded-lg transition-all duration-200 text-gray-400 hover:text-white"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        {/* Navigation Items */}
        <nav className="space-y-1 px-3 py-4">
          {navItems.map((item) => (
            <button
              key={item.path}
              onClick={() => {
                navigate(item.path);
                closeSidebar(); // Close drawer on mobile when navigating
              }}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 group ${
                isActive(item.path)
                  ? 'bg-gradient-to-r from-emerald-500/20 to-emerald-600/10 text-emerald-400 border-l-4 border-emerald-500 shadow-sm'
                  : 'text-gray-300 hover:text-white hover:bg-gray-700/50 border-l-4 border-transparent'
              }`}
              title={expanded ? item.label : item.label}
            >
              <span className={`text-lg flex-shrink-0 ${isActive(item.path) ? 'text-emerald-400' : 'text-gray-400 group-hover:text-emerald-400 transition-colors'}`}>
                {item.icon}
              </span>
              <span className={`text-sm font-medium hidden md:inline ${isActive(item.path) ? 'text-emerald-400' : 'group-hover:text-white'} ${!expanded && 'md:hidden'}`}>
                {item.label}
              </span>
            </button>
          ))}
        </nav>

        {/* Info Section */}
        {expanded && (
          <div className="absolute bottom-0 left-0 right-0 mx-3 mb-6 hidden md:block">
            <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-5 border border-gray-700/50 shadow-lg">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-emerald-400 to-emerald-600 flex items-center justify-center">
                  <span className="text-white text-xs font-bold">i</span>
                </div>
                <p className="text-xs font-medium text-gray-200">Quick Tip</p>
              </div>
              <p className="text-xs text-gray-400 leading-relaxed">
                Use the navigation to explore evaluation modules and analyze your crop data effectively.
              </p>
              <div className="mt-4 pt-3 border-t border-gray-700/50">
                <div className="flex items-center gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></div>
                  <span className="text-[10px] text-gray-500">All systems operational</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </aside>
    </>
  );
}

export default Sidebar;