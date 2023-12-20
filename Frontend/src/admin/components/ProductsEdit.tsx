import React, { SyntheticEvent, useEffect, useState } from "react";
import Wrapper from "./Wrapper";
import { useParams, useNavigate } from "react-router-dom";

const ProductsEdit = () => {
  const { id } = useParams();
  const [title, setTitle] = useState("");
  const [image, setImage] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await fetch(`http://localhost:8003/api/product/${id}`);
        const product = await response.json();
        setTitle(product.title);
        setImage(product.image);
      } catch (error) {
        console.error(error);
      }
    };

    fetchProduct();
  }, [id]);

  const submit = async (e: SyntheticEvent) => {
    e.preventDefault();

    try {
      await fetch(`http://localhost:8003/api/product/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title,
          image,
        }),
      });

      navigate("/admin/products");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Wrapper>
      <form onSubmit={submit}>
        <div className="form-group">
          <label>Title</label>
          <input
            type="text"
            className="form-control"
            name="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label>Image</label>
          <input
            type="text"
            className="form-control"
            name="image"
            value={image}
            onChange={(e) => setImage(e.target.value)}
          />
        </div>
        <button className="btn btn-outline-secondary" type="submit">
          Save
        </button>
      </form>
    </Wrapper>
  );
};

export default ProductsEdit;
