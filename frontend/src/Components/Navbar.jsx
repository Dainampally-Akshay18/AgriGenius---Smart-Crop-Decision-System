import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { isAuthenticated, logout } from '../Services/authService';
import { useSidebar } from '../Context/SidebarContext';

function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const { toggleSidebar } = useSidebar();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [userName, setUserName] = useState('');

  useEffect(() => {
    setIsLoggedIn(isAuthenticated());
    const storedName = localStorage.getItem('userName') || 'User';
    setUserName(storedName);
  }, [location]);

  const handleLogout = () => {
    logout();
    setIsLoggedIn(false);
    setDropdownOpen(false);
    navigate('/login');
  };

  const getInitials = (name) => {
    return name
      .split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <nav className="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 border-b border-gray-700/50 shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* LEFT - Logo and Navigation */}
          <div className="flex items-center gap-4 md:gap-10">
            {/* Hamburger Menu - Mobile Only */}
            <button
              onClick={toggleSidebar}
              className="md:hidden p-2 rounded-lg hover:bg-gray-700/50 transition-all duration-200 text-gray-400 hover:text-white"
              title="Toggle sidebar"
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
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>

            {/* Logo */}
            <button
              onClick={() => navigate('/dashboard')}
              className="flex items-center gap-2.5 group"
            >
              {/* Logo Mark */}
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-emerald-400 to-emerald-600 flex items-center justify-center text-white font-extrabold text-sm group-hover:scale-110 transition-all duration-300 shadow-lg shadow-emerald-500/20">
                A
              </div>
              {/* Logo Text */}
              <span className="text-lg font-extrabold bg-gradient-to-r from-white via-gray-100 to-gray-300 bg-clip-text text-transparent group-hover:from-emerald-400 group-hover:to-emerald-300 transition-all duration-300">
                AgreeGenius
              </span>
            </button>

            {/* Nav Links */}
            <div className="hidden md:flex gap-8">
              <button
                onClick={() => navigate('/dashboard')}
                className={`text-sm font-medium transition-all duration-200 px-1 py-2 border-b-2 ${
                  location.pathname === '/dashboard'
                    ? 'text-emerald-400 border-emerald-500'
                    : 'text-gray-400 hover:text-gray-200 border-transparent hover:border-gray-600'
                }`}
              >
                Dashboard
              </button>
              <button
                onClick={() => navigate('/about')}
                className={`text-sm font-medium transition-all duration-200 px-1 py-2 border-b-2 ${
                  location.pathname === '/about'
                    ? 'text-emerald-400 border-emerald-500'
                    : 'text-gray-400 hover:text-gray-200 border-transparent hover:border-gray-600'
                }`}
              >
                About
              </button>
            </div>
          </div>

          {/* RIGHT - Auth */}
          <div className="flex items-center gap-4">
            {isLoggedIn ? (
              <div className="relative">
                <button
                  onClick={() => setDropdownOpen(!dropdownOpen)}
                  className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-700/50 transition-all duration-200 border border-transparent hover:border-gray-600/50"
                >
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-emerald-400 to-emerald-600 flex items-center justify-center text-white text-xs font-bold shadow-lg shadow-emerald-500/20">
                    {getInitials(userName)}
                  </div>
                  <span className="text-sm font-medium text-gray-300 hidden sm:block">{userName}</span>
                  <svg
                    className={`w-4 h-4 text-gray-400 transition-all duration-200 ${
                      dropdownOpen ? 'rotate-180 text-emerald-400' : ''
                    }`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                  </svg>
                </button>

                {/* Dropdown Menu */}
                {dropdownOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-gray-800 rounded-xl shadow-2xl border border-gray-700/50 py-1 backdrop-blur-sm">
                    <button
                      onClick={() => {
                        setDropdownOpen(false);
                      }}
                      className="w-full text-left px-4 py-2.5 text-sm text-gray-300 hover:bg-gray-700/50 hover:text-white transition-all duration-200 flex items-center gap-2"
                    >
                      <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      Account Settings
                    </button>
                    <div className="border-t border-gray-700/50" />
                    <button
                      onClick={handleLogout}
                      className="w-full text-left px-4 py-2.5 text-sm text-red-400 hover:bg-red-500/10 hover:text-red-300 transition-all duration-200 flex items-center gap-2"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                      </svg>
                      Logout
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <>
                <button
                  onClick={() => navigate('/login')}
                  className="px-4 py-2 text-sm font-medium text-gray-300 hover:text-white transition-all duration-200 relative group"
                >
                  Sign In
                  <span className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-0 h-0.5 bg-emerald-400 group-hover:w-full transition-all duration-300"></span>
                </button>
                <button
                  onClick={() => navigate('/signup')}
                  className="px-4 py-2 text-sm font-medium text-white bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700 rounded-lg transition-all duration-200 shadow-lg shadow-emerald-500/20 hover:shadow-emerald-500/30"
                >
                  Sign Up
                </button>
              </>
            )}
          </div>
        </div>

        {/* Mobile Menu */}
        <div className="md:hidden border-t border-gray-700/50 py-2 space-y-1">
          <button
            onClick={() => navigate('/dashboard')}
            className={`block w-full text-left px-3 py-2.5 text-sm font-medium rounded-lg transition-all duration-200 ${
              location.pathname === '/dashboard'
                ? 'bg-gradient-to-r from-emerald-500/20 to-emerald-600/10 text-emerald-400'
                : 'text-gray-300 hover:text-white hover:bg-gray-700/50'
            }`}
          >
            Dashboard
          </button>
          <button
            onClick={() => navigate('/about')}
            className={`block w-full text-left px-3 py-2.5 text-sm font-medium rounded-lg transition-all duration-200 ${
              location.pathname === '/about'
                ? 'bg-gradient-to-r from-emerald-500/20 to-emerald-600/10 text-emerald-400'
                : 'text-gray-300 hover:text-white hover:bg-gray-700/50'
            }`}
          >
            About
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;