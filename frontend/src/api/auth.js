import api from "./config"; // api configurada

// objeto que guarda todas as funções relacionadas à autenticação
/*

funções que authService faz:
- registrar usuário
- Fazer login
- fazer logout
- armazenas dados do usuário 
- verifica se está logado
- verifica se é admin ou cliente

*/

// cria um objeto de serviço
export const authService = {
  // Registrar novo usuário
  register: async (name, email, password, userType = "cliente") => {
    const response = await api.post("/api/auth/register", {
      name,
      email,
      password,
      user_type: userType,
    });
    return response.data;
  },
  /*

  Envia um POST para /api/auth/register
  Manda name, email, senha e tipo de usuário para o backend
  O backend cria o usuário
  Retorna a resposta (sucesso ou erro)

  */

  // Fazer login
  login: async (email, password) => {
    const response = await api.post("/api/auth/login", {
      email,
      password,
    });

    if (response.data.token) {
      // se existir token
      localStorage.setItem("token", response.data.token);
      localStorage.setItem("user_id", response.data.user.id);
      localStorage.setItem("user_name", response.data.user.name);
      localStorage.setItem("user_email", response.data.user.email);
      localStorage.setItem("user_type", response.data.user.user_type);

      // Dispara o evento global avisando que mudou o estado de login
      window.dispatchEvent(new Event("authChange"));
    }

    return response.data; // retorno da resposta
  },

  /*

  local Storage não é seguro para guardar informações sensíveis, mas é prático para tokens JWT
    
  Envia email e senha para /api/auth/login.
  O backend retorna um token JWT e os dados do usuário.
  Esses dados são salvos no localStorage: persistem mesmo recarregando a página
  permitem verificar se o usuário está logado
  Dispara um evento global:
  window.dispatchEvent(new Event('authChange'));
  Isso serve para avisar todo o frontend:
  <Header />, por exemplo, escuta esse evento.

  o service salva tudo em localStorage
  - token (JWT)
  - id
  - nome
  - email
  - user_type 

  */

  // Fazer logout
  logout: () => {
    // Apaga os dados do LocalStorage
    localStorage.removeItem("token");
    localStorage.removeItem("user_id");
    localStorage.removeItem("user_name");
    localStorage.removeItem("user_email");
    localStorage.removeItem("user_type");

    // Dispara o evento de mudança também
    window.dispatchEvent(new Event("authChange"));
  },

  // Getters

  // Obter token do localStorage
  getToken: () => {
    return localStorage.getItem("token");
  },

  // Obter ID do usuário do localStorage
  getUserId: () => {
    return localStorage.getItem("user_id");
  },

  // Obter nome do usuário
  getUserName: () => {
    return localStorage.getItem("user_name");
  },

  // Obter email do usuário
  getUserEmail: () => {
    return localStorage.getItem("user_email");
  },

  // Obter tipo de usuário
  getUserType: () => {
    return localStorage.getItem("user_type");
  },

  // retorna um objeto com todos os dados
  getUser: () => {
    return {
      id: localStorage.getItem("user_id"),
      name: localStorage.getItem("user_name"),
      email: localStorage.getItem("user_email"),
      user_type: localStorage.getItem("user_type"),
    };
  },

  // Verificar se está autenticado
  // se nao houver token, retorna false
  isAuthenticated: () => {
    return !!localStorage.getItem("token");
  },

  // Verificar se é administrador
  // se user_type for "admin", retorna true
  isAdmin: () => {
    return localStorage.getItem("user_type") === "admin";
  },

  // Verificar se é cliente
  // se user_type for "cliente", retorna true
  isClient: () => {
    return localStorage.getItem("user_type") === "cliente";
  },
};
