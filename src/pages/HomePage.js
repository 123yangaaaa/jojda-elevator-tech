import React from 'react';
import { ArrowRight, HardHat, Wrench, Building, Zap, Users, Globe } from 'lucide-react';
import { Link } from 'react-router-dom';
import ElevatorProductDrawings from '../components/ElevatorProductDrawings';
import './HomePage.css';

const HomePage = () => {
  return (
    <div className="homepage-container">
      <section className="hero-section">
        <div className="hero-content">
          <h1>数智腾飞 引领未来</h1>
          <p>joj达电梯科技，为您提供安全、可靠、智能的垂直交通解决方案。</p>
          <div className="hero-buttons">
            <ElevatorProductDrawings />
            <Link to="/knowledge-hub" className="cta-button knowledge-btn">
              <div className="button-icon">
                <Globe size={24} />
              </div>
              <span>知识中心</span>
            </Link>
            <Link to="/requirement" className="cta-button">
              <div className="button-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M9 12l2 2 4-4"/>
                  <path d="M21 12c-1 0-2-1-2-2s1-2 2-2 2 1 2 2-1 2-2 2z"/>
                  <path d="M3 12c1 0 2-1 2-2s-1-2-2-2-2 1-2 2 1 2 2 2z"/>
                  <path d="M12 3c0 1-1 2-2 2s-2-1-2-2 1-2 2-2 2 1 2 2z"/>
                  <path d="M12 21c0-1 1-2 2-2s2 1 2 2-1 2-2 2-2-1-2-2z"/>
                </svg>
              </div>
              <span>需求提交</span>
            </Link>
          </div>
        </div>
      </section>

      <section className="highlights-section">
        <h2>亮点</h2>
        <div className="highlights-grid">
          <div className="highlight-card">
            <Building size={40} />
            <h3>joj达无机房家用电梯</h3>
            <p>为您的家居生活带来舒适与便捷。</p>
          </div>
          <div className="highlight-card">
            <Wrench size={40} />
            <h3>智能维保服务</h3>
            <p>joj达云管家，为电梯和自动扶梯提供全天候智能维保。</p>
          </div>
          <div className="highlight-card">
            <HardHat size={40} />
            <h3>无电梯建筑加装解决方案</h3>
            <p>无需搬离寓所，即可轻松完成电梯安装。</p>
          </div>
        </div>
      </section>

      <section className="smart-solution-section">
        <div className="smart-solution-content">
          <div className="solution-text">
            <h2>🤖 AI智能定制方案</h2>
            <p>基于您的具体需求，我们的智能系统将为您推荐最适合的电梯解决方案</p>
            <ul className="features-list">
              <li>✨ 智能参数推荐</li>
              <li>📊 实时成本估算</li>
              <li>🎯 精准方案匹配</li>
              <li>⚡ 专家24小时响应</li>
            </ul>
            <Link to="/requirement-pro" className="smart-cta">
              <Users size={20} />
              立即体验智能定制
              <ArrowRight size={20} />
            </Link>
          </div>
          <div className="solution-visual">
            <div className="feature-cards">
              <div className="feature-card">
                <div className="feature-icon">🏢</div>
                <span>商业楼宇</span>
              </div>
              <div className="feature-card">
                <div className="feature-icon">🏠</div>
                <span>住宅小区</span>
              </div>
              <div className="feature-card">
                <div className="feature-icon">🏭</div>
                <span>工业厂房</span>
              </div>
              <div className="feature-card">
                <div className="feature-icon">🏥</div>
                <span>医疗机构</span>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <section className="solutions-section">
        <div className="solution-block new-buildings">
          <h3>为新建建筑定制解决方案</h3>
          <p>提供行业领先的高效节能电梯、自动扶梯、自动人行道和自动门产品。</p>
          <button type="button" className="solution-link">了解详情 <ArrowRight size={16}/></button>
        </div>
        <div className="solution-block existing-buildings">
          <h3>为既有建筑定制解决方案</h3>
          <p>充分了解设备及客户需求，确保设备在整个生命周期内顺畅运行。</p>
          <button type="button" className="solution-link">了解详情 <ArrowRight size={16}/></button>
        </div>
      </section>

    </div>
  );
};

export default HomePage; 