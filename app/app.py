import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import cv2

from comics_generator import generate_video
from settings import PREVIEW_TEMP_FILE

def preview_video(lines):
    progress_window = tk.Toplevel()
    progress_window.title("Generating Preview")
    progress = ttk.Progressbar(progress_window, mode='determinate')
    progress.pack(pady=20, padx=20)
    progress_window.update()

    generate_video(lines, PREVIEW_TEMP_FILE.name, progress)
    progress_window.destroy()

    cap = cv2.VideoCapture(PREVIEW_TEMP_FILE.name)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Preview', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def save_video(lines):
    save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if save_path:
        progress_window = tk.Toplevel()
        progress_window.title("Saving Video")
        progress = ttk.Progressbar(progress_window, mode='determinate')
        progress.pack(pady=20, padx=20)
        progress_window.update()

        generate_video(lines, PREVIEW_TEMP_FILE.name, progress)
        shutil.copy(PREVIEW_TEMP_FILE.name, save_path)
        progress_window.destroy()

        messagebox.showinfo("Success", f"Video saved to {save_path}")

def main():
    root = tk.Tk()
    root.title("Comics Video Generator")

    lines = []

    def add_line():
        line = entry.get()
        if line:
            lines.append(line)
            listbox.insert(tk.END, line)
            entry.delete(0, tk.END)

    frame = tk.Frame(root)
    frame.pack(pady=10)

    entry = tk.Entry(frame, width=50)
    entry.pack(side=tk.LEFT, padx=5)

    add_button = tk.Button(frame, text="Add Line", command=add_line)
    add_button.pack(side=tk.LEFT, padx=5)

    listbox = tk.Listbox(root, width=60, height=10)
    listbox.pack(pady=10)

    preview_button = tk.Button(root, text="Preview Video", command=lambda: preview_video(lines))
    preview_button.pack(pady=5)

    save_button = tk.Button(root, text="Save Video", command=lambda: save_video(lines))
    save_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()