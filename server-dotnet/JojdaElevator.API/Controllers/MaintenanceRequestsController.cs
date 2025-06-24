using Microsoft.AspNetCore.Mvc;
using JojdaElevator.API.DTOs;
using JojdaElevator.API.Models;
using JojdaElevator.API.Services;

namespace JojdaElevator.API.Controllers;

[ApiController]
[Route("api/[controller]")]
[Produces("application/json")]
public class MaintenanceRequestsController : ControllerBase
{
    private readonly IMaintenanceRequestService _maintenanceService;
    private readonly ILogger<MaintenanceRequestsController> _logger;

    public MaintenanceRequestsController(
        IMaintenanceRequestService maintenanceService,
        ILogger<MaintenanceRequestsController> logger)
    {
        _maintenanceService = maintenanceService;
        _logger = logger;
    }

    /// <summary>
    /// 提交新的维保申请
    /// </summary>
    /// <param name="dto">维保申请信息</param>
    /// <returns>创建的维保申请详情</returns>
    [HttpPost]
    [ProducesResponseType(typeof(ApiResponse<MaintenanceRequestResponseDto>), 201)]
    [ProducesResponseType(typeof(ApiResponse<MaintenanceRequestResponseDto>), 400)]
    [ProducesResponseType(typeof(ApiResponse<MaintenanceRequestResponseDto>), 500)]
    public async Task<ActionResult<ApiResponse<MaintenanceRequestResponseDto>>> CreateRequest(
        [FromBody] CreateMaintenanceRequestDto dto)
    {
        if (!ModelState.IsValid)
        {
            var errors = ModelState
                .SelectMany(x => x.Value!.Errors)
                .Select(x => x.ErrorMessage)
                .ToList();

            return BadRequest(ApiResponse<MaintenanceRequestResponseDto>.ErrorResult(
                "输入数据验证失败", errors));
        }

        var result = await _maintenanceService.CreateRequestAsync(dto);

        if (result.Success)
        {
            return CreatedAtAction(
                nameof(GetRequest),
                new { id = result.Data!.Id },
                result);
        }

        return StatusCode(500, result);
    }

    /// <summary>
    /// 获取维保申请详情
    /// </summary>
    /// <param name="id">维保申请ID</param>
    /// <returns>维保申请详情</returns>
    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(ApiResponse<MaintenanceRequestResponseDto>), 200)]
    [ProducesResponseType(typeof(ApiResponse<MaintenanceRequestResponseDto>), 404)]
    [ProducesResponseType(typeof(ApiResponse<MaintenanceRequestResponseDto>), 500)]
    public async Task<ActionResult<ApiResponse<MaintenanceRequestResponseDto>>> GetRequest(int id)
    {
        var result = await _maintenanceService.GetRequestByIdAsync(id);

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
    /// 获取所有维保申请列表（管理员功能）
    /// </summary>
    /// <returns>维保申请列表</returns>
    [HttpGet]
    [ProducesResponseType(typeof(ApiResponse<List<MaintenanceRequestResponseDto>>), 200)]
    [ProducesResponseType(typeof(ApiResponse<List<MaintenanceRequestResponseDto>>), 500)]
    public async Task<ActionResult<ApiResponse<List<MaintenanceRequestResponseDto>>>> GetAllRequests()
    {
        var result = await _maintenanceService.GetAllRequestsAsync();

        if (result.Success)
        {
            return Ok(result);
        }

        return StatusCode(500, result);
    }

    /// <summary>
    /// 更新维保申请状态（管理员功能）
    /// </summary>
    /// <param name="id">维保申请ID</param>
    /// <param name="dto">状态更新信息</param>
    /// <returns>更新后的维保申请详情</returns>
    [HttpPut("{id:int}/status")]
    [ProducesResponseType(typeof(ApiResponse<MaintenanceRequestResponseDto>), 200)]
    [ProducesResponseType(typeof(ApiResponse<MaintenanceRequestResponseDto>), 400)]
    [ProducesResponseType(typeof(ApiResponse<MaintenanceRequestResponseDto>), 404)]
    [ProducesResponseType(typeof(ApiResponse<MaintenanceRequestResponseDto>), 500)]
    public async Task<ActionResult<ApiResponse<MaintenanceRequestResponseDto>>> UpdateRequestStatus(
        int id, [FromBody] UpdateMaintenanceStatusDto dto)
    {
        if (!ModelState.IsValid)
        {
            var errors = ModelState
                .SelectMany(x => x.Value!.Errors)
                .Select(x => x.ErrorMessage)
                .ToList();

            return BadRequest(ApiResponse<MaintenanceRequestResponseDto>.ErrorResult(
                "输入数据验证失败", errors));
        }

        var result = await _maintenanceService.UpdateRequestStatusAsync(id, dto);

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
    /// 删除维保申请（管理员功能）
    /// </summary>
    /// <param name="id">维保申请ID</param>
    /// <returns>删除结果</returns>
    [HttpDelete("{id:int}")]
    [ProducesResponseType(typeof(ApiResponse<bool>), 200)]
    [ProducesResponseType(typeof(ApiResponse<bool>), 404)]
    [ProducesResponseType(typeof(ApiResponse<bool>), 500)]
    public async Task<ActionResult<ApiResponse<bool>>> DeleteRequest(int id)
    {
        var result = await _maintenanceService.DeleteRequestAsync(id);

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
    /// 根据状态获取维保申请列表
    /// </summary>
    /// <param name="status">维保状态</param>
    /// <returns>符合状态的维保申请列表</returns>
    [HttpGet("status/{status}")]
    [ProducesResponseType(typeof(ApiResponse<List<MaintenanceRequestResponseDto>>), 200)]
    [ProducesResponseType(typeof(ApiResponse<List<MaintenanceRequestResponseDto>>), 400)]
    [ProducesResponseType(typeof(ApiResponse<List<MaintenanceRequestResponseDto>>), 500)]
    public async Task<ActionResult<ApiResponse<List<MaintenanceRequestResponseDto>>>> GetRequestsByStatus(
        MaintenanceStatus status)
    {
        var result = await _maintenanceService.GetRequestsByStatusAsync(status);

        if (result.Success)
        {
            return Ok(result);
        }

        return StatusCode(500, result);
    }

    /// <summary>
    /// 根据电话号码查询维保申请
    /// </summary>
    /// <param name="phone">联系电话</param>
    /// <returns>该电话号码的维保申请列表</returns>
    [HttpGet("phone/{phone}")]
    [ProducesResponseType(typeof(ApiResponse<List<MaintenanceRequestResponseDto>>), 200)]
    [ProducesResponseType(typeof(ApiResponse<List<MaintenanceRequestResponseDto>>), 500)]
    public async Task<ActionResult<ApiResponse<List<MaintenanceRequestResponseDto>>>> GetRequestsByPhone(string phone)
    {
        var result = await _maintenanceService.GetRequestsByPhoneAsync(phone);

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
        return Ok(new { message = "维保申请数据库连接成功！", timestamp = DateTime.UtcNow });
    }
} 