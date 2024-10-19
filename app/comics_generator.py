import cv2
import numpy as np

from contracts import FadeInOutParams
from settings import NUM_FRAMES, TEXT_SIZE, TEXT_COLOR, TEXT_THICKNESS, BACKGROUND_PATH, OVERLAY_PATH, \
    FPS

def fade_in_out(params: FadeInOutParams):
    for alpha in np.linspace(0, 1, NUM_FRAMES):
        bg_img = params.background_img.copy()
        bg_img[params.mask] = cv2.addWeighted(bg_img, 1-alpha, params.overlay_img, alpha, 0)[params.mask]

        if alpha >= 0.5:
            cv2.putText(bg_img, params.text_line, (params.mask.shape[0]//2 + 240, 250), cv2.FONT_HERSHEY_SIMPLEX, TEXT_SIZE, TEXT_COLOR, TEXT_THICKNESS)

        bg_img = cv2.resize(bg_img, (800, 600))
        params.frame_buffer.append(bg_img)
        params.step += 1
        params.progress['value'] = (params.step / params.total_steps) * 100
        params.progress.update_idletasks()

    for alpha in np.linspace(0, 1, NUM_FRAMES)[::-1]:
        bg_img = params.background_img.copy()
        bg_img[params.mask] = cv2.addWeighted(bg_img, 1-alpha, params.overlay_img, alpha, 0)[params.mask]

        if alpha >= 0.5:
            cv2.putText(bg_img, params.text_line, (params.mask.shape[0]//2 + 240, 250), cv2.FONT_HERSHEY_SIMPLEX, TEXT_SIZE, TEXT_COLOR, TEXT_THICKNESS)

        bg_img = cv2.resize(bg_img, (800, 600))
        params.frame_buffer.append(bg_img)
        params.step += 1
        params.progress['value'] = (params.step / params.total_steps) * 100
        params.progress.update_idletasks()

    return params.step

def generate_video(lines, save_path, progress):
    background = cv2.imread(BACKGROUND_PATH)
    overlay = cv2.imread(OVERLAY_PATH)

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
    total_steps = len(lines) * NUM_FRAMES * 2
    step = 0

    for i, line in enumerate(lines):
        params = FadeInOutParams(background, shapes_left if i % 2 == 0 else shapes_right, mask_left if i % 2 == 0 else mask_right, line, frames, progress, total_steps, step)
        step = fade_in_out(params)

    cv2.destroyAllWindows()

    video_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), FPS, (800, 600))
    for frame in frames:
        video_writer.write(frame)
    video_writer.release()
