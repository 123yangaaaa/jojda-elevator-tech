using Microsoft.EntityFrameworkCore;
using JojdaElevator.API.Models;

namespace JojdaElevator.API.Data;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options)
    {
    }

    public DbSet<ElevatorRequirement> ElevatorRequirements { get; set; }
    public DbSet<MaintenanceRequest> MaintenanceRequests { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // 配置 ElevatorRequirement 实体
        modelBuilder.Entity<ElevatorRequirement>(entity =>
        {
            entity.ToTable("elevator_requirements");

            entity.HasKey(e => e.Id);

            entity.Property(e => e.Id)
                .HasColumnName("id")
                .ValueGeneratedOnAdd();

            entity.Property(e => e.ContactName)
                .HasColumnName("contact_name")
                .HasMaxLength(100)
                .IsRequired();

            entity.Property(e => e.ContactPhone)
                .HasColumnName("contact_phone")
                .HasMaxLength(50)
                .IsRequired();

            entity.Property(e => e.ContactEmail)
                .HasColumnName("contact_email")
                .HasMaxLength(100);

            entity.Property(e => e.CompanyName)
                .HasColumnName("company_name")
                .HasMaxLength(200);

            entity.Property(e => e.ProjectName)
                .HasColumnName("project_name")
                .HasMaxLength(200);

            entity.Property(e => e.ProjectAddress)
                .HasColumnName("project_address")
                .HasMaxLength(500);

            entity.Property(e => e.ElevatorType)
                .HasColumnName("elevator_type")
                .HasConversion<string>()
                .IsRequired();

            entity.Property(e => e.Quantity)
                .HasColumnName("quantity")
                .HasDefaultValue(1)
                .IsRequired();

            entity.Property(e => e.Floors)
                .HasColumnName("floors")
                .IsRequired();

            entity.Property(e => e.FloorHeight)
                .HasColumnName("floor_height")
                .HasColumnType("decimal(5,2)");

            entity.Property(e => e.CarCapacity)
                .HasColumnName("car_capacity");

            entity.Property(e => e.CarSpeed)
                .HasColumnName("car_speed")
                .HasColumnType("decimal(4,2)");

            entity.Property(e => e.HoistwayWidth)
                .HasColumnName("hoistway_width")
                .HasColumnType("decimal(6,2)");

            entity.Property(e => e.HoistwayDepth)
                .HasColumnName("hoistway_depth")
                .HasColumnType("decimal(6,2)");

            entity.Property(e => e.PitDepth)
                .HasColumnName("pit_depth")
                .HasColumnType("decimal(7,2)");

            entity.Property(e => e.OverheadHeight)
                .HasColumnName("overhead_height")
                .HasColumnType("decimal(5,2)");

            entity.Property(e => e.CarWidth)
                .HasColumnName("car_width")
                .HasColumnType("decimal(6,2)");

            entity.Property(e => e.CarDepth)
                .HasColumnName("car_depth")
                .HasColumnType("decimal(6,2)");

            entity.Property(e => e.CarHeight)
                .HasColumnName("car_height")
                .HasColumnType("decimal(5,2)");

            entity.Property(e => e.DoorWidth)
                .HasColumnName("door_width")
                .HasColumnType("decimal(7,2)");

            entity.Property(e => e.DoorHeight)
                .HasColumnName("door_height")
                .HasColumnType("decimal(7,2)");

            entity.Property(e => e.SpecialRequirements)
                .HasColumnName("special_requirements")
                .HasColumnType("text");

            entity.Property(e => e.BudgetRange)
                .HasColumnName("budget_range")
                .HasMaxLength(100);

            entity.Property(e => e.DeliveryTime)
                .HasColumnName("delivery_time")
                .HasMaxLength(100);

            entity.Property(e => e.Status)
                .HasColumnName("status")
                .HasConversion<string>()
                .HasDefaultValue(RequirementStatus.Pending);

            entity.Property(e => e.AdminNotes)
                .HasColumnName("admin_notes")
                .HasColumnType("text");

            entity.Property(e => e.QuoteAmount)
                .HasColumnName("quote_amount")
                .HasColumnType("decimal(12,2)");

            entity.Property(e => e.QuoteDate)
                .HasColumnName("quote_date");

            entity.Property(e => e.CreatedAt)
                .HasColumnName("created_at")
                .HasDefaultValueSql("CURRENT_TIMESTAMP");

            entity.Property(e => e.UpdatedAt)
                .HasColumnName("updated_at")
                .HasDefaultValueSql("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP");

            // 添加索引
            entity.HasIndex(e => e.ContactPhone)
                .HasDatabaseName("idx_contact_phone");

            entity.HasIndex(e => e.ElevatorType)
                .HasDatabaseName("idx_elevator_type");

            entity.HasIndex(e => e.Status)
                .HasDatabaseName("idx_status");

            entity.HasIndex(e => e.CreatedAt)
                .HasDatabaseName("idx_created_at");
        });

        // 配置枚举值
        modelBuilder.Entity<ElevatorRequirement>()
            .Property(e => e.ElevatorType)
            .HasConversion(
                v => v.ToString().ToLower(),
                v => (ElevatorType)Enum.Parse(typeof(ElevatorType), v, true));

        modelBuilder.Entity<ElevatorRequirement>()
            .Property(e => e.Status)
            .HasConversion(
                v => v.ToString().ToLower(),
                v => (RequirementStatus)Enum.Parse(typeof(RequirementStatus), v, true));

        // MaintenanceRequest 配置
        modelBuilder.Entity<MaintenanceRequest>(entity =>
        {
            entity.ToTable("maintenance_requests");

            entity.HasKey(e => e.Id);

            entity.Property(e => e.Id)
                .HasColumnName("id")
                .ValueGeneratedOnAdd();

            entity.Property(e => e.CustomerName)
                .HasColumnName("customer_name")
                .HasMaxLength(100)
                .IsRequired();

            entity.Property(e => e.ContactPhone)
                .HasColumnName("contact_phone")
                .HasMaxLength(50)
                .IsRequired();

            entity.Property(e => e.ContactEmail)
                .HasColumnName("contact_email")
                .HasMaxLength(100);

            entity.Property(e => e.ElevatorLocation)
                .HasColumnName("elevator_location")
                .HasMaxLength(500)
                .IsRequired();

            entity.Property(e => e.ElevatorType)
                .HasColumnName("elevator_type")
                .HasMaxLength(100);

            entity.Property(e => e.MaintenanceType)
                .HasColumnName("maintenance_type")
                .HasConversion<string>()
                .IsRequired();

            entity.Property(e => e.UrgencyLevel)
                .HasColumnName("urgency_level")
                .HasConversion<string>()
                .IsRequired();

            entity.Property(e => e.Description)
                .HasColumnName("description")
                .HasMaxLength(1000);

            entity.Property(e => e.PreferredTime)
                .HasColumnName("preferred_time")
                .HasMaxLength(50);

            entity.Property(e => e.Status)
                .HasColumnName("status")
                .HasConversion<string>()
                .HasDefaultValue(MaintenanceStatus.Pending)
                .IsRequired();

            entity.Property(e => e.TechnicianNotes)
                .HasColumnName("technician_notes")
                .HasColumnType("text");

            entity.Property(e => e.ScheduledTime)
                .HasColumnName("scheduled_time")
                .HasColumnType("datetime");

            entity.Property(e => e.CompletedTime)
                .HasColumnName("completed_time")
                .HasColumnType("datetime");

            entity.Property(e => e.CreatedAt)
                .HasColumnName("created_at")
                .HasColumnType("datetime")
                .HasDefaultValueSql("CURRENT_TIMESTAMP")
                .IsRequired();

            entity.Property(e => e.UpdatedAt)
                .HasColumnName("updated_at")
                .HasColumnType("datetime")
                .HasDefaultValueSql("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
                .IsRequired();
        });
    }
} 