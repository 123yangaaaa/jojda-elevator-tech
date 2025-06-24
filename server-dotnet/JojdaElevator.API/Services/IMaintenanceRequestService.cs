using JojdaElevator.API.DTOs;
using JojdaElevator.API.Models;

namespace JojdaElevator.API.Services;

public interface IMaintenanceRequestService
{
    Task<ApiResponse<MaintenanceRequestResponseDto>> CreateRequestAsync(CreateMaintenanceRequestDto dto);
    Task<ApiResponse<MaintenanceRequestResponseDto>> GetRequestByIdAsync(int id);
    Task<ApiResponse<List<MaintenanceRequestResponseDto>>> GetAllRequestsAsync();
    Task<ApiResponse<MaintenanceRequestResponseDto>> UpdateRequestStatusAsync(int id, UpdateMaintenanceStatusDto dto);
    Task<ApiResponse<bool>> DeleteRequestAsync(int id);
    Task<ApiResponse<List<MaintenanceRequestResponseDto>>> GetRequestsByStatusAsync(MaintenanceStatus status);
    Task<ApiResponse<List<MaintenanceRequestResponseDto>>> GetRequestsByPhoneAsync(string phone);
} 