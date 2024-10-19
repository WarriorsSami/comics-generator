import cv2
import numpy as np

TEXT_COLOR = (200, 200, 200)
TEXT_SIZE = 2
TEXT_THICKNESS = 7
FPS = 25
DURATION = 2.0
NUM_FRAMES = int(FPS * DURATION)

def fade_in_out(background_img, overlay_img, mask, text_line, frame_buffer):
    for alpha in np.linspace(0, 1, NUM_FRAMES):
        bg_img = background_img.copy()
        bg_img[mask] = cv2.addWeighted(bg_img, 1-alpha, overlay_img, alpha, 0)[mask]

        if alpha >= 0.5:
            cv2.putText(bg_img, text_line, (mask.shape[0]//2 + 240, 250), cv2.FONT_HERSHEY_SIMPLEX, TEXT_SIZE, TEXT_COLOR, TEXT_THICKNESS)

        print(f'Writing frame {len(frame_buffer)}')
        bg_img = cv2.resize(bg_img, (800, 600))
        frame_buffer.append(bg_img)

    for alpha in np.linspace(0, 1, NUM_FRAMES)[::-1]:
        bg_img = background_img.copy()
        bg_img[mask] = cv2.addWeighted(bg_img, 1-alpha, overlay_img, alpha, 0)[mask]

        if alpha >= 0.5:
            cv2.putText(bg_img, text_line, (mask.shape[0]//2 + 240, 250), cv2.FONT_HERSHEY_SIMPLEX, TEXT_SIZE, TEXT_COLOR, TEXT_THICKNESS)

        print(f'Writing frame {len(frame_buffer)}')
        bg_img = cv2.resize(bg_img, (800, 600))
        frame_buffer.append(bg_img)

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
fade_in_out(background, shapes_left, mask_left, 'Hi, Spiderman impostor!', frames)
fade_in_out(background, shapes_right, mask_right, 'We finally meet, Spiderman impostor!', frames)
fade_in_out(background, shapes_left, mask_left, 'Get ready for the show!', frames)
fade_in_out(background, shapes_right, mask_right, 'I was born ready!', frames)
fade_in_out(background, shapes_left, mask_left, 'Let\'s see who is the best!', frames)
fade_in_out(background, shapes_right, mask_right, 'I am the best!', frames)
cv2.destroyAllWindows()

video_writer = cv2.VideoWriter('assets/comics.mp4', cv2.VideoWriter_fourcc(*'mp4v'), FPS, (800, 600))
for frame in frames:
    video_writer.write(frame)
video_writer.release()
