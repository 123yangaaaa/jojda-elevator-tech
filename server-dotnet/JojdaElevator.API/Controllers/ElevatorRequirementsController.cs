using Microsoft.AspNetCore.Mvc;
using JojdaElevator.API.DTOs;
using JojdaElevator.API.Models;
using JojdaElevator.API.Services;

namespace JojdaElevator.API.Controllers;

[ApiController]
[Route("api/[controller]")]
[Produces("application/json")]
public class ElevatorRequirementsController : ControllerBase
{
    private readonly IElevatorRequirementService _requirementService;
    private readonly ILogger<ElevatorRequirementsController> _logger;

    public ElevatorRequirementsController(
        IElevatorRequirementService requirementService,
        ILogger<ElevatorRequirementsController> logger)
    {
        _requirementService = requirementService;
        _logger = logger;
    }

    /// <summary>
    /// 提交新的电梯采购需求
    /// </summary>
    /// <param name="dto">采购需求信息</param>
    /// <returns>创建的采购需求详情</returns>
    [HttpPost]
    [ProducesResponseType(typeof(ApiResponse<ElevatorRequirementResponseDto>), 201)]
    [ProducesResponseType(typeof(ApiResponse<ElevatorRequirementResponseDto>), 400)]
    [ProducesResponseType(typeof(ApiResponse<ElevatorRequirementResponseDto>), 500)]
    public async Task<ActionResult<ApiResponse<ElevatorRequirementResponseDto>>> CreateRequirement(
        [FromBody] CreateElevatorRequirementDto dto)
    {
        if (!ModelState.IsValid)
        {
            var errors = ModelState
                .SelectMany(x => x.Value!.Errors)
                .Select(x => x.ErrorMessage)
                .ToList();

            return BadRequest(ApiResponse<ElevatorRequirementResponseDto>.ErrorResult(
                "输入数据验证失败", errors));
        }

        var result = await _requirementService.CreateRequirementAsync(dto);

        if (result.Success)
        {
            return CreatedAtAction(
                nameof(GetRequirement),
                new { id = result.Data!.Id },
                result);
        }

        return StatusCode(500, result);
    }

    /// <summary>
    /// 获取所有采购需求列表
    /// </summary>
    /// <returns>采购需求列表</returns>
    [HttpGet]
    [ProducesResponseType(typeof(ApiResponse<List<ElevatorRequirementResponseDto>>), 200)]
    [ProducesResponseType(typeof(ApiResponse<List<ElevatorRequirementResponseDto>>), 500)]
    public async Task<ActionResult<ApiResponse<List<ElevatorRequirementResponseDto>>>> GetAllRequirements()
    {
        var result = await _requirementService.GetAllRequirementsAsync();

        if (result.Success)
        {
            return Ok(result);
        }

        return StatusCode(500, result);
    }

    /// <summary>
    /// 根据ID获取采购需求详情
    /// </summary>
    /// <param name="id">采购需求ID</param>
    /// <returns>采购需求详情</returns>
    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(ApiResponse<ElevatorRequirementResponseDto>), 200)]
    [ProducesResponseType(typeof(ApiResponse<ElevatorRequirementResponseDto>), 404)]
    [ProducesResponseType(typeof(ApiResponse<ElevatorRequirementResponseDto>), 500)]
    public async Task<ActionResult<ApiResponse<ElevatorRequirementResponseDto>>> GetRequirement(int id)
    {
        var result = await _requirementService.GetRequirementByIdAsync(id);

        if (result.Success)
        {
            return Ok(result);
        }

        if (result.Message.Contains("不存在"))
        {
            return NotFound(result);
        }

        return StatusCode(500, result);
    }

    /// <summary>
    /// 更新采购需求状态（管理员功能）
    /// </summary>
    /// <param name="id">采购需求ID</param>
    /// <param name="dto">状态更新信息</param>
    /// <returns>更新后的采购需求详情</returns>
    [HttpPut("{id:int}/status")]
    [ProducesResponseType(typeof(ApiResponse<ElevatorRequirementResponseDto>), 200)]
    [ProducesResponseType(typeof(ApiResponse<ElevatorRequirementResponseDto>), 400)]
    [ProducesResponseType(typeof(ApiResponse<ElevatorRequirementResponseDto>), 404)]
    [ProducesResponseType(typeof(ApiResponse<ElevatorRequirementResponseDto>), 500)]
    public async Task<ActionResult<ApiResponse<ElevatorRequirementResponseDto>>> UpdateRequirementStatus(
        int id, [FromBody] UpdateRequirementStatusDto dto)
    {
        if (!ModelState.IsValid)
        {
            var errors = ModelState
                .SelectMany(x => x.Value!.Errors)
                .Select(x => x.ErrorMessage)
                .ToList();

            return BadRequest(ApiResponse<ElevatorRequirementResponseDto>.ErrorResult(
                "输入数据验证失败", errors));
        }

        var result = await _requirementService.UpdateRequirementStatusAsync(id, dto);

        if (result.Success)
        {
            return Ok(result);
        }

        if (result.Message.Contains("不存在"))
        {
            return NotFound(result);
        }

        return StatusCode(500, result);
    }

    /// <summary>
    /// 删除采购需求（管理员功能）
    /// </summary>
    /// <param name="id">采购需求ID</param>
    /// <returns>删除结果</returns>
    [HttpDelete("{id:int}")]
    [ProducesResponseType(typeof(ApiResponse<bool>), 200)]
    [ProducesResponseType(typeof(ApiResponse<bool>), 404)]
    [ProducesResponseType(typeof(ApiResponse<bool>), 500)]
    public async Task<ActionResult<ApiResponse<bool>>> DeleteRequirement(int id)
    {
        var result = await _requirementService.DeleteRequirementAsync(id);

        if (result.Success)
        {
            return Ok(result);
        }

        if (result.Message.Contains("不存在"))
        {
            return NotFound(result);
        }

        return StatusCode(500, result);
    }

    /// <summary>
    /// 根据状态获取采购需求列表
    /// </summary>
    /// <param name="status">需求状态</param>
    /// <returns>符合状态的采购需求列表</returns>
    [HttpGet("status/{status}")]
    [ProducesResponseType(typeof(ApiResponse<List<ElevatorRequirementResponseDto>>), 200)]
    [ProducesResponseType(typeof(ApiResponse<List<ElevatorRequirementResponseDto>>), 400)]
    [ProducesResponseType(typeof(ApiResponse<List<ElevatorRequirementResponseDto>>), 500)]
    public async Task<ActionResult<ApiResponse<List<ElevatorRequirementResponseDto>>>> GetRequirementsByStatus(
        RequirementStatus status)
    {
        var result = await _requirementService.GetRequirementsByStatusAsync(status);

        if (result.Success)
        {
            return Ok(result);
        }

        return StatusCode(500, result);
    }

    /// <summary>
    /// 测试数据库连接
    /// </summary>
    /// <returns>连接状态</returns>
    [HttpGet("test-db")]
    [ProducesResponseType(typeof(object), 200)]
    public ActionResult TestDatabase()
    {
        return Ok(new { message = "数据库连接成功！", timestamp = DateTime.UtcNow });
    }
} 