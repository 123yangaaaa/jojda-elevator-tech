using Microsoft.EntityFrameworkCore;
using JojdaElevator.API.Data;
using JojdaElevator.API.Services;
using JojdaElevator.API.Profiles;
using System.Text.Json.Serialization;

// 加载 .env 文件
DotNetEnv.Env.Load();

var builder = WebApplication.CreateBuilder(args);

// 添加服务到容器
builder.Services.AddControllers()
    .AddJsonOptions(options =>
    {
        options.JsonSerializerOptions.Converters.Add(new JsonStringEnumConverter());
        options.JsonSerializerOptions.PropertyNamingPolicy = null; // 保持原始属性名
    });

// 数据库配置 - 从环境变量读取
var dbHost = Environment.GetEnvironmentVariable("DB_HOST") ?? "localhost";
var dbUser = Environment.GetEnvironmentVariable("DB_USER") ?? "root";
var dbPassword = Environment.GetEnvironmentVariable("DB_PASSWORD") ?? "";
var dbName = Environment.GetEnvironmentVariable("DB_NAME") ?? "jojda_elevator";
var dbPort = Environment.GetEnvironmentVariable("DB_PORT") ?? "3306";

var connectionString = $"Server={dbHost};Port={dbPort};Database={dbName};User={dbUser};Password={dbPassword};";

builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseMySql(connectionString, ServerVersion.AutoDetect(connectionString)));

// AutoMapper 配置
builder.Services.AddAutoMapper(typeof(MappingProfile));

// 注册服务
builder.Services.AddScoped<IElevatorRequirementService, ElevatorRequirementService>();
builder.Services.AddScoped<IMaintenanceRequestService, MaintenanceRequestService>();

// Swagger/OpenAPI 配置
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new Microsoft.OpenApi.Models.OpenApiInfo
    {
        Title = "joj达电梯科技 API",
        Version = "v1",
        Description = "joj达电梯科技有限公司后端API服务",
        Contact = new Microsoft.OpenApi.Models.OpenApiContact
        {
            Name = "joj达电梯科技",
            Email = "info@jojda.com",
            Url = new Uri("https://www.jojda.com")
        }
    });

    // 包含XML注释
    var xmlFile = $"{System.Reflection.Assembly.GetExecutingAssembly().GetName().Name}.xml";
    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    if (File.Exists(xmlPath))
    {
        c.IncludeXmlComments(xmlPath);
    }
});

// CORS 配置
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowReactApp", policy =>
    {
        policy.WithOrigins("http://localhost:3000", "http://localhost:3001")
              .AllowAnyHeader()
              .AllowAnyMethod()
              .AllowCredentials()
              .SetIsOriginAllowed(origin => true); // 允许所有来源（开发环境）
    });
});

// 日志配置
builder.Logging.ClearProviders();
builder.Logging.AddConsole();
builder.Logging.AddDebug();

var app = builder.Build();

// 配置HTTP请求管道
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "joj达电梯科技 API v1");
        c.RoutePrefix = string.Empty; // 设置Swagger UI为根路径
    });
}

// 移除 HTTPS 重定向以避免端口问题
// app.UseHttpsRedirection();

app.UseCors("AllowReactApp");

app.UseAuthorization();

app.MapControllers();

// 根路径
app.MapGet("/", () => new
{
    message = "joj达电梯科技 API 服务器运行中",
    version = "1.0.0",
    timestamp = DateTime.UtcNow,
    environment = app.Environment.EnvironmentName,
    databaseConfig = new
    {
        host = dbHost,
        database = dbName,
        user = dbUser,
        passwordSet = !string.IsNullOrEmpty(dbPassword)
    }
});

// 健康检查
app.MapGet("/health", () => new
{
    status = "健康",
    timestamp = DateTime.UtcNow
});

// 数据库迁移和初始化
using (var scope = app.Services.CreateScope())
{
    try
    {
        var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
        
        // 测试数据库连接
        if (await context.Database.CanConnectAsync())
        {
            await context.Database.EnsureCreatedAsync();
            
            // 手动创建maintenance_requests表（如果不存在）
            var createMaintenanceTableSql = @"
                CREATE TABLE IF NOT EXISTS `maintenance_requests` (
                  `id` int NOT NULL AUTO_INCREMENT,
                  `customer_name` varchar(100) NOT NULL,
                  `contact_phone` varchar(50) NOT NULL,
                  `contact_email` varchar(100) DEFAULT NULL,
                  `elevator_location` varchar(500) NOT NULL,
                  `elevator_type` varchar(100) DEFAULT NULL,
                  `maintenance_type` varchar(50) NOT NULL,
                  `urgency_level` varchar(50) NOT NULL,
                  `description` varchar(1000) DEFAULT NULL,
                  `preferred_time` varchar(50) DEFAULT NULL,
                  `status` varchar(50) NOT NULL DEFAULT 'Pending',
                  `technician_notes` text,
                  `scheduled_time` datetime DEFAULT NULL,
                  `completed_time` datetime DEFAULT NULL,
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                  PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;";
            
            await context.Database.ExecuteSqlRawAsync(createMaintenanceTableSql);
            
            var logger = scope.ServiceProvider.GetRequiredService<ILogger<Program>>();
            logger.LogInformation("数据库连接成功，表结构已确保创建");
        }
        else
        {
            var logger = scope.ServiceProvider.GetRequiredService<ILogger<Program>>();
            logger.LogWarning("数据库连接失败，但服务将继续运行。请检查数据库配置。");
        }
    }
    catch (Exception ex)
    {
        var logger = scope.ServiceProvider.GetRequiredService<ILogger<Program>>();
        logger.LogError(ex, "数据库初始化失败，但服务将继续运行。请检查数据库配置。");
    }
}

app.Run(); 