// CRIAÇÃO DA INSTÂNCIA CONFIGURADA DO AXIOS

import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:3000";
// pega a URL da API do arquivo .env do vite
// caso não encontre, usa localhost:3000 como padrão

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
export { API_BASE_URL };
