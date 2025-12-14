import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { authService } from "../api/auth";

function AdminTest() {
  const navigate = useNavigate();
  const [userInfo, setUserInfo] = useState(null);
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    const user = authService.getUser();
    setUserInfo(user);
    setIsAdmin(authService.isAdmin());

    console.log("User Info:", user);
    console.log("Is Admin:", authService.isAdmin());
    console.log("Is Authenticated:", authService.isAuthenticated());
    console.log("Token:", authService.getToken());
  }, []);

  if (!authService.isAuthenticated()) {
    return (
      <div style={{ padding: "2rem", textAlign: "center" }}>
        <h1>Acesso Negado</h1>
        <p>Você precisa estar autenticado para acessar esta página.</p>
        <button onClick={() => navigate("/login")}>Ir para Login</button>
      </div>
    );
  }

  return (
    <div style={{ padding: "2rem", maxWidth: "600px", margin: "0 auto" }}>
      <h1>Informações do Usuário</h1>

      <div style={{ 
        background: "#f5f5f5", 
        padding: "1rem", 
        borderRadius: "8px",
        marginBottom: "1rem"
      }}>
        <h2>Dados Armazenados:</h2>
        <pre>{JSON.stringify(userInfo, null, 2)}</pre>
      </div>

      <div style={{ 
        background: isAdmin ? "#d4edda" : "#f8d7da", 
        padding: "1rem", 
        borderRadius: "8px",
        marginBottom: "1rem",
        border: `2px solid ${isAdmin ? "#28a745" : "#dc3545"}`
      }}>
        <h2>Status de Admin:</h2>
        <p><strong>É Administrador?</strong> {isAdmin ? "✓ SIM" : "✗ NÃO"}</p>
        <p><strong>Tipo de Usuário:</strong> {userInfo?.user_type}</p>
      </div>

      <div style={{ display: "flex", gap: "1rem" }}>
        <button 
          onClick={() => navigate("/")}
          style={{
            padding: "0.75rem 1.5rem",
            background: "#007bff",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer"
          }}
        >
          Voltar para Home
        </button>
        {isAdmin && (
          <button 
            onClick={() => navigate("/admin/users")}
            style={{
              padding: "0.75rem 1.5rem",
              background: "#28a745",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer"
            }}
          >
            Ir para Gerenciamento de Usuários
          </button>
        )}
      </div>
    </div>
  );
}

export default AdminTest;
