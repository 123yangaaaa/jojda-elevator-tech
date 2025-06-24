import React, { useState } from 'react';
import './RequirementForm.css';

const RequirementForm = () => {
  const [formData, setFormData] = useState({
    contact_name: '',
    contact_phone: '',
    contact_email: '',
    company_name: '',
    project_name: '',
    project_address: '',
    elevator_type: '',
    quantity: 1,
    floors: '',
    floor_height: '',
    car_capacity: '',
    car_speed: '',
    hoistway_width: '',
    hoistway_depth: '',
    pit_depth: '',
    overhead_height: '',
    car_width: '',
    car_depth: '',
    car_height: '',
    door_width: '',
    door_height: '',
    special_requirements: '',
    budget_range: '',
    delivery_time: ''
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitStatus(null);

    console.log('开始提交采购需求...');
    console.log('请求地址:', 'http://localhost:5000/api/elevatorrequirements');
    console.log('请求数据:', formData);

    try {
      const requestBody = {
        contactName: formData.contact_name,
        contactPhone: formData.contact_phone,
        contactEmail: formData.contact_email,
        companyName: formData.company_name,
        projectName: formData.project_name,
        projectAddress: formData.project_address,
        elevatorType: formData.elevator_type,
        quantity: parseInt(formData.quantity),
        floors: parseInt(formData.floors),
        floorHeight: formData.floor_height ? parseFloat(formData.floor_height) : null,
        carCapacity: formData.car_capacity ? parseInt(formData.car_capacity) : null,
        carSpeed: formData.car_speed ? parseFloat(formData.car_speed) : null,
        hoistwayWidth: formData.hoistway_width ? parseFloat(formData.hoistway_width) : null,
        hoistwayDepth: formData.hoistway_depth ? parseFloat(formData.hoistway_depth) : null,
        pitDepth: formData.pit_depth ? parseFloat(formData.pit_depth) : null,
        overheadHeight: formData.overhead_height ? parseFloat(formData.overhead_height) : null,
        carWidth: formData.car_width ? parseFloat(formData.car_width) : null,
        carDepth: formData.car_depth ? parseFloat(formData.car_depth) : null,
        carHeight: formData.car_height ? parseFloat(formData.car_height) : null,
        doorWidth: formData.door_width ? parseFloat(formData.door_width) : null,
        doorHeight: formData.door_height ? parseFloat(formData.door_height) : null,
        specialRequirements: formData.special_requirements,
        budgetRange: formData.budget_range,
        deliveryTime: formData.delivery_time
      };

      console.log('发送的请求体:', requestBody);

      const response = await fetch('http://localhost:5000/api/elevatorrequirements', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      console.log('响应状态:', response.status);
      console.log('响应头:', response.headers);

      const result = await response.json();
      console.log('响应数据:', result);

      if (result.Success) {
        setSubmitStatus({
          type: 'success',
          message: result.Message || '采购需求提交成功！我们会尽快与您联系。'
        });
        // 重置表单
        setFormData({
          contact_name: '',
          contact_phone: '',
          contact_email: '',
          company_name: '',
          project_name: '',
          project_address: '',
          elevator_type: '',
          quantity: 1,
          floors: '',
          floor_height: '',
          car_capacity: '',
          car_speed: '',
          hoistway_width: '',
          hoistway_depth: '',
          pit_depth: '',
          overhead_height: '',
          car_width: '',
          car_depth: '',
          car_height: '',
          door_width: '',
          door_height: '',
          special_requirements: '',
          budget_range: '',
          delivery_time: ''
        });
      } else {
        setSubmitStatus({
          type: 'error',
          message: result.Message || '提交失败，请重试'
        });
      }
    } catch (error) {
      console.error('提交错误详情:', error);
      console.error('错误名称:', error.name);
      console.error('错误消息:', error.message);
      console.error('错误堆栈:', error.stack);
      
      setSubmitStatus({
        type: 'error',
        message: '网络错误，请检查网络连接后重试'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const elevatorTypes = [
    { value: 'Passenger', label: '乘客电梯' },
    { value: 'Freight', label: '货梯' },
    { value: 'Home', label: '家用电梯' },
    { value: 'Escalator', label: '自动扶梯' },
    { value: 'MovingWalkway', label: '自动人行道' }
  ];

  const budgetRanges = [
    { value: '100万以下', label: '100万以下' },
    { value: '100-200万', label: '100-200万' },
    { value: '200-500万', label: '200-500万' },
    { value: '500-1000万', label: '500-1000万' },
    { value: '1000万以上', label: '1000万以上' }
  ];

  return (
    <div className="requirement-form-container">
      <div className="requirement-form-header">
        <h1>电梯采购需求提交</h1>
        <p>请填写您的电梯采购需求，我们将为您提供专业的解决方案</p>
      </div>

      {submitStatus && (
        <div className={`submit-status ${submitStatus.type}`}>
          {submitStatus.message}
        </div>
      )}

      <form onSubmit={handleSubmit} className="requirement-form">
        {/* 联系信息 */}
        <div className="form-section">
          <h2>联系信息</h2>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="contact_name">联系人姓名 *</label>
              <input
                type="text"
                id="contact_name"
                name="contact_name"
                value={formData.contact_name}
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
                value={formData.contact_phone}
                onChange={handleInputChange}
                required
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="contact_email">联系邮箱</label>
              <input
                type="email"
                id="contact_email"
                name="contact_email"
                value={formData.contact_email}
                onChange={handleInputChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="company_name">公司名称</label>
              <input
                type="text"
                id="company_name"
                name="company_name"
                value={formData.company_name}
                onChange={handleInputChange}
              />
            </div>
          </div>
        </div>

        {/* 项目信息 */}
        <div className="form-section">
          <h2>项目信息</h2>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="project_name">项目名称</label>
              <input
                type="text"
                id="project_name"
                name="project_name"
                value={formData.project_name}
                onChange={handleInputChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="project_address">项目地址</label>
              <input
                type="text"
                id="project_address"
                name="project_address"
                value={formData.project_address}
                onChange={handleInputChange}
              />
            </div>
          </div>
        </div>

        {/* 电梯基本参数 */}
        <div className="form-section">
          <h2>电梯基本参数</h2>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="elevator_type">电梯类型 *</label>
              <select
                id="elevator_type"
                name="elevator_type"
                value={formData.elevator_type}
                onChange={handleInputChange}
                required
              >
                <option value="">请选择电梯类型</option>
                {elevatorTypes.map(type => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="quantity">数量 *</label>
              <input
                type="number"
                id="quantity"
                name="quantity"
                min="1"
                value={formData.quantity}
                onChange={handleInputChange}
                required
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="floors">楼层数 *</label>
              <input
                type="number"
                id="floors"
                name="floors"
                min="2"
                value={formData.floors}
                onChange={handleInputChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="floor_height">层高(米)</label>
              <input
                type="number"
                id="floor_height"
                name="floor_height"
                step="0.1"
                value={formData.floor_height}
                onChange={handleInputChange}
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="car_capacity">载重量(kg)</label>
              <input
                type="number"
                id="car_capacity"
                name="car_capacity"
                value={formData.car_capacity}
                onChange={handleInputChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="car_speed">运行速度(m/s)</label>
              <input
                type="number"
                id="car_speed"
                name="car_speed"
                step="0.1"
                value={formData.car_speed}
                onChange={handleInputChange}
              />
            </div>
          </div>
        </div>

        {/* 井道参数 */}
        <div className="form-section">
          <h2>井道参数</h2>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="hoistway_width">井道宽度(mm)</label>
              <input
                type="number"
                id="hoistway_width"
                name="hoistway_width"
                value={formData.hoistway_width}
                onChange={handleInputChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="hoistway_depth">井道深度(mm)</label>
              <input
                type="number"
                id="hoistway_depth"
                name="hoistway_depth"
                value={formData.hoistway_depth}
                onChange={handleInputChange}
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="pit_depth">底坑深度(m)</label>
              <input
                type="number"
                id="pit_depth"
                name="pit_depth"
                step="0.1"
                value={formData.pit_depth}
                onChange={handleInputChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="overhead_height">顶层高度(m)</label>
              <input
                type="number"
                id="overhead_height"
                name="overhead_height"
                step="0.1"
                value={formData.overhead_height}
                onChange={handleInputChange}
              />
            </div>
          </div>
        </div>

        {/* 轿厢参数 */}
        <div className="form-section">
          <h2>轿厢参数</h2>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="car_width">轿厢宽度(mm)</label>
              <input
                type="number"
                id="car_width"
                name="car_width"
                value={formData.car_width}
                onChange={handleInputChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="car_depth">轿厢深度(mm)</label>
              <input
                type="number"
                id="car_depth"
                name="car_depth"
                value={formData.car_depth}
                onChange={handleInputChange}
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="car_height">轿厢高度(m)</label>
              <input
                type="number"
                id="car_height"
                name="car_height"
                step="0.1"
                value={formData.car_height}
                onChange={handleInputChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="door_width">门宽(mm)</label>
              <input
                type="number"
                id="door_width"
                name="door_width"
                value={formData.door_width}
                onChange={handleInputChange}
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="door_height">门高(mm)</label>
              <input
                type="number"
                id="door_height"
                name="door_height"
                value={formData.door_height}
                onChange={handleInputChange}
              />
            </div>
          </div>
        </div>

        {/* 其他要求 */}
        <div className="form-section">
          <h2>其他要求</h2>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="budget_range">预算范围</label>
              <select
                id="budget_range"
                name="budget_range"
                value={formData.budget_range}
                onChange={handleInputChange}
              >
                <option value="">请选择预算范围</option>
                {budgetRanges.map(range => (
                  <option key={range.value} value={range.value}>
                    {range.label}
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="delivery_time">交货期要求</label>
              <input
                type="text"
                id="delivery_time"
                name="delivery_time"
                placeholder="例如：3个月内"
                value={formData.delivery_time}
                onChange={handleInputChange}
              />
            </div>
          </div>
          <div className="form-group full-width">
            <label htmlFor="special_requirements">特殊要求</label>
            <textarea
              id="special_requirements"
              name="special_requirements"
              rows="4"
              placeholder="请描述您的特殊要求或备注信息"
              value={formData.special_requirements}
              onChange={handleInputChange}
            />
          </div>
        </div>

        <div className="form-actions">
          <button
            type="submit"
            className="submit-btn"
            disabled={isSubmitting}
          >
            {isSubmitting ? '提交中...' : '提交采购需求'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default RequirementForm; 