import React, { useState } from 'react';
import { Building, Users, ArrowRight, CheckCircle } from 'lucide-react';
import './ElevatorRequirement.css';

const ElevatorRequirement = () => {
  const [formData, setFormData] = useState({
    buildingType: '',
    floors: '',
    usage: '',
    capacity: '',
    speed: '',
    contactName: '',
    contactPhone: '',
    contactEmail: '',
    projectAddress: '',
    additionalRequirements: ''
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
    // 这里可以添加实际的提交逻辑
    console.log('提交的需求数据:', formData);
    setIsSubmitted(true);
  };

  if (isSubmitted) {
    return (
      <div className="requirement-success">
        <div className="success-content">
          <CheckCircle size={80} color="#4CAF50" />
          <h2>需求提交成功！</h2>
          <p>我们已收到您的电梯需求，专业顾问将在24小时内与您联系</p>
          <button 
            onClick={() => setIsSubmitted(false)}
            className="back-btn"
          >
            提交新需求
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="elevator-requirement">
      <div className="requirement-hero">
        <div className="hero-content">
          <h1>
            <Building className="hero-icon" />
            电梯需求提交
          </h1>
          <p>告诉我们您的需求，我们将为您提供专业的电梯解决方案</p>
        </div>
      </div>

      <div className="requirement-form-section">
        <div className="form-container">
          <form onSubmit={handleSubmit} className="requirement-form">
            <div className="form-group">
              <label>建筑类型 *</label>
              <select 
                name="buildingType" 
                value={formData.buildingType} 
                onChange={handleInputChange}
                required
              >
                <option value="">请选择建筑类型</option>
                <option value="residential">住宅建筑</option>
                <option value="commercial">商业建筑</option>
                <option value="office">办公建筑</option>
                <option value="hospital">医疗建筑</option>
                <option value="industrial">工业建筑</option>
                <option value="other">其他</option>
              </select>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>楼层数 *</label>
                <input
                  type="number"
                  name="floors"
                  value={formData.floors}
                  onChange={handleInputChange}
                  placeholder="请输入楼层数"
                  required
                />
              </div>
              
              <div className="form-group">
                <label>预期载重 *</label>
                <select 
                  name="capacity" 
                  value={formData.capacity} 
                  onChange={handleInputChange}
                  required
                >
                  <option value="">请选择载重</option>
                  <option value="630kg">630kg</option>
                  <option value="800kg">800kg</option>
                  <option value="900kg">900kg</option>
                  <option value="1000kg">1000kg</option>
                  <option value="1050kg">1050kg</option>
                  <option value="custom">自定义</option>
                </select>
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>使用频率</label>
                <select 
                  name="usage" 
                  value={formData.usage} 
                  onChange={handleInputChange}
                >
                  <option value="">请选择使用频率</option>
                  <option value="low">低频使用</option>
                  <option value="medium">中频使用</option>
                  <option value="high">高频使用</option>
                </select>
              </div>
              
              <div className="form-group">
                <label>运行速度</label>
                <select 
                  name="speed" 
                  value={formData.speed} 
                  onChange={handleInputChange}
                >
                  <option value="">请选择速度</option>
                  <option value="1.0">1.0 m/s</option>
                  <option value="1.5">1.5 m/s</option>
                  <option value="1.75">1.75 m/s</option>
                  <option value="2.0">2.0 m/s</option>
                  <option value="2.5">2.5 m/s</option>
                </select>
              </div>
            </div>

            <div className="contact-section">
              <h3>联系信息</h3>
              <div className="form-row">
                <div className="form-group">
                  <label>联系人姓名 *</label>
                  <input
                    type="text"
                    name="contactName"
                    value={formData.contactName}
                    onChange={handleInputChange}
                    placeholder="请输入您的姓名"
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>联系电话 *</label>
                  <input
                    type="tel"
                    name="contactPhone"
                    value={formData.contactPhone}
                    onChange={handleInputChange}
                    placeholder="请输入手机号码"
                    required
                  />
                </div>
              </div>

              <div className="form-group">
                <label>邮箱地址</label>
                <input
                  type="email"
                  name="contactEmail"
                  value={formData.contactEmail}
                  onChange={handleInputChange}
                  placeholder="请输入邮箱地址"
                />
              </div>

              <div className="form-group">
                <label>项目地址</label>
                <input
                  type="text"
                  name="projectAddress"
                  value={formData.projectAddress}
                  onChange={handleInputChange}
                  placeholder="请输入项目所在地址"
                />
              </div>
            </div>

            <div className="form-group">
              <label>其他需求说明</label>
              <textarea
                name="additionalRequirements"
                value={formData.additionalRequirements}
                onChange={handleInputChange}
                placeholder="请描述您的特殊需求或其他要求..."
                rows="4"
              />
            </div>

            <button type="submit" className="submit-btn">
              <Users size={20} />
              提交需求
              <ArrowRight size={20} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ElevatorRequirement; 