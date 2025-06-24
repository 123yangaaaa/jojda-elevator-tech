import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer-container">
      <div className="footer-content">
        <div className="footer-section">
          <h4>新梯解决方案</h4>
          <ul>
            <li><a href="#">电梯解决方案</a></li>
            <li><a href="#">自动扶梯和自动人行道解决方案</a></li>
            <li><a href="#">智能客流解决方案</a></li>
          </ul>
        </div>
        <div className="footer-section">
          <h4>无机房家用电梯</h4>
          <ul>
            <li><a href="#">joj达 唯家</a></li>
            <li><a href="#">joj达 悦家</a></li>
          </ul>
        </div>
        <div className="footer-section">
          <h4>维保与更新改造</h4>
          <ul>
            <li><a href="#">维修保养</a></li>
            <li><a href="#">电梯更新改造</a></li>
            <li><a href="#">自动扶梯更新改造</a></li>
            <li><a href="#">无电梯建筑解决方案</a></li>
          </ul>
        </div>
        <div className="footer-section">
          <h4>关于joj达</h4>
          <ul>
            <li><a href="#">joj达公司</a></li>
            <li><a href="#">职业规划</a></li>
            <li><a href="#">联系我们</a></li>
          </ul>
        </div>
      </div>
      <div className="footer-bottom">
        <p>joj达中国总部, 上海市延安西路2299号上海世贸商城8A88, 200336 | Copyright © joj达电梯有限公司 版权所有</p>
        <p>苏ICP备XXXXXXXX号-1 | 沪公网安备 XXXXXXXXXXXXXX号</p>
      </div>
    </footer>
  );
};

export default Footer; 