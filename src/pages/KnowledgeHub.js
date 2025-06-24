import React, { useState } from 'react';
import { ArrowRight, ExternalLink, Building, Calendar, MapPin, Users, Zap, Globe } from 'lucide-react';
import './KnowledgeHub.css';

const KnowledgeHub = () => {
  const [activeTab, setActiveTab] = useState('news');

  const newsStories = [
    {
      id: 1,
      title: "KONE智能电梯助力斯德哥尔摩房地产预测性维护革命",
      summary: "瑞典房地产公司Humlegården与KONE合作，利用IBM Watson IoT平台实现电梯故障预测，大幅减少停机时间。",
      category: "技术创新",
      date: "2025年1月",
      image: "/images/stockholm-smart-elevators.jpg",
      content: "在斯德哥尔摩，领先的房地产公司Humlegården正在使用KONE 24/7 Connected Services系统，这是一项使用IBM Watson IoT平台处理电梯监控设备云数据的突破性技术。该系统通过分析和预测设备问题，实现了电梯维护的革命性转变。传统的基于日历的维护方式存在局限性，而这种新方法通过全天候收集数据、分析每台设备的个性化需求，并预测问题发生，实现了计划性维护。系统监控约200个数据点，通过AI驱动的分析发现复杂模式：比如当组件A显示特定振动，而组件B温度上升0.5度时，组件C很可能在一周内出现故障。"
    },
    {
      id: 2,
      title: "One World Trade Center：西半球最快电梯技术突破",
      summary: "纽约世贸中心一号楼配备了西半球最快的电梯系统，采用先进的计算机化导轨技术和气压平衡系统。",
      category: "工程奇迹",
      date: "2024年12月",
      image: "/images/one-wtc-elevators.jpg",
      content: "高达541米的One World Trade Center配备了73部电梯，其中5部快速电梯速度超过36.5公里/小时（10.16米/秒），是西半球最快的电梯。这些快速电梯可承载1814公斤载重，只需约40秒就能从地面到达394米高的102层观景台。为了实现如此高速运行，ThyssenKrupp设计了创新的自动滚轮导向系统，就像高速列车一样需要极其平滑的轨道。由于摩天大楼会因温度变化和风力而轻微摆动，电梯必须适应导轨间距的微小变化。智能滚轮导向系统像实时减震器一样工作，当检测到轨道不平整时会自动调整，确保乘客舒适无震动的乘坐体验。"
    },
    {
      id: 3,
      title: "德国盲人学校：智能电梯辅助技术创新应用",
      summary: "德国BFW Würzburg职业培训中心与KONE合作，将BlindSquare导航应用与电梯API集成，为视障学生提供独立出行支持。",
      category: "社会责任",
      date: "2024年11月",
      image: "/images/germany-accessibility.jpg",
      content: "在德国巴伐利亚州的BFW Würzburg职业培训中心，一项开创性的技术正在改变220名视障学生的生活。通过将BlindSquare智能手机导航应用与KONE电梯API集成，学生们现在可以通过语音提示独立地在楼层间导航。BlindSquare应用结合了GPS技术和听觉提示，描述周围环境并指出行进路径。虽然该应用已经能够绘制大部分室外世界地图，但建筑内部导航一直是挑战。通过在建筑内安装蓝牙位置标识信标，并与电梯控制系统集成，BlindSquare现在能够帮助用户安全、高效地呼叫电梯并到达目标楼层。这项技术的价值在于创造了一个无障碍环境，使视障人士能够从A点到B点独立出行，无需陪同。"
    },
    {
      id: 4,
      title: "ThyssenKrupp MULTI系统：无绳电梯技术的未来",
      summary: "德国ThyssenKrupp公司推出革命性MULTI电梯系统，实现垂直、水平、前后移动，突破传统电梯高度限制。",
      category: "未来技术",
      date: "2024年10月",
      image: "/images/multi-elevator-system.jpg",
      content: "ThyssenKrupp开发的MULTI系统彻底颠覆了传统电梯概念。与传统电梯只能上下移动不同，MULTI系统的轿厢可以垂直、水平、前后移动，就像地铁系统一样管理电梯。每个系统包含多个轿厢，每个都由线性感应电机驱动。受TWIN系统启发，这项2017年推出的技术是首个多轿厢无绳电梯系统。由于不再需要绳索移动轿厢，系统不再受高度限制，为超高层建筑提供了解决方案。MULTI系统还承诺通过'智能'设备减少高达60%的峰值功耗需求，从而降低整个建筑的碳足迹。这项技术为建筑师提供了前所未有的设计自由度，电梯可以在垂直和水平方向移动，在相邻井道中相互穿越。"
    },
    {
      id: 5,
      title: "KONE UltraRope技术：碳纤维绳索的突破性应用",
      summary: "芬兰KONE公司的UltraRope碳纤维技术使电梯行程达到1000米，重量减少90%，在伦敦South Quay Plaza等项目中成功应用。",
      category: "材料科学",
      date: "2024年9月",
      image: "/images/ultrarope-technology.jpg",
      content: "KONE的UltraRope技术代表了电梯绳索技术的重大突破。这种碳纤维芯绳索配备特殊高摩擦涂层，使电梯轿厢能够在单次运行中行进1000米，是传统钢绳最大行程500米的两倍。最显著的创新在于绳索重量减少90%，为2000公斤电梯行进500米时，UltraRope重量仅为2500公斤，而传统超高张力钢绳重达27000公斤。这种重量减少带来显著的节能效果。UltraRope技术已在伦敦South Quay Plaza等欧洲最高住宅建筑中成功应用，该项目安装了8部UltraRope电梯。新加坡滨海湾金沙酒店也采用了这项技术。计划中的1000米高的沙特阿拉伯吉达塔（目前暂停建设）也将使用KONE UltraRope电梯系统。"
    },
    {
      id: 6,
      title: "智能建筑革命：电梯成为IoT生态系统核心",
      summary: "全球电梯行业正在经历数字化转型，AI、IoT和预测性维护技术正在重新定义垂直交通的未来。",
      category: "行业趋势",
      date: "2024年8月",
      image: "/images/smart-building-iot.jpg",
      content: "现代智能建筑正在将电梯从简单的交通工具转变为IoT生态系统的核心组件。通过传感器收集的数据不仅用于私营企业，更重要的是为建筑用户带来优势。KONE每天为全球超过10亿人提供电梯和自动扶梯服务，正在分析电梯使用数据以指导可持续建筑规划，并帮助人们更安全、高效地在建筑物中移动。这些数字解决方案通过提升物理环境的服务质量，为人们的日常出行提供安心保障。目前全球有4500万智能建筑，预计到2026年将增长到1.15亿，增长率超过150%。智能建筑的好处包括：改善租户/员工福祉、降低成本和能耗（可节省高达23%的能源）、增强安全性、预测性维护等。"
    }
  ];

  const projectCases = [
    {
      id: 1,
      title: "迪拜哈利法塔",
      subtitle: "世界最高建筑的垂直交通解决方案",
      location: "阿联酋迪拜",
      height: "828米",
      floors: "163层",
      elevators: "57部电梯 + 8部自动扶梯",
      description: "世界最高建筑采用了最先进的电梯技术，包括世界上行程最长的电梯系统。",
      features: [
        "电梯速度达18米/秒，是世界最快的电梯之一",
        "配备双层轿厢系统，提高运输效率",
        "采用先进的目的层控制系统(DCS)",
        "配备气压调节系统，确保乘客舒适性",
        "24/7智能监控和预测性维护系统"
      ],
      image: "/images/burj-khalifa.jpg",
      year: "2010年",
      architect: "SOM建筑设计事务所",
      client: "Emaar地产"
    },
    {
      id: 2,
      title: "上海中心大厦",
      subtitle: "中国第一高楼的创新电梯系统",
      location: "中国上海",
      height: "632米",
      floors: "128层",
      elevators: "149部电梯",
      description: "中国最高建筑采用了多项电梯技术创新，包括世界最快的超高速电梯。",
      features: [
        "观光电梯速度达20.5米/秒，创世界纪录",
        "采用磁悬浮导靴技术，减少噪音和振动",
        "配备三菱超高速电梯系统",
        "智能群控系统优化交通流量",
        "绿色节能技术，配备能量回收系统"
      ],
      image: "/images/shanghai-tower.jpg",
      year: "2015年",
      architect: "Gensler建筑设计",
      client: "上海中心大厦建设发展有限公司"
    },
    {
      id: 3,
      title: "纽约世贸中心一号楼",
      subtitle: "安全与效率并重的电梯设计",
      location: "美国纽约",
      height: "541米",
      floors: "104层",
      elevators: "73部电梯",
      description: "重建的世贸中心一号楼在安全性和技术创新方面树立了新标准。",
      features: [
        "5部快速电梯速度达10.16米/秒",
        "采用ThyssenKrupp先进导轨系统",
        "配备压力平衡系统防止耳鸣",
        "增强的安全系统和应急疏散功能",
        "47秒内从地面到达102层观景台"
      ],
      image: "/images/one-world-trade.jpg",
      year: "2014年",
      architect: "SOM建筑设计事务所",
      client: "港务局"
    },
    {
      id: 4,
      title: "台北101大厦",
      subtitle: "亚洲地标的高速电梯系统",
      location: "中国台湾",
      height: "508米",
      floors: "101层",
      elevators: "61部电梯",
      description: "曾经的世界第一高楼，拥有当时世界最快的电梯系统。",
      features: [
        "观景电梯速度达16.83米/秒",
        "东芝制造的超高速电梯系统",
        "采用双层轿厢设计提高效率",
        "先进的阻尼系统抵抗台风影响",
        "37秒内到达89层观景台"
      ],
      image: "/images/taipei-101.jpg",
      year: "2004年",
      architect: "C.Y. Lee建筑师事务所",
      client: "台北金融大楼"
    },
    {
      id: 5,
      title: "伦敦碎片大厦",
      subtitle: "欧洲最高建筑的电梯创新",
      location: "英国伦敦",
      height: "310米",
      floors: "87层",
      elevators: "36部电梯",
      description: "西欧最高建筑采用了多项电梯技术创新和可持续发展解决方案。",
      features: [
        "KONE超高速电梯，速度达6米/秒",
        "采用KONE目的层控制系统",
        "节能电梯技术，配备再生制动系统",
        "智能交通管理系统",
        "为残障人士优化的无障碍设计"
      ],
      image: "/images/shard-london.jpg",
      year: "2012年",
      architect: "Renzo Piano建筑工作室",
      client: "Sellar地产集团"
    },
    {
      id: 6,
      title: "新加坡滨海湾金沙",
      subtitle: "复合功能建筑的智能电梯系统",
      location: "新加坡",
      height: "200米",
      floors: "55层",
      elevators: "156部电梯",
      description: "集酒店、购物中心、赌场于一体的综合建筑，采用了先进的电梯调度系统。",
      features: [
        "KONE UltraRope碳纤维绳索技术",
        "智能群控系统管理复杂交通流量",
        "节能型电梯系统",
        "为不同功能区域定制的电梯解决方案",
        "24/7预测性维护系统"
      ],
      image: "/images/marina-bay-sands.jpg",
      year: "2010年",
      architect: "Moshe Safdie",
      client: "拉斯维加斯金沙集团"
    }
  ];

  return (
    <div className="knowledge-hub">
      <div className="knowledge-hero">
        <div className="hero-content">
          <h1>
            <Globe className="hero-icon" />
            国际电梯知识中心
          </h1>
          <p>探索全球电梯行业最新技术、创新案例和工程奇迹</p>
        </div>
      </div>

      <div className="knowledge-tabs">
        <button 
          className={`tab-button ${activeTab === 'news' ? 'active' : ''}`}
          onClick={() => setActiveTab('news')}
        >
          <Calendar size={20} />
          新闻故事
        </button>
        <button 
          className={`tab-button ${activeTab === 'projects' ? 'active' : ''}`}
          onClick={() => setActiveTab('projects')}
        >
          <Building size={20} />
          样板工程
        </button>
      </div>

      {activeTab === 'news' && (
        <div className="news-section">
          <div className="section-header">
            <h2>全球电梯行业新闻与创新故事</h2>
            <p>了解最新的电梯技术突破、智能化应用和行业发展趋势</p>
          </div>
          
          <div className="news-grid">
            {newsStories.map((story) => (
              <div key={story.id} className="news-card">
                <div className="news-header">
                  <span className="news-category">{story.category}</span>
                  <span className="news-date">{story.date}</span>
                </div>
                <h3 className="news-title">{story.title}</h3>
                <p className="news-summary">{story.summary}</p>
                <div className="news-content">
                  <p>{story.content}</p>
                </div>
                <div className="news-footer">
                  <button className="read-more-btn">
                    阅读全文 <ArrowRight size={16} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'projects' && (
        <div className="projects-section">
          <div className="section-header">
            <h2>世界著名建筑电梯工程案例</h2>
            <p>探索全球标志性建筑中的电梯技术应用和工程创新</p>
          </div>
          
          <div className="projects-grid">
            {projectCases.map((project) => (
              <div key={project.id} className="project-card">
                <div className="project-image">
                  <div className="image-placeholder">
                    <Building size={60} />
                  </div>
                  <div className="project-year">{project.year}</div>
                </div>
                
                <div className="project-content">
                  <div className="project-header">
                    <h3 className="project-title">{project.title}</h3>
                    <p className="project-subtitle">{project.subtitle}</p>
                  </div>

                  <div className="project-stats">
                    <div className="stat-item">
                      <MapPin size={16} />
                      <span>{project.location}</span>
                    </div>
                    <div className="stat-item">
                      <Building size={16} />
                      <span>{project.height} | {project.floors}</span>
                    </div>
                    <div className="stat-item">
                      <Zap size={16} />
                      <span>{project.elevators}</span>
                    </div>
                  </div>

                  <p className="project-description">{project.description}</p>

                  <div className="project-features">
                    <h4>技术特点：</h4>
                    <ul>
                      {project.features.map((feature, index) => (
                        <li key={index}>{feature}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="project-meta">
                    <div className="meta-item">
                      <strong>建筑师：</strong> {project.architect}
                    </div>
                    <div className="meta-item">
                      <strong>业主：</strong> {project.client}
                    </div>
                  </div>

                  <button className="project-detail-btn">
                    查看详细案例 <ExternalLink size={16} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="knowledge-footer">
        <div className="footer-content">
          <h3>持续更新的知识库</h3>
          <p>我们定期更新全球电梯行业的最新资讯、技术突破和工程案例，为您提供最前沿的行业洞察。</p>
          <div className="update-schedule">
            <div className="schedule-item">
              <Calendar size={20} />
              <span>新闻故事：每周更新2篇</span>
            </div>
            <div className="schedule-item">
              <Building size={20} />
              <span>样板工程：每月新增1个案例</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default KnowledgeHub; 