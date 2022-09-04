def main() -> None:
    from pyglet.window import Window
    import pyglet.resource
    import pyglet.app

    image = pyglet.resource.image(r'mando.jpg')
    window = Window(
        resizable=True,
        width=image.width,
        height=image.height
    )

    @window.event
    def on_draw():
        window.clear()
        image.blit(0, 0)

    pyglet.app.run()


if __name__ == '__main__':
    main()
