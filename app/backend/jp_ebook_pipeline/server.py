from __future__ import annotations

import re
from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse

from jp_ebook_pipeline.converter import convert_file
from jp_ebook_pipeline.models import ConvertOptions

app = FastAPI(title="JP Ebook Furigana Pipeline")

INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>JP Ebook Furigana Pipeline</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      color: #202124;
      background: #f5f4ef;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    main {
      width: min(900px, calc(100vw - 32px));
      margin: 34px auto 56px;
    }
    h1 {
      margin: 0 0 8px;
      font-size: 30px;
      letter-spacing: 0;
    }
    p {
      margin: 0;
      line-height: 1.65;
      color: #4b4d4a;
    }
    form {
      margin-top: 24px;
      display: grid;
      gap: 18px;
      padding-top: 22px;
      border-top: 1px solid #d7d4c9;
    }
    fieldset {
      border: 1px solid #d3d0c4;
      border-radius: 8px;
      padding: 16px;
      background: #fff;
    }
    legend {
      padding: 0 6px;
      font-weight: 700;
    }
    label {
      display: flex;
      align-items: center;
      gap: 10px;
      min-height: 34px;
    }
    input[type="file"] {
      width: 100%;
      padding: 12px;
      border: 1px dashed #aaa596;
      border-radius: 8px;
      background: #fafaf8;
    }
    input[type="text"] {
      width: 140px;
      min-height: 34px;
      padding: 6px 8px;
      border: 1px solid #bbb7aa;
      border-radius: 6px;
      font: inherit;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px 18px;
    }
    .actions {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }
    button {
      min-height: 42px;
      padding: 0 16px;
      border: 1px solid #245b47;
      border-radius: 7px;
      background: #245b47;
      color: white;
      font: inherit;
      font-weight: 700;
      cursor: pointer;
    }
    button:disabled {
      opacity: 0.55;
      cursor: wait;
    }
    #status {
      min-height: 24px;
      color: #39433d;
      font-weight: 600;
    }
    .note {
      margin-top: 18px;
      font-size: 14px;
      color: #656761;
    }
    @media (max-width: 680px) {
      .grid { grid-template-columns: 1fr; }
      h1 { font-size: 25px; }
    }
  </style>
</head>
<body>
  <main>
    <h1>JP Ebook Furigana Pipeline</h1>
    <p>Upload a local Japanese EPUB, TXT, or HTML file. The app returns a horizontal, furigana-enabled, KOReader-friendly EPUB.</p>

    <form id="convert-form">
      <fieldset>
        <legend>Input</legend>
        <input id="file" name="file" type="file" accept=".epub,.txt,.html,.xhtml,.htm" required />
      </fieldset>

      <fieldset>
        <legend>Options</legend>
        <div class="grid">
          <label><input name="horizontal" type="checkbox" checked /> Convert to horizontal layout</label>
          <label><input name="furigana" type="checkbox" checked /> Add furigana</label>
          <label>Font size <input name="font_size" type="text" value="1.08em" /></label>
          <label>Line height <input name="line_height" type="text" value="1.9" /></label>
        </div>
      </fieldset>

      <div class="actions">
        <button id="submit" type="submit">Convert and download EPUB</button>
        <span id="status"></span>
      </div>
    </form>

    <p class="note">This local app does not download books, remove DRM, or send files to any cloud service. It only processes the file you choose on this computer.</p>
  </main>

  <script>
    const form = document.getElementById("convert-form");
    const status = document.getElementById("status");
    const submit = document.getElementById("submit");

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const data = new FormData(form);
      status.textContent = "Converting...";
      submit.disabled = true;
      try {
        const response = await fetch("/convert", { method: "POST", body: data });
        if (!response.ok) {
          const text = await response.text();
          throw new Error(text || "Conversion failed");
        }
        const blob = await response.blob();
        const disposition = response.headers.get("content-disposition") || "";
        const match = disposition.match(/filename\\*?=(?:UTF-8''|")?([^";]+)/i);
        const filename = match ? decodeURIComponent(match[1].replace(/"/g, "")) : "converted.epub";
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        link.remove();
        URL.revokeObjectURL(url);
        status.textContent = "Done. Check your downloads folder.";
      } catch (error) {
        status.textContent = error.message || "Conversion failed";
      } finally {
        submit.disabled = false;
      }
    });
  </script>
</body>
</html>
"""


def safe_stem(filename: str | None) -> str:
    raw = Path(filename or "converted").stem
    cleaned = re.sub(r"[^\w\u3040-\u30ff\u3400-\u9fff\u4e00-\u9fff-]+", "-", raw).strip("-")
    return cleaned or "converted"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return INDEX_HTML


@app.post("/convert")
async def convert_endpoint(
    file: UploadFile = File(...),
    horizontal: bool = Form(True),
    furigana: bool = Form(True),
    font_size: str = Form("1.05em"),
    line_height: str = Form("1.85"),
) -> FileResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Please choose a file.")

    stem = safe_stem(file.filename)
    suffix = "-horizontal" if horizontal else ""
    suffix += "-furigana" if furigana else ""
    download_name = f"{stem}{suffix}-koreader.epub"
    stable_output = Path("output") / download_name
    stable_output.parent.mkdir(exist_ok=True)

    options = ConvertOptions(
        horizontal=horizontal,
        furigana=furigana,
        font_size=font_size,
        line_height=line_height,
    )
    try:
        with TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            input_path = tmpdir / file.filename
            output_path = tmpdir / download_name
            input_path.write_bytes(await file.read())
            convert_file(input_path, output_path, options)
            stable_output.write_bytes(output_path.read_bytes())
    except NotImplementedError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {exc}") from exc

    return FileResponse(stable_output, filename=download_name)


def main() -> None:
    import uvicorn

    uvicorn.run(
        "jp_ebook_pipeline.server:app",
        host="127.0.0.1",
        port=8765,
        reload=False,
    )
