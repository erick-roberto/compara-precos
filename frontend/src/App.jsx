import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useState, useEffect } from "react";
import Header from "./components/Header";
import Home from "./pages/Home";
import ProductDetail from "./pages/ProductDetail";
import Compare from "./pages/Compare";
import Login from "./pages/Login";
import Register from "./pages/Register";
import AdminUsers from "./pages/AdminUsers";
import AdminTest from "./pages/AdminTest";
import { authService } from "./api/auth";
import "./App.css";

// Componente para proteger rotas de admin
function ProtectedAdminRoute({ children }) {
  const [isAdmin, setIsAdmin] = useState(authService.isAdmin());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(false);
    const handleAuthChange = () => {
      setIsAdmin(authService.isAdmin());
    };

    window.addEventListener("authChange", handleAuthChange);
    return () => window.removeEventListener("authChange", handleAuthChange);
  }, []);

  if (loading) {
    return <div>Carregando...</div>;
  }

  return isAdmin ? children : <Navigate to="/login" replace />;
}

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/product/:id" element={<ProductDetail />} />
            <Route path="/compare" element={<Compare />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/admin-test" element={<AdminTest />} />
            <Route 
              path="/admin/users" 
              element={
                <ProtectedAdminRoute>
                  <AdminUsers />
                </ProtectedAdminRoute>
              } 
            />
          </Routes>
        </main>
        <footer className="footer">
          <div className="container">
            <p>
              &copy; 2025 Comparador de Preços. Todos os direitos reservados.
            </p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
