from typing import Optional

import click
from click.core import Context, Option


def validate_paths(_context: Context, _param: Option, paths: list[str]) -> str:
    import os

    for path in paths:
        if not os.path.exists(path):
            raise click.BadParameter(f'"{path}"')

    return path


@click.command()
@click.option(
    '--image',
    'paths',
    multiple=True,
    type=str,
    help='Path to image file',
    callback=validate_paths
)
def display(paths: Optional[list[str]]) -> None:
    from viewer import Viewer
    import pyglet.app

    print(f'{paths=}: {type(paths)}')

    viewers = []
    for path in paths:
        print(f'{path=}: {type(path)}')

        viewers.append(Viewer(path))

    for viewer in viewers:
        if not viewer.is_alive:
            viewer.close()

    print(f'{viewers=}')

    if viewers:
        pyglet.app.run()


if __name__ == '__main__':
    display(None)
