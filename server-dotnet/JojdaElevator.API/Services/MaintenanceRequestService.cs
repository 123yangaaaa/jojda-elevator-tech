using AutoMapper;
using Microsoft.EntityFrameworkCore;
using JojdaElevator.API.Data;
using JojdaElevator.API.DTOs;
using JojdaElevator.API.Models;

namespace JojdaElevator.API.Services;

public class MaintenanceRequestService : IMaintenanceRequestService
{
    private readonly ApplicationDbContext _context;
    private readonly IMapper _mapper;
    private readonly ILogger<MaintenanceRequestService> _logger;

    public MaintenanceRequestService(
        ApplicationDbContext context,
        IMapper mapper,
        ILogger<MaintenanceRequestService> logger)
    {
        _context = context;
        _mapper = mapper;
        _logger = logger;
    }

    public async Task<ApiResponse<MaintenanceRequestResponseDto>> CreateRequestAsync(CreateMaintenanceRequestDto dto)
    {
        try
        {
            // 验证枚举值
            if (!Enum.TryParse<MaintenanceType>(dto.MaintenanceType, true, out var maintenanceType))
            {
                return ApiResponse<MaintenanceRequestResponseDto>.ErrorResult("无效的维保类型");
            }

            if (!Enum.TryParse<UrgencyLevel>(dto.UrgencyLevel, true, out var urgencyLevel))
            {
                return ApiResponse<MaintenanceRequestResponseDto>.ErrorResult("无效的紧急程度");
            }

            var request = new MaintenanceRequest
            {
                CustomerName = dto.CustomerName,
                ContactPhone = dto.ContactPhone,
                ContactEmail = dto.ContactEmail,
                ElevatorLocation = dto.ElevatorLocation,
                ElevatorType = dto.ElevatorType,
                MaintenanceType = maintenanceType,
                UrgencyLevel = urgencyLevel,
                Description = dto.Description,
                PreferredTime = dto.PreferredTime,
                Status = MaintenanceStatus.Pending,
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow
            };

            _context.MaintenanceRequests.Add(request);
            await _context.SaveChangesAsync();

            var responseDto = _mapper.Map<MaintenanceRequestResponseDto>(request);
            
            _logger.LogInformation("维保申请创建成功，ID: {RequestId}, 客户: {CustomerName}", 
                request.Id, request.CustomerName);

            return ApiResponse<MaintenanceRequestResponseDto>.SuccessResult(responseDto, "维保申请提交成功");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "创建维保申请时发生错误");
            return ApiResponse<MaintenanceRequestResponseDto>.ErrorResult("提交维保申请失败，请稍后重试");
        }
    }

    public async Task<ApiResponse<MaintenanceRequestResponseDto>> GetRequestByIdAsync(int id)
    {
        try
        {
            var request = await _context.MaintenanceRequests
                .FirstOrDefaultAsync(r => r.Id == id);

            if (request == null)
            {
                return ApiResponse<MaintenanceRequestResponseDto>.ErrorResult("维保申请不存在");
            }

            var responseDto = _mapper.Map<MaintenanceRequestResponseDto>(request);
            return ApiResponse<MaintenanceRequestResponseDto>.SuccessResult(responseDto);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "获取维保申请详情时发生错误，ID: {RequestId}", id);
            return ApiResponse<MaintenanceRequestResponseDto>.ErrorResult("获取维保申请详情失败");
        }
    }

    public async Task<ApiResponse<List<MaintenanceRequestResponseDto>>> GetAllRequestsAsync()
    {
        try
        {
            var requests = await _context.MaintenanceRequests
                .OrderByDescending(r => r.CreatedAt)
                .ToListAsync();

            var responseDtos = _mapper.Map<List<MaintenanceRequestResponseDto>>(requests);
            return ApiResponse<List<MaintenanceRequestResponseDto>>.SuccessResult(responseDtos);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "获取维保申请列表时发生错误");
            return ApiResponse<List<MaintenanceRequestResponseDto>>.ErrorResult("获取维保申请列表失败");
        }
    }

    public async Task<ApiResponse<MaintenanceRequestResponseDto>> UpdateRequestStatusAsync(int id, UpdateMaintenanceStatusDto dto)
    {
        try
        {
            var request = await _context.MaintenanceRequests
                .FirstOrDefaultAsync(r => r.Id == id);

            if (request == null)
            {
                return ApiResponse<MaintenanceRequestResponseDto>.ErrorResult("维保申请不存在");
            }

            if (!Enum.TryParse<MaintenanceStatus>(dto.Status, true, out var status))
            {
                return ApiResponse<MaintenanceRequestResponseDto>.ErrorResult("无效的状态值");
            }

            request.Status = status;
            request.TechnicianNotes = dto.TechnicianNotes;
            request.ScheduledTime = dto.ScheduledTime;
            request.CompletedTime = dto.CompletedTime;
            request.UpdatedAt = DateTime.UtcNow;

            await _context.SaveChangesAsync();

            var responseDto = _mapper.Map<MaintenanceRequestResponseDto>(request);
            
            _logger.LogInformation("维保申请状态更新成功，ID: {RequestId}, 新状态: {Status}", 
                request.Id, status);

            return ApiResponse<MaintenanceRequestResponseDto>.SuccessResult(responseDto, "状态更新成功");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "更新维保申请状态时发生错误，ID: {RequestId}", id);
            return ApiResponse<MaintenanceRequestResponseDto>.ErrorResult("更新状态失败");
        }
    }

    public async Task<ApiResponse<bool>> DeleteRequestAsync(int id)
    {
        try
        {
            var request = await _context.MaintenanceRequests
                .FirstOrDefaultAsync(r => r.Id == id);

            if (request == null)
            {
                return ApiResponse<bool>.ErrorResult("维保申请不存在");
            }

            _context.MaintenanceRequests.Remove(request);
            await _context.SaveChangesAsync();

            _logger.LogInformation("维保申请删除成功，ID: {RequestId}", id);
            return ApiResponse<bool>.SuccessResult(true, "维保申请删除成功");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "删除维保申请时发生错误，ID: {RequestId}", id);
            return ApiResponse<bool>.ErrorResult("删除维保申请失败");
        }
    }

    public async Task<ApiResponse<List<MaintenanceRequestResponseDto>>> GetRequestsByStatusAsync(MaintenanceStatus status)
    {
        try
        {
            var requests = await _context.MaintenanceRequests
                .Where(r => r.Status == status)
                .OrderByDescending(r => r.CreatedAt)
                .ToListAsync();

            var responseDtos = _mapper.Map<List<MaintenanceRequestResponseDto>>(requests);
            return ApiResponse<List<MaintenanceRequestResponseDto>>.SuccessResult(responseDtos);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "根据状态获取维保申请列表时发生错误，状态: {Status}", status);
            return ApiResponse<List<MaintenanceRequestResponseDto>>.ErrorResult("获取维保申请列表失败");
        }
    }

    public async Task<ApiResponse<List<MaintenanceRequestResponseDto>>> GetRequestsByPhoneAsync(string phone)
    {
        try
        {
            var requests = await _context.MaintenanceRequests
                .Where(r => r.ContactPhone == phone)
                .OrderByDescending(r => r.CreatedAt)
                .ToListAsync();

            var responseDtos = _mapper.Map<List<MaintenanceRequestResponseDto>>(requests);
            return ApiResponse<List<MaintenanceRequestResponseDto>>.SuccessResult(responseDtos);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "根据电话号码获取维保申请列表时发生错误，电话: {Phone}", phone);
            return ApiResponse<List<MaintenanceRequestResponseDto>>.ErrorResult("查询维保申请失败");
        }
    }
} 