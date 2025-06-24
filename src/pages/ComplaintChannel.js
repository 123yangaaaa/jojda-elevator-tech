import React, { useState } from 'react';
import { MessageCircle, AlertTriangle, CheckCircle, Phone, Mail, Clock, Star } from 'lucide-react';
import './ComplaintChannel.css';

const ComplaintChannel = () => {
  const [complaintForm, setComplaintForm] = useState({
    customer_name: '',
    contact_phone: '',
    contact_email: '',
    complaint_type: '',
    complaint_level: '',
    description: '',
    location: '',
    preferred_contact: ''
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setComplaintForm(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitStatus(null);

    try {
      // 这里可以调用后端API
      await new Promise(resolve => setTimeout(resolve, 2000)); // 模拟API调用
      
      setSubmitStatus({
        type: 'success',
        message: '投诉提交成功！我们的客服团队会在24小时内与您联系处理。'
      });
      
      // 重置表单
      setComplaintForm({
        customer_name: '', contact_phone: '', contact_email: '', complaint_type: '',
        complaint_level: '', description: '', location: '', preferred_contact: ''
      });
    } catch (error) {
      setSubmitStatus({
        type: 'error',
        message: '提交失败，请重试或联系客服'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const complaintTypes = [
    { value: 'service', label: '服务质量', icon: '👨‍🔧', description: '维保服务相关问题' },
    { value: 'product', label: '产品质量', icon: '🏗️', description: '设备质量问题' },
    { value: 'safety', label: '安全隐患', icon: '⚠️', description: '安全相关问题' },
    { value: 'response', label: '响应速度', icon: '⏰', description: '服务响应时间' },
    { value: 'attitude', label: '服务态度', icon: '😊', description: '工作人员态度' },
    { value: 'other', label: '其他问题', icon: '❓', description: '其他类型问题' }
  ];

  const complaintLevels = [
    { value: 'low', label: '一般', color: '#28a745', time: '48小时内处理' },
    { value: 'medium', label: '重要', color: '#ffc107', time: '24小时内处理' },
    { value: 'high', label: '紧急', color: '#dc3545', time: '4小时内处理' }
  ];

  return (
    <div className="complaint-container">
      {/* 头部 */}
      <div className="complaint-header">
        <div className="header-content">
          <h1>客户投诉与建议</h1>
          <p>我们重视每一位客户的意见，您的反馈是我们改进的动力</p>
        </div>
      </div>

      {/* 服务承诺 */}
      <div className="service-promises">
        <div className="promise-card">
          <Clock size={40} />
          <h3>快速响应</h3>
          <p>24小时内响应您的投诉</p>
        </div>
        <div className="promise-card">
          <CheckCircle size={40} />
          <h3>专业处理</h3>
          <p>专业团队负责处理</p>
        </div>
        <div className="promise-card">
          <Star size={40} />
          <h3>持续改进</h3>
          <p>根据反馈持续优化服务</p>
        </div>
      </div>

      {/* 主要内容区域 */}
      <div className="complaint-content">
        <div className="complaint-form-section">
          <h2>投诉建议提交</h2>
          <p>请详细描述您遇到的问题，我们将认真处理并给您满意的答复</p>

          {submitStatus && (
            <div className={`status-message ${submitStatus.type}`}>
              {submitStatus.type === 'success' ? <CheckCircle size={20} /> : <AlertTriangle size={20} />}
              {submitStatus.message}
            </div>
          )}

          <form onSubmit={handleSubmit} className="complaint-form">
            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="customer_name">客户姓名 *</label>
                <input
                  type="text"
                  id="customer_name"
                  name="customer_name"
                  value={complaintForm.customer_name}
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
                  value={complaintForm.contact_phone}
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
                  value={complaintForm.contact_email}
                  onChange={handleInputChange}
                />
              </div>

              <div className="form-group">
                <label htmlFor="location">问题发生地点</label>
                <input
                  type="text"
                  id="location"
                  name="location"
                  value={complaintForm.location}
                  onChange={handleInputChange}
                  placeholder="详细地址"
                />
              </div>
            </div>

            <div className="form-section">
              <h3>投诉类型</h3>
              <div className="complaint-types">
                {complaintTypes.map(type => (
                  <div
                    key={type.value}
                    className={`complaint-type-card ${complaintForm.complaint_type === type.value ? 'selected' : ''}`}
                    onClick={() => setComplaintForm(prev => ({ ...prev, complaint_type: type.value }))}
                  >
                    <div className="type-icon">{type.icon}</div>
                    <h4>{type.label}</h4>
                    <p>{type.description}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="form-section">
              <h3>紧急程度</h3>
              <div className="complaint-levels">
                {complaintLevels.map(level => (
                  <div
                    key={level.value}
                    className={`complaint-level-card ${complaintForm.complaint_level === level.value ? 'selected' : ''}`}
                    onClick={() => setComplaintForm(prev => ({ ...prev, complaint_level: level.value }))}
                    style={{ borderColor: level.color }}
                  >
                    <div className="level-indicator" style={{ backgroundColor: level.color }}></div>
                    <h4>{level.label}</h4>
                    <p>处理时间：{level.time}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="description">详细描述 *</label>
              <textarea
                id="description"
                name="description"
                rows="6"
                value={complaintForm.description}
                onChange={handleInputChange}
                placeholder="请详细描述您遇到的问题、发生时间、具体情况等..."
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="preferred_contact">首选联系方式</label>
              <select
                id="preferred_contact"
                name="preferred_contact"
                value={complaintForm.preferred_contact}
                onChange={handleInputChange}
              >
                <option value="">请选择</option>
                <option value="phone">电话联系</option>
                <option value="email">邮件联系</option>
                <option value="both">电话和邮件</option>
              </select>
            </div>

            <button type="submit" className="submit-button" disabled={isSubmitting}>
              {isSubmitting ? '提交中...' : '提交投诉建议'}
            </button>
          </form>
        </div>

        {/* 联系信息 */}
        <div className="contact-info-section">
          <h2>其他联系方式</h2>
          <div className="contact-methods">
            <div className="contact-method">
              <Phone size={30} />
              <div>
                <h3>24小时服务热线</h3>
                <p>400-888-9999</p>
                <small>紧急问题请直接拨打</small>
              </div>
            </div>
            
            <div className="contact-method">
              <Mail size={30} />
              <div>
                <h3>投诉邮箱</h3>
                <p>complaint@jojda.com</p>
                <small>非紧急问题可发送邮件</small>
              </div>
            </div>
            
            <div className="contact-method">
              <MessageCircle size={30} />
              <div>
                <h3>在线客服</h3>
                <p>工作日 9:00-18:00</p>
                <small>实时在线咨询</small>
              </div>
            </div>
          </div>

          <div className="feedback-process">
            <h3>投诉处理流程</h3>
            <div className="process-steps">
              <div className="process-step">
                <div className="step-number">1</div>
                <div className="step-content">
                  <h4>提交投诉</h4>
                  <p>通过表单或电话提交投诉</p>
                </div>
              </div>
              <div className="process-step">
                <div className="step-number">2</div>
                <div className="step-content">
                  <h4>受理确认</h4>
                  <p>24小时内确认受理</p>
                </div>
              </div>
              <div className="process-step">
                <div className="step-number">3</div>
                <div className="step-content">
                  <h4>调查处理</h4>
                  <p>专业团队调查处理</p>
                </div>
              </div>
              <div className="process-step">
                <div className="step-number">4</div>
                <div className="step-content">
                  <h4>反馈结果</h4>
                  <p>及时反馈处理结果</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ComplaintChannel; 