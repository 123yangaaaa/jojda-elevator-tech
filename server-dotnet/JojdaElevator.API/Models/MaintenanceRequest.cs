using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace JojdaElevator.API.Models;

public class MaintenanceRequest
{
    [Key]
    public int Id { get; set; }

    [Required]
    [StringLength(100)]
    public string CustomerName { get; set; } = string.Empty;

    [Required]
    [StringLength(50)]
    [Phone]
    public string ContactPhone { get; set; } = string.Empty;

    [StringLength(100)]
    [EmailAddress]
    public string? ContactEmail { get; set; }

    [Required]
    [StringLength(500)]
    public string ElevatorLocation { get; set; } = string.Empty;

    [StringLength(100)]
    public string? ElevatorType { get; set; }

    [Required]
    public MaintenanceType MaintenanceType { get; set; }

    [Required]
    public UrgencyLevel UrgencyLevel { get; set; }

    [StringLength(1000)]
    public string? Description { get; set; }

    [StringLength(50)]
    public string? PreferredTime { get; set; }

    public MaintenanceStatus Status { get; set; } = MaintenanceStatus.Pending;

    public string? TechnicianNotes { get; set; }

    public DateTime? ScheduledTime { get; set; }

    public DateTime? CompletedTime { get; set; }

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
}

public enum MaintenanceType
{
    Routine,    // 定期保养
    Emergency,  // 紧急维修
    Inspection, // 安全检查
    Upgrade     // 设备升级
}

public enum UrgencyLevel
{
    Low,    // 一般
    Medium, // 紧急
    High    // 非常紧急
}

public enum MaintenanceStatus
{
    Pending,    // 待处理
    Scheduled,  // 已安排
    InProgress, // 进行中
    Completed,  // 已完成
    Cancelled   // 已取消
} 