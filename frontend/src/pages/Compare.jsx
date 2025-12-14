import { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { productService } from '../api/products';
import '../css/Compare.css';

function Compare() {
  const [searchParams] = useSearchParams();
  const [comparison, setComparison] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const ids = searchParams.get('ids');
    if (ids) {
      loadComparison(ids.split(',').map(Number));
    } else {
      setLoading(false);
    }
  }, [searchParams]);

  const loadComparison = async (productIds) => {
    try {
      setLoading(true);
      setError(null);
      const data = await productService.compare(productIds);
      setComparison(data);
    } catch (err) {
      setError('Erro ao carregar comparação.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(price);
  };

  if (loading) {
    return (
      <div className="compare-page">
        <div className="container">
          <div className="loading">
            <div className="spinner"></div>
            <p>Carregando comparação...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="compare-page">
        <div className="container">
          <div className="error-message">
            <p>{error}</p>
            <Link to="/" className="btn btn-primary">
              Voltar para home
            </Link>
          </div>
        </div>
      </div>
    );
  }

  if (comparison.length === 0) {
    return (
      <div className="compare-page">
        <div className="container">
          <div className="empty-state">
            <h2>Nenhum produto para comparar</h2>
            <p>Selecione produtos na página inicial para começar a comparar preços.</p>
            <Link to="/" className="btn btn-primary">
              Ver produtos
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="compare-page">
      <div className="container">
        <div className="compare-header">
          <h1>Comparação de Produtos</h1>
          <p>Compare preços e economize na sua compra</p>
        </div>

        <div className="comparison-grid">
          {comparison.map((product) => {
            const minPrice = product.prices.length > 0 
              ? Math.min(...product.prices.map(p => p.price)) 
              : 0;
            const maxPrice = product.prices.length > 0 
              ? Math.max(...product.prices.map(p => p.price)) 
              : 0;
            const savings = maxPrice - minPrice;

            return (
              <div key={product.id} className="comparison-card">
                <div className="comparison-product">
                  <div className="comparison-image">
                    <img src={product.image_url} alt={product.name} />
                  </div>
                  <div className="comparison-info">
                    <span className="comparison-category">{product.category}</span>
                    <h3 className="comparison-name">{product.name}</h3>
                    <p className="comparison-description">{product.description}</p>
                  </div>
                </div>

                <div className="comparison-summary">
                  <div className="summary-item">
                    <span className="summary-label">Melhor preço</span>
                    <span className="summary-value best">{formatPrice(minPrice)}</span>
                  </div>
                  {savings > 0 && (
                    <div className="summary-item">
                      <span className="summary-label">Economia</span>
                      <span className="summary-value savings">{formatPrice(savings)}</span>
                    </div>
                  )}
                </div>

                <div className="comparison-prices">
                  <h4>Preços por loja</h4>
                  {product.prices.length === 0 ? (
                    <p className="no-prices-text">Nenhum preço disponível</p>
                  ) : (
                    <div className="prices-table">
                      {product.prices.map((price, index) => (
                        <div key={price.store_name} className={`price-row ${index === 0 ? 'best' : ''}`}>
                          <span className="store">{price.store_name}</span>
                          <span className="price">{formatPrice(price.price)}</span>
                          {price.url && (
                            <a 
                              href={price.url} 
                              target="_blank" 
                              rel="noopener noreferrer"
                              className="price-link"
                            >
                              Ver →
                            </a>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                <Link to={`/product/${product.id}`} className="btn btn-outline btn-full">
                  Ver detalhes completos
                </Link>
              </div>
            );
          })}
        </div>

        <div className="compare-actions">
          <Link to="/" className="btn btn-primary">
            ← Voltar para produtos
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Compare;
