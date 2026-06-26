# OCR API Server

uvicorn app.main:app --reload


A FastAPI-based OCR API server with adapter-based integration for:

- PP-OCR
- PaddleOCR-VL
- PP-StructureV3
- Health check

## Python Version

This project is pinned to:

- **Python 3.11**

See:

- `.python-version`
- `Dockerfile`

## Endpoints

- `GET /healthz`
- `POST /ocr/pp-ocr`
- `POST /ocr/paddleocr-vl`
- `POST /ocr/pp-structure-v3`

## Why adapter pattern?

This project uses an adapter layer so that the API contract stays stable even if the underlying OCR/VL/structure runtime changes.

Benefits:

- Keep routers simple
- Swap model/runtime implementation without changing endpoints
- Normalize outputs from different engines
- Easier testing and mocking
- Better maintainability when Paddle ecosystem versions change

## Project Structure

```text
app/
├─ main.py
├─ core/
│  ├─ config.py
│  └─ errors.py
├─ adapters/
│  ├─ base.py
│  ├─ pp_ocr_adapter.py
│  ├─ paddleocr_vl_adapter.py
│  └─ pp_structure_v3_adapter.py
├─ routers/
│  ├─ health.py
│  └─ ocr.py
├─ schemas/
│  └─ responses.py
├─ services/
│  └─ ocr_service.py
└─ utils/
   └─ files.py
```

## Notes

### PP-OCR
Implemented using `PaddleOCR`.

### PaddleOCR-VL
This starter project exposes the endpoint, but the actual runtime integration is intentionally left in adapter form as a placeholder. Replace the adapter implementation with your actual VL runtime.

### PP-StructureV3
This starter uses `PPStructure` where available in the installed `paddleocr` package. Depending on your exact environment and desired V3 features, you may need to customize the adapter further.

## Install

### 1. Create virtual environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Docs

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Docker

### Build

```bash
docker build -t ocr-api-server .
```

### Run

```bash
docker run --rm -p 8000:8000 ocr-api-server
```

## Example Requests

### Health Check

```bash
curl http://localhost:8000/healthz
```

Response:

```json
{
  "status": "ok"
}
```

### PP-OCR

```bash
curl -X POST "http://localhost:8000/ocr/pp-ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample.png"
```

### PaddleOCR-VL

```bash
curl -X POST "http://localhost:8000/ocr/paddleocr-vl" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample.png"
```

### PP-StructureV3

```bash
curl -X POST "http://localhost:8000/ocr/pp-structure-v3" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample.png"
```

## Response Format

```json
{
  "engine": "pp-ocr",
  "success": true,
  "results": [
    {
      "text": "Hello World",
      "score": 0.998,
      "bbox": [[0, 0], [100, 0], [100, 20], [0, 20]],
      "type": "text",
      "raw": {}
    }
  ],
  "error": null
}
```

## Environment Variables

- `APP_NAME`
- `APP_ENV`
- `LOG_LEVEL`
- `USE_GPU`
- `OCR_LANG`
- `OCR_USE_ANGLE_CLS`
- `TMP_DIR`
- `MAX_UPLOAD_SIZE_MB`

Example:

```bash
export USE_GPU=false
export OCR_LANG=en
export MAX_UPLOAD_SIZE_MB=20
```

## Limitations

1. `PaddleOCR-VL` adapter is a placeholder until you provide actual runtime integration.
2. `PP-StructureV3` behavior depends on installed PaddleOCR capabilities.
3. Some models may auto-download on first run.
4. Production deployment should consider:
   - warm-up/preload
   - timeout settings
   - workers
   - GPU isolation
   - request limits
   - authentication