import React, { useState, useEffect, useCallback } from 'react';
import { ChevronRight, ChevronLeft, CheckCircle, AlertCircle, Building, Users, Cog, DollarSign } from 'lucide-react';
import './RequirementFormOptimized.css';

const RequirementFormOptimized = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState({
    // 联系信息
    contact_name: '',
    contact_phone: '',
    contact_email: '',
    company_name: '',
    
    // 项目信息
    project_name: '',
    project_address: '',
    building_type: '', // 建筑类型
    usage_scenario: '', // 使用场景
    
    // 项目环境信息（新增）
    project_location: '', // 项目地理位置
    climate_conditions: '', // 气候条件
    is_outdoor: '', // 是否露天
    environmental_factors: '', // 环境因素描述
    seismic_zone: '', // 地震带等级
    coastal_area: '', // 是否沿海地区
    
    // 电梯基本参数
    elevator_type: '',
    quantity: 1,
    floors: '',
    floor_height: '',
    car_capacity: '',
    car_speed: '',
    daily_traffic: '', // 日客流量
    
    // 井道参数
    hoistway_width: '',
    hoistway_depth: '',
    pit_depth: '',
    overhead_height: '',
    
    // 轿厢参数
    car_width: '',
    car_depth: '',
    car_height: '',
    door_width: '',
    door_height: '',
    
    // 特殊要求
    special_requirements: '',
    budget_range: '',
    delivery_time: '',
    energy_efficiency: '', // 节能要求
    noise_level: '', // 噪音要求
    safety_features: [] // 安全功能要求
  });

  const [estimatedCost, setEstimatedCost] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);
  const [validationErrors, setValidationErrors] = useState({});

  // 表单步骤配置
  const steps = [
    {
      id: 'contact',
      title: '联系信息',
      icon: Users,
      description: '请提供您的联系方式，我们将为您提供专业服务'
    },
    {
      id: 'project',
      title: '项目概况',
      icon: Building,
      description: '了解您的项目基本情况，为您提供精准方案'
    },
    {
      id: 'requirements',
      title: '需求详情',
      icon: Cog,
      description: '详细的技术参数，确保方案完美匹配'
    },
    {
      id: 'budget',
      title: '预算与时间',
      icon: DollarSign,
      description: '预算和时间安排，为您定制最优方案'
    }
  ];

  // 电梯类型配置
  const elevatorTypes = [
    { 
      value: 'Passenger', 
      label: '乘客电梯',
      description: '适用于办公楼、住宅楼等载人场所',
      image: '🏢',
      speed_range: [0.5, 4.0]
    },
    { 
      value: 'Freight', 
      label: '货梯',
      description: '适用于货物运输，载重量大',
      image: '📦',
      speed_range: [0.25, 1.0]
    },
    { 
      value: 'Home', 
      label: '家用电梯',
      description: '适用于别墅、复式住宅',
      image: '🏠',
      speed_range: [0.15, 0.4]
    },
    { 
      value: 'Escalator', 
      label: '自动扶梯',
      description: '适用于商场、地铁等公共场所',
      image: '🛗',
      speed_range: [0.5, 0.75]
    },
    { 
      value: 'MovingWalkway', 
      label: '自动人行道',
      description: '适用于机场、大型建筑的水平运输',
      image: '🚶',
      speed_range: [0.5, 0.9]
    }
  ];

  // 建筑类型选项
  const buildingTypes = [
    { value: 'residential', label: '住宅楼', floors: [6, 33] },
    { value: 'office', label: '办公楼', floors: [5, 50] },
    { value: 'hotel', label: '酒店', floors: [3, 30] },
    { value: 'hospital', label: '医院', floors: [3, 20] },
    { value: 'shopping', label: '商场', floors: [2, 8] },
    { value: 'factory', label: '工厂', floors: [1, 10] },
    { value: 'villa', label: '别墅', floors: [2, 4] }
  ];

  // 智能推荐算法
  const generateRecommendations = useCallback(() => {
    const { elevator_type, floors, building_type, daily_traffic, climate_conditions, is_outdoor, seismic_zone, coastal_area } = formData;
    const newRecommendations = [];

    if (elevator_type && floors) {
      const selectedType = elevatorTypes.find(t => t.value === elevator_type);
      
      // 载重推荐
      if (building_type === 'residential' && elevator_type === 'Passenger') {
        newRecommendations.push({
          type: 'capacity',
          title: '载重建议',
          message: `住宅楼建议载重 ${floors <= 18 ? '800-1000kg' : '1000-1350kg'}`,
          value: floors <= 18 ? 800 : 1000
        });
      }

      // 速度推荐
      if (floors >= 10) {
        const recommendedSpeed = Math.min(selectedType.speed_range[1], floors * 0.15);
        newRecommendations.push({
          type: 'speed',
          title: '速度建议',
          message: `${floors}层建筑建议速度 ${recommendedSpeed.toFixed(1)}m/s`,
          value: recommendedSpeed.toFixed(1)
        });
      }

      // 数量推荐
      if (daily_traffic && building_type) {
        const trafficNum = parseInt(daily_traffic);
        let recommendedQuantity = 1;
        
        if (building_type === 'office' && trafficNum > 500) {
          recommendedQuantity = Math.ceil(trafficNum / 300);
        } else if (building_type === 'residential' && trafficNum > 200) {
          recommendedQuantity = Math.ceil(trafficNum / 150);
        }
        
        if (recommendedQuantity > 1) {
          newRecommendations.push({
            type: 'quantity',
            title: '数量建议',
            message: `根据客流量建议安装 ${recommendedQuantity} 台电梯`,
            value: recommendedQuantity
          });
        }
      }

      // 环境因素推荐
      if (climate_conditions === 'humid' || coastal_area === 'yes') {
        newRecommendations.push({
          type: 'environment',
          title: '防腐蚀建议',
          message: '高湿度或沿海环境建议选择不锈钢材质和防腐蚀涂层',
          value: 'corrosion_resistant'
        });
      }

      if (is_outdoor === 'yes') {
        newRecommendations.push({
          type: 'environment',
          title: '室外环境建议',
          message: '露天环境建议选择全封闭井道和防水等级IP65以上的控制系统',
          value: 'outdoor_protection'
        });
      }

      if (seismic_zone && parseInt(seismic_zone) >= 7) {
        newRecommendations.push({
          type: 'safety',
          title: '抗震建议',
          message: '高地震烈度区域建议配置地震感应器和紧急平层装置',
          value: 'earthquake_protection'
        });
      }

      if (climate_conditions === 'extreme_cold') {
        newRecommendations.push({
          type: 'environment',
          title: '低温环境建议',
          message: '极寒地区建议配置井道加热系统和低温润滑油',
          value: 'cold_weather_package'
        });
      }
    }

    setRecommendations(newRecommendations);
  }, [formData.elevator_type, formData.floors, formData.building_type, formData.daily_traffic, formData.climate_conditions, formData.is_outdoor, formData.seismic_zone, formData.coastal_area]);

  // 成本估算
  const calculateEstimatedCost = useCallback(() => {
    const { elevator_type, quantity, floors, car_capacity, climate_conditions, is_outdoor, seismic_zone, coastal_area } = formData;
    
    if (!elevator_type || !quantity || !floors) return;

    let baseCost = 0;
    const quantityNum = parseInt(quantity) || 1;
    const floorsNum = parseInt(floors) || 1;
    const capacityNum = parseInt(car_capacity) || 0;

    // 基础价格
    switch (elevator_type) {
      case 'Passenger':
        baseCost = 150000; // 15万基础价
        break;
      case 'Freight':
        baseCost = 200000; // 20万基础价
        break;
      case 'Home':
        baseCost = 100000; // 10万基础价
        break;
      case 'Escalator':
        baseCost = 300000; // 30万基础价
        break;
      default:
        baseCost = 150000; // 默认价格
        break;
    }

    // 楼层系数
    const floorMultiplier = Math.max(1, 1 + floorsNum * 0.05);
    
    // 载重系数
    const capacityMultiplier = capacityNum ? Math.max(1, capacityNum / 1000) : 1;
    
    // 环境因素成本调整
    let environmentMultiplier = 1;
    
    // 露天环境增加成本
    if (is_outdoor === 'yes') {
      environmentMultiplier += 0.25; // 增加25%
    } else if (is_outdoor === 'semi') {
      environmentMultiplier += 0.15; // 增加15%
    }
    
    // 特殊气候条件增加成本
    if (climate_conditions === 'extreme_cold' || climate_conditions === 'extreme_hot') {
      environmentMultiplier += 0.2; // 增加20%
    } else if (climate_conditions === 'humid' || climate_conditions === 'tropical') {
      environmentMultiplier += 0.15; // 增加15%
    }
    
    // 沿海地区防腐蚀处理
    if (coastal_area === 'yes') {
      environmentMultiplier += 0.12; // 增加12%
    }
    
    // 抗震要求增加成本
    if (seismic_zone && parseInt(seismic_zone) >= 8) {
      environmentMultiplier += 0.18; // 增加18%
    } else if (seismic_zone && parseInt(seismic_zone) === 7) {
      environmentMultiplier += 0.1; // 增加10%
    }
    
    // 总成本计算
    const totalCost = baseCost * quantityNum * floorMultiplier * capacityMultiplier * environmentMultiplier;
    
    setEstimatedCost({
      min: Math.round(totalCost * 0.8),
      max: Math.round(totalCost * 1.2),
      recommended: Math.round(totalCost),
      environmentFactor: Math.round((environmentMultiplier - 1) * 100) // 环境因素影响百分比
    });
  }, [formData.elevator_type, formData.quantity, formData.floors, formData.car_capacity, formData.climate_conditions, formData.is_outdoor, formData.seismic_zone, formData.coastal_area]);

  // 监听表单变化，触发智能推荐
  useEffect(() => {
    generateRecommendations();
    calculateEstimatedCost();
  }, [generateRecommendations, calculateEstimatedCost]);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    if (type === 'checkbox') {
      if (checked) {
        setFormData(prev => ({
          ...prev,
          [name]: [...(prev[name] || []), value]
        }));
      } else {
        setFormData(prev => ({
          ...prev,
          [name]: (prev[name] || []).filter(item => item !== value)
        }));
      }
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const applyRecommendation = (recommendation) => {
    setFormData(prev => ({
      ...prev,
      [recommendation.type === 'capacity' ? 'car_capacity' : 
       recommendation.type === 'speed' ? 'car_speed' :
       recommendation.type === 'quantity' ? 'quantity' : recommendation.type]: recommendation.value
    }));
  };

  // 表单验证
  const validateCurrentStep = () => {
    const errors = {};
    
    switch (currentStep) {
      case 0: // 联系信息
        if (!formData.contact_name.trim()) {
          errors.contact_name = '请输入联系人姓名';
        }
        if (!formData.contact_phone.trim()) {
          errors.contact_phone = '请输入联系电话';
        } else if (!/^1[3-9]\d{9}$/.test(formData.contact_phone)) {
          errors.contact_phone = '请输入正确的手机号码';
        }
        if (formData.contact_email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.contact_email)) {
          errors.contact_email = '请输入正确的邮箱地址';
        }
        break;
        
      case 1: // 项目概况
        if (!formData.building_type) {
          errors.building_type = '请选择建筑类型';
        }
        if (!formData.elevator_type) {
          errors.elevator_type = '请选择电梯类型';
        }
        break;
        
      case 2: // 需求详情
        if (!formData.quantity || formData.quantity < 1) {
          errors.quantity = '请输入正确的电梯数量';
        }
        if (!formData.floors || formData.floors < 2) {
          errors.floors = '请输入正确的楼层数';
        }
        break;
    }
    
    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const nextStep = () => {
    if (validateCurrentStep() && currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
      setValidationErrors({});
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitStatus(null);

    try {
      console.log('提交数据:', {
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
      });

      const response = await fetch('http://localhost:5000/api/elevatorrequirements', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
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
        })
      });

      console.log('响应状态:', response.status);
      console.log('响应头:', Object.fromEntries(response.headers.entries()));

      if (!response.ok) {
        const errorText = await response.text();
        console.error('HTTP错误:', response.status, errorText);
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }

      const result = await response.json();
      console.log('响应数据:', result);

      if (result.Success) {
        setSubmitStatus({
          type: 'success',
          message: '采购需求提交成功！我们的专家团队会在24小时内与您联系，为您提供专业的解决方案。'
        });
        // 重置表单
        setCurrentStep(0);
        setFormData({
          contact_name: '', contact_phone: '', contact_email: '', company_name: '',
          project_name: '', project_address: '', building_type: '', usage_scenario: '',
          project_location: '', climate_conditions: '', is_outdoor: '', environmental_factors: '',
          seismic_zone: '', coastal_area: '', elevator_type: '', quantity: 1, floors: '',
          floor_height: '', car_capacity: '', car_speed: '', daily_traffic: '',
          hoistway_width: '', hoistway_depth: '', pit_depth: '', overhead_height: '',
          car_width: '', car_depth: '', car_height: '', door_width: '', door_height: '',
          special_requirements: '', budget_range: '', delivery_time: '', energy_efficiency: '',
          noise_level: '', safety_features: []
        });
      } else {
        console.error('业务逻辑错误:', result.Message, result.Errors);
        setSubmitStatus({
          type: 'error',
          message: result.Message || '提交失败，请重试'
        });
      }
    } catch (error) {
      console.error('提交错误:', error);
      setSubmitStatus({
        type: 'error',
        message: `提交失败: ${error.message}`
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 0: // 联系信息
        return (
          <div className="step-content">
            <h3>请提供您的联系信息</h3>
            <p className="step-description">我们将严格保护您的隐私，仅用于为您提供专业的电梯解决方案</p>
            
            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="contact_name">
                  联系人姓名 <span className="required">*</span>
                </label>
                <input
                  type="text"
                  id="contact_name"
                  name="contact_name"
                  value={formData.contact_name}
                  onChange={handleInputChange}
                  placeholder="请输入您的姓名"
                  className={validationErrors.contact_name ? 'error' : ''}
                  required
                />
                {validationErrors.contact_name && (
                  <span className="error-message">{validationErrors.contact_name}</span>
                )}
              </div>

              <div className="form-group">
                <label htmlFor="contact_phone">
                  联系电话 <span className="required">*</span>
                </label>
                <input
                  type="tel"
                  id="contact_phone"
                  name="contact_phone"
                  value={formData.contact_phone}
                  onChange={handleInputChange}
                  placeholder="请输入您的手机号码"
                  className={validationErrors.contact_phone ? 'error' : ''}
                  required
                />
                {validationErrors.contact_phone && (
                  <span className="error-message">{validationErrors.contact_phone}</span>
                )}
              </div>

              <div className="form-group">
                <label htmlFor="contact_email">邮箱地址</label>
                <input
                  type="email"
                  id="contact_email"
                  name="contact_email"
                  value={formData.contact_email}
                  onChange={handleInputChange}
                  placeholder="请输入您的邮箱地址"
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
                  placeholder="请输入您的公司名称"
                />
              </div>
            </div>
          </div>
        );

      case 1: // 项目概况
        return (
          <div className="step-content">
            <h3>项目基本信息</h3>
            <p className="step-description">了解您的项目背景，帮助我们为您推荐最适合的解决方案</p>
            
            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="project_name">项目名称</label>
                <input
                  type="text"
                  id="project_name"
                  name="project_name"
                  value={formData.project_name}
                  onChange={handleInputChange}
                  placeholder="如：某某大厦、某某小区"
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
                  placeholder="请输入项目所在地址"
                />
              </div>

              <div className="form-group">
                <label htmlFor="building_type">
                  建筑类型 <span className="required">*</span>
                </label>
                <select
                  id="building_type"
                  name="building_type"
                  value={formData.building_type}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">请选择建筑类型</option>
                  {buildingTypes.map(type => (
                    <option key={type.value} value={type.value}>
                      {type.label}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="daily_traffic">预估日客流量（人/天）</label>
                <input
                  type="number"
                  id="daily_traffic"
                  name="daily_traffic"
                  value={formData.daily_traffic}
                  onChange={handleInputChange}
                  placeholder="如：500"
                />
                <small className="help-text">帮助我们推荐合适的电梯数量和配置</small>
              </div>
            </div>

            {/* 项目环境信息 */}
            <div className="environment-section">
              <h4>🌍 项目环境信息</h4>
              <p className="section-description">环境信息帮助我们为您推荐更适合的配置和防护方案</p>
              
              <div className="form-grid">
                <div className="form-group">
                  <label htmlFor="project_location">项目地理位置</label>
                  <select
                    id="project_location"
                    name="project_location"
                    value={formData.project_location}
                    onChange={handleInputChange}
                  >
                    <option value="">请选择地理位置</option>
                    <option value="north">北方地区</option>
                    <option value="south">南方地区</option>
                    <option value="coastal">沿海地区</option>
                    <option value="inland">内陆地区</option>
                    <option value="mountain">山区</option>
                    <option value="plateau">高原地区</option>
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="climate_conditions">气候条件</label>
                  <select
                    id="climate_conditions"
                    name="climate_conditions"
                    value={formData.climate_conditions}
                    onChange={handleInputChange}
                  >
                    <option value="">请选择气候条件</option>
                    <option value="temperate">温带气候</option>
                    <option value="humid">高湿度环境</option>
                    <option value="dry">干燥环境</option>
                    <option value="extreme_cold">极寒地区</option>
                    <option value="extreme_hot">高温地区</option>
                    <option value="tropical">热带气候</option>
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="is_outdoor">是否露天环境</label>
                  <select
                    id="is_outdoor"
                    name="is_outdoor"
                    value={formData.is_outdoor}
                    onChange={handleInputChange}
                  >
                    <option value="">请选择</option>
                    <option value="no">室内安装</option>
                    <option value="semi">半露天</option>
                    <option value="yes">完全露天</option>
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="seismic_zone">地震烈度</label>
                  <select
                    id="seismic_zone"
                    name="seismic_zone"
                    value={formData.seismic_zone}
                    onChange={handleInputChange}
                  >
                    <option value="">请选择地震烈度</option>
                    <option value="6">6度及以下</option>
                    <option value="7">7度</option>
                    <option value="8">8度</option>
                    <option value="9">9度及以上</option>
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="coastal_area">是否沿海地区</label>
                  <select
                    id="coastal_area"
                    name="coastal_area"
                    value={formData.coastal_area}
                    onChange={handleInputChange}
                  >
                    <option value="">请选择</option>
                    <option value="no">非沿海地区</option>
                    <option value="yes">沿海地区（距海岸线10km内）</option>
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="environmental_factors">特殊环境因素描述</label>
                <textarea
                  id="environmental_factors"
                  name="environmental_factors"
                  rows="3"
                  value={formData.environmental_factors}
                  onChange={handleInputChange}
                  placeholder="请描述项目所在地的特殊环境因素，如：工业污染、盐雾腐蚀、沙尘、振动等"
                />
              </div>
            </div>

            <div className="elevator-type-selection">
              <label className="section-label">
                电梯类型 <span className="required">*</span>
              </label>
              <div className="elevator-types-grid">
                {elevatorTypes.map(type => (
                  <div
                    key={type.value}
                    className={`elevator-type-card ${formData.elevator_type === type.value ? 'selected' : ''}`}
                    onClick={() => setFormData(prev => ({ ...prev, elevator_type: type.value }))}
                  >
                    <div className="elevator-type-icon">{type.image}</div>
                    <h4>{type.label}</h4>
                    <p>{type.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );

      case 2: // 需求详情
        return (
          <div className="step-content">
            <h3>技术参数需求</h3>
            <p className="step-description">详细的技术参数确保我们为您提供精确的解决方案</p>
            
            {/* 智能推荐面板 */}
            {recommendations.length > 0 && (
              <div className="recommendations-panel">
                <h4>💡 智能推荐</h4>
                <div className="recommendations-list">
                  {recommendations.map((rec, index) => (
                    <div key={index} className="recommendation-item">
                      <div className="recommendation-content">
                        <strong>{rec.title}</strong>
                        <p>{rec.message}</p>
                      </div>
                      <button
                        type="button"
                        className="apply-recommendation"
                        onClick={() => applyRecommendation(rec)}
                      >
                        采纳建议
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="form-sections">
              {/* 基本参数 */}
              <div className="form-section">
                <h5>基本参数</h5>
                <div className="form-grid">
                  <div className="form-group">
                    <label htmlFor="quantity">数量 <span className="required">*</span></label>
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

                  <div className="form-group">
                    <label htmlFor="floors">楼层数 <span className="required">*</span></label>
                    <input
                      type="number"
                      id="floors"
                      name="floors"
                      min="2"
                      value={formData.floors}
                      onChange={handleInputChange}
                      placeholder="包含地下层"
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
                      placeholder="如：3.0"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="car_capacity">载重量(kg)</label>
                    <input
                      type="number"
                      id="car_capacity"
                      name="car_capacity"
                      value={formData.car_capacity}
                      onChange={handleInputChange}
                      placeholder="如：1000"
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
                      placeholder="如：1.5"
                    />
                  </div>
                </div>
              </div>

              {/* 井道参数 */}
              <div className="form-section">
                <h5>井道参数 <small>(如已知)</small></h5>
                <div className="form-grid">
                  <div className="form-group">
                    <label htmlFor="hoistway_width">井道宽度(mm)</label>
                    <input
                      type="number"
                      id="hoistway_width"
                      name="hoistway_width"
                      value={formData.hoistway_width}
                      onChange={handleInputChange}
                      placeholder="如：2000"
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
                      placeholder="如：2100"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="pit_depth">底坑深度(mm)</label>
                    <input
                      type="number"
                      id="pit_depth"
                      name="pit_depth"
                      value={formData.pit_depth}
                      onChange={handleInputChange}
                      placeholder="如：1500"
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
                      placeholder="如：4.5"
                    />
                  </div>
                </div>
              </div>

              {/* 特殊要求 */}
              <div className="form-section">
                <h5>特殊要求</h5>
                <div className="form-grid">
                  <div className="form-group">
                    <label htmlFor="energy_efficiency">节能等级要求</label>
                    <select
                      id="energy_efficiency"
                      name="energy_efficiency"
                      value={formData.energy_efficiency}
                      onChange={handleInputChange}
                    >
                      <option value="">无特殊要求</option>
                      <option value="standard">标准节能</option>
                      <option value="high">高效节能</option>
                      <option value="premium">顶级节能</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label htmlFor="noise_level">噪音控制要求</label>
                    <select
                      id="noise_level"
                      name="noise_level"
                      value={formData.noise_level}
                      onChange={handleInputChange}
                    >
                      <option value="">无特殊要求</option>
                      <option value="standard">标准静音 (≤55dB)</option>
                      <option value="quiet">超静音 (≤45dB)</option>
                      <option value="silent">极静音 (≤35dB)</option>
                    </select>
                  </div>
                </div>

                <div className="form-group">
                  <label className="section-label">安全功能要求</label>
                  <div className="checkbox-group">
                    {[
                      { value: 'emergency_power', label: '应急电源' },
                      { value: 'fire_service', label: '消防功能' },
                      { value: 'earthquake_protection', label: '抗震保护' },
                      { value: 'anti_vandal', label: '防暴力功能' },
                      { value: 'monitoring', label: '远程监控' }
                    ].map(feature => (
                      <label key={feature.value} className="checkbox-label">
                        <input
                          type="checkbox"
                          name="safety_features"
                          value={feature.value}
                          checked={formData.safety_features.includes(feature.value)}
                          onChange={handleInputChange}
                        />
                        <span>{feature.label}</span>
                      </label>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        );

      case 3: // 预算与时间
        return (
          <div className="step-content">
            <h3>预算与交付时间</h3>
            <p className="step-description">预算和时间安排帮助我们为您制定最合适的方案</p>
            
            {/* 成本估算显示 */}
            {estimatedCost && (
              <div className="cost-estimation">
                <h4>💰 智能成本估算</h4>
                <div className="cost-breakdown">
                  <div className="cost-item">
                    <span className="cost-label">预估价格区间：</span>
                    <span className="cost-value">
                      {(estimatedCost.min / 10000).toFixed(1)}万 - {(estimatedCost.max / 10000).toFixed(1)}万元
                    </span>
                  </div>
                  <div className="cost-item recommended">
                    <span className="cost-label">推荐配置价格：</span>
                    <span className="cost-value">
                      {(estimatedCost.recommended / 10000).toFixed(1)}万元
                    </span>
                  </div>
                  {estimatedCost.environmentFactor > 0 && (
                    <div className="cost-item environment-factor">
                      <span className="cost-label">环境因素影响：</span>
                      <span className="cost-value environment">
                        +{estimatedCost.environmentFactor}%
                      </span>
                    </div>
                  )}
                </div>
                <small className="cost-note">
                  *价格已考虑项目环境因素，最终报价以实际配置和现场勘测为准
                </small>
              </div>
            )}

            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="budget_range">预算范围</label>
                <select
                  id="budget_range"
                  name="budget_range"
                  value={formData.budget_range}
                  onChange={handleInputChange}
                >
                  <option value="">请选择预算范围</option>
                  <option value="50万以下">50万以下</option>
                  <option value="50-100万">50-100万</option>
                  <option value="100-200万">100-200万</option>
                  <option value="200-500万">200-500万</option>
                  <option value="500-1000万">500-1000万</option>
                  <option value="1000万以上">1000万以上</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="delivery_time">期望交付时间</label>
                <select
                  id="delivery_time"
                  name="delivery_time"
                  value={formData.delivery_time}
                  onChange={handleInputChange}
                >
                  <option value="">请选择期望交付时间</option>
                  <option value="1个月内">1个月内</option>
                  <option value="3个月内">3个月内</option>
                  <option value="6个月内">6个月内</option>
                  <option value="1年内">1年内</option>
                  <option value="时间充裕">时间充裕</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="special_requirements">其他特殊要求</label>
              <textarea
                id="special_requirements"
                name="special_requirements"
                rows="4"
                value={formData.special_requirements}
                onChange={handleInputChange}
                placeholder="请描述您的其他特殊要求，如装饰风格、特殊功能、安装环境等"
              />
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="optimized-form-container">
      {/* 头部 */}
      <div className="form-header">
        <div className="header-content">
          <h1>电梯解决方案定制</h1>
          <p>专业团队为您量身定制最适合的电梯解决方案</p>
        </div>
        
        {/* 进度指示器 */}
        <div className="progress-indicator">
          {steps.map((step, index) => {
            const StepIcon = step.icon;
            return (
              <div
                key={step.id}
                className={`progress-step ${index <= currentStep ? 'active' : ''} ${index === currentStep ? 'current' : ''}`}
              >
                <div className="step-icon">
                  {index < currentStep ? (
                    <CheckCircle size={24} />
                  ) : (
                    <StepIcon size={24} />
                  )}
                </div>
                <div className="step-info">
                  <span className="step-title">{step.title}</span>
                  <span className="step-description">{step.description}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 状态消息 */}
      {submitStatus && (
        <div className={`submit-status ${submitStatus.type}`}>
          {submitStatus.type === 'success' ? (
            <CheckCircle size={20} />
          ) : (
            <AlertCircle size={20} />
          )}
          <span>{submitStatus.message}</span>
        </div>
      )}

      {/* 表单内容 */}
      <form onSubmit={handleSubmit} className="optimized-form">
        <div className="form-body">
          {renderStepContent()}
        </div>

        {/* 导航按钮 */}
        <div className="form-navigation">
          <button
            type="button"
            className="nav-button prev"
            onClick={prevStep}
            disabled={currentStep === 0}
          >
            <ChevronLeft size={20} />
            上一步
          </button>

          <div className="step-counter">
            {currentStep + 1} / {steps.length}
          </div>

          {currentStep === steps.length - 1 ? (
            <button
              type="submit"
              className="nav-button submit"
              disabled={isSubmitting}
            >
              {isSubmitting ? '提交中...' : '提交需求'}
              <CheckCircle size={20} />
            </button>
          ) : (
            <button
              type="button"
              className="nav-button next"
              onClick={nextStep}
            >
              下一步
              <ChevronRight size={20} />
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default RequirementFormOptimized; 