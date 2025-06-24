import React, { useState, useEffect } from 'react';
import { Download, Search, Filter, FileText } from 'lucide-react';
import './ElevatorDrawings.css';

const ElevatorDrawings = () => {
  const [selectedWeight, setSelectedWeight] = useState('');
  const [selectedSpeed, setSelectedSpeed] = useState('');
  const [selectedWidth, setSelectedWidth] = useState('');
  const [filteredDrawings, setFilteredDrawings] = useState([]);
  const [allDrawings] = useState([
    // 630kg系列
    { weight: '630kg', speed: '1m每秒', width: '1100mm', file: '载重630kg-速度1m每秒-轿厢宽度1100mm.pdf' },
    { weight: '630kg', speed: '1.5m每秒', width: '1100mm', file: '载重630kg-速度1.5m每秒-轿厢宽度1100mm.pdf' },
    { weight: '630kg', speed: '1m每秒', width: '1400mm', file: '载重630kg-速度1m每秒-轿厢宽度1400mm.pdf' },
    { weight: '630kg', speed: '1.75m每秒', width: '1400mm', file: '载重630kg-速度1.75m每秒-轿厢宽度1400mm.pdf' },
    
    // 800kg系列
    { weight: '800kg', speed: '1m每秒', width: '1400mm', file: '载重800kg-速度1m每秒-轿厢宽度1400mm.pdf' },
    { weight: '800kg', speed: '1.5m每秒', width: '1400mm', file: '载重800kg-速度1.5m每秒-轿厢宽度1400mm.pdf' },
    { weight: '800kg', speed: '1.75m每秒', width: '1400mm', file: '载重800kg-速度1.75m每秒-轿厢宽度1400mm.pdf' },
    { weight: '800kg', speed: '2m每秒', width: '1400mm', file: '载重800kg-速度2m每秒-轿厢宽度1400mm.pdf' },
    { weight: '800kg', speed: '2.5m每秒', width: '1400mm', file: '载重800kg-速度2.5m每秒-轿厢宽度1400mm.pdf' },
    
    // 900kg系列
    { weight: '900kg', speed: '1m每秒', width: '1500mm', file: '载重900kg-速度1m每秒-轿厢宽度1500mm.pdf' },
    { weight: '900kg', speed: '1.5m每秒', width: '1500mm', file: '载重900kg-速度1.5m每秒-轿厢宽度1500mm.pdf' },
    { weight: '900kg', speed: '1.75m每秒', width: '1500mm', file: '载重900kg-速度1.75m每秒-轿厢宽度1500mm.pdf' },
    { weight: '900kg', speed: '2m每秒', width: '1500mm', file: '载重900kg-速度2m每秒-轿厢宽度1500mm.pdf' },
    { weight: '900kg', speed: '2.5m每秒', width: '1500mm', file: '载重900kg-速度2.5m每秒-轿厢宽度1500mm.pdf' },
    
    // 1000kg系列
    { weight: '1000kg', speed: '1m每秒', width: '1100mm', file: '载重1000kg-速度1m每秒-轿厢宽度1100mm.pdf' },
    { weight: '1000kg', speed: '1.5m每秒', width: '1100mm', file: '载重1000kg-速度1.5m每秒-轿厢宽度1100mm.pdf' },
    { weight: '1000kg', speed: '1.75m每秒', width: '1100mm', file: '载重1000kg-速度1.75m每秒-轿厢宽度1100mm.pdf' },
    { weight: '1000kg', speed: '2m每秒', width: '1100mm', file: '载重1000kg-速度2m每秒-轿厢宽度1100mm.pdf' },
    { weight: '1000kg', speed: '2.5m每秒', width: '1100mm', file: '载重1000kg-速度2.5m每秒-轿厢宽度1100mm.pdf' },
    { weight: '1000kg', speed: '1m每秒', width: '1600mm', file: '载重1000kg-速度1m每秒-轿厢宽度1600mm.pdf' },
    { weight: '1000kg', speed: '1.5m每秒', width: '1600mm', file: '载重1000kg-速度1.5m每秒-轿厢宽度1600mm.pdf' },
    { weight: '1000kg', speed: '1.75m每秒', width: '1600mm', file: '载重1000kg-速度1.75m每秒-轿厢宽度1600mm.pdf' },
    { weight: '1000kg', speed: '2m每秒', width: '1600mm', file: '载重1000kg-速度2m每秒-轿厢宽度1600mm.pdf' },
    { weight: '1000kg', speed: '2.5m每秒', width: '1600mm', file: '载重1000kg-速度2.5m每秒-轿厢宽度1600mm.pdf' },
    
    // 1050kg系列
    { weight: '1050kg', speed: '1m每秒', width: '1100mm', file: '载重1050kg-速度1m每秒-轿厢宽度1100mm.pdf' },
    { weight: '1050kg', speed: '1.5m每秒', width: '1100mm', file: '载重1050kg-速度1.5m每秒-轿厢宽度1100mm.pdf' },
    { weight: '1050kg', speed: '1.75m每秒', width: '1100mm', file: '载重1050kg-速度1.75m每秒-轿厢宽度1100mm.pdf' },
    { weight: '1050kg', speed: '2m每秒', width: '1100mm', file: '载重1050kg-速度2m每秒-轿厢宽度1100mm.pdf' },
    { weight: '1050kg', speed: '2.5m每秒', width: '1100mm', file: '载重1050kg-速度2.5m每秒-轿厢宽度1100mm.pdf' },
    { weight: '1050kg', speed: '1m每秒', width: '1600mm', file: '载重1050kg-速度1m每秒-轿厢宽度1600mm.pdf' },
    { weight: '1050kg', speed: '1.5m每秒', width: '1600mm', file: '载重1050kg-速度1.5m每秒-轿厢宽度1600mm.pdf' },
    { weight: '1050kg', speed: '1.75m每秒', width: '1600mm', file: '载重1050kg-速度1.75m每秒-轿厢宽度1600mm.pdf' },
    { weight: '1050kg', speed: '2m每秒', width: '1600mm', file: '载重1050kg-速度2m每秒-轿厢宽度1600mm.pdf' },
    { weight: '1050kg', speed: '2.5m每秒', width: '1600mm', file: '载重1050kg-速度2.5m每秒-轿厢宽度1600mm.pdf' }
  ]);

  // 获取唯一的选项值
  const weightOptions = [...new Set(allDrawings.map(d => d.weight))].sort();
  const speedOptions = [...new Set(allDrawings.map(d => d.speed))].sort();
  const widthOptions = [...new Set(allDrawings.map(d => d.width))].sort();

  // 筛选图纸
  useEffect(() => {
    let filtered = allDrawings;
    
    if (selectedWeight) {
      filtered = filtered.filter(d => d.weight === selectedWeight);
    }
    if (selectedSpeed) {
      filtered = filtered.filter(d => d.speed === selectedSpeed);
    }
    if (selectedWidth) {
      filtered = filtered.filter(d => d.width === selectedWidth);
    }
    
    setFilteredDrawings(filtered);
  }, [selectedWeight, selectedSpeed, selectedWidth, allDrawings]);

  // 下载PDF
  const handleDownload = (filename) => {
    const link = document.createElement('a');
    link.href = `/drawings/${filename}`;
    link.download = filename;
    link.click();
  };

  // 重置筛选
  const resetFilters = () => {
    setSelectedWeight('');
    setSelectedSpeed('');
    setSelectedWidth('');
  };

  // 智能推荐
  const getRecommendation = () => {
    if (!selectedWeight && !selectedSpeed && !selectedWidth) {
      return "请选择规格参数，我们将为您推荐最适合的产品图纸";
    }
    
    const count = filteredDrawings.length;
    if (count === 0) {
      return "未找到匹配的图纸，请调整筛选条件";
    } else if (count === 1) {
      return "找到1个完全匹配的产品图纸";
    } else {
      return `找到${count}个匹配的产品图纸，建议根据具体使用场景选择`;
    }
  };

  return (
    <div className="elevator-drawings">
      <div className="drawings-hero">
        <div className="hero-content">
          <h1>
            <FileText className="hero-icon" />
            电梯产品技术图纸下载
          </h1>
          <p>根据您的需求选择对应规格，即可下载高清技术图纸</p>
        </div>
      </div>

      <div className="filter-section">
        <div className="filter-header">
          <h2>
            <Filter size={24} />
            规格筛选
          </h2>
          <button onClick={resetFilters} className="reset-btn">
            重置筛选
          </button>
        </div>

        <div className="filter-controls">
          <div className="filter-group">
            <label>载重规格</label>
            <select 
              value={selectedWeight} 
              onChange={(e) => setSelectedWeight(e.target.value)}
              className="filter-select"
            >
              <option value="">请选择载重</option>
              {weightOptions.map(weight => (
                <option key={weight} value={weight}>{weight}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label>运行速度</label>
            <select 
              value={selectedSpeed} 
              onChange={(e) => setSelectedSpeed(e.target.value)}
              className="filter-select"
            >
              <option value="">请选择速度</option>
              {speedOptions.map(speed => (
                <option key={speed} value={speed}>{speed}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label>轿厢宽度</label>
            <select 
              value={selectedWidth} 
              onChange={(e) => setSelectedWidth(e.target.value)}
              className="filter-select"
            >
              <option value="">请选择宽度</option>
              {widthOptions.map(width => (
                <option key={width} value={width}>{width}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="recommendation">
          <div className="recommendation-icon">💡</div>
          <div className="recommendation-text">
            {getRecommendation()}
          </div>
        </div>
      </div>

      <div className="drawings-grid-section">
        <div className="grid-header">
          <h3>
            <Search size={20} />
            图纸列表 ({filteredDrawings.length}个结果)
          </h3>
        </div>

        {filteredDrawings.length === 0 ? (
          <div className="no-results">
            <FileText size={60} />
            <h3>暂无匹配的图纸</h3>
            <p>请调整筛选条件或联系我们获取定制图纸</p>
          </div>
        ) : (
          <div className="drawings-grid">
            {filteredDrawings.map((drawing, index) => (
              <div key={index} className="drawing-card">
                <div className="drawing-preview">
                  <FileText size={40} />
                </div>
                
                <div className="drawing-info">
                  <h4 className="drawing-title">
                    载重{drawing.weight} 电梯技术图纸
                  </h4>
                  
                  <div className="drawing-specs">
                    <div className="spec-item">
                      <span className="spec-label">载重：</span>
                      <span className="spec-value">{drawing.weight}</span>
                    </div>
                    <div className="spec-item">
                      <span className="spec-label">速度：</span>
                      <span className="spec-value">{drawing.speed}</span>
                    </div>
                    <div className="spec-item">
                      <span className="spec-label">宽度：</span>
                      <span className="spec-value">{drawing.width}</span>
                    </div>
                  </div>

                  <div className="drawing-meta">
                    <span className="file-type">PDF格式</span>
                    <span className="file-size">~2.3MB</span>
                  </div>

                  <button 
                    onClick={() => handleDownload(drawing.file)}
                    className="download-btn"
                  >
                    <Download size={16} />
                    下载图纸
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="drawings-footer">
        <div className="footer-content">
          <h3>技术支持</h3>
          <p>如需其他规格的图纸或有技术问题，请联系我们的技术团队</p>
          <div className="contact-info">
            <div className="contact-item">
              <span>📧 技术邮箱：tech@jojdaelevator.com</span>
            </div>
            <div className="contact-item">
              <span>📞 技术热线：400-123-4567</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ElevatorDrawings; 