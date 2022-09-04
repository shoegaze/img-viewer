def main() -> None:
    from viewer import Viewer
    import pyglet.app

    _viewer = Viewer(r'src/mando.jpg')

    pyglet.app.run()


if __name__ == '__main__':
    main()
