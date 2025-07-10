import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import os
import glob

def run_command(command, output_callback=None):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
    for line in process.stdout:
        if output_callback:
            output_callback(line.strip())
    process.wait()

def analyze_formats():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Input Required", "Enter the video URL first.")
        return

    format_output.delete("1.0", tk.END)
    format_output.pack(padx=10, pady=(5, 0), fill="both", expand=True)
    progress_bar["value"] = 0
    progress_label["text"] = "Analyzing formats..."

    def update_output(line):
        format_output.insert(tk.END, line + "\n")
        format_output.see(tk.END)
        progress_label["text"] = "Analysis complete."

    command = f'yt-dlp -F "{url}"'
    threading.Thread(target=run_command, args=(command, update_output), daemon=True).start()

def download():
    url = url_entry.get().strip()
    fmt = format_entry.get().strip()

    if not url or not fmt:
        messagebox.showwarning("Missing Input", "Enter both URL and format code.")
        return

    format_output.pack_forget()
    progress_bar["value"] = 0
    progress_label["text"] = "Starting download..."

    command = f'yt-dlp -f {fmt} --write-auto-subs --sub-lang en --convert-subs srt --embed-subs --remux-video mkv "{url}"'

    def update_progress(line):
        if "%" in line:
            try:
                percent = float(line.split('%')[0].split()[-1])
                progress_bar["value"] = percent
                progress_label["text"] = f"Downloading... {percent:.1f}%"
            except:
                pass
        elif "100%" in line or "Merger" in line or "Merging formats into" in line:
            progress_bar["value"] = 100
            progress_label["text"] = "✅ Done. Output saved!"
            root.after(2000, delete_subtitles)

    threading.Thread(target=run_command, args=(command, update_progress), daemon=True).start()


def delete_subtitles():
    for ext in ("*.srt", "*.vtt"):
        for file in glob.glob(ext):
            try:
                os.remove(file)
            except:
                pass



    threading.Thread(target=run_command, args=(command, update_progress), daemon=True).start()

# ----- GUI SETUP -----
root = tk.Tk()
root.title("yt-dlp GUI Downloader")
root.geometry("1000x500")
root.configure(bg="#1e1e1e")

bg_color = "#1e1e1e"
fg_color = "#ffffff"
entry_bg = "#2d2d2d"
btn_bg = "#3a3a3a"
btn_fg = "#ffffff"

# ----- INPUT ROW 1 -----
top_frame = tk.Frame(root, bg=bg_color)
top_frame.pack(padx=10, pady=10, fill="x")

tk.Label(top_frame, text="Video URL:", bg=bg_color, fg=fg_color).pack(side="left", padx=(0, 5))
url_entry = tk.Entry(top_frame, width=70, bg=entry_bg, fg=fg_color, insertbackground=fg_color, relief="flat")
url_entry.pack(side="left", padx=(0, 5))

tk.Button(top_frame, text="Analyze", command=analyze_formats, bg="#007acc", fg=btn_fg, relief="flat", width=12).pack(side="left")

# ----- INPUT ROW 2 -----
second_frame = tk.Frame(root, bg=bg_color)
second_frame.pack(padx=10, pady=(0, 10), fill="x")

tk.Label(second_frame, text="Format Code:", bg=bg_color, fg=fg_color).pack(side="left", padx=(0, 5))
format_entry = tk.Entry(second_frame, width=30, bg=entry_bg, fg=fg_color, insertbackground=fg_color, relief="flat")
format_entry.pack(side="left", padx=(0, 10))

tk.Button(second_frame, text="Download", command=download, bg="#00af66", fg=btn_fg, relief="flat", width=20).pack(side="left")

# ----- FORMAT DISPLAY AREA (Hidden after download) -----
format_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, bg=entry_bg, fg=fg_color, insertbackground=fg_color)

# ----- PROGRESS BAR -----
progress_label = tk.Label(root, text="", bg=bg_color, fg=fg_color)
progress_label.pack(pady=(10, 5))

progress_bar = ttk.Progressbar(root, orient="horizontal", length=800, mode="determinate")
progress_bar.pack(pady=(0, 10))

style = ttk.Style()
style.theme_use("default")
style.configure("TProgressbar", troughcolor="#2d2d2d", background="#007acc", bordercolor="#2d2d2d", lightcolor="#007acc", darkcolor="#007acc")

root.mainloop()
