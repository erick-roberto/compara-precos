import { Link, useNavigate } from "react-router-dom";
// Link: utilizado para navegação entre páginas sem recarregar
// useNavigate: hook para navegação programática
import { authService } from "../api/auth";
// importa o serviço de autenticação, lida com JWT, tokens no localStorage
import { useState, useEffect } from "react";
// useState: cria variáveis reativas, que atualizam os componentes
// useEffect: executa ações quando um componente carrega ou quando alguma variável muda
import logo from "../assets/Compara_precos_logo.png";
import "../css/Header.css";

function Header() {
  const navigate = useNavigate(); // permite mudar de página via código
  // Verifica o estado de autenticação do usuário
  // valor inicial vem de authService.isAuthenticated()
  const [isAuthenticated, setIsAuthenticated] = useState(
    authService.isAuthenticated()
  );
  const [isAdmin, setIsAdmin] = useState(authService.isAdmin());
  const [userName, setUserName] = useState(authService.getUserName());

  // useEffect para atualizar o estado de autenticação quando houver mudanças
  useEffect(() => {
    const handleAuthChange = () => {
      setIsAuthenticated(authService.isAuthenticated());
      setIsAdmin(authService.isAdmin());
      setUserName(authService.getUserName());
      // verifica se existe um token válido no localStorage
    };

    // escuta as mudanças de autenticação
    // evento disparado pelo authService quando o usuário faz login ou logout
    window.addEventListener("authChange", handleAuthChange);
    // é responsável por atualizar o componente Header quando o estado de autenticação muda

    // limpa o listener ao desmontar o componente (importante para evitar vazamentos de memória)
    return () => window.removeEventListener("authChange", handleAuthChange);
  }, []);

  // função de logout
  const handleLogout = () => {
    authService.logout();
    navigate("/login");
  };

  return (
    <header className="header">
      <div className="container">
        <div className="header-content">

          {/*logo que muda para a home*/}
          <Link to="/" className="logo">
            <img src={logo} alt="Logo Compara Preço" className="logo-icon" />
            <span className="logo-text">Compara Preços</span>
          </Link>

          {/*menu de navegação*/}
          <nav className="nav">
            <Link to="/" className="nav-link">
              Produtos
            </Link>
            {isAuthenticated ? (
              <>
                {isAdmin && (
                  <Link to="/admin/users" className="nav-link admin-link">
                    Gerenciar Usuários
                  </Link>
                )}
                <div className="user-info">
                  <span className="user-name">{userName}</span>
                  <button onClick={handleLogout} className="nav-link btn-logout">
                    Sair
                  </button>
                </div>
              </>
            ) : (
              <Link to="/login" className="nav-link">
                Login
              </Link>
            )}
          </nav>
          {/*mostra o botão de sair se autenticado, senão mostra o link de login*/} 

        </div>
      </div>
    </header>
  );
}

export default Header;
