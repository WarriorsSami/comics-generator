from tempfile import NamedTemporaryFile

TEXT_COLOR = (200, 200, 200)
TEXT_SIZE = 2
TEXT_THICKNESS = 7
FPS = 25
DURATION = 2.0
NUM_FRAMES = int(FPS * DURATION)
BACKGROUND_PATH = 'assets/comics-background.jpg'
OVERLAY_PATH = 'assets/comics-overlay.png'
PREVIEW_TEMP_FILE = NamedTemporaryFile(prefix='comics_generated', suffix='.mp4')
