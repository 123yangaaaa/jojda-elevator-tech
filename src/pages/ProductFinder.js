import React, { useState, useEffect } from 'react';
import './ProductFinder.css';

const ProductFinder = () => {
  const [selectedLoad, setSelectedLoad] = useState('');
  const [selectedSpeed, setSelectedSpeed] = useState('');
  const [selectedWidth, setSelectedWidth] = useState('');
  const [availableFiles, setAvailableFiles] = useState([]);
  const [filteredFiles, setFilteredFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 从文件名解析参数的函数
  const parseFileName = (fileName) => {
    const regex = /载重(\d+)kg-速度([\d.]+)m每秒-轿厢宽度(\d+)mm\.pdf/;
    const match = fileName.match(regex);
    if (match) {
      return {
        load: match[1],
        speed: match[2],
        width: match[3],
        fileName: fileName
      };
    }
    return null;
  };

  // 从服务器获取文件列表
  useEffect(() => {
    const fetchFiles = async () => {
      try {
        setLoading(true);
        const response = await fetch('http://localhost:5000/api/files');
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // 转换服务器返回的数据格式
        const parsedFiles = data.files
          .filter(file => file.specs) // 只保留能解析规格的文件
          .map(file => ({
            load: file.specs.load,
            speed: file.specs.speed,
            width: file.specs.width,
            fileName: file.fileName,
            size: file.size,
            modifiedDate: file.modifiedDate
          }));
          
        setAvailableFiles(parsedFiles);
        setFilteredFiles(parsedFiles);
        setError(null);
      } catch (err) {
        console.error('获取文件列表失败:', err);
        setError('无法加载文件列表，请检查服务器连接');
        
        // 如果服务器不可用，使用之前的硬编码数据作为备选
        const fallbackFileList = [
          '载重630kg-速度1m每秒-轿厢宽度1100mm.pdf',
          '载重630kg-速度1.5m每秒-轿厢宽度1100mm.pdf',
          '载重630kg-速度1m每秒-轿厢宽度1400mm.pdf',
          '载重630kg-速度1.75m每秒-轿厢宽度1400mm.pdf',
          '载重800kg-速度1m每秒-轿厢宽度1400mm.pdf',
          '载重800kg-速度1.5m每秒-轿厢宽度1400mm.pdf',
          '载重800kg-速度1.75m每秒-轿厢宽度1400mm.pdf',
          '载重800kg-速度2m每秒-轿厢宽度1400mm.pdf',
          '载重800kg-速度2.5m每秒-轿厢宽度1400mm.pdf',
          '载重900kg-速度1m每秒-轿厢宽度1500mm.pdf',
          '载重900kg-速度1.5m每秒-轿厢宽度1500mm.pdf',
          '载重900kg-速度1.75m每秒-轿厢宽度1500mm.pdf',
          '载重900kg-速度2m每秒-轿厢宽度1500mm.pdf',
          '载重900kg-速度2.5m每秒-轿厢宽度1500mm.pdf',
          '载重1000kg-速度1m每秒-轿厢宽度1100mm.pdf',
          '载重1000kg-速度1.5m每秒-轿厢宽度1100mm.pdf',
          '载重1000kg-速度1.75m每秒-轿厢宽度1100mm.pdf',
          '载重1000kg-速度2m每秒-轿厢宽度1100mm.pdf',
          '载重1000kg-速度2.5m每秒-轿厢宽度1100mm.pdf',
          '载重1000kg-速度1m每秒-轿厢宽度1600mm.pdf',
          '载重1000kg-速度1.5m每秒-轿厢宽度1600mm.pdf',
          '载重1000kg-速度1.75m每秒-轿厢宽度1600mm.pdf',
          '载重1000kg-速度2m每秒-轿厢宽度1600mm.pdf',
          '载重1000kg-速度2.5m每秒-轿厢宽度1600mm.pdf',
          '载重1050kg-速度1m每秒-轿厢宽度1100mm.pdf',
          '载重1050kg-速度1.5m每秒-轿厢宽度1100mm.pdf',
          '载重1050kg-速度1.75m每秒-轿厢宽度1100mm.pdf',
          '载重1050kg-速度2m每秒-轿厢宽度1100mm.pdf',
          '载重1050kg-速度2.5m每秒-轿厢宽度1100mm.pdf',
          '载重1050kg-速度1m每秒-轿厢宽度1600mm.pdf',
          '载重1050kg-速度1.5m每秒-轿厢宽度1600mm.pdf',
          '载重1050kg-速度1.75m每秒-轿厢宽度1600mm.pdf',
          '载重1050kg-速度2m每秒-轿厢宽度1600mm.pdf',
          '载重1050kg-速度2.5m每秒-轿厢宽度1600mm.pdf'
        ];
        
        const fallbackParsedFiles = fallbackFileList.map(parseFileName).filter(Boolean);
        setAvailableFiles(fallbackParsedFiles);
        setFilteredFiles(fallbackParsedFiles);
      } finally {
        setLoading(false);
      }
    };

    fetchFiles();
  }, []);

  // 过滤文件
  useEffect(() => {
    let filtered = availableFiles;

    if (selectedLoad) {
      filtered = filtered.filter(file => file.load === selectedLoad);
    }
    if (selectedSpeed) {
      filtered = filtered.filter(file => file.speed === selectedSpeed);
    }
    if (selectedWidth) {
      filtered = filtered.filter(file => file.width === selectedWidth);
    }

    setFilteredFiles(filtered);
  }, [selectedLoad, selectedSpeed, selectedWidth, availableFiles]);

  // 获取可选项
  const getUniqueValues = (key) => {
    const values = availableFiles.map(file => file[key]);
    return [...new Set(values)].sort((a, b) => parseFloat(a) - parseFloat(b));
  };

  // 下载文件
  const downloadFile = async (fileName) => {
    try {
      const response = await fetch(`http://localhost:5000/api/download/${encodeURIComponent(fileName)}`);
      
      if (!response.ok) {
        throw new Error(`下载失败: ${response.status}`);
      }

      // 获取文件blob
      const blob = await response.blob();
      
      // 创建下载链接
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = fileName;
      document.body.appendChild(link);
      link.click();
      
      // 清理
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
    } catch (error) {
      console.error('下载文件失败:', error);
      alert('文件下载失败，请稍后重试');
    }
  };

  // 重置所有选择
  const resetFilters = () => {
    setSelectedLoad('');
    setSelectedSpeed('');
    setSelectedWidth('');
  };

  // 格式化文件大小
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  if (loading) {
    return (
      <div className="product-finder">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>正在加载产品资料...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="product-finder">
      <div className="product-finder-header">
        <h1>电梯产品查找器</h1>
        <p>选择您的电梯规格要求，查找并下载相应的技术资料</p>
        {error && (
          <div className="error-notice">
            <p>⚠️ {error}</p>
            <p>当前显示离线数据</p>
          </div>
        )}
      </div>

      <div className="product-finder-content">
        <div className="filter-section">
          <h2>产品规格选择</h2>
          
          <div className="filter-grid">
            <div className="filter-group">
              <label>载重量 (kg)</label>
              <select 
                value={selectedLoad} 
                onChange={(e) => setSelectedLoad(e.target.value)}
                className="filter-select"
              >
                <option value="">选择载重量</option>
                {getUniqueValues('load').map(load => (
                  <option key={load} value={load}>{load}kg</option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <label>运行速度 (m/s)</label>
              <select 
                value={selectedSpeed} 
                onChange={(e) => setSelectedSpeed(e.target.value)}
                className="filter-select"
              >
                <option value="">选择速度</option>
                {getUniqueValues('speed').map(speed => (
                  <option key={speed} value={speed}>{speed}m/s</option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <label>轿厢宽度 (mm)</label>
              <select 
                value={selectedWidth} 
                onChange={(e) => setSelectedWidth(e.target.value)}
                className="filter-select"
              >
                <option value="">选择宽度</option>
                {getUniqueValues('width').map(width => (
                  <option key={width} value={width}>{width}mm</option>
                ))}
              </select>
            </div>
          </div>

          <div className="filter-actions">
            <button onClick={resetFilters} className="reset-btn">
              重置选择
            </button>
            <div className="results-count">
              找到 {filteredFiles.length} 个匹配结果
            </div>
          </div>
        </div>

        <div className="results-section">
          <h2>匹配的产品资料</h2>
          
          {filteredFiles.length === 0 ? (
            <div className="no-results">
              <p>未找到匹配的产品资料</p>
              <p>请调整您的选择条件</p>
            </div>
          ) : (
            <div className="results-grid">
              {filteredFiles.map((file, index) => (
                <div key={index} className="result-card">
                  <div className="result-icon">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14,2 14,8 20,8"/>
                      <line x1="16" y1="13" x2="8" y2="13"/>
                      <line x1="16" y1="17" x2="8" y2="17"/>
                      <polyline points="10,9 9,9 8,9"/>
                    </svg>
                  </div>
                  <div className="result-info">
                    <h3>电梯技术图纸</h3>
                    <div className="result-specs">
                      <span className="spec">载重: {file.load}kg</span>
                      <span className="spec">速度: {file.speed}m/s</span>
                      <span className="spec">宽度: {file.width}mm</span>
                      {file.size && (
                        <span className="spec">大小: {formatFileSize(file.size)}</span>
                      )}
                    </div>
                    <button 
                      onClick={() => downloadFile(file.fileName)}
                      className="download-btn"
                    >
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                        <polyline points="7,10 12,15 17,10"/>
                        <line x1="12" y1="15" x2="12" y2="3"/>
                      </svg>
                      下载PDF
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductFinder; 