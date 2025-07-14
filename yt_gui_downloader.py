import tkinter as tk
from tkinter import messagebox, simpledialog
import yt_dlp


class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("500x300")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="YouTube Video URL:").pack(pady=10)
        self.url_entry = tk.Entry(self.root, width=60)
        self.url_entry.pack()

        self.fetch_btn = tk.Button(self.root, text="Fetch Formats", command=self.fetch_formats)
        self.fetch_btn.pack(pady=5)

        # Frame to hold listbox + scrollbar
        list_frame = tk.Frame(self.root)
        list_frame.pack(pady=10, expand=True)

        # Add scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add listbox and connect scrollbar
        self.format_listbox = tk.Listbox(list_frame, width=70, height=10, yscrollcommand=scrollbar.set)
        self.format_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar.config(command=self.format_listbox.yview)

        self.download_btn = tk.Button(self.root, text="Download Selected Format", command=self.download_video)
        self.download_btn.pack()

    def fetch_formats(self):
        self.format_listbox.delete(0, tk.END)
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a valid YouTube URL.")
            return

        try:
            with yt_dlp.YoutubeDL() as ydl:
                self.info = ydl.extract_info(url, download=False)
                self.formats = self.info.get("formats", [])
                self.format_map = {}

                for f in self.formats:
                    fid = f.get("format_id")
                    ext = f.get("ext")
                    height = f.get("height")
                    acodec = f.get("acodec")
                    vcodec = f.get("vcodec")
                    abr = f.get("abr", None)

                    # Determine stream type
                    if vcodec != "none" and acodec != "none":
                        stream_type = "Video + Audio"
                    elif vcodec != "none":
                        stream_type = "Video only"
                    elif acodec != "none":
                        stream_type = "Audio only"
                    else:
                        stream_type = "Unknown"

                    # Build resolution or audio quality
                    quality = f"{height}p" if height else f"{int(abr)} kbps" if abr else "N/A"

                    # Final human-readable string
                    display = f"[{fid}] {ext} - {quality} - {stream_type}"
                    self.format_listbox.insert(tk.END, display)
                    self.format_map[display] = fid

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch formats:\n{e}")

    def download_video(self):
        selected = self.format_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a format.")
            return

        choice = self.format_listbox.get(selected[0])
        fmt = self.format_map.get(choice)
        url = self.url_entry.get().strip()

        # Extract format info
        selected_format = next((f for f in self.formats if f.get("format_id") == fmt), None)
        if not selected_format:
            messagebox.showerror("Error", "Selected format not found.")
            return

        acodec = selected_format.get("acodec")
        vcodec = selected_format.get("vcodec")

        # Auto-merge if needed (video-only or audio-only)
        if vcodec != "none" and acodec == "none":
            # This is a video-only stream: merge with best audio
            ydl_format = f"{fmt}+bestaudio"
        elif vcodec == "none" and acodec != "none":
            # Audio-only stream
            ydl_format = fmt
        else:
            # Video + Audio combined
            ydl_format = fmt

        ydl_opts = {
            'format': ydl_format,
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegMerger'
            }]
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                messagebox.showinfo("Done", "Download complete!")
        except Exception as e:
            messagebox.showerror("Error", f"Download failed:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()
