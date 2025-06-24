using System.ComponentModel.DataAnnotations;
using JojdaElevator.API.Models;

namespace JojdaElevator.API.DTOs;

public class CreateElevatorRequirementDto
{
    [Required(ErrorMessage = "联系人姓名为必填项")]
    [StringLength(100, ErrorMessage = "联系人姓名不能超过100个字符")]
    public string ContactName { get; set; } = string.Empty;

    [Required(ErrorMessage = "联系电话为必填项")]
    [StringLength(50, ErrorMessage = "联系电话不能超过50个字符")]
    [Phone(ErrorMessage = "请输入有效的电话号码")]
    public string ContactPhone { get; set; } = string.Empty;

    [StringLength(100, ErrorMessage = "联系邮箱不能超过100个字符")]
    [EmailAddress(ErrorMessage = "请输入有效的邮箱地址")]
    public string? ContactEmail { get; set; }

    [StringLength(200, ErrorMessage = "公司名称不能超过200个字符")]
    public string? CompanyName { get; set; }

    [StringLength(200, ErrorMessage = "项目名称不能超过200个字符")]
    public string? ProjectName { get; set; }

    [StringLength(500, ErrorMessage = "项目地址不能超过500个字符")]
    public string? ProjectAddress { get; set; }

    [Required(ErrorMessage = "电梯类型为必填项")]
    public ElevatorType ElevatorType { get; set; }

    [Required(ErrorMessage = "数量为必填项")]
    [Range(1, int.MaxValue, ErrorMessage = "数量必须大于0")]
    public int Quantity { get; set; } = 1;

    [Required(ErrorMessage = "楼层数为必填项")]
    [Range(2, int.MaxValue, ErrorMessage = "楼层数必须大于等于2")]
    public int Floors { get; set; }

    [Range(0.1, 10.0, ErrorMessage = "层高必须在0.1-10.0米之间")]
    public decimal? FloorHeight { get; set; }

    [Range(100, 10000, ErrorMessage = "载重量必须在100-10000kg之间")]
    public int? CarCapacity { get; set; }

    [Range(0.1, 10.0, ErrorMessage = "运行速度必须在0.1-10.0m/s之间")]
    public decimal? CarSpeed { get; set; }

    public decimal? HoistwayWidth { get; set; }
    public decimal? HoistwayDepth { get; set; }
    public decimal? PitDepth { get; set; }
    public decimal? OverheadHeight { get; set; }
    public decimal? CarWidth { get; set; }
    public decimal? CarDepth { get; set; }
    public decimal? CarHeight { get; set; }
    public decimal? DoorWidth { get; set; }
    public decimal? DoorHeight { get; set; }

    [StringLength(2000, ErrorMessage = "特殊要求不能超过2000个字符")]
    public string? SpecialRequirements { get; set; }

    [StringLength(100, ErrorMessage = "预算范围不能超过100个字符")]
    public string? BudgetRange { get; set; }

    [StringLength(100, ErrorMessage = "交货期要求不能超过100个字符")]
    public string? DeliveryTime { get; set; }
}

public class ElevatorRequirementResponseDto
{
    public int Id { get; set; }
    public string ContactName { get; set; } = string.Empty;
    public string ContactPhone { get; set; } = string.Empty;
    public string? ContactEmail { get; set; }
    public string? CompanyName { get; set; }
    public string? ProjectName { get; set; }
    public string? ProjectAddress { get; set; }
    public string ElevatorType { get; set; } = string.Empty;
    public int Quantity { get; set; }
    public int Floors { get; set; }
    public decimal? FloorHeight { get; set; }
    public int? CarCapacity { get; set; }
    public decimal? CarSpeed { get; set; }
    public decimal? HoistwayWidth { get; set; }
    public decimal? HoistwayDepth { get; set; }
    public decimal? PitDepth { get; set; }
    public decimal? OverheadHeight { get; set; }
    public decimal? CarWidth { get; set; }
    public decimal? CarDepth { get; set; }
    public decimal? CarHeight { get; set; }
    public decimal? DoorWidth { get; set; }
    public decimal? DoorHeight { get; set; }
    public string? SpecialRequirements { get; set; }
    public string? BudgetRange { get; set; }
    public string? DeliveryTime { get; set; }
    public string Status { get; set; } = string.Empty;
    public string? AdminNotes { get; set; }
    public decimal? QuoteAmount { get; set; }
    public DateTime? QuoteDate { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
}

public class UpdateRequirementStatusDto
{
    [Required(ErrorMessage = "状态为必填项")]
    public RequirementStatus Status { get; set; }

    [StringLength(2000, ErrorMessage = "管理员备注不能超过2000个字符")]
    public string? AdminNotes { get; set; }

    [Range(0, double.MaxValue, ErrorMessage = "报价金额必须大于等于0")]
    public decimal? QuoteAmount { get; set; }
}

public class ApiResponse<T>
{
    public bool Success { get; set; }
    public string Message { get; set; } = string.Empty;
    public T? Data { get; set; }
    public List<string>? Errors { get; set; }

    public static ApiResponse<T> SuccessResult(T data, string message = "操作成功")
    {
        return new ApiResponse<T>
        {
            Success = true,
            Message = message,
            Data = data
        };
    }

    public static ApiResponse<T> ErrorResult(string message, List<string>? errors = null)
    {
        return new ApiResponse<T>
        {
            Success = false,
            Message = message,
            Errors = errors
        };
    }
} 