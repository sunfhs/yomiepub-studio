from __future__ import annotations

import re
from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse

from jp_ebook_pipeline.converter import convert_file
from jp_ebook_pipeline.models import ConvertOptions

app = FastAPI(title="YomiEpub Studio")

INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>YomiEpub Studio</title>
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
    fieldset, .source-links {
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
    .source-links {
      margin-top: 14px;
    }
    .source-links h2 {
      margin: 0 0 8px;
      font-size: 17px;
    }
    .source-links p {
      font-size: 14px;
    }
    .links {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
      margin-top: 12px;
    }
    .links a {
      display: block;
      min-height: 68px;
      padding: 10px;
      border: 1px solid #dedbd1;
      border-radius: 7px;
      color: #193f33;
      background: #fafaf8;
      text-decoration: none;
    }
    .links strong {
      display: block;
      margin-bottom: 4px;
      font-size: 14px;
    }
    .links span {
      display: block;
      color: #62645e;
      font-size: 12px;
      line-height: 1.35;
    }
    @media (max-width: 680px) {
      .grid, .links { grid-template-columns: 1fr; }
      h1 { font-size: 25px; }
    }
  </style>
</head>
<body>
  <main>
    <h1>YomiEpub Studio</h1>
    <p>把本地日文 EPUB、TXT 或 HTML 转成横排、带ふりがな、适合 KOReader 阅读的 EPUB。</p>

    <form id="convert-form">
      <fieldset>
        <legend>导入文件</legend>
        <input id="file" name="file" type="file" accept=".epub,.txt,.html,.xhtml,.htm" required />
        <section class="source-links" aria-label="Legal source links">
          <h2>合法/公版日文文本来源</h2>
          <p>本工具不提供电子书下载、盗版搜索或 DRM 移除。下面只是公开来源入口，请只处理你有权使用的文件。</p>
          <div class="links">
            <a href="https://www.aozora.gr.jp/" target="_blank" rel="noreferrer">
              <strong>青空文庫</strong>
              <span>日本公版文学与授权公开作品</span>
            </a>
            <a href="https://www.gutenberg.org/browse/languages/ja" target="_blank" rel="noreferrer">
              <strong>Project Gutenberg JP</strong>
              <span>Project Gutenberg 日文分类</span>
            </a>
            <a href="https://wikisource.org/wiki/Wikisource:About_Wikisource/ja" target="_blank" rel="noreferrer">
              <strong>Wikisource</strong>
              <span>公版或自由授权文本资料库</span>
            </a>
            <a href="https://dl.ndl.go.jp/" target="_blank" rel="noreferrer">
              <strong>国会图书馆</strong>
              <span>日本国立国会图书馆数字馆藏</span>
            </a>
            <a href="https://syosetu.com/" target="_blank" rel="noreferrer">
              <strong>小説家になろう</strong>
              <span>作者投稿小说，注意站内条款</span>
            </a>
            <a href="https://kakuyomu.jp/" target="_blank" rel="noreferrer">
              <strong>カクヨム</strong>
              <span>作者投稿小说，注意站内条款</span>
            </a>
          </div>
        </section>
      </fieldset>

      <fieldset>
        <legend>整理选项</legend>
        <div class="grid">
          <label><input name="horizontal" type="checkbox" checked /> 转成横排</label>
          <label><input name="furigana" type="checkbox" checked /> 添加ふりがな</label>
          <label>字号 <input name="font_size" type="text" value="1.08em" /></label>
          <label>行距 <input name="line_height" type="text" value="1.9" /></label>
        </div>
      </fieldset>

      <div class="actions">
        <button id="submit" type="submit">转换并下载 EPUB</button>
        <span id="status"></span>
      </div>
    </form>

    <p class="note">所有处理都在本机完成；文件不会上传到云端。</p>
  </main>

  <script>
    const form = document.getElementById("convert-form");
    const status = document.getElementById("status");
    const submit = document.getElementById("submit");

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const data = new FormData(form);
      status.textContent = "正在转换...";
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
        status.textContent = "完成。请查看浏览器下载目录。";
      } catch (error) {
        status.textContent = error.message || "转换失败";
      } finally {
        submit.disabled = false;
      }
    });
  </script>
</body>
</html>
"""


def output_filename(filename: str | None) -> str:
    raw = Path(filename or "converted").stem
    cleaned = re.sub(r"[\x00-\x1f\x7f/\\:]+", "", raw).strip()
    cleaned = re.sub(
        r"\s*\([^)]*(?:z-library|z-lib|1lib)[^)]*\)\s*$",
        "",
        cleaned,
        flags=re.IGNORECASE,
    ).strip()
    return f"{cleaned or 'converted'}Yomi.epub"


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

    download_name = output_filename(file.filename)
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
