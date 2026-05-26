import React from "react";
import { Download, FileUp, Settings } from "lucide-react";
import { createRoot } from "react-dom/client";
import "./styles.css";

function App() {
  return (
    <main className="shell">
      <section className="toolbar" aria-label="Conversion controls">
        <label className="upload">
          <FileUp size={18} />
          <span>Select EPUB/TXT/HTML</span>
          <input type="file" accept=".epub,.txt,.html,.xhtml" />
        </label>
        <button type="button">
          <Settings size={18} />
          <span>Options</span>
        </button>
        <button type="button" className="primary">
          <Download size={18} />
          <span>Download EPUB</span>
        </button>
      </section>

      <section className="panel">
        <div>
          <h1>JP Ebook Furigana Pipeline</h1>
          <p>CLI-first MVP. Web conversion flow will connect to the FastAPI backend.</p>
        </div>
        <div className="options">
          <label><input type="checkbox" defaultChecked /> Horizontal layout</label>
          <label><input type="checkbox" /> Add furigana</label>
          <label><input type="checkbox" disabled /> Bilingual layout</label>
        </div>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);

