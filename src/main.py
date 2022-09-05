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
    '--path',
    required=True,
    type=str,
    help='Image file to display',
    callback=validate_path
)
def main(path: Optional[str]) -> None:
    from viewer import Viewer
    import pyglet.app

    Viewer(path)

    pyglet.app.run()


if __name__ == '__main__':
    main(None)
