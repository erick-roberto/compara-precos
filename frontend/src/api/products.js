import api from "./config";

/*
Funciona servindo o Frontend com todas as funções relacionadas a produtos
como:
- Listar produtos
- Buscar produtos
- Pegar detalhes
- pegar preços
- categorias
- comparar produtos
- adicionar produtos
- adicionar preços

*/

export const productService = {
  // Listar todos os produtos
  getAll: async () => {
    const response = await api.get("/api/products");
    return response.data;
  },

  // Buscar produto
  search: async (query, category) => {
    const params = {}; // guarda os filtros
    if (query) params.q = query;
    if (category) params.category = category;

    // monta os filtros dinamicamente
    const response = await api.get("/api/products/search", { params });
    return response.data;
  },

  // Obter detalhes de um produto
  getById: async (id) => {
    const response = await api.get(`/api/products/${id}`);
    return response.data;
  },

  // Obter preços de um produto
  getPrices: async (id) => {
    const response = await api.get(`/api/products/${id}/prices`);
    return response.data;
  },

  // Obter categorias
  getCategories: async () => {
    const response = await api.get("/api/categories");
    return response.data;
  },

  // Comparar produtos
  compare: async (productIds) => {
    const response = await api.post("/api/compare", {
      product_ids: productIds,
    }); // lista de produtos que o cliente quer comparar
    return response.data;
  },

  // Adicionar produto
  create: async (productData) => {
    const response = await api.post("/api/products", productData);
    return response.data;
  },

  /*
  // Adicionar preço
  addPrice: async (productId, priceData) => {
    const response = await api.post(
      `/api/products/${productId}/prices`,
      priceData
    );
    return response.data;
  },
  */
};
