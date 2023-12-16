import React from 'react';

const Menu = () => {
    return (
        <div>
            <div className="sidebar border border-right col-md-3 col-lg-2 p-0 bg-body-tertiary">
                <ul className="nav flex-column">
                    <li className="nav-item">
                        <a className="nav-link d-flex align-items-center gap-2 active" aria-current="page" href="#">
                            Products
                        </a>
                    </li>
                </ul>
            </div>

        </div>
    );
};

export default Menu;