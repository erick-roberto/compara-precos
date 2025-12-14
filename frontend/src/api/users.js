import api from "./config";
import { authService } from "./auth";

/*
Serviço para o gerenciamento de usuários (usado apenas por adminsitrador)

- Listar todos os usuários
- Buscar um usuário específico
- Criar usuário
- atualizar usuário
- excluir usuário

*/

// Objeto que guarda todas as funções relacionadas ao gerenciamento de usuários
export const userService = {
  // Obter todos os usuários (admin only)
  getAllUsers: async () => {
    const token = authService.getToken(); //
    const response = await api.get("/api/users", {
      headers: {
        Authorization: `Bearer ${token}`, // verifica se o token é de ADM
      },
    });
    return response.data; // lista de users
  },

  // Obter detalhes de um usuário (admin only)
  getUserById: async (userId) => {
    const token = authService.getToken();
    const response = await api.get(`/api/users/${userId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  },

  // Criar novo usuário (admin only)
  createUser: async (userData) => {
    const token = authService.getToken();
    // userData: body da requisição
    const response = await api.post("/api/users", userData, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  },

  // Atualizar usuário (admin only)
  updateUser: async (userId, userData) => {
    const token = authService.getToken();
    const response = await api.put(`/api/users/${userId}`, userData, {
      // userData: pode ser um body parcial da requisição
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  },

  // Deletar usuário (admin only)
  deleteUser: async (userId) => {
    const token = authService.getToken();
    const response = await api.delete(`/api/users/${userId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  },
};
