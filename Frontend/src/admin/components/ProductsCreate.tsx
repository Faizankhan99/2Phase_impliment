import React, { SyntheticEvent, useState } from "react";

import Wrapper from "./Wrapper";
import { useNavigate } from "react-router-dom";

const ProductsCreate = () => {
  const [title, setTitle] = useState("");
  const [image, setImage] = useState("");
  const navigate = useNavigate();

  const submit = async (e: SyntheticEvent) => {
    e.preventDefault();

    await fetch("http://localhost:8003/api/product", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        image,
      }),
    });

    // Use the navigate function to navigate to the desired route
    navigate("/admin/products");
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
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label>Image</label>
          <input
            type="text"
            className="form-control"
            name="image"
            onChange={(e) => setImage(e.target.value)}
          />
        </div>
        <button className="btn btn-outline-secondary">Save</button>
      </form>
    </Wrapper>
  );
};

export default ProductsCreate;
