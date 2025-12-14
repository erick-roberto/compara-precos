import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { productService } from '../api/products';
import '../css/ProductDetail.css';

function ProductDetail() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [prices, setPrices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadProductDetails();
  }, [id]);

  const loadProductDetails = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [productData, pricesData] = await Promise.all([
        productService.getById(id),
        productService.getPrices(id)
      ]);
      
      setProduct(productData);
      setPrices(pricesData);
    } catch (err) {
      setError('Erro ao carregar detalhes do produto.');
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

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="product-detail">
        <div className="container">
          <div className="loading">
            <div className="spinner"></div>
            <p>Carregando...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="product-detail">
        <div className="container">
          <div className="error-message">
            <p>{error || 'Produto não encontrado.'}</p>
            <Link to="/" className="btn btn-primary">
              Voltar para home
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const minPrice = prices.length > 0 ? Math.min(...prices.map(p => p.price)) : 0;
  const maxPrice = prices.length > 0 ? Math.max(...prices.map(p => p.price)) : 0;
  const savings = maxPrice - minPrice;

  return (
    <div className="product-detail">
      <div className="container">
        <Link to="/" className="back-link">
          ← Voltar para produtos
        </Link>

        <div className="product-content">
          <div className="product-main">
            <div className="product-image-large">
              <img src={product.image_url} alt={product.name} />
            </div>
            <div className="product-details">
              <span className="product-category-badge">{product.category}</span>
              <h1 className="product-title">{product.name}</h1>
              <p className="product-description">{product.description}</p>
              
              <div className="price-summary">
                <div className="price-box">
                  <span className="price-label">Melhor preço</span>
                  <span className="price-value best">{formatPrice(minPrice)}</span>
                </div>
                {savings > 0 && (
                  <div className="price-box savings-box">
                    <span className="price-label">Economia máxima</span>
                    <span className="price-value savings">{formatPrice(savings)}</span>
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="prices-section">
            <h2>Comparação de Preços</h2>
            <p className="prices-subtitle">
              Encontramos {prices.length} {prices.length === 1 ? 'oferta' : 'ofertas'} para este produto
            </p>

            {prices.length === 0 ? (
              <div className="no-prices">
                <p>Nenhum preço disponível no momento.</p>
              </div>
            ) : (
              <div className="prices-list">
                {prices.map((price, index) => (
                  <div key={price.id} className={`price-item ${index === 0 ? 'best-price' : ''}`}>
                    <div className="price-item-header">
                      <div className="store-info">
                        <h3 className="store-name">{price.store_name}</h3>
                        {index === 0 && <span className="best-badge">Melhor preço</span>}
                      </div>
                      <div className="price-info">
                        <span className="price-amount">{formatPrice(price.price)}</span>
                      </div>
                    </div>
                    <div className="price-item-footer">
                      <span className="last-updated">
                        Atualizado em {formatDate(price.last_updated)}
                      </span>
                      {price.url && (
                        <a 
                          href={price.url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="btn btn-primary btn-sm"
                        >
                          Ver oferta →
                        </a>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductDetail;
