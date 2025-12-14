// Componente responsável pela barra de busca com filtro por categoria

import { useState, useEffect } from 'react';
import { productService } from '../api/products';
// arquivo onde fica as funções de requisições relacionadas a produtos

import '../css/SearchBar.css';

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState(''); // texto da busca
  const [category, setCategory] = useState(''); // categoria selecionada
  const [categories, setCategories] = useState([]); // lista de categorias disponíveis

  // carrega as categorias
  useEffect(() => {
    loadCategories();
  }, []);

  // faz uma requisição GET para obter as categorias através do productService  
  const loadCategories = async () => {
    try {
      const data = await productService.getCategories();
      setCategories(data);
    } catch (error) {
      console.error('Erro ao carregar categorias:', error);
    }
  };

  // lida com o envio do formulário de busca
  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query, category);
    // executa o filtro de busca
  };

  // função de resetar os campos de busca (limpar filtros)
  const handleReset = () => {
    setQuery('');
    setCategory('');
    onSearch('', '');
  };

  return (
    <div className="search-bar">
      <form onSubmit={handleSubmit} className="search-form">
        <div className="search-inputs">
          <input
            type="text"
            placeholder="Buscar produtos..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="search-input"
          />
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="category-select"
          >
            <option value="">Todas as categorias</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        </div>
        <div className="search-actions">
          <button type="submit" className="btn btn-primary">
            🔍 Buscar
          </button>
          <button type="button" onClick={handleReset} className="btn btn-outline">
            Limpar
          </button>
        </div>
      </form>
    </div>
  );
}

export default SearchBar;
