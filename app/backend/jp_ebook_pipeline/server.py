from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse

from jp_ebook_pipeline.converter import convert_file
from jp_ebook_pipeline.models import ConvertOptions

app = FastAPI(title="JP Ebook Furigana Pipeline")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/convert")
async def convert_endpoint(
    file: UploadFile = File(...),
    horizontal: bool = Form(True),
    furigana: bool = Form(False),
    font_size: str = Form("1.05em"),
    line_height: str = Form("1.85"),
) -> FileResponse:
    with TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        input_path = tmpdir / (file.filename or "input.epub")
        output_path = tmpdir / "converted.epub"
        input_path.write_bytes(await file.read())
        options = ConvertOptions(
            horizontal=horizontal,
            furigana=furigana,
            font_size=font_size,
            line_height=line_height,
        )
        convert_file(input_path, output_path, options)
        stable_output = Path("output") / "converted.epub"
        stable_output.parent.mkdir(exist_ok=True)
        stable_output.write_bytes(output_path.read_bytes())
    return FileResponse(stable_output, filename="converted.epub")

