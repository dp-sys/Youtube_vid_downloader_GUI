import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import threading
import os
import glob
import sys

class YouTubeDownloader:
    def __init__(self):
        self.formats_data = []
        self.video_formats = []
        self.audio_formats = []
        self.download_folder = os.path.join(os.path.expanduser("~"), "Videos")
        
        # Setup paths to yt-dlp and ffmpeg
        self.setup_executable_paths()
        self.setup_gui()
    
    def setup_executable_paths(self):
        """Set up paths for yt-dlp and ffmpeg"""
        if os.path.exists("C:\\YT-dlp-GUI\\yt-dlp.exe"):
            self.ytdlp_path = "C:\\YT-dlp-GUI\\yt-dlp.exe"
            self.ffmpeg_path = "C:\\YT-dlp-GUI\\ffmpeg.exe"
        else:
            self.ytdlp_path = "yt-dlp"
            self.ffmpeg_path = "ffmpeg"
        
        # Check if yt-dlp and ffmpeg are usable
        try:
            subprocess.run([self.ytdlp_path, '--version'], capture_output=True, check=True)
            subprocess.run([self.ffmpeg_path, '-version'], capture_output=True, check=True)
        except:
            messagebox.showerror("Missing Dependencies", "yt-dlp or ffmpeg not found.\nPlease reinstall YouTube Downloader GUI.")
            sys.exit(1)

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("YouTube Downloader GUI v1.0 - By Lord Mariappan")
        self.root.geometry("1000x450")
        self.root.configure(bg="#1e1e1e")

        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.entry_bg = "#2d2d2d"
        self.btn_bg = "#3a3a3a"
        self.btn_fg = "#ffffff"

        self.create_widgets()

    def create_widgets(self):
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(padx=10, pady=(10, 5), fill="x")
        
        tk.Label(title_frame, text="YouTube Downloader GUI", font=("Arial", 16, "bold"), bg=self.bg_color, fg="#007acc").pack(side="left")
        tk.Label(title_frame, text="v1.0 - By Lord Mariappan", font=("Arial", 10), bg=self.bg_color, fg="#888888").pack(side="right")

        top_frame = tk.Frame(self.root, bg=self.bg_color)
        top_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(top_frame, text="Video URL:", bg=self.bg_color, fg=self.fg_color).pack(side="left", padx=(0, 5))
        self.url_entry = tk.Entry(top_frame, width=50, bg=self.entry_bg, fg=self.fg_color, insertbackground=self.fg_color, relief="flat")
        self.url_entry.pack(side="left", padx=(0, 5))

        tk.Button(top_frame, text="Paste", command=self.paste_url, bg="#ff6b35", fg=self.btn_fg, relief="flat", width=8).pack(side="left", padx=(0, 5))
        tk.Button(top_frame, text="Analyze", command=self.analyze_formats, bg="#007acc", fg=self.btn_fg, relief="flat", width=12).pack(side="left")

        self.dropdown_frame = tk.Frame(self.root, bg=self.bg_color)
        self.dropdown_frame.pack(padx=10, pady=10, fill="x")

        video_frame = tk.Frame(self.dropdown_frame, bg=self.bg_color)
        video_frame.pack(side="left", padx=(0, 20))
        tk.Label(video_frame, text="Video Formats:", bg=self.bg_color, fg=self.fg_color).pack(anchor="w")
        self.video_var = tk.StringVar()
        self.video_dropdown = ttk.Combobox(video_frame, textvariable=self.video_var, width=40, state="readonly")
        self.video_dropdown.pack(pady=(5, 0))

        audio_frame = tk.Frame(self.dropdown_frame, bg=self.bg_color)
        audio_frame.pack(side="left")
        tk.Label(audio_frame, text="Audio Formats:", bg=self.bg_color, fg=self.fg_color).pack(anchor="w")
        self.audio_var = tk.StringVar()
        self.audio_dropdown = ttk.Combobox(audio_frame, textvariable=self.audio_var, width=25, state="readonly")
        self.audio_dropdown.pack(pady=(5, 0))

        self.dropdown_frame.pack_forget()

        self.folder_frame = tk.Frame(self.root, bg=self.bg_color)
        tk.Label(self.folder_frame, text="Download Folder:", bg=self.bg_color, fg=self.fg_color).pack(side="left", padx=(0, 5))
        self.folder_entry = tk.Entry(self.folder_frame, width=60, bg=self.entry_bg, fg=self.fg_color, insertbackground=self.fg_color, relief="flat")
        self.folder_entry.pack(side="left", padx=(0, 5))
        self.folder_entry.insert(0, self.download_folder)
        tk.Button(self.folder_frame, text="Browse", command=self.browse_folder, bg="#6c5ce7", fg=self.btn_fg, relief="flat", width=10).pack(side="left")

        self.download_btn = tk.Button(self.root, text="Download", command=self.download, bg="#00af66", fg=self.btn_fg, relief="flat", width=20)

        self.progress_label = tk.Label(self.root, text="Ready to download YouTube videos", bg=self.bg_color, fg=self.fg_color)
        self.progress_label.pack(pady=(10, 5))

        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=800, mode="determinate")
        self.progress_bar.pack(pady=(0, 10))

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TProgressbar", troughcolor="#2d2d2d", background="#007acc", bordercolor="#2d2d2d", lightcolor="#007acc", darkcolor="#007acc")

        footer_frame = tk.Frame(self.root, bg=self.bg_color)
        footer_frame.pack(side="bottom", fill="x", padx=10, pady=(0, 10))
        tk.Label(footer_frame, text="Installed at: C:\\YT-dlp-GUI\\", font=("Arial", 8), bg=self.bg_color, fg="#666666").pack(side="left")
        tk.Label(footer_frame, text="All executables added to PATH", font=("Arial", 8), bg=self.bg_color, fg="#666666").pack(side="right")

    def paste_url(self):
        try:
            clipboard_text = self.root.clipboard_get()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, clipboard_text)
        except:
            messagebox.showwarning("Clipboard Error", "Unable to paste from clipboard.")

    def browse_folder(self):
        folder_selected = filedialog.askdirectory(initialdir=self.download_folder, title="Select Download Folder")
        if folder_selected:
            self.download_folder = folder_selected
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_selected)

    def run_command(self, command, output_callback=None):
        command = command.replace('yt-dlp', self.ytdlp_path)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
        output_lines = []
        for line in process.stdout:
            output_lines.append(line.strip())
            if output_callback:
                output_callback(line.strip())
        process.wait()
        return output_lines

    def parse_formats(self, output_lines):
        self.formats_data = []
        self.video_formats = []
        self.audio_formats = []
        for line in output_lines:
            if not line or line.startswith('ID') or line.startswith('[') or line.startswith('-'):
                continue
            parts = line.split()
            if len(parts) < 4:
                continue
            format_id = parts[0]
            ext = parts[1]
            resolution = parts[2] if len(parts) > 2 else 'N/A'
            fps = 'N/A'
            filesize = 'N/A'
            for part in parts:
                if 'fps' in part:
                    fps = part.replace('fps', '').strip()
                elif 'MiB' in part or 'GiB' in part or 'KiB' in part:
                    filesize = part
            format_data = {'id': format_id, 'ext': ext, 'resolution': resolution, 'fps': fps, 'filesize': filesize, 'full_line': line}
            self.formats_data.append(format_data)
            if resolution != 'audio' and 'video' in line.lower():
                fps_display = fps if fps != 'N/A' else '60'
                display_text = f"{resolution} @ {fps_display}fps - {filesize}"
                self.video_formats.append({'display': display_text, 'id': format_id})
            elif resolution == 'audio' or 'audio' in line.lower():
                display_text = f"{filesize}"
                self.audio_formats.append({'display': display_text, 'id': format_id})

    def analyze_formats(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Input Required", "Enter the video URL first.")
            return
        self.progress_bar["value"] = 0
        self.progress_label["text"] = "Analyzing formats..."
        self.dropdown_frame.pack_forget()
        self.folder_frame.pack_forget()
        self.download_btn.pack_forget()
        def analysis_complete():
            command = f'yt-dlp -F "{url}"'
            output_lines = self.run_command(command)
            self.parse_formats(output_lines)
            video_display_list = [item['display'] for item in self.video_formats]
            audio_display_list = [item['display'] for item in self.audio_formats]
            self.video_dropdown['values'] = video_display_list
            self.audio_dropdown['values'] = audio_display_list
            if video_display_list:
                self.video_var.set(video_display_list[0])
            if audio_display_list:
                self.audio_var.set(audio_display_list[0])
            self.dropdown_frame.pack(padx=10, pady=10, fill="x")
            self.folder_frame.pack(padx=10, pady=10, fill="x")
            self.download_btn.pack(pady=10)
            self.progress_label["text"] = "Analysis complete. Select formats and download folder."
            self.progress_bar["value"] = 100
        threading.Thread(target=analysis_complete, daemon=True).start()

    def get_format_id_by_display(self, display_text, format_list):
        for item in format_list:
            if item['display'] == display_text:
                return item['id']
        return None

    def download(self):
        url = self.url_entry.get().strip()
        video_selection = self.video_var.get()
        audio_selection = self.audio_var.get()
        download_path = self.folder_entry.get().strip() or self.download_folder
        if not url:
            messagebox.showwarning("Missing Input", "Enter video URL.")
            return
        if not video_selection and not audio_selection:
            messagebox.showwarning("Missing Selection", "Select at least one format.")
            return
        video_id = self.get_format_id_by_display(video_selection, self.video_formats) if video_selection else None
        audio_id = self.get_format_id_by_display(audio_selection, self.audio_formats) if audio_selection else None
        format_code = f"{video_id}+{audio_id}" if video_id and audio_id else (video_id or audio_id)
        self.progress_bar["value"] = 0
        self.progress_label["text"] = "Starting download..."
        os.chdir(download_path)
        command = f'yt-dlp -f {format_code} --ffmpeg-location "{os.path.dirname(self.ffmpeg_path)}" --write-auto-subs --sub-lang en --convert-subs srt --embed-subs --remux-video mkv "{url}"'
        def update_progress(line):
            if "%" in line:
                try:
                    percent = float(line.split('%')[0].split()[-1])
                    self.progress_bar["value"] = percent
                    self.progress_label["text"] = f"Downloading... {percent:.1f}%"
                except:
                    pass
            elif "100%" in line or "Merger" in line or "Merging formats into" in line:
                self.progress_bar["value"] = 100
                self.progress_label["text"] = f"✅ Done. Saved to: {download_path}"
                self.root.after(2000, self.delete_subtitles)
        threading.Thread(target=self.run_command, args=(command, update_progress), daemon=True).start()

    def delete_subtitles(self):
        for ext in ("*.srt", "*.vtt"):
            for file in glob.glob(ext):
                try:
                    os.remove(file)
                except:
                    pass

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = YouTubeDownloader()
    app.run()
