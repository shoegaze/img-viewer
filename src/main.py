from typing import Optional

import click


@click.command()
@click.option(
    '--path',
    type=str,
    help='Image file to display'
)
def main(path: Optional[str]) -> None:
    from viewer import Viewer
    import pyglet.app

    if not path:
        print('Please enter a valid path to an image file.')
        return

    Viewer(path)

    pyglet.app.run()


if __name__ == '__main__':
    main(None)
