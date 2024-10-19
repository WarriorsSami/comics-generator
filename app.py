import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os

TEXT_COLOR = (200, 200, 200)
TEXT_SIZE = 2
TEXT_THICKNESS = 7
FPS = 25
DURATION = 2.0
NUM_FRAMES = int(FPS * DURATION)
TEMP_PATH = 'assets/temp_preview.mp4'

def fade_in_out(background_img, overlay_img, mask, text_line, frame_buffer, progress, total_steps, step):
    for alpha in np.linspace(0, 1, NUM_FRAMES):
        bg_img = background_img.copy()
        bg_img[mask] = cv2.addWeighted(bg_img, 1-alpha, overlay_img, alpha, 0)[mask]

        if alpha >= 0.5:
            cv2.putText(bg_img, text_line, (mask.shape[0]//2 + 240, 250), cv2.FONT_HERSHEY_SIMPLEX, TEXT_SIZE, TEXT_COLOR, TEXT_THICKNESS)

        bg_img = cv2.resize(bg_img, (800, 600))
        frame_buffer.append(bg_img)
        step += 1
        progress['value'] = (step / total_steps) * 100
        progress.update_idletasks()

    for alpha in np.linspace(0, 1, NUM_FRAMES)[::-1]:
        bg_img = background_img.copy()
        bg_img[mask] = cv2.addWeighted(bg_img, 1-alpha, overlay_img, alpha, 0)[mask]

        if alpha >= 0.5:
            cv2.putText(bg_img, text_line, (mask.shape[0]//2 + 240, 250), cv2.FONT_HERSHEY_SIMPLEX, TEXT_SIZE, TEXT_COLOR, TEXT_THICKNESS)

        bg_img = cv2.resize(bg_img, (800, 600))
        frame_buffer.append(bg_img)
        step += 1
        progress['value'] = (step / total_steps) * 100
        progress.update_idletasks()

    return step

def generate_video(lines, save_path, progress):
    background = cv2.imread('assets/comics-background.jpg')
    overlay = cv2.imread('assets/comics-overlay.png')

    overlay = cv2.resize(overlay, (background.shape[1]//4, background.shape[0]//4))
    h, w = overlay.shape[:2]

    overlay_left = overlay
    overlay_right = cv2.flip(overlay, 1)

    shapes_left = np.zeros_like(background, np.uint8)
    shapes_left[0:h, (background.shape[1] - w) // 2:(background.shape[1] + w) // 2] = overlay_left
    mask_left = shapes_left.astype(bool)

    shapes_right = np.zeros_like(background, np.uint8)
    shapes_right[0:h, (background.shape[1] - w) // 2:(background.shape[1] + w) // 2] = overlay_right
    mask_right = shapes_right.astype(bool)

    frames = []
    total_steps = len(lines) * NUM_FRAMES * 2  # Adjusted total steps
    step = 0

    for i, line in enumerate(lines):
        if i % 2 == 0:
            step = fade_in_out(background, shapes_left, mask_left, line, frames, progress, total_steps, step)
        else:
            step = fade_in_out(background, shapes_right, mask_right, line, frames, progress, total_steps, step)

    cv2.destroyAllWindows()

    video_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), FPS, (800, 600))
    for frame in frames:
        video_writer.write(frame)
    video_writer.release()

def preview_video(lines):
    progress_window = tk.Toplevel()
    progress_window.title("Generating Preview")
    progress = ttk.Progressbar(progress_window, mode='determinate')
    progress.pack(pady=20, padx=20)
    progress_window.update()

    generate_video(lines, TEMP_PATH, progress)
    progress_window.destroy()

    cap = cv2.VideoCapture(TEMP_PATH)
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

        generate_video(lines, TEMP_PATH, progress)
        os.rename(TEMP_PATH, save_path)
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