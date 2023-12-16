import React, { useState, useEffect, ReactNode } from "react";

interface Product {
  image: string | undefined;
  id: number;
  title: string; // Added a missing title property
  duration: number;
  likes: number; // Added a likes property
}

const Main = () => {
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    (async () => {
      const response = await fetch("http://localhost:8002/api/products");
      const data = await response.json();
      setProducts(data);
    })();
  }, []);

  async function like(data: Product): Promise<void> {
    let { id, title, image, likes } = data;
    products.map((p: Product) => {
      if (p.id === id) {
        likes++;
      }
      return p;
    });

    await fetch(`http://localhost:8002/api/products/${id}/like`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id,
        title,
        image,
        likes,
      }),
    });

    setProducts(
      products.map((p: Product) => {
        if (p.id === id) {
          p.likes++;
        }
        return p;
      })
    );
  }

  return (
    <main role="main">
      <div className="album py-5 bg-light">
        <div className="container">
          <div className="row">
            {products.map((p: Product) => (
              <div className="col-md-4" key={p.id}>
                <div className="card mb-4 shadow-sm">
                  <img src={p.image} height="180" />
                  <div className="card-body">
                    <p className="card-text">{p.title}</p>
                    <div className="d-flex justify-content-between align-items-center">
                      <div className="btn-group">
                        <button
                          type="button"
                          className="btn btn-sm btn-outline-secondary"
                          onClick={() => like(p)}
                        >
                          Like
                        </button>
                      </div>
                      <small className="text-muted">{p.likes || 0} likes</small>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
};

export default Main;
