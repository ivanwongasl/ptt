from fastapi import APIRouter, File, HTTPException, UploadFile, status
from app.core.errors import BadRequestError, ServiceUnavailableError
from app.schemas.responses import OCRResponse, OCRItem
from app.services.ocr_service import ocr_service
from app.utils.files import cleanup_temp_file, save_upload_to_temp

router = APIRouter()


def build_response(engine: str, results: list) -> OCRResponse:
    return OCRResponse(
        engine=engine,
        success=True,
        results=[OCRItem(**item) for item in results],
        error=None,
    )


@router.post("/pp-ocr", response_model=OCRResponse)
async def pp_ocr(file: UploadFile = File(...)):
    temp_path = None
    try:
        temp_path = await save_upload_to_temp(file)
        results = ocr_service.pp_ocr_adapter.run(temp_path)
        return build_response("pp-ocr", results)
    except BadRequestError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    except ServiceUnavailableError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected server error: {str(e)}",
        )
    finally:
        if temp_path:
            cleanup_temp_file(temp_path)


@router.post("/paddleocr-vl", response_model=OCRResponse)
async def paddleocr_vl(file: UploadFile = File(...)):
    temp_path = None
    try:
        temp_path = await save_upload_to_temp(file)
        results = ocr_service.paddleocr_vl_adapter.run(temp_path)
        return build_response("paddleocr-vl", results)
    except BadRequestError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    except ServiceUnavailableError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected server error: {str(e)}",
        )
    finally:
        if temp_path:
            cleanup_temp_file(temp_path)


@router.post("/pp-structure-v3", response_model=OCRResponse)
async def pp_structure_v3(file: UploadFile = File(...)):
    temp_path = None
    try:
        temp_path = await save_upload_to_temp(file)
        results = ocr_service.pp_structure_v3_adapter.run(temp_path)
        return build_response("pp-structure-v3", results)
    except BadRequestError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    except ServiceUnavailableError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected server error: {str(e)}",
        )
    finally:
        if temp_path:
            cleanup_temp_file(temp_path)