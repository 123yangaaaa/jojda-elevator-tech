using JojdaElevator.API.DTOs;
using JojdaElevator.API.Models;

namespace JojdaElevator.API.Services;

public interface IElevatorRequirementService
{
    Task<ApiResponse<ElevatorRequirementResponseDto>> CreateRequirementAsync(CreateElevatorRequirementDto dto);
    Task<ApiResponse<ElevatorRequirementResponseDto>> GetRequirementByIdAsync(int id);
    Task<ApiResponse<List<ElevatorRequirementResponseDto>>> GetAllRequirementsAsync();
    Task<ApiResponse<ElevatorRequirementResponseDto>> UpdateRequirementStatusAsync(int id, UpdateRequirementStatusDto dto);
    Task<ApiResponse<bool>> DeleteRequirementAsync(int id);
    Task<ApiResponse<List<ElevatorRequirementResponseDto>>> GetRequirementsByStatusAsync(RequirementStatus status);
} 