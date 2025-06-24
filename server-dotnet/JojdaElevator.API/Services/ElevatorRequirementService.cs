using AutoMapper;
using Microsoft.EntityFrameworkCore;
using JojdaElevator.API.Data;
using JojdaElevator.API.DTOs;
using JojdaElevator.API.Models;

namespace JojdaElevator.API.Services;

public class ElevatorRequirementService : IElevatorRequirementService
{
    private readonly ApplicationDbContext _context;
    private readonly IMapper _mapper;
    private readonly ILogger<ElevatorRequirementService> _logger;

    public ElevatorRequirementService(
        ApplicationDbContext context,
        IMapper mapper,
        ILogger<ElevatorRequirementService> logger)
    {
        _context = context;
        _mapper = mapper;
        _logger = logger;
    }

    public async Task<ApiResponse<ElevatorRequirementResponseDto>> CreateRequirementAsync(CreateElevatorRequirementDto dto)
    {
        try
        {
            var requirement = _mapper.Map<ElevatorRequirement>(dto);
            requirement.CreatedAt = DateTime.UtcNow;
            requirement.UpdatedAt = DateTime.UtcNow;

            _context.ElevatorRequirements.Add(requirement);
            await _context.SaveChangesAsync();

            var responseDto = _mapper.Map<ElevatorRequirementResponseDto>(requirement);

            _logger.LogInformation("成功创建电梯采购需求，ID: {RequirementId}, 联系人: {ContactName}", 
                requirement.Id, requirement.ContactName);

            return ApiResponse<ElevatorRequirementResponseDto>.SuccessResult(
                responseDto, "采购需求提交成功！我们会尽快与您联系。");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "创建电梯采购需求失败");
            return ApiResponse<ElevatorRequirementResponseDto>.ErrorResult("提交采购需求失败，请重试");
        }
    }

    public async Task<ApiResponse<ElevatorRequirementResponseDto>> GetRequirementByIdAsync(int id)
    {
        try
        {
            var requirement = await _context.ElevatorRequirements
                .FirstOrDefaultAsync(r => r.Id == id);

            if (requirement == null)
            {
                return ApiResponse<ElevatorRequirementResponseDto>.ErrorResult("采购需求不存在");
            }

            var responseDto = _mapper.Map<ElevatorRequirementResponseDto>(requirement);
            return ApiResponse<ElevatorRequirementResponseDto>.SuccessResult(responseDto);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "获取采购需求详情失败，ID: {RequirementId}", id);
            return ApiResponse<ElevatorRequirementResponseDto>.ErrorResult("获取采购需求详情失败");
        }
    }

    public async Task<ApiResponse<List<ElevatorRequirementResponseDto>>> GetAllRequirementsAsync()
    {
        try
        {
            var requirements = await _context.ElevatorRequirements
                .OrderByDescending(r => r.CreatedAt)
                .ToListAsync();

            var responseDtos = _mapper.Map<List<ElevatorRequirementResponseDto>>(requirements);
            return ApiResponse<List<ElevatorRequirementResponseDto>>.SuccessResult(responseDtos);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "获取采购需求列表失败");
            return ApiResponse<List<ElevatorRequirementResponseDto>>.ErrorResult("获取采购需求列表失败");
        }
    }

    public async Task<ApiResponse<ElevatorRequirementResponseDto>> UpdateRequirementStatusAsync(int id, UpdateRequirementStatusDto dto)
    {
        try
        {
            var requirement = await _context.ElevatorRequirements
                .FirstOrDefaultAsync(r => r.Id == id);

            if (requirement == null)
            {
                return ApiResponse<ElevatorRequirementResponseDto>.ErrorResult("采购需求不存在");
            }

            requirement.Status = dto.Status;
            requirement.AdminNotes = dto.AdminNotes;
            requirement.QuoteAmount = dto.QuoteAmount;
            requirement.UpdatedAt = DateTime.UtcNow;

            if (dto.Status == RequirementStatus.Quoted)
            {
                requirement.QuoteDate = DateTime.UtcNow;
            }

            await _context.SaveChangesAsync();

            var responseDto = _mapper.Map<ElevatorRequirementResponseDto>(requirement);

            _logger.LogInformation("成功更新采购需求状态，ID: {RequirementId}, 新状态: {Status}", 
                id, dto.Status);

            return ApiResponse<ElevatorRequirementResponseDto>.SuccessResult(responseDto, "状态更新成功");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "更新采购需求状态失败，ID: {RequirementId}", id);
            return ApiResponse<ElevatorRequirementResponseDto>.ErrorResult("更新采购需求状态失败");
        }
    }

    public async Task<ApiResponse<bool>> DeleteRequirementAsync(int id)
    {
        try
        {
            var requirement = await _context.ElevatorRequirements
                .FirstOrDefaultAsync(r => r.Id == id);

            if (requirement == null)
            {
                return ApiResponse<bool>.ErrorResult("采购需求不存在");
            }

            _context.ElevatorRequirements.Remove(requirement);
            await _context.SaveChangesAsync();

            _logger.LogInformation("成功删除采购需求，ID: {RequirementId}", id);

            return ApiResponse<bool>.SuccessResult(true, "删除成功");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "删除采购需求失败，ID: {RequirementId}", id);
            return ApiResponse<bool>.ErrorResult("删除采购需求失败");
        }
    }

    public async Task<ApiResponse<List<ElevatorRequirementResponseDto>>> GetRequirementsByStatusAsync(RequirementStatus status)
    {
        try
        {
            var requirements = await _context.ElevatorRequirements
                .Where(r => r.Status == status)
                .OrderByDescending(r => r.CreatedAt)
                .ToListAsync();

            var responseDtos = _mapper.Map<List<ElevatorRequirementResponseDto>>(requirements);
            return ApiResponse<List<ElevatorRequirementResponseDto>>.SuccessResult(responseDtos);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "根据状态获取采购需求列表失败，状态: {Status}", status);
            return ApiResponse<List<ElevatorRequirementResponseDto>>.ErrorResult("获取采购需求列表失败");
        }
    }
} 