using System.ComponentModel.DataAnnotations;
using JojdaElevator.API.Models;

namespace JojdaElevator.API.DTOs;

public class CreateMaintenanceRequestDto
{
    [Required(ErrorMessage = "客户姓名不能为空")]
    [StringLength(100, ErrorMessage = "客户姓名长度不能超过100个字符")]
    public string CustomerName { get; set; } = string.Empty;

    [Required(ErrorMessage = "联系电话不能为空")]
    [Phone(ErrorMessage = "请输入有效的电话号码")]
    [StringLength(50, ErrorMessage = "联系电话长度不能超过50个字符")]
    public string ContactPhone { get; set; } = string.Empty;

    [EmailAddress(ErrorMessage = "请输入有效的邮箱地址")]
    [StringLength(100, ErrorMessage = "邮箱地址长度不能超过100个字符")]
    public string? ContactEmail { get; set; }

    [Required(ErrorMessage = "设备位置不能为空")]
    [StringLength(500, ErrorMessage = "设备位置长度不能超过500个字符")]
    public string ElevatorLocation { get; set; } = string.Empty;

    [StringLength(100, ErrorMessage = "电梯类型长度不能超过100个字符")]
    public string? ElevatorType { get; set; }

    [Required(ErrorMessage = "维保类型不能为空")]
    public string MaintenanceType { get; set; } = string.Empty;

    [Required(ErrorMessage = "紧急程度不能为空")]
    public string UrgencyLevel { get; set; } = string.Empty;

    [StringLength(1000, ErrorMessage = "问题描述长度不能超过1000个字符")]
    public string? Description { get; set; }

    [StringLength(50, ErrorMessage = "期望服务时间长度不能超过50个字符")]
    public string? PreferredTime { get; set; }
}

public class MaintenanceRequestResponseDto
{
    public int Id { get; set; }
    public string CustomerName { get; set; } = string.Empty;
    public string ContactPhone { get; set; } = string.Empty;
    public string? ContactEmail { get; set; }
    public string ElevatorLocation { get; set; } = string.Empty;
    public string? ElevatorType { get; set; }
    public string MaintenanceType { get; set; } = string.Empty;
    public string UrgencyLevel { get; set; } = string.Empty;
    public string? Description { get; set; }
    public string? PreferredTime { get; set; }
    public string Status { get; set; } = string.Empty;
    public string? TechnicianNotes { get; set; }
    public DateTime? ScheduledTime { get; set; }
    public DateTime? CompletedTime { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
}

public class UpdateMaintenanceStatusDto
{
    [Required(ErrorMessage = "状态不能为空")]
    public string Status { get; set; } = string.Empty;
    
    public string? TechnicianNotes { get; set; }
    public DateTime? ScheduledTime { get; set; }
    public DateTime? CompletedTime { get; set; }
} 