import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { authService } from "../api/auth";
import "../css/Auth.css";

function Login() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await authService.login(formData.email, formData.password);
      console.log("Login response:", response);
      console.log("User type:", authService.getUserType());
      navigate("/");
    } catch (err) {
      setError(
        err.response?.data?.error || "Erro ao fazer login. Tente novamente."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>Login</h1>
          <p>Acesse sua conta para comparar preços</p>
        </div>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="seu@email.com"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Senha</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Sua senha"
              required
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary btn-full"
            disabled={loading}
          >
            {loading ? "Entrando..." : "Entrar"}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            Não tem uma conta? <Link to="/register">Cadastre-se aqui</Link>
          </p>
          <div className="demo-hints">
            <p className="demo-hint"><strong>Admin:</strong> admin@email.com / Admin@123</p>
            <p className="demo-hint"><strong>Cliente:</strong> teste@exemplo.com / password</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
