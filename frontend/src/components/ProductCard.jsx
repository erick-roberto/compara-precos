import { Link } from "react-router-dom";
// permite a navegação entre páginas sem recarregar
import "../css/ProductCard.css";

// O componente recebe 3 props:
// product: objeto que contém os dados do produto
// onAddToCompare: função chamada quando o usuário clica em "Comparar"
// isComparing: booleando que indica se o produto está sendo comparada ou não

function ProductCard({ product, onAddToCompare, isComparing }) {
  // função para formatar os preços em reais (BRL)
  const formatPrice = (price) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(price);
  };

  // cálculo de economia potencial
  const savings =
    product.max_price && product.min_price
      ? product.max_price - product.min_price
      : 0;

  return (
    <div className="product-card">
      {/*link para a página do produto*/}
      {/* /product/123 (exemplo) */}
      <Link to={`/product/${product.id}`} className="product-link">
        {/* imagem do produto */}
        <div className="product-image">
          <img src={product.image_url} alt={product.name} />
        </div>

        <div className="product-info">
          {/* exibe nome e categoria do produto */}
          <h3 className="product-name">{product.name}</h3>
          <p className="product-category">{product.category}</p>

          <div className="product-pricing">
            <div className="price-range">
              {/* preço Mínimo */}
              <span className="price-label">A partir de</span>
              <span className="price-value">
                {formatPrice(product.min_price)}
              </span>
            </div>

            {/* Economia (aparece somente se houver economia)*/}
            {savings > 0 && (
              <div className="savings">
                <span className="savings-label">Economize até</span>
                <span className="savings-value">{formatPrice(savings)}</span>
              </div>
            )}
          </div>

          {/* quantidade de lojas */}
          <div className="store-count">
            {product.store_count} {product.store_count === 1 ? "loja" : "lojas"}
          </div>
        </div>
      </Link>

      {/* botão de comparação */}
      {onAddToCompare && (
        <button
          className={`btn-compare ${isComparing ? "active" : ""}`}
          onClick={(e) => {
            e.preventDefault();
            onAddToCompare(product);
          }}
        >
          {isComparing ? "✓ Comparando" : "+ Comparar"}
        </button>
      )}
    </div>
  );
}

export default ProductCard;
