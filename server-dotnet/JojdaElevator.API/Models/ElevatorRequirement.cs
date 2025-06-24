using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace JojdaElevator.API.Models;

public class ElevatorRequirement
{
    [Key]
    public int Id { get; set; }

    [Required]
    [StringLength(100)]
    public string ContactName { get; set; } = string.Empty;

    [Required]
    [StringLength(50)]
    [Phone]
    public string ContactPhone { get; set; } = string.Empty;

    [StringLength(100)]
    [EmailAddress]
    public string? ContactEmail { get; set; }

    [StringLength(200)]
    public string? CompanyName { get; set; }

    [StringLength(200)]
    public string? ProjectName { get; set; }

    [StringLength(500)]
    public string? ProjectAddress { get; set; }

    [Required]
    public ElevatorType ElevatorType { get; set; }

    [Required]
    [Range(1, int.MaxValue)]
    public int Quantity { get; set; } = 1;

    [Required]
    [Range(2, int.MaxValue)]
    public int Floors { get; set; }

    [Column(TypeName = "decimal(5,2)")]
    public decimal? FloorHeight { get; set; }

    public int? CarCapacity { get; set; }

    [Column(TypeName = "decimal(4,2)")]
    public decimal? CarSpeed { get; set; }

    [Column(TypeName = "decimal(6,2)")]
    public decimal? HoistwayWidth { get; set; }

    [Column(TypeName = "decimal(6,2)")]
    public decimal? HoistwayDepth { get; set; }

    [Column(TypeName = "decimal(7,2)")]
    public decimal? PitDepth { get; set; }

    [Column(TypeName = "decimal(5,2)")]
    public decimal? OverheadHeight { get; set; }

    [Column(TypeName = "decimal(6,2)")]
    public decimal? CarWidth { get; set; }

    [Column(TypeName = "decimal(6,2)")]
    public decimal? CarDepth { get; set; }

    [Column(TypeName = "decimal(5,2)")]
    public decimal? CarHeight { get; set; }

    [Column(TypeName = "decimal(7,2)")]
    public decimal? DoorWidth { get; set; }

    [Column(TypeName = "decimal(7,2)")]
    public decimal? DoorHeight { get; set; }

    public string? SpecialRequirements { get; set; }

    [StringLength(100)]
    public string? BudgetRange { get; set; }

    [StringLength(100)]
    public string? DeliveryTime { get; set; }

    public RequirementStatus Status { get; set; } = RequirementStatus.Pending;

    public string? AdminNotes { get; set; }

    [Column(TypeName = "decimal(12,2)")]
    public decimal? QuoteAmount { get; set; }

    public DateTime? QuoteDate { get; set; }

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
}

public enum ElevatorType
{
    Passenger,
    Freight,
    Home,
    Escalator,
    MovingWalkway
}

public enum RequirementStatus
{
    Pending,
    Reviewing,
    Quoted,
    Accepted,
    Rejected
} 