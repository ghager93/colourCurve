import tkinter as tk

from PIL import Image, ImageTk

from hsl2rgb import hsl2rgb


# https://stackoverflow.com/questions/42476040/tkinter-get-mouse-coordinates-on-click-and-use-them-as-variables
def getorigin(eventorigin):
    global x, y
    x = eventorigin.x
    y = eventorigin.y

    mouse_click()


def mouse_click():
    if 0 <= y - im_hoffset < im_height and 0 <= x - im_woffset < im_width:
        h, s = (x - im_woffset) * 360 / im_width, (y - im_hoffset) * 1 / im_height
        print(h, s)
        rgb = hsl2rgb(h, s, 0.5)

        canvas.configure(bg=rgb2hex(*rgb))
        
        
def rgb2hex(r, g, b):
    return '#' + hex(int(r * 255))[2:] + hex(int(g * 255))[2:] + hex(int(b * 255))[2:]


global im_height, im_width, im_hoffset, im_woffset
global root, canvas

root = tk.Tk()

canvas = tk.Canvas(root, height=1000, width=1000)
canvas.pack()

pil_im = Image.open('lib/images/rgb_square.png')
im = ImageTk.PhotoImage(pil_im)
canvas.create_image(256, 256, im=im, anchor=tk.NW)

im_height, im_width = pil_im.size
im_hoffset = 256
im_woffset = 256

root.bind('<Button 1>', getorigin)

root.mainloop()
