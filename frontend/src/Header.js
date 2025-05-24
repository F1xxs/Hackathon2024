import React from 'react';
import './Header.css'; 
import { Link, useLocation } from 'react-router-dom';
function Header() {
  const location = useLocation(); // Отримати розташування (current path)

  return (
    <header className="header">
      <nav>
        <ul>
          <li>
            <Link to="/" className={location.pathname === '/' ? 'active' : ''}>Main</Link>
          </li>
          <li>
            <Link to="/about" className={location.pathname === '/about' ? 'active' : ''}>About us</Link>
          </li>
          <li>
            <Link to="/contact" className={location.pathname === '/contact' ? 'active' : ''}>Contact</Link>
          </li>
          <li>
            <Link to="/webAPI" className={location.pathname === '/webAPI' ? 'active' : ''}>WebAPI</Link>
          </li>
          <li>
            <Link to="/collaboration" className={location.pathname === '/collaboration' ? 'active' : ''}>Collaboration</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;