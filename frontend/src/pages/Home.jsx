import { useState, useEffect } from 'react';
import { productService } from '../api/products';
import ProductCard from '../components/ProductCard';
import SearchBar from '../components/SearchBar';
import '../css/Home.css';

function Home() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [compareList, setCompareList] = useState([]);

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await productService.getAll();
      setProducts(data);
    } catch (err) {
      setError('Erro ao carregar produtos. Tente novamente.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (query, category) => {
    try {
      setLoading(true);
      setError(null);
      
      if (!query && !category) {
        await loadProducts();
        return;
      }
      
      const data = await productService.search(query, category);
      setProducts(data);
    } catch (err) {
      setError('Erro ao buscar produtos. Tente novamente.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCompare = (product) => {
    setCompareList(prev => {
      const exists = prev.find(p => p.id === product.id);
      if (exists) {
        return prev.filter(p => p.id !== product.id);
      }
      if (prev.length >= 4) {
        alert('Você pode comparar no máximo 4 produtos por vez.');
        return prev;
      }
      return [...prev, product];
    });
  };

  const isProductInCompareList = (productId) => {
    return compareList.some(p => p.id === productId);
  };

  return (
    <div className="home">
      <div className="container">
        <div className="home-header">
          <h1>Encontre os melhores preços</h1>
          <p>Compare preços de produtos em diversas lojas e economize!</p>
        </div>

        <SearchBar onSearch={handleSearch} />

        {compareList.length > 0 && (
          <div className="compare-banner">
            <div className="compare-info">
              <span className="compare-count">
                {compareList.length} {compareList.length === 1 ? 'produto selecionado' : 'produtos selecionados'}
              </span>
              <button 
                className="btn btn-primary"
                onClick={() => {
                  const ids = compareList.map(p => p.id).join(',');
                  window.location.href = `/compare?ids=${ids}`;
                }}
              >
                Comparar agora
              </button>
            </div>
          </div>
        )}

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Carregando produtos...</p>
          </div>
        )}

        {error && (
          <div className="error-message">
            <p>{error}</p>
            <button onClick={loadProducts} className="btn btn-primary">
              Tentar novamente
            </button>
          </div>
        )}

        {!loading && !error && products.length === 0 && (
          <div className="no-results">
            <p>Nenhum produto encontrado.</p>
          </div>
        )}

        {!loading && !error && products.length > 0 && (
          <div className="products-grid">
            {products.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                onAddToCompare={handleAddToCompare}
                isComparing={isProductInCompareList(product.id)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Home;
