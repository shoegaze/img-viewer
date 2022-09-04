from PIL import Image
from pyglet.window import Window
from pyglet.image import ImageData


def to_image_data(handle: Image.Image) -> ImageData:
    return ImageData(
        handle.width,
        handle.height,
        handle.mode,
        handle.tobytes()
    )


class Viewer(Window):
    image_handle: Image.Image
    image_data: ImageData

    def __init__(self, url: str):
        # Try to open and load the image at path `url`
        try:
            with Image.open(url) as im:
                self.image_handle = im.transpose(Image.FLIP_TOP_BOTTOM)
                self.image_data = to_image_data(self.image_handle)
                    self.image_handle.width,
                    self.image_handle.height,
                    self.image_handle.mode,
                    self.image_handle.tobytes()
                )
        except:
            print(f'ERROR: Unable to open file `{url}`')

        super().__init__(
            resizable=True,
            width=self.image_data.width,
            height=self.image_data.height
        )

    def on_draw(self):
        self.clear()
        self.image_data.blit(0, 0)

    def on_key_release(self, symbol: int, modifiers: int):
        from pyglet.window import key

        # Rotate image
        if symbol == key.LEFT:
            self.image_handle = self.image_handle.transpose(Image.ROTATE_270)
        elif symbol == key.RIGHT:
            self.image_handle = self.image_handle.transpose(Image.ROTATE_90)

        self.image_data = ImageData(
            self.image_handle.width,
            self.image_handle.height,
            self.image_handle.mode,
            self.image_handle.tobytes()
        )
