import React, { useState } from 'react';
import { Phone, Mail, MapPin, Clock, Send, CheckCircle } from 'lucide-react';
import './Contact.css';

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: ''
  });
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('联系表单提交:', formData);
    setIsSubmitted(true);
    // 3秒后重置表单
    setTimeout(() => {
      setIsSubmitted(false);
      setFormData({
        name: '',
        email: '',
        phone: '',
        subject: '',
        message: ''
      });
    }, 3000);
  };

  return (
    <div className="contact-page">
      <div className="contact-hero">
        <div className="hero-content">
          <h1>联系我们</h1>
          <p>我们随时为您提供专业的电梯解决方案咨询服务</p>
        </div>
      </div>

      <div className="contact-content">
        <div className="contact-info">
          <h2>联系方式</h2>
          
          <div className="contact-item">
            <div className="contact-icon">
              <Phone size={24} />
            </div>
            <div className="contact-details">
              <h3>客服热线</h3>
              <p>400-123-4567</p>
              <span>24小时服务热线</span>
            </div>
          </div>

          <div className="contact-item">
            <div className="contact-icon">
              <Mail size={24} />
            </div>
            <div className="contact-details">
              <h3>邮箱地址</h3>
              <p>info@jojdaelevator.com</p>
              <span>business@jojdaelevator.com</span>
            </div>
          </div>

          <div className="contact-item">
            <div className="contact-icon">
              <MapPin size={24} />
            </div>
            <div className="contact-details">
              <h3>公司地址</h3>
              <p>北京市朝阳区科技园区</p>
              <span>joj达电梯科技大厦</span>
            </div>
          </div>

          <div className="contact-item">
            <div className="contact-icon">
              <Clock size={24} />
            </div>
            <div className="contact-details">
              <h3>工作时间</h3>
              <p>周一至周五：8:00-18:00</p>
              <span>周六至周日：9:00-17:00</span>
            </div>
          </div>

          <div className="company-info">
            <h3>关于joj达电梯</h3>
            <p>
              joj达电梯科技有限公司专注于电梯设计、制造、安装和维护服务。
              我们致力于为客户提供安全、可靠、智能的垂直交通解决方案，
              拥有一流的技术团队和完善的服务体系。
            </p>
          </div>
        </div>

        <div className="contact-form-container">
          <h2>在线咨询</h2>
          
          {isSubmitted ? (
            <div className="form-success">
              <CheckCircle size={48} color="#4CAF50" />
              <h3>消息发送成功！</h3>
              <p>我们已收到您的消息，将在24小时内回复您</p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="contact-form">
              <div className="form-row">
                <div className="form-group">
                  <label>姓名 *</label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    placeholder="请输入您的姓名"
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>联系电话 *</label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    placeholder="请输入手机号码"
                    required
                  />
                </div>
              </div>

              <div className="form-group">
                <label>邮箱地址 *</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  placeholder="请输入邮箱地址"
                  required
                />
              </div>

              <div className="form-group">
                <label>咨询主题</label>
                <select 
                  name="subject" 
                  value={formData.subject} 
                  onChange={handleInputChange}
                >
                  <option value="">请选择咨询主题</option>
                  <option value="product">产品咨询</option>
                  <option value="quote">报价询问</option>
                  <option value="maintenance">维保服务</option>
                  <option value="technical">技术支持</option>
                  <option value="complaint">投诉建议</option>
                  <option value="other">其他问题</option>
                </select>
              </div>

              <div className="form-group">
                <label>详细信息 *</label>
                <textarea
                  name="message"
                  value={formData.message}
                  onChange={handleInputChange}
                  placeholder="请详细描述您的问题或需求..."
                  rows="5"
                  required
                />
              </div>

              <button type="submit" className="submit-btn">
                <Send size={20} />
                发送消息
              </button>
            </form>
          )}
        </div>
      </div>

      <div className="map-section">
        <div className="map-container">
          <div className="map-placeholder">
            <MapPin size={48} />
            <h3>公司位置</h3>
            <p>北京市朝阳区科技园区 joj达电梯科技大厦</p>
            <div className="map-actions">
              <button className="map-btn">查看地图</button>
              <button className="map-btn">导航路线</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Contact; 