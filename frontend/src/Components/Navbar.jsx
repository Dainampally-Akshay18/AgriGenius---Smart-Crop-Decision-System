import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { isAuthenticated, logout } from '../Services/authService';

function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Check auth state on mount and when location changes
  useEffect(() => {
    setIsLoggedIn(isAuthenticated());
  }, [location]);

  const handleLogout = () => {
    logout();
    setIsLoggedIn(false);
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* LEFT SIDE - Logo and Links */}
          <div className="flex items-center space-x-8">
            {/* Logo */}
            <h1 className="text-2xl font-bold text-green-600">AgreeGenius</h1>

            {/* Navigation Links */}
            <div className="hidden md:flex space-x-6">
              <button
                onClick={() => navigate('/dashboard')}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  location.pathname === '/dashboard'
                    ? 'bg-green-100 text-green-700'
                    : 'text-gray-700 hover:text-green-600'
                }`}
              >
                Dashboard
              </button>
              <button
                onClick={() => navigate('/about')}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  location.pathname === '/about'
                    ? 'bg-green-100 text-green-700'
                    : 'text-gray-700 hover:text-green-600'
                }`}
              >
                About Us
              </button>
            </div>
          </div>

          {/* RIGHT SIDE - Auth Buttons */}
          <div className="flex items-center space-x-3">
            {isLoggedIn ? (
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg transition-colors"
              >
                Logout
              </button>
            ) : (
              <>
                <button
                  onClick={() => navigate('/login')}
                  className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
                    location.pathname === '/login'
                      ? 'bg-green-100 text-green-700'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  Login
                </button>
                <button
                  onClick={() => navigate('/signup')}
                  className={`px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition-colors ${
                    location.pathname === '/signup'
                      ? 'bg-green-700'
                      : ''
                  }`}
                >
                  Sign Up
                </button>
              </>
            )}
          </div>
        </div>

        {/* Mobile Menu Links */}
        <div className="md:hidden pb-4 space-y-2 border-t border-gray-200 pt-4">
          <button
            onClick={() => navigate('/dashboard')}
            className={`block w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors ${
              location.pathname === '/dashboard'
                ? 'bg-green-100 text-green-700'
                : 'text-gray-700 hover:text-green-600'
            }`}
          >
            Dashboard
          </button>
          <button
            onClick={() => navigate('/about')}
            className={`block w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors ${
              location.pathname === '/about'
                ? 'bg-green-100 text-green-700'
                : 'text-gray-700 hover:text-green-600'
            }`}
          >
            About Us
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
