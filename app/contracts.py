class FadeInOutParams:
    def __init__(self, background_img, overlay_img, mask, text_line, frame_buffer, progress, total_steps, step):
        self.background_img = background_img
        self.overlay_img = overlay_img
        self.mask = mask
        self.text_line = text_line
        self.frame_buffer = frame_buffer
        self.progress = progress
        self.total_steps = total_steps
        self.step = step