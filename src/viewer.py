from typing import Literal, Union

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
        except:
            print(f'ERROR: Unable to open file `{url}`')

        super().__init__(
            resizable=True,
            width=self.image_data.width,
            height=self.image_data.height
        )

    def rotate(self, dir: Union[Literal['cw'], Literal['ccw']]) -> None:
        if dir == None:
            return

        rot = Image.ROTATE_90 if dir == 'ccw' else Image.ROTATE_270
        self.image_handle = self.image_handle.transpose(rot)
        self.image_data = to_image_data(self.image_handle)

    def on_draw(self):
        self.clear()
        self.image_data.blit(0, 0)

    def on_key_release(self, symbol: int, modifiers: int):
        from pyglet.window import key

        if symbol == key.RIGHT:
            self.rotate('ccw')
        elif symbol == key.LEFT:
            self.rotate('cw')
