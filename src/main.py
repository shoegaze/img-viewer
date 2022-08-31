def main():
    from PIL import Image

    im = Image.open("src/mando.jpg")
    print(im.format, im.size, im.mode)


if __name__ == '__main__':
    main()
