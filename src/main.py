from typing import Optional

import click
from click.core import Context, Option


def validate_path(_context: Context, _param: Option, path: str) -> bool:
    import os

    if not os.path.exists(path):
        raise click.BadParameter(f'"{path}"')

    return path


@click.command()
@click.option(
    '--image',
    'path',
    required=True,
    type=str,
    help='Path to image file',
    callback=validate_path
)
def display(path: Optional[str]) -> None:
    from viewer import Viewer

    viewer = Viewer(path)

    while viewer.is_alive:
        viewer.update()


if __name__ == '__main__':
    display(None)
