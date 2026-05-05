"""
gui.py - YouTube AI Uploader GUI
Usage: python gui.py
Requires: pip install tkinter (usually built-in)
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import importlib

# --- try imports ---
try:
    from api_manager import APIManager
    HAS_API = True
except ImportError:
    HAS_API = False

try:
    from uploader import upload_video
    HAS_UPLOADER = True
except ImportError:
    HAS_UPLOADER = False


# ─────────────────────────────────────────────────────────
# COLORS & FONTS
# ─────────────────────────────────────────────────────────
BG        = "#0d0d0d"
BG2       = "#141414"
BG3       = "#1c1c1c"
ACCENT    = "#00ff88"
ACCENT2   = "#00ccff"
MUTED     = "#444444"
TEXT      = "#e0e0e0"
TEXT_DIM  = "#666666"
RED       = "#ff4455"
YELLOW    = "#ffcc00"

FONT_MONO  = ("Courier New", 10)
FONT_TITLE = ("Courier New", 18, "bold")
FONT_LABEL = ("Courier New", 9)
FONT_SMALL = ("Courier New", 8)


# ─────────────────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube AI Uploader")
        self.geometry("900x700")
        self.minsize(800, 600)
        self.configure(bg=BG)
        self.resizable(True, True)

        self._build_ui()

    # ── BUILD ─────────────────────────────────────────────
    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=BG, pady=12)
        header.pack(fill="x", padx=20)
        tk.Label(header, text="▶ YouTube AI Uploader",
                 font=FONT_TITLE, fg=ACCENT, bg=BG).pack(side="left")
        tk.Label(header, text="v1.0",
                 font=FONT_SMALL, fg=TEXT_DIM, bg=BG).pack(side="left", padx=10, pady=4)

        # Separator
        tk.Frame(self, bg=MUTED, height=1).pack(fill="x", padx=20)

        # Notebook tabs
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab",
                        background=BG2, foreground=TEXT_DIM,
                        font=FONT_MONO, padding=[14, 6],
                        borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", BG3)],
                  foreground=[("selected", ACCENT)])

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=20, pady=12)

        self._tab_generate(nb)
        self._tab_upload(nb)
        self._tab_settings(nb)

        # Log
        tk.Frame(self, bg=MUTED, height=1).pack(fill="x", padx=20)
        self._build_log()

    # ── TAB: GENERATE ─────────────────────────────────────
    def _tab_generate(self, nb):
        f = tk.Frame(nb, bg=BG3)
        nb.add(f, text=" Generate ")

        self._label(f, "Topic / Prompt").pack(anchor="w", padx=16, pady=(14, 2))
        self.topic_var = tk.StringVar(value="The Future of Artificial Intelligence")
        self._entry(f, self.topic_var).pack(fill="x", padx=16)

        row = tk.Frame(f, bg=BG3)
        row.pack(fill="x", padx=16, pady=10)

        # AI Provider
        col1 = tk.Frame(row, bg=BG3)
        col1.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self._label(col1, "Text AI").pack(anchor="w")
        self.text_ai_var = tk.StringVar(value="auto")
        self._dropdown(col1, self.text_ai_var,
                       ["auto", "openai", "anthropic", "groq", "gemini"]).pack(fill="x")

        col2 = tk.Frame(row, bg=BG3)
        col2.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self._label(col2, "Voice AI").pack(anchor="w")
        self.voice_ai_var = tk.StringVar(value="auto")
        self._dropdown(col2, self.voice_ai_var,
                       ["auto", "elevenlab", "openai", "pyttsx3"]).pack(fill="x")

        col3 = tk.Frame(row, bg=BG3)
        col3.pack(side="left", fill="x", expand=True)
        self._label(col3, "Image AI").pack(anchor="w")
        self.image_ai_var = tk.StringVar(value="auto")
        self._dropdown(col3, self.image_ai_var,
                       ["auto", "stability", "openai", "replicate"]).pack(fill="x")

        # Output files
        row2 = tk.Frame(f, bg=BG3)
        row2.pack(fill="x", padx=16, pady=(0, 10))

        c1 = tk.Frame(row2, bg=BG3)
        c1.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self._label(c1, "Audio output").pack(anchor="w")
        self.audio_out_var = tk.StringVar(value="audio.mp3")
        self._entry(c1, self.audio_out_var).pack(fill="x")

        c2 = tk.Frame(row2, bg=BG3)
        c2.pack(side="left", fill="x", expand=True)
        self._label(c2, "Thumbnail output").pack(anchor="w")
        self.img_out_var = tk.StringVar(value="thumbnail.png")
        self._entry(c2, self.img_out_var).pack(fill="x")

        # Checkboxes
        crow = tk.Frame(f, bg=BG3)
        crow.pack(fill="x", padx=16, pady=4)
        self.gen_script_var = tk.BooleanVar(value=True)
        self.gen_voice_var  = tk.BooleanVar(value=True)
        self.gen_image_var  = tk.BooleanVar(value=True)
        for var, label in [(self.gen_script_var, "Script"),
                           (self.gen_voice_var,  "Voice"),
                           (self.gen_image_var,  "Thumbnail")]:
            cb = tk.Checkbutton(crow, text=label, variable=var,
                                bg=BG3, fg=TEXT, selectcolor=BG,
                                activebackground=BG3, activeforeground=ACCENT,
                                font=FONT_MONO, cursor="hand2")
            cb.pack(side="left", padx=8)

        # Run button
        self._btn(f, "⚡ RUN GENERATE", self._run_generate).pack(padx=16, pady=12, anchor="w")

        # Script preview
        self._label(f, "Generated Script").pack(anchor="w", padx=16, pady=(4, 2))
        self.script_box = scrolledtext.ScrolledText(
            f, height=6, bg=BG2, fg=ACCENT,
            insertbackground=ACCENT, font=FONT_MONO,
            relief="flat", bd=0, wrap="word")
        self.script_box.pack(fill="both", expand=True, padx=16, pady=(0, 14))

    # ── TAB: UPLOAD ────────────────────────────────────────
    def _tab_upload(self, nb):
        f = tk.Frame(nb, bg=BG3)
        nb.add(f, text=" Upload ")

        self._label(f, "Video File").pack(anchor="w", padx=16, pady=(14, 2))
        vrow = tk.Frame(f, bg=BG3)
        vrow.pack(fill="x", padx=16)
        self.video_var = tk.StringVar(value="video.mp4")
        self._entry(vrow, self.video_var).pack(side="left", fill="x", expand=True)
        self._btn(vrow, "Browse", self._browse_video, small=True).pack(side="left", padx=(6, 0))

        self._label(f, "Title").pack(anchor="w", padx=16, pady=(10, 2))
        self.title_var = tk.StringVar(value="My AI Video")
        self._entry(f, self.title_var).pack(fill="x", padx=16)

        self._label(f, "Description").pack(anchor="w", padx=16, pady=(10, 2))
        self.desc_box = tk.Text(f, height=4, bg=BG2, fg=TEXT,
                                insertbackground=ACCENT, font=FONT_MONO,
                                relief="flat", bd=4)
        self.desc_box.pack(fill="x", padx=16)
        self.desc_box.insert("1.0", "Auto-generated video.")

        row = tk.Frame(f, bg=BG3)
        row.pack(fill="x", padx=16, pady=10)

        c1 = tk.Frame(row, bg=BG3)
        c1.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self._label(c1, "Tags (comma separated)").pack(anchor="w")
        self.tags_var = tk.StringVar(value="ai, automation, youtube")
        self._entry(c1, self.tags_var).pack(fill="x")

        c2 = tk.Frame(row, bg=BG3)
        c2.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self._label(c2, "Category ID").pack(anchor="w")
        self.cat_var = tk.StringVar(value="27")
        self._entry(c2, self.cat_var).pack(fill="x")

        c3 = tk.Frame(row, bg=BG3)
        c3.pack(side="left", fill="x", expand=True)
        self._label(c3, "Privacy").pack(anchor="w")
        self.privacy_var = tk.StringVar(value="public")
        self._dropdown(c3, self.privacy_var, ["public", "unlisted", "private"]).pack(fill="x")

        tk.Frame(f, bg=MUTED, height=1).pack(fill="x", padx=16, pady=8)

        brow = tk.Frame(f, bg=BG3)
        brow.pack(fill="x", padx=16, pady=4)
        self._btn(brow, "📋 Use Generated Script", self._use_script, small=True).pack(side="left", padx=(0, 8))
        self._btn(brow, "▲ UPLOAD TO YOUTUBE", self._run_upload).pack(side="left")

    # ── TAB: SETTINGS ─────────────────────────────────────
    def _tab_settings(self, nb):
        f = tk.Frame(nb, bg=BG3)
        nb.add(f, text=" Settings ")

        canvas = tk.Canvas(f, bg=BG3, highlightthickness=0)
        scroll = ttk.Scrollbar(f, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=BG3)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        keys = [
            ("OPENAI_API_KEY",     "OpenAI API Key",          "sk-..."),
            ("ANTHROPIC_API_KEY",  "Anthropic API Key",       "sk-ant-..."),
            ("GROQ_API_KEY",       "Groq API Key",            "gsk_..."),
            ("GEMINI_API_KEY",     "Gemini API Key",          "..."),
            ("ELEVENLAB_API_KEY",  "ElevenLabs API Key",      "..."),
            ("ELEVENLAB_VOICE_ID", "ElevenLabs Voice ID",     "21m00Tcm4TlvDq8ikWAM"),
            ("STABILITY_API_KEY",  "Stability AI Key",        "sk-..."),
            ("REPLICATE_API_KEY",  "Replicate API Key",       "r8_..."),
        ]

        self.key_vars = {}
        for env_key, label, placeholder in keys:
            self._label(inner, label).pack(anchor="w", padx=16, pady=(10, 2))
            var = tk.StringVar(value=os.getenv(env_key, ""))
            show = "*" if "KEY" in env_key else ""
            e = self._entry(inner, var, show=show)
            e.pack(fill="x", padx=16)
            self.key_vars[env_key] = var

        brow = tk.Frame(inner, bg=BG3)
        brow.pack(fill="x", padx=16, pady=16)
        self._btn(brow, "💾 Save to .env", self._save_env).pack(side="left", padx=(0, 8))
        self._btn(brow, "🔍 Check Status", self._check_status, small=True).pack(side="left")

    # ── LOG ───────────────────────────────────────────────
    def _build_log(self):
        lf = tk.Frame(self, bg=BG)
        lf.pack(fill="x", padx=20, pady=(6, 12))
        tk.Label(lf, text="LOG", font=FONT_SMALL, fg=TEXT_DIM, bg=BG).pack(anchor="w")
        self.log_box = scrolledtext.ScrolledText(
            lf, height=5, bg=BG2, fg=TEXT_DIM,
            insertbackground=ACCENT, font=FONT_SMALL,
            relief="flat", bd=0, state="disabled")
        self.log_box.pack(fill="x")

    # ── ACTIONS ───────────────────────────────────────────
    def _run_generate(self):
        threading.Thread(target=self._generate_worker, daemon=True).start()

    def _generate_worker(self):
        if not HAS_API:
            self._log("❌ api_manager.py not found", RED); return

        topic = self.topic_var.get().strip()
        if not topic:
            self._log("❌ No topic entered", RED); return

        if self.gen_script_var.get():
            prefer = self.text_ai_var.get()
            if prefer == "auto": prefer = None
            self._log(f"📝 Generating script ({prefer or 'auto'})...")
            script = APIManager.generate_text(
                f"Write a short 1-minute YouTube video script about: {topic}.",
                prefer=prefer)
            if script.startswith("❌"):
                self._log(script, RED)
            else:
                self.script_box.delete("1.0", "end")
                self.script_box.insert("1.0", script)
                self._log(f"✅ Script done ({len(script)} chars)", ACCENT)

        if self.gen_voice_var.get():
            prefer = self.voice_ai_var.get()
            if prefer == "auto": prefer = None
            self._log(f"🎙️ Generating voice ({prefer or 'auto'})...")
            result = APIManager.generate_voice(
                self.script_box.get("1.0", "end").strip(),
                self.audio_out_var.get(),
                prefer=prefer)
            self._log(result, ACCENT if result.startswith("✅") else RED)

        if self.gen_image_var.get():
            prefer = self.image_ai_var.get()
            if prefer == "auto": prefer = None
            self._log(f"🖼️ Generating thumbnail ({prefer or 'auto'})...")
            result = APIManager.generate_image(
                f"YouTube thumbnail: {topic}",
                self.img_out_var.get(),
                prefer=prefer)
            self._log(result, ACCENT if result.startswith("✅") else RED)

    def _run_upload(self):
        threading.Thread(target=self._upload_worker, daemon=True).start()

    def _upload_worker(self):
        if not HAS_UPLOADER:
            self._log("❌ uploader.py not found", RED); return
        video = self.video_var.get().strip()
        if not os.path.exists(video):
            self._log(f"❌ File not found: {video}", RED); return

        self._log(f"📤 Uploading '{video}'...")
        tags = [t.strip() for t in self.tags_var.get().split(",") if t.strip()]
        desc = self.desc_box.get("1.0", "end").strip()

        try:
            result = upload_video(
                file_path=video,
                title=self.title_var.get(),
                description=desc,
                tags=tags,
                category_id=self.cat_var.get()
            )
            vid_id = result.get("id", "?") if result else "?"
            self._log(f"✅ Uploaded: https://youtu.be/{vid_id}", ACCENT)
        except Exception as e:
            self._log(f"❌ Upload failed: {e}", RED)

    def _use_script(self):
        script = self.script_box.get("1.0", "end").strip()
        if script:
            self.desc_box.delete("1.0", "end")
            self.desc_box.insert("1.0", script)
            self.title_var.set(self.topic_var.get())
            self._log("📋 Script copied to upload tab", ACCENT2)

    def _save_env(self):
        lines = []
        for key, var in self.key_vars.items():
            val = var.get().strip()
            if val:
                lines.append(f"{key}={val}")
        with open(".env", "w") as f:
            f.write("\n".join(lines) + "\n")
        self._log("💾 Saved to .env", ACCENT)

    def _check_status(self):
        if HAS_API:
            self._log("🔍 Checking API status...")
            APIManager.status()
            self._log("✅ Check complete (see terminal for details)", ACCENT2)
        else:
            self._log("❌ api_manager.py not found", RED)

    def _browse_video(self):
        path = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4 *.mkv *.avi *.mov"), ("All", "*.*")])
        if path:
            self.video_var.set(path)

    def _log(self, msg, color=TEXT):
        def _do():
            self.log_box.config(state="normal")
            self.log_box.insert("end", msg + "\n")
            self.log_box.see("end")
            self.log_box.config(state="disabled")
        self.after(0, _do)

    # ── WIDGETS ───────────────────────────────────────────
    def _label(self, parent, text):
        return tk.Label(parent, text=text, font=FONT_LABEL,
                        fg=TEXT_DIM, bg=parent["bg"])

    def _entry(self, parent, var, show=""):
        return tk.Entry(parent, textvariable=var, show=show,
                        bg=BG2, fg=TEXT, insertbackground=ACCENT,
                        font=FONT_MONO, relief="flat", bd=6,
                        highlightthickness=1,
                        highlightcolor=ACCENT,
                        highlightbackground=MUTED)

    def _btn(self, parent, text, cmd, small=False):
        font = FONT_SMALL if small else FONT_MONO
        fg   = TEXT_DIM if small else BG
        bg   = BG2 if small else ACCENT
        abg  = BG3 if small else "#00cc66"
        return tk.Button(parent, text=text, command=cmd,
                         bg=bg, fg=fg, activebackground=abg,
                         activeforeground=fg, font=font,
                         relief="flat", bd=0, padx=12, pady=6,
                         cursor="hand2")

    def _dropdown(self, parent, var, options):
        style = ttk.Style()
        style.configure("Dark.TCombobox",
                        fieldbackground=BG2,
                        background=BG2,
                        foreground=TEXT,
                        arrowcolor=ACCENT,
                        borderwidth=0)
        cb = ttk.Combobox(parent, textvariable=var, values=options,
                          style="Dark.TCombobox", font=FONT_MONO,
                          state="readonly")
        return cb


# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
