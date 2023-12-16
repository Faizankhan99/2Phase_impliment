import React from 'react';

const Nav = () => {
    return (
        <div className="offcanvas-body d-md-flex flex-column p-0 pt-lg-3 overflow-y-auto">
          <ul className="nav flex-column">
            <li className="nav-item">
              <a className="nav-link d-flex align-items-center gap-2 active" aria-current="page" href="#">
                <svg className="bi"><use xlinkHref="#house-fill"></use></svg>
                Products
              </a>
            </li>
            </ul>
            
          <ul className="nav flex-column mb-auto">
            <li className="nav-item">
              <a className="nav-link d-flex align-items-center gap-2" href="#">
                <svg className="bi"><use xlinkHref="#gear-wide-connected"></use></svg>
                Settings
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link d-flex align-items-center gap-2" href="#">
                <svg className="bi"><use xlinkHref="#door-closed"></use></svg>
                Sign out
              </a>
            </li>
          </ul>
        </div>
    );
};

export default Nav;
