from typing import Optional, Literal, Tuple, Union

from PIL import Image
from pyglet.window import Window
from pyglet.image import ImageData


DOUBLE_CLICK_INTERVAL = 0.25


def to_image_data(handle: Image.Image) -> Optional[ImageData]:
    return ImageData(
        handle.width,
        handle.height,
        handle.mode,
        handle.tobytes()
    )


class Viewer(Window):
    image_handle: Image.Image
    image_data: ImageData
    drag_displacement: Optional[Tuple[int, int]] = None

    original_size: Tuple[int, int]

    last_click: float = 0.0
    is_fullscreened: bool
    location_before_fullscreen: Tuple[int, int]
    size_before_fullscreen: Tuple[int, int]

    def __init__(self, url: str):
        should_crash = False

        # Try to open and load the image at path `url`
        try:
            with Image.open(url) as im:
                self.image_handle = im.transpose(Image.FLIP_TOP_BOTTOM)
                self.image_data = to_image_data(self.image_handle)

                if not self.image_data:
                    raise ValueError('Unable to convert file to image data')
        except:
            print(f'ERROR: Unable to open file "{url}"')
            should_crash = True

        if not should_crash:
            super().__init__(
                resizable=True,
                width=self.image_data.width,
                height=self.image_data.height,
                style=Window.WINDOW_STYLE_BORDERLESS
            )
        else:
            super().__init__()
            self.close()
            return

        self.set_minimum_size(100, 100)

        self.original_size = self.get_size()

        self.is_fullscreened = False
        self.location_before_fullscreen = self.get_location()
        self.size_before_fullscreen = self.get_size()

    # Rotation:

    def rotate(self, dir: Union[Literal['cw'], Literal['ccw']]) -> None:
        if dir == None:
            return

        rot = Image.ROTATE_90 if dir == 'cw' else Image.ROTATE_270
        self.image_handle = self.image_handle.transpose(rot)
        self.image_data = to_image_data(self.image_handle)

        width, height = self.image_handle.size
        self.set_size(width, height)

    # Resize:

    def resize(self, width: int, height: int) -> None:
        # Copy to preserve image quality
        self.image_data = to_image_data(
            self.image_handle.copy().resize((width, height))
        )

    # Translation:

    #  Converts position from mouse-space (M) => screen-space (S)
    #  ... M => W => S
    def mouse_to_screen(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        m_M = pos

        # Window position in screen-space (S)
        w_S = self.get_location()
        _, height = self.get_size()

        # Mouse position in S
        #  Converts from mouse-space => window-space => screen-space
        #  M => W => S
        m_S = (
            0 + m_M[0] + w_S[0],
            height - m_M[1] + w_S[1]
        )

        return m_S

    def set_location_to_mouse(self, x_mouse: int, y_mouse: int, _dx_mouse: int, _dy_mouse: int) -> None:
        if not self.drag_displacement:
            return

        # New mouse position in screen-space (S)
        m_S = self.mouse_to_screen((x_mouse, y_mouse))

        # Final window position in S
        w_S = (
            self.drag_displacement[0] + m_S[0],
            self.drag_displacement[1] + m_S[1]
        )

        self.set_location(*w_S)

    def toggle_fullscreen(self) -> None:
        import pyglet

        if not self.is_fullscreened:
            self.location_before_fullscreen = self.get_location()
            self.size_before_fullscreen = self.get_size()

            display = pyglet.canvas.Display()
            screen = display.get_default_screen()

            self.set_location(0, 0)
            self.set_size(screen.width, screen.height)
        else:
            self.set_location(*self.location_before_fullscreen)
            self.set_size(*self.size_before_fullscreen)

        self.is_fullscreened = not self.is_fullscreened

    def reset_size(self) -> None:
        self.set_size(*self.original_size)

    # Events

    def on_key_release(self, symbol: int, _modifiers: int) -> None:
        from pyglet.window import key

        if symbol == key.RIGHT:
            self.rotate('cw')
        elif symbol == key.LEFT:
            self.rotate('ccw')

    def on_resize(self, width: int, height: int) -> None:
        super().on_resize(width, height)

        self.resize(width, height)

    def on_mouse_press(self, x: int, y: int, button: int, _modifiers: int):
        from pyglet.window import mouse

        if button & mouse.LEFT:
            # Window position in screen-space (S)
            w_S = self.get_location()

            # Mouse position in S
            m_S = self.mouse_to_screen((x, y))

            # Displacement between drag origin and window position in S
            #  to be preserved after mouse displacement
            self.drag_displacement = (
                w_S[0] - m_S[0],
                w_S[1] - m_S[1]
            )

    def on_mouse_release(self, _x: int, _y: int, button: int, _modifiers: int) -> None:
        from pyglet.window import mouse
        import time

        if button & mouse.LEFT:
            self.drag_origin = None

            # Toggle fullscreen on double click
            t = time.time()
            if t - self.last_click < DOUBLE_CLICK_INTERVAL:
                self.toggle_fullscreen()

            self.last_click = t

        if button & mouse.MIDDLE:
            self.reset_size()
        elif button & mouse.RIGHT:
            self.close()

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, _modifiers: int) -> None:
        from pyglet.window import mouse

        if buttons & mouse.LEFT:
            if self.is_fullscreened:
                return

            self.set_location_to_mouse(x, y, dx, dy)

    def on_draw(self) -> None:
        self.clear()
        self.image_data.blit(0, 0)
