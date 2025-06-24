using AutoMapper;
using JojdaElevator.API.DTOs;
using JojdaElevator.API.Models;

namespace JojdaElevator.API.Profiles;

public class MappingProfile : Profile
{
    public MappingProfile()
    {
        // CreateElevatorRequirementDto -> ElevatorRequirement
        CreateMap<CreateElevatorRequirementDto, ElevatorRequirement>()
            .ForMember(dest => dest.Id, opt => opt.Ignore())
            .ForMember(dest => dest.Status, opt => opt.MapFrom(src => RequirementStatus.Pending))
            .ForMember(dest => dest.AdminNotes, opt => opt.Ignore())
            .ForMember(dest => dest.QuoteAmount, opt => opt.Ignore())
            .ForMember(dest => dest.QuoteDate, opt => opt.Ignore())
            .ForMember(dest => dest.CreatedAt, opt => opt.Ignore())
            .ForMember(dest => dest.UpdatedAt, opt => opt.Ignore());

        // ElevatorRequirement -> ElevatorRequirementResponseDto
        CreateMap<ElevatorRequirement, ElevatorRequirementResponseDto>()
            .ForMember(dest => dest.ElevatorType, opt => opt.MapFrom(src => GetElevatorTypeDisplayName(src.ElevatorType)))
            .ForMember(dest => dest.Status, opt => opt.MapFrom(src => GetStatusDisplayName(src.Status)));

        // MaintenanceRequest mappings
        CreateMap<CreateMaintenanceRequestDto, MaintenanceRequest>()
            .ForMember(dest => dest.MaintenanceType, opt => opt.Ignore())
            .ForMember(dest => dest.UrgencyLevel, opt => opt.Ignore());
            
        CreateMap<MaintenanceRequest, MaintenanceRequestResponseDto>()
            .ForMember(dest => dest.MaintenanceType, opt => opt.MapFrom(src => src.MaintenanceType.ToString()))
            .ForMember(dest => dest.UrgencyLevel, opt => opt.MapFrom(src => src.UrgencyLevel.ToString()))
            .ForMember(dest => dest.Status, opt => opt.MapFrom(src => src.Status.ToString()));
    }

    private static string GetElevatorTypeDisplayName(ElevatorType type)
    {
        return type switch
        {
            ElevatorType.Passenger => "乘客电梯",
            ElevatorType.Freight => "货梯",
            ElevatorType.Home => "家用电梯",
            ElevatorType.Escalator => "自动扶梯",
            ElevatorType.MovingWalkway => "自动人行道",
            _ => type.ToString()
        };
    }

    private static string GetStatusDisplayName(RequirementStatus status)
    {
        return status switch
        {
            RequirementStatus.Pending => "待处理",
            RequirementStatus.Reviewing => "审核中",
            RequirementStatus.Quoted => "已报价",
            RequirementStatus.Accepted => "已接受",
            RequirementStatus.Rejected => "已拒绝",
            _ => status.ToString()
        };
    }
} 