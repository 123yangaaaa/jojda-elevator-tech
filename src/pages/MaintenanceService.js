import React, { useState } from 'react';
import { Wrench, Clock, CheckCircle, AlertTriangle, Phone, Mail, MapPin } from 'lucide-react';
import './MaintenanceService.css';

const MaintenanceService = () => {
  const [activeTab, setActiveTab] = useState('request');
  const [maintenanceForm, setMaintenanceForm] = useState({
    customer_name: '',
    contact_phone: '',
    contact_email: '',
    elevator_location: '',
    elevator_type: '',
    maintenance_type: '',
    urgency_level: '',
    description: '',
    preferred_time: ''
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setMaintenanceForm(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitStatus(null);

    // 调试信息
    console.log('当前表单状态:', maintenanceForm);
    console.log('维保类型:', maintenanceForm.maintenance_type);
    console.log('紧急程度:', maintenanceForm.urgency_level);

    // 前端验证
    if (!maintenanceForm.customer_name || !maintenanceForm.contact_phone || 
        !maintenanceForm.elevator_location || !maintenanceForm.maintenance_type || 
        !maintenanceForm.urgency_level) {
      setSubmitStatus({
        type: 'error',
        message: '请填写所有必填字段，包括选择维保类型和紧急程度'
      });
      setIsSubmitting(false);
      return;
    }

    try {
      // 调用后端API
      const requestData = {
        customerName: maintenanceForm.customer_name,
        contactPhone: maintenanceForm.contact_phone,
        contactEmail: maintenanceForm.contact_email || '',
        elevatorLocation: maintenanceForm.elevator_location,
        elevatorType: maintenanceForm.elevator_type || '',
        maintenanceType: maintenanceForm.maintenance_type,
        urgencyLevel: maintenanceForm.urgency_level,
        description: maintenanceForm.description || '',
        preferredTime: maintenanceForm.preferred_time || ''
      };

      console.log('发送的数据:', requestData);

      const response = await fetch('http://localhost:5000/api/maintenancerequests', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      });

      const result = await response.json();
      console.log('服务器响应:', result);

      if (response.ok && result.Success) {
        setSubmitStatus({
          type: 'success',
          message: `维保申请提交成功！申请编号：${result.Data.id}，我们的技术团队会在2小时内与您联系确认。`
        });
        
        // 重置表单
        setMaintenanceForm({
          customer_name: '', contact_phone: '', contact_email: '', elevator_location: '',
          elevator_type: '', maintenance_type: '', urgency_level: '', description: '', preferred_time: ''
        });
      } else {
        setSubmitStatus({
          type: 'error',
          message: result.Message || '提交失败，请重试或联系客服'
        });
      }
    } catch (error) {
      console.error('提交维保申请时发生错误:', error);
      setSubmitStatus({
        type: 'error',
        message: '网络错误，请检查网络连接后重试'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const maintenanceTypes = [
    { value: 'routine', label: '定期保养', icon: '🔧', description: '按计划进行的预防性维护' },
    { value: 'emergency', label: '紧急维修', icon: '🚨', description: '故障或安全问题需要立即处理' },
    { value: 'inspection', label: '安全检查', icon: '✅', description: '年度安全检查和认证' },
    { value: 'upgrade', label: '设备升级', icon: '⚡', description: '功能升级或技术改造' }
  ];

  const urgencyLevels = [
    { value: 'low', label: '一般', color: '#28a745', time: '24小时内' },
    { value: 'medium', label: '紧急', color: '#ffc107', time: '4小时内' },
    { value: 'high', label: '非常紧急', color: '#dc3545', time: '1小时内' }
  ];

  return (
    <div className="maintenance-container">
      {/* 头部 */}
      <div className="maintenance-header">
        <div className="header-content">
          <h1>维保与更新改造服务</h1>
          <p>专业的技术团队，为您的电梯设备提供全方位的维护保养服务</p>
        </div>
      </div>

      {/* 服务特色 */}
      <div className="service-features">
        <div className="feature-card">
          <Wrench size={40} />
          <h3>专业技术</h3>
          <p>持证上岗的专业技术人员</p>
        </div>
        <div className="feature-card">
          <Clock size={40} />
          <h3>快速响应</h3>
          <p>24小时紧急响应服务</p>
        </div>
        <div className="feature-card">
          <CheckCircle size={40} />
          <h3>质量保证</h3>
          <p>标准化作业流程</p>
        </div>
      </div>

      {/* 主要内容区域 */}
      <div className="maintenance-content">
        {/* 标签页切换 */}
        <div className="tab-navigation">
          <button
            className={`tab-button ${activeTab === 'request' ? 'active' : ''}`}
            onClick={() => setActiveTab('request')}
          >
            <Wrench size={20} />
            维保申请
          </button>
          <button
            className={`tab-button ${activeTab === 'status' ? 'active' : ''}`}
            onClick={() => setActiveTab('status')}
          >
            <Clock size={20} />
            状态查询
          </button>
          <button
            className={`tab-button ${activeTab === 'contact' ? 'active' : ''}`}
            onClick={() => setActiveTab('contact')}
          >
            <Phone size={20} />
            联系我们
          </button>
        </div>

        {/* 维保申请表单 */}
        {activeTab === 'request' && (
          <div className="tab-content">
            <div className="form-section">
              <h2>维保服务申请</h2>
              <p>请填写以下信息，我们将为您安排专业的维保服务</p>

              {submitStatus && (
                <div className={`status-message ${submitStatus.type}`}>
                  {submitStatus.type === 'success' ? <CheckCircle size={20} /> : <AlertTriangle size={20} />}
                  {submitStatus.message}
                </div>
              )}

              <form onSubmit={handleSubmit} className="maintenance-form">
                <div className="form-grid">
                  <div className="form-group">
                    <label htmlFor="customer_name">客户姓名 *</label>
                    <input
                      type="text"
                      id="customer_name"
                      name="customer_name"
                      value={maintenanceForm.customer_name}
                      onChange={handleInputChange}
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="contact_phone">联系电话 *</label>
                    <input
                      type="tel"
                      id="contact_phone"
                      name="contact_phone"
                      value={maintenanceForm.contact_phone}
                      onChange={handleInputChange}
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="contact_email">邮箱地址</label>
                    <input
                      type="email"
                      id="contact_email"
                      name="contact_email"
                      value={maintenanceForm.contact_email}
                      onChange={handleInputChange}
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="elevator_location">设备位置 *</label>
                    <input
                      type="text"
                      id="elevator_location"
                      name="elevator_location"
                      value={maintenanceForm.elevator_location}
                      onChange={handleInputChange}
                      placeholder="详细地址"
                      required
                    />
                  </div>
                </div>

                <div className="form-section">
                  <h3>维保类型选择 *</h3>
                  <div className="maintenance-types">
                    {maintenanceTypes.map(type => (
                      <div
                        key={type.value}
                        className={`maintenance-type-card ${maintenanceForm.maintenance_type === type.value ? 'selected' : ''}`}
                        onClick={() => {
                          console.log('选择维保类型:', type.value);
                          setMaintenanceForm(prev => ({ ...prev, maintenance_type: type.value }));
                        }}
                      >
                        <div className="type-icon">{type.icon}</div>
                        <h4>{type.label}</h4>
                        <p>{type.description}</p>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="form-section">
                  <h3>紧急程度 *</h3>
                  <div className="urgency-levels">
                    {urgencyLevels.map(level => (
                      <div
                        key={level.value}
                        className={`urgency-card ${maintenanceForm.urgency_level === level.value ? 'selected' : ''}`}
                        onClick={() => {
                          console.log('选择紧急程度:', level.value);
                          setMaintenanceForm(prev => ({ ...prev, urgency_level: level.value }));
                        }}
                        style={{ borderColor: level.color }}
                      >
                        <div className="urgency-indicator" style={{ backgroundColor: level.color }}></div>
                        <h4>{level.label}</h4>
                        <p>响应时间：{level.time}</p>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="form-group">
                  <label htmlFor="description">问题描述</label>
                  <textarea
                    id="description"
                    name="description"
                    rows="4"
                    value={maintenanceForm.description}
                    onChange={handleInputChange}
                    placeholder="请详细描述设备问题或维保需求..."
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="preferred_time">期望服务时间</label>
                  <select
                    id="preferred_time"
                    name="preferred_time"
                    value={maintenanceForm.preferred_time}
                    onChange={handleInputChange}
                  >
                    <option value="">请选择</option>
                    <option value="morning">上午 (8:00-12:00)</option>
                    <option value="afternoon">下午 (13:00-17:00)</option>
                    <option value="evening">晚上 (18:00-22:00)</option>
                    <option value="urgent">紧急处理</option>
                  </select>
                </div>

                <button type="submit" className="submit-button" disabled={isSubmitting}>
                  {isSubmitting ? '提交中...' : '提交维保申请'}
                </button>
              </form>
            </div>
          </div>
        )}

        {/* 状态查询 */}
        {activeTab === 'status' && (
          <div className="tab-content">
            <div className="status-section">
              <h2>维保状态查询</h2>
              <p>输入您的联系电话或申请编号查询维保进度</p>
              
              <div className="search-form">
                <input
                  type="text"
                  placeholder="请输入联系电话或申请编号"
                  className="search-input"
                />
                <button className="search-button">查询</button>
              </div>

              <div className="status-example">
                <h3>查询结果示例</h3>
                <div className="status-card">
                  <div className="status-header">
                    <span className="status-badge in-progress">进行中</span>
                    <span className="order-number">申请编号：WB20241221001</span>
                  </div>
                  <div className="status-content">
                    <p><strong>服务类型：</strong>定期保养</p>
                    <p><strong>申请时间：</strong>2024-12-21 10:30</p>
                    <p><strong>预计完成：</strong>2024-12-21 16:00</p>
                    <p><strong>当前状态：</strong>技术人员已到达现场，正在进行检查</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 联系我们 */}
        {activeTab === 'contact' && (
          <div className="tab-content">
            <div className="contact-section">
              <h2>联系我们</h2>
              <p>多种联系方式，随时为您提供专业服务</p>

              <div className="contact-grid">
                <div className="contact-card">
                  <Phone size={40} />
                  <h3>24小时服务热线</h3>
                  <p className="contact-info">400-888-9999</p>
                  <p className="contact-desc">紧急故障请拨打此号码</p>
                </div>

                <div className="contact-card">
                  <Mail size={40} />
                  <h3>邮箱服务</h3>
                  <p className="contact-info">service@jojda.com</p>
                  <p className="contact-desc">非紧急问题可发送邮件</p>
                </div>

                <div className="contact-card">
                  <MapPin size={40} />
                  <h3>服务网点</h3>
                  <p className="contact-info">全国200+服务网点</p>
                  <p className="contact-desc">就近服务，快速响应</p>
                </div>
              </div>

              <div className="service-commitment">
                <h3>服务承诺</h3>
                <div className="commitment-list">
                  <div className="commitment-item">
                    <CheckCircle size={20} />
                    <span>24小时响应机制</span>
                  </div>
                  <div className="commitment-item">
                    <CheckCircle size={20} />
                    <span>专业技术人员持证上岗</span>
                  </div>
                  <div className="commitment-item">
                    <CheckCircle size={20} />
                    <span>标准化作业流程</span>
                  </div>
                  <div className="commitment-item">
                    <CheckCircle size={20} />
                    <span>质量保证体系</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MaintenanceService; 