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
<html lang="ja">
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
      width: min(980px, calc(100vw - 32px));
      margin: 34px auto 56px;
    }
    .intro {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 280px;
      gap: 28px;
      align-items: center;
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
    .tagline {
      max-width: 650px;
      font-size: 17px;
    }
    .format-note {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      margin-top: 12px;
      padding: 8px 10px;
      border: 1px solid #d7d0bf;
      border-radius: 7px;
      color: #3b3d38;
      background: #fffdf8;
      font-size: 14px;
    }
    .format-note strong {
      white-space: nowrap;
    }
    .format-note code {
      color: #183f33;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 13px;
      overflow-wrap: anywhere;
    }
    .visual-panel {
      overflow: hidden;
      border: 1px solid #c9c2b2;
      border-radius: 8px;
      background: #fffdf8;
      transform: translateZ(0);
    }
    .visual-panel svg {
      display: block;
      width: 100%;
      height: auto;
    }
    .preview-arrow,
    .preview-arrow-head,
    .preview-line,
    .preview-highlight {
      transform-box: fill-box;
      transform-origin: center;
    }
    .preview-line {
      stroke-dasharray: 18 9;
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
      transition: background-color 160ms ease, box-shadow 160ms ease, transform 160ms ease;
    }
    button:hover {
      background: #1f4f3e;
      box-shadow: 0 8px 18px rgba(36, 91, 71, 0.18);
      transform: translateY(-1px);
    }
    button:active {
      transform: translateY(0);
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
      transition: background-color 160ms ease, border-color 160ms ease, transform 160ms ease;
    }
    .links a:hover {
      border-color: #b7c9c0;
      background: #f3f8f5;
      transform: translateY(-1px);
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
      .intro, .grid, .links { grid-template-columns: 1fr; }
      .visual-panel { max-width: 340px; }
      .format-note {
        display: grid;
        gap: 4px;
        justify-items: start;
      }
      h1 { font-size: 25px; }
    }
    @media (prefers-reduced-motion: no-preference) {
      .intro > div {
        animation: riseIn 520ms ease both;
      }
      .visual-panel {
        animation: riseIn 620ms ease 80ms both, gentleFloat 5.5s ease-in-out 900ms infinite;
      }
      form {
        animation: riseIn 520ms ease 140ms both;
      }
      .preview-arrow,
      .preview-arrow-head {
        animation: arrowPulse 1.9s ease-in-out infinite;
      }
      .preview-line {
        animation: lineFlow 3.2s linear infinite;
      }
      .preview-highlight {
        animation: softBlink 2.4s ease-in-out infinite;
      }
    }
    @media (prefers-reduced-motion: reduce) {
      *,
      *::before,
      *::after {
        animation-duration: 0.001ms !important;
        animation-iteration-count: 1 !important;
        scroll-behavior: auto !important;
        transition-duration: 0.001ms !important;
      }
    }
    @keyframes riseIn {
      from {
        opacity: 0;
        transform: translateY(8px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
    @keyframes gentleFloat {
      0%, 100% {
        transform: translateY(0);
      }
      50% {
        transform: translateY(-4px);
      }
    }
    @keyframes arrowPulse {
      0%, 100% {
        opacity: 0.7;
        transform: translateX(0);
      }
      50% {
        opacity: 1;
        transform: translateX(7px);
      }
    }
    @keyframes lineFlow {
      from {
        stroke-dashoffset: 0;
      }
      to {
        stroke-dashoffset: -54;
      }
    }
    @keyframes softBlink {
      0%, 100% {
        opacity: 0.55;
      }
      50% {
        opacity: 1;
      }
    }
  </style>
</head>
<body>
  <main>
    <section class="intro" aria-label="YomiEpub Studio">
      <div>
        <h1>YomiEpub Studio</h1>
        <p class="tagline">ローカルの縦書き・ふりがななしの日本語 EPUB、TXT、HTML を、横書き・ふりがな付き・KOReader 向け EPUB に変換します。</p>
        <p class="format-note"><strong>生成ファイル名</strong><code>【書名（作者）Yomi.epub】</code></p>
      </div>
      <figure class="visual-panel" aria-label="横書きふりがなプレビュー">
        <svg viewBox="0 0 560 360" role="img" aria-labelledby="preview-title" xmlns="http://www.w3.org/2000/svg">
          <title id="preview-title">YomiEpub 横書きふりがなプレビュー</title>
          <rect width="560" height="360" fill="#fffdf8"/>
          <rect x="40" y="36" width="196" height="288" rx="8" fill="#f3efe5" stroke="#cbc2b0" stroke-width="3"/>
          <rect x="324" y="36" width="196" height="288" rx="8" fill="#f7fbff" stroke="#b9c7d9" stroke-width="3"/>
          <text x="80" y="92" fill="#5f5750" font-family="Georgia, serif" font-size="34" writing-mode="tb">阪急電車</text>
          <text x="148" y="92" fill="#5f5750" font-family="Georgia, serif" font-size="26" writing-mode="tb">宝塚駅</text>
          <path class="preview-arrow" d="M260 176h38" stroke="#245b47" stroke-width="6" stroke-linecap="round"/>
          <path class="preview-arrow-head" d="M294 160l24 16-24 16" fill="none" stroke="#245b47" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
          <text x="358" y="98" fill="#7d6a43" font-family="Georgia, serif" font-size="15">はんきゅう</text>
          <text x="360" y="126" fill="#202124" font-family="Georgia, serif" font-size="36">阪急</text>
          <text x="430" y="98" fill="#7d6a43" font-family="Georgia, serif" font-size="15">でんしゃ</text>
          <text x="432" y="126" fill="#202124" font-family="Georgia, serif" font-size="36">電車</text>
          <line class="preview-line" x1="356" y1="164" x2="488" y2="164" stroke="#cfc8b9" stroke-width="3"/>
          <line class="preview-line" x1="356" y1="198" x2="486" y2="198" stroke="#cfc8b9" stroke-width="3"/>
          <line class="preview-line" x1="356" y1="232" x2="472" y2="232" stroke="#cfc8b9" stroke-width="3"/>
          <rect class="preview-highlight" x="356" y="262" width="96" height="20" rx="4" fill="#d6e5de"/>
        </svg>
      </figure>
    </section>

    <form id="convert-form">
      <fieldset>
        <legend>ファイルを選択</legend>
        <input id="file" name="file" type="file" accept=".epub,.txt,.html,.xhtml,.htm" required />
        <section class="source-links" aria-label="Legal source links">
          <h2>合法・パブリックドメインの日本語テキスト</h2>
          <p>本ツールは電子書籍のダウンロード、海賊版検索、DRM 解除を行いません。利用権のあるローカルファイルだけを処理してください。</p>
          <div class="links">
            <a href="https://www.aozora.gr.jp/" target="_blank" rel="noreferrer">
              <strong>青空文庫</strong>
              <span>日本語のパブリックドメイン作品と公開作品</span>
            </a>
            <a href="https://www.gutenberg.org/browse/languages/ja" target="_blank" rel="noreferrer">
              <strong>Project Gutenberg JP</strong>
              <span>Project Gutenberg の日本語カテゴリ</span>
            </a>
            <a href="https://wikisource.org/wiki/Wikisource:About_Wikisource/ja" target="_blank" rel="noreferrer">
              <strong>Wikisource</strong>
              <span>パブリックドメイン・自由ライセンスの資料</span>
            </a>
            <a href="https://dl.ndl.go.jp/" target="_blank" rel="noreferrer">
              <strong>国立国会図書館</strong>
              <span>国立国会図書館デジタルコレクション</span>
            </a>
            <a href="https://syosetu.com/" target="_blank" rel="noreferrer">
              <strong>小説家になろう</strong>
              <span>投稿作品。サイト規約を確認してください</span>
            </a>
            <a href="https://kakuyomu.jp/" target="_blank" rel="noreferrer">
              <strong>カクヨム</strong>
              <span>投稿作品。サイト規約を確認してください</span>
            </a>
          </div>
        </section>
      </fieldset>

      <fieldset>
        <legend>変換オプション</legend>
        <div class="grid">
          <label><input name="horizontal" type="checkbox" checked /> 横書きに変換</label>
          <label><input name="furigana" type="checkbox" checked /> ふりがなを追加</label>
          <label>文字サイズ <input name="font_size" type="text" value="1.08em" /></label>
          <label>行間 <input name="line_height" type="text" value="1.9" /></label>
        </div>
      </fieldset>

      <div class="actions">
        <button id="submit" type="submit">変換して EPUB をダウンロード</button>
        <span id="status"></span>
      </div>
    </form>

    <p class="note">すべての処理はこの端末内で完了します。ファイルはクラウドにアップロードされません。ダウンロード後、EPUB を KOReader に転送して開いてください。</p>
  </main>

  <script>
    const form = document.getElementById("convert-form");
    const status = document.getElementById("status");
    const submit = document.getElementById("submit");

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const data = new FormData(form);
      status.textContent = "変換中...";
      submit.disabled = true;
      try {
        const response = await fetch("/convert", { method: "POST", body: data });
        if (!response.ok) {
          const text = await response.text();
          throw new Error(text || "変換に失敗しました");
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
        status.textContent = "完了しました。ブラウザのダウンロードフォルダを確認してください。";
      } catch (error) {
        status.textContent = error.message || "変換に失敗しました";
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
        raise HTTPException(status_code=400, detail="ファイルを選択してください。")

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
        raise HTTPException(status_code=500, detail=f"変換に失敗しました: {exc}") from exc

    return FileResponse(stable_output, filename=download_name)


def main() -> None:
    import uvicorn

    uvicorn.run(
        "jp_ebook_pipeline.server:app",
        host="127.0.0.1",
        port=8765,
        reload=False,
    )
