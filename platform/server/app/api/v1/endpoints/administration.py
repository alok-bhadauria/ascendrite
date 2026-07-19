from fastapi import Depends, status
from typing import Dict, Any
from app.core.routing import APIRouter
from app.core.runtime.context import RuntimeContext
from app.api.v1.dependencies import (
    get_runtime_context,
    get_administration_service
)
from app.modules.administration.services.admin import AdministrationService

router = APIRouter()

@router.get("/config", tags=["Administration Tooling"])
async def get_config(
    service: AdministrationService = Depends(get_administration_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve global system features and security configurations"""
    config = await service.get_platform_config(context)
    return config.model_dump()

@router.put("/config", tags=["Administration Tooling"])
async def update_config(
    payload: Dict[str, Any],
    service: AdministrationService = Depends(get_administration_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Update global feature flags and maintenance configurations"""
    config = await service.update_platform_config(payload, context)
    return config.model_dump()

@router.get("/dashboard", tags=["Administration Tooling"])
async def get_dashboard_metrics(
    service: AdministrationService = Depends(get_administration_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve administrative metrics overview of database content and user footprint"""
    return await service.get_administrative_dashboard_stats(context)
