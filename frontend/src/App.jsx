import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './Components/Navbar';
import ProtectedRoute from './Components/ProtectedRoute';
import { SidebarProvider } from './Context/SidebarContext';
import Login from './Pages/Login';
import Signup from './Pages/Signup';
import Dashboard from './Pages/Dashboard';
import PredictForm from './Pages/PredictForm';
import Prediction from './Pages/Prediction';
import Noise from './Pages/Noise';
import Missing from './Pages/Missing';
import Agreement from './Pages/Agreement';
import About from './Pages/About';

function App() {
  return (
    <BrowserRouter>
      <SidebarProvider>
        <Navbar />
        <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/about" element={<About />} />
        
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } />
        
        <Route path="/predict" element={
          <ProtectedRoute>
            <PredictForm />
          </ProtectedRoute>
        } />
        
        <Route path="/prediction" element={
          <ProtectedRoute>
            <Prediction />
          </ProtectedRoute>
        } />
        
        <Route path="/prediction/noise" element={
          <ProtectedRoute>
            <Noise />
          </ProtectedRoute>
        } />
        
        <Route path="/prediction/missing" element={
          <ProtectedRoute>
            <Missing />
          </ProtectedRoute>
        } />
        
        <Route path="/prediction/agreement" element={
          <ProtectedRoute>
            <Agreement />
          </ProtectedRoute>
        } />
        
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
      </SidebarProvider>
    </BrowserRouter>
  );
}

export default App;
