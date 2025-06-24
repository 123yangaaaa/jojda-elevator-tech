# joj达电梯科技 .NET API

## 项目介绍

这是 joj达电梯科技有限公司的后端 API 服务，使用 ASP.NET Core 8.0 和 Entity Framework Core 构建。

## 技术栈

- **框架**: ASP.NET Core 8.0 Web API
- **数据库**: MySQL 8.0+
- **ORM**: Entity Framework Core
- **文档**: Swagger/OpenAPI
- **映射**: AutoMapper
- **验证**: FluentValidation
- **日志**: Microsoft.Extensions.Logging

## 项目结构

```
JojdaElevator.API/
├── Controllers/           # API 控制器
├── Models/               # 数据模型
├── DTOs/                 # 数据传输对象
├── Services/             # 业务逻辑服务
├── Data/                 # 数据访问层
├── Profiles/             # AutoMapper 配置
├── Program.cs            # 应用程序入口
├── appsettings.json      # 配置文件
└── JojdaElevator.API.csproj
```

## 功能特性

### ✅ 已实现功能

- **电梯采购需求管理**
  - 创建采购需求
  - 查询需求列表
  - 查询需求详情
  - 更新需求状态
  - 删除需求
  - 按状态筛选

- **数据验证**
  - 输入数据验证
  - 业务规则验证
  - 错误信息本地化

- **API 文档**
  - Swagger UI 自动生成
  - 完整的 API 文档

- **跨域支持**
  - 支持前端 React 应用访问

## 安装和运行

### 前置要求

- .NET 8.0 SDK
- MySQL 8.0+
- Visual Studio 2022 或 VS Code

### 1. 克隆项目

```bash
git clone <repository-url>
cd server-dotnet/JojdaElevator.API
```

### 2. 配置数据库

修改 `appsettings.json` 中的数据库连接字符串：

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=jojda_elevator;User=root;Password=your_password;"
  }
}
```

### 3. 安装依赖

```bash
dotnet restore
```

### 4. 运行应用

```bash
dotnet run
```

应用将在以下地址启动：
- API: https://localhost:7000
- Swagger UI: https://localhost:7000

## API 端点

### 电梯采购需求

| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/api/elevatorrequirements` | 创建采购需求 |
| GET | `/api/elevatorrequirements` | 获取所有需求 |
| GET | `/api/elevatorrequirements/{id}` | 获取需求详情 |
| PUT | `/api/elevatorrequirements/{id}/status` | 更新需求状态 |
| DELETE | `/api/elevatorrequirements/{id}` | 删除需求 |
| GET | `/api/elevatorrequirements/status/{status}` | 按状态获取需求 |

### 系统端点

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/` | 服务器状态 |
| GET | `/health` | 健康检查 |
| GET | `/api/elevatorrequirements/test-db` | 数据库连接测试 |

## 数据模型

### 电梯采购需求 (ElevatorRequirement)

```csharp
public class ElevatorRequirement
{
    public int Id { get; set; }
    public string ContactName { get; set; }        // 联系人姓名
    public string ContactPhone { get; set; }       // 联系电话
    public string? ContactEmail { get; set; }      // 联系邮箱
    public string? CompanyName { get; set; }       // 公司名称
    public string? ProjectName { get; set; }       // 项目名称
    public string? ProjectAddress { get; set; }    // 项目地址
    public ElevatorType ElevatorType { get; set; } // 电梯类型
    public int Quantity { get; set; }              // 数量
    public int Floors { get; set; }                // 楼层数
    // ... 其他技术参数
    public RequirementStatus Status { get; set; }  // 状态
    public DateTime CreatedAt { get; set; }        // 创建时间
    public DateTime UpdatedAt { get; set; }        // 更新时间
}
```

### 枚举类型

```csharp
public enum ElevatorType
{
    Passenger,      // 乘客电梯
    Freight,        // 货梯
    Home,           // 家用电梯
    Escalator,      // 自动扶梯
    MovingWalkway   // 自动人行道
}

public enum RequirementStatus
{
    Pending,    // 待处理
    Reviewing,  // 审核中
    Quoted,     // 已报价
    Accepted,   // 已接受
    Rejected    // 已拒绝
}
```

## 开发指南

### 添加新功能

1. 在 `Models/` 中定义数据模型
2. 在 `DTOs/` 中定义传输对象
3. 在 `Services/` 中实现业务逻辑
4. 在 `Controllers/` 中添加 API 端点
5. 在 `Profiles/` 中配置对象映射

### 数据库迁移

```bash
# 添加迁移
dotnet ef migrations add MigrationName

# 更新数据库
dotnet ef database update
```

## 部署

### Docker 部署

```dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 80

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["JojdaElevator.API.csproj", "."]
RUN dotnet restore
COPY . .
RUN dotnet build -c Release -o /app/build

FROM build AS publish
RUN dotnet publish -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "JojdaElevator.API.dll"]
```

### 生产环境配置

1. 更新 `appsettings.Production.json`
2. 配置 HTTPS 证书
3. 设置环境变量
4. 配置反向代理 (Nginx/IIS)

## 与 JavaScript 版本的对比

### 优势

- **类型安全**: 编译时类型检查，减少运行时错误
- **性能**: 更好的性能和内存管理
- **工具支持**: 强大的 IDE 支持和调试工具
- **企业级**: 成熟的企业级开发框架
- **文档**: 自动生成的 API 文档

### 迁移指南

前端只需要更新 API 端点地址：

```javascript
// 原来的 JavaScript 版本
const response = await fetch('http://localhost:5000/api/requirements', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(formData)
});

// 新的 .NET 版本
const response = await fetch('https://localhost:7000/api/elevatorrequirements', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(formData)
});
```

## 许可证

MIT License

## 联系方式

- 公司: joj达电梯科技有限公司
- 邮箱: info@jojda.com
- 网站: https://www.jojda.com 