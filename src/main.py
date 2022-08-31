def main():
    from PIL import Image, ImageTk
    from tkinter import Tk, ttk

    root = Tk()

    image = Image.open(r"src/mando.jpg")
    image = ImageTk.PhotoImage(image)

    label = ttk.Label(root, image=image)
    label.pack()

    root.mainloop()


if __name__ == '__main__':
    main()
