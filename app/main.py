from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI(title="PPT 批量转 PDF")

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

ALLOWED_SUFFIXES = {".ppt", ".pptx"}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/convert")
async def convert(background_tasks: BackgroundTasks, files: list[UploadFile] = File(...)) -> FileResponse:
    if not files:
        raise HTTPException(status_code=400, detail="请至少上传一个 PPT 文件。")

    with tempfile.TemporaryDirectory(prefix="ppt2pdf_") as temp_dir:
        temp_path = Path(temp_dir)
        input_dir = temp_path / "input"
        output_dir = temp_path / "output"
        input_dir.mkdir(parents=True, exist_ok=True)
        output_dir.mkdir(parents=True, exist_ok=True)

        for upload in files:
            source_name = Path(upload.filename or "").name
            if not source_name:
                raise HTTPException(status_code=400, detail="文件名不能为空。")

            suffix = Path(source_name).suffix.lower()
            if suffix not in ALLOWED_SUFFIXES:
                raise HTTPException(
                    status_code=400,
                    detail=f"文件 {source_name} 格式不支持，仅支持 .ppt/.pptx。",
                )

            target_path = input_dir / source_name
            with target_path.open("wb") as f:
                shutil.copyfileobj(upload.file, f)

            cmd = [
                "soffice",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                str(output_dir),
                str(target_path),
            ]
            process = subprocess.run(cmd, capture_output=True, text=True)
            if process.returncode != 0:
                raise HTTPException(
                    status_code=500,
                    detail=(
                        f"转换失败：{source_name}。请确认服务器已安装 LibreOffice。"
                        f" stderr: {process.stderr.strip()}"
                    ),
                )

        pdfs = sorted(output_dir.glob("*.pdf"))
        if not pdfs:
            raise HTTPException(status_code=500, detail="未生成 PDF 文件。")

        zip_path = temp_path / "converted_pdfs.zip"
        with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zip_file:
            for pdf_file in pdfs:
                zip_file.write(pdf_file, arcname=pdf_file.name)

        final_zip = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
        final_zip.close()
        shutil.copy2(zip_path, final_zip.name)

    background_tasks.add_task(Path(final_zip.name).unlink, missing_ok=True)

    return FileResponse(
        final_zip.name,
        media_type="application/zip",
        filename="converted_pdfs.zip",
        background=background_tasks,
    )
