from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api.dependencies import verify_api_key
from app.core.config import get_settings
from app.core.feature_flags import get_feature_flags
from app.schemas.inference import InferenceResponse

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(
    prefix="/inference",
    tags=["inference"],
    dependencies=[Depends(verify_api_key)],
)


@router.post("/predict", response_model=InferenceResponse)
@limiter.limit("30/minute")
async def predict(
    request: Request,
    file: UploadFile = File(...),
):
    contents = await file.read()
    max_bytes = get_settings().max_file_size_mb * 1024 * 1024
    if len(contents) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds {get_settings().max_file_size_mb} MB limit",
        )
    inference_service = request.app.state.inference_service
    result = await inference_service.predict(contents)
    payload = result.model_dump()
    public_keys = get_feature_flags().public_inference_keys()
    return {key: value for key, value in payload.items() if key in public_keys}
