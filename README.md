# 🏢 joj达电梯科技有限公司官方网站

<div align="center">

![joj达电梯](public/logo.png)

**数智腾飞 引领未来**

[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org/)
[![.NET](https://img.shields.io/badge/.NET-8.0-purple.svg)](https://dotnet.microsoft.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[在线演示](https://ailingjing.cn) | [部署文档](deployment/README.md) | [API文档](#api-接口)

</div>

## 📋 项目简介

joj达电梯科技有限公司官方网站，提供安全、可靠、智能的垂直交通解决方案。本项目采用现代化全栈技术架构，包含React前端、.NET后端API和MySQL数据库。

### ✨ 主要特性

- 🎨 **现代化UI设计** - 响应式界面，支持移动端
- 🚀 **高性能优化** - 代码分割、懒加载、缓存策略
- 📱 **移动端适配** - 完美支持各种屏幕尺寸
- 🔒 **安全可靠** - 数据加密、XSS防护、CSRF保护
- 📊 **智能分析** - AI需求分析、智能推荐系统
- 🛠️ **易于维护** - 模块化架构、详细文档

## 🏗️ 项目结构

```
rxg/
├── public/                    # 静态资源
│   ├── drawings/             # 电梯技术图纸 (34个PDF文件)
│   ├── index.html            # 入口HTML
│   └── logo.png              # 公司Logo
├── src/                      # React前端源码
│   ├── components/           # 可复用组件
│   │   ├── ElevatorProductDrawings.js  # 电梯产品图组件
│   │   ├── Footer.js         # 页脚组件
│   │   └── Header.js         # 页头组件
│   ├── pages/                # 页面组件
│   │   ├── HomePage.js       # 首页
│   │   ├── ElevatorDrawings.js      # 电梯图纸下载页
│   │   ├── KnowledgeHub.js   # 知识中心
│   │   ├── ElevatorRequirement.js  # 需求提交
│   │   ├── MaintenanceService.js   # 维护服务
│   │   ├── ComplaintChannel.js     # 投诉渠道
│   │   └── Contact.js        # 联系我们
│   ├── services/             # API服务层
│   │   └── api.js            # API调用封装
│   ├── App.js                # 主应用组件
│   └── index.js              # 应用入口
├── server-dotnet/            # .NET后端API
│   ├── JojdaElevator.API/    # API项目
│   │   ├── Controllers/      # 控制器
│   │   ├── Models/           # 数据模型
│   │   ├── Services/         # 业务服务
│   │   ├── DTOs/             # 数据传输对象
│   │   └── Data/             # 数据访问层
│   └── README.md             # 后端说明文档
├── deployment/               # 部署配置
│   ├── nginx.conf            # Nginx配置
│   ├── deploy.sh             # 部署脚本
│   ├── Dockerfile            # Docker配置
│   ├── docker-compose.yml    # Docker Compose
│   └── README.md             # 部署文档
├── package.json              # 前端依赖配置
├── quick-deploy.bat          # Windows快速部署
└── README.md                 # 项目说明
```

## 🛠️ 技术栈

### 前端技术
- **React 18.2** - 现代化前端框架
- **React Router 6** - 客户端路由
- **Lucide React** - 现代图标库
- **CSS3** - 响应式样式设计
- **Webpack** - 模块打包工具

### 后端技术
- **.NET 8.0** - 高性能后端框架
- **ASP.NET Core** - Web API框架
- **Entity Framework Core** - ORM框架
- **AutoMapper** - 对象映射
- **MySQL 8.0** - 关系型数据库

### 部署运维
- **Nginx** - 反向代理和静态文件服务
- **Docker** - 容器化部署
- **Let's Encrypt** - SSL证书
- **PM2** - 进程管理（可选）

## 🚀 快速开始

### 环境要求
- **Node.js** 18.0+
- **.NET SDK** 8.0+
- **MySQL** 8.0+
- **Git** 2.0+

### 1. 克隆项目

```bash
git clone https://github.com/your-username/jojda-elevator-tech.git
cd jojda-elevator-tech
```

### 2. 前端启动

```bash
# 安装前端依赖
npm install

# 启动开发服务器
npm start
```

前端将在 `http://localhost:3000` 启动 🎉

### 3. 后端启动

```bash
# 进入后端目录
cd server-dotnet/JojdaElevator.API

# 恢复依赖
dotnet restore

# 启动后端服务
dotnet run
```

后端API将在 `http://localhost:5000` 启动 🚀

### 4. 数据库配置

#### 安装MySQL
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server

# Windows
# 下载并安装MySQL: https://dev.mysql.com/downloads/mysql/

# macOS (使用Homebrew)
brew install mysql
```

#### 创建数据库
```sql
CREATE DATABASE JojdaElevatorDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'jojda_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON JojdaElevatorDB.* TO 'jojda_user'@'localhost';
FLUSH PRIVILEGES;
```

#### 配置连接字符串
在 `server-dotnet/JojdaElevator.API/appsettings.json` 中配置：

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=JojdaElevatorDB;User=jojda_user;Password=your_password;"
  }
}
```

## 🎯 核心功能

### 🏠 前端功能
- ✅ **响应式首页** - 现代化设计，移动端完美适配
- ✅ **电梯产品图下载** - 34个技术图纸，支持规格筛选
- ✅ **智能需求分析** - AI驱动的电梯方案推荐
- ✅ **维护服务管理** - 在线报修，状态跟踪
- ✅ **知识中心** - 行业资讯，技术文档
- ✅ **投诉渠道** - 多渠道客户反馈
- ✅ **联系我们** - 完整的联系信息和在线表单

### 🔧 后端功能
- ✅ **RESTful API** - 标准化接口设计
- ✅ **数据持久化** - MySQL数据存储
- ✅ **业务逻辑层** - 清晰的架构分层
- ✅ **数据传输对象** - DTO模式，安全传输
- ✅ **自动映射** - AutoMapper对象转换
- ✅ **健康检查** - 系统状态监控

### 📱 特色功能详解

#### 电梯产品图下载系统
- **规格筛选**：载重(630kg-1050kg)、速度(1-2.5m/s)、宽度(1100-1600mm)
- **智能推荐**：根据选择提供推荐方案
- **一键下载**：高清PDF技术图纸下载
- **响应式设计**：支持各种设备访问

#### 智能需求分析系统
- **AI驱动**：智能分析用户需求
- **个性化推荐**：基于建筑类型和使用场景
- **实时成本估算**：透明的价格预估
- **专家响应**：24小时内专业回复

#### 维护服务管理
- **在线报修**：便捷的故障报告
- **状态跟踪**：实时维修进度
- **历史记录**：完整的服务档案
- **评价系统**：服务质量反馈

## 📡 API 接口

### 电梯需求管理
```http
GET    /api/ElevatorRequirements     # 获取需求列表
POST   /api/ElevatorRequirements     # 创建新需求
GET    /api/ElevatorRequirements/{id} # 获取需求详情
PUT    /api/ElevatorRequirements/{id} # 更新需求
DELETE /api/ElevatorRequirements/{id} # 删除需求
```

### 维护请求管理
```http
GET    /api/MaintenanceRequests      # 获取维护请求列表
POST   /api/MaintenanceRequests      # 创建维护请求
GET    /api/MaintenanceRequests/{id} # 获取请求详情
PUT    /api/MaintenanceRequests/{id} # 更新请求状态
GET    /api/MaintenanceRequests/search/{phone} # 按电话搜索
```

### 请求示例

#### 创建电梯需求
```bash
curl -X POST "http://localhost:5000/api/ElevatorRequirements" \
  -H "Content-Type: application/json" \
  -d '{
    "buildingType": "商业建筑",
    "floors": 20,
    "capacity": 1000,
    "speed": 2.0,
    "customerName": "张先生",
    "contactPhone": "13800138000",
    "projectAddress": "上海市浦东新区"
  }'
```

#### 创建维护请求
```bash
curl -X POST "http://localhost:5000/api/MaintenanceRequests" \
  -H "Content-Type: application/json" \
  -d '{
    "customerName": "李女士",
    "phoneNumber": "13900139000",
    "elevatorLocation": "办公楼A座3号电梯",
    "maintenanceType": "Emergency",
    "urgencyLevel": "High",
    "problemDescription": "电梯突然停止运行"
  }'
```

## 🚀 部署指南

### 一键部署到生产环境

#### 方法一：自动脚本部署（推荐）
```bash
# 1. 配置环境变量
cp deployment/env.example deployment/.env
# 编辑 .env 文件设置服务器信息

# 2. 执行部署
chmod +x deployment/deploy.sh
./deployment/deploy.sh
```

#### 方法二：Docker容器化部署
```bash
# 1. 构建镜像
docker build -f deployment/Dockerfile -t jojda-elevator:latest .

# 2. 启动服务栈
cd deployment
docker-compose up -d
```

#### 方法三：Windows快速部署
```cmd
# 双击运行
quick-deploy.bat
```

### 部署到 ailingjing.cn 域名

详细的部署文档请查看：[deployment/README.md](deployment/README.md)

主要步骤：
1. **服务器准备** - Ubuntu 20.04+, 2GB RAM
2. **域名配置** - DNS解析到服务器IP
3. **SSL证书** - Let's Encrypt免费证书
4. **一键部署** - 运行自动化脚本

## 🎨 项目预览

### 🏠 首页
- 现代化设计风格
- 响应式布局
- 动画交互效果

### 📱 电梯产品图页面
- 三级筛选系统
- 34个PDF技术图纸
- 智能推荐功能

### 🔧 维护服务页面
- 在线报修表单
- 状态跟踪系统
- 历史记录查询

### 📞 联系我们页面
- 完整联系信息
- 在线咨询表单
- 地图位置展示

## 🔧 开发指南

### 前端开发
```bash
# 启动开发服务器
npm start

# 构建生产版本
npm run build

# 运行测试
npm test

# 代码检查
npm run lint
```

### 后端开发
```bash
# 启动开发服务器
dotnet run

# 构建发布版本
dotnet build --configuration Release

# 运行测试
dotnet test

# 数据库迁移
dotnet ef database update
```

### 代码规范
- **前端**：使用ESLint + Prettier
- **后端**：遵循.NET编码规范
- **提交**：使用Conventional Commits规范

## 📊 数据库设计

### 核心表结构

#### elevator_requirements - 电梯需求
```sql
CREATE TABLE elevator_requirements (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    BuildingType NVARCHAR(100),
    Floors INT,
    Capacity INT,
    Speed DECIMAL(3,1),
    CustomerName NVARCHAR(100),
    ContactPhone NVARCHAR(20),
    ProjectAddress NVARCHAR(500),
    CreatedAt DATETIME,
    UpdatedAt DATETIME
);
```

#### maintenance_requests - 维护请求
```sql
CREATE TABLE maintenance_requests (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    CustomerName NVARCHAR(100),
    PhoneNumber NVARCHAR(20),
    ElevatorLocation NVARCHAR(200),
    MaintenanceType ENUM('Routine', 'Emergency', 'Inspection'),
    UrgencyLevel ENUM('Low', 'Medium', 'High', 'Critical'),
    ProblemDescription TEXT,
    Status ENUM('Pending', 'InProgress', 'Completed', 'Cancelled'),
    CreatedAt DATETIME,
    UpdatedAt DATETIME
);
```

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 贡献方式
1. **报告Bug** - 提交Issue描述问题
2. **功能建议** - 提出新功能想法
3. **代码贡献** - 提交Pull Request
4. **文档改进** - 完善项目文档

### 开发流程
1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 许可证

本项目基于 MIT 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系我们

- **公司**: joj达电梯科技有限公司
- **网站**: [https://ailingjing.cn](https://ailingjing.cn)
- **邮箱**: 605490648@qq.com
- **电话**: 18262591815
- **地址**: 北京市朝阳区科技园区 joj达电梯科技大厦

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给我们一个星标！**

Made with ❤️ by joj达电梯科技团队

</div>
