import React from 'react';
import { Search } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import './Header.css';

const Header = () => {
  const navigate = useNavigate();

  const handleNavigation = (path) => {
    navigate(path);
  };

  return (
    <header className="header-container">
      <div className="top-bar">
        <div className="logo">
          {/* 替换为joj达的logo */}
          <img src="/logo.png" alt="joj达电梯有限公司 LOGO" style={{ height: 40 }} />
        </div>
        <div className="top-nav">
          <button type="button" className="nav-button">joj达 Online</button>
          <button type="button" className="nav-button">joj达 中国</button>
          <button type="button" className="nav-button"><Search size={16} /> 搜索</button>
          <button type="button" className="nav-button">联系我们</button>
        </div>
      </div>
      <nav className="main-nav">
        <ul>
          <li><button type="button" className="nav-button" onClick={() => handleNavigation('/')}>新梯解决方案</button></li>
          <li><button type="button" className="nav-button" onClick={() => handleNavigation('/')}>无机房家用电梯</button></li>
          <li><button type="button" className="nav-button" onClick={() => handleNavigation('/maintenance')}>维保与更新改造</button></li>
          <li><button type="button" className="nav-button" onClick={() => handleNavigation('/')}>新闻故事与样板工程</button></li>
          <li><Link to="/requirement-pro" className="special">智能定制方案</Link></li>
          <li><Link to="/requirement" className="special">快速需求提交</Link></li>
          <li><button type="button" className="nav-button" onClick={() => handleNavigation('/complaint')}>关于joj达</button></li>
        </ul>
      </nav>
    </header>
  );
};

export default Header; 