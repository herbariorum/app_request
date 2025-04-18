import tkinter as tk
from ctypes import windll
from PIL import Image, ImageTk
from pathlib import Path

try:
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

IMG_PATH = Path(__file__).parent.parent / 'images'

class Notification(tk.Frame):
    def __init__(self, master, width, height, bg, image, text, img_pad, text_pad, font, y_pos):
        super().__init__(master, bg=bg, width=width, height=height)
        self.pack_propagate(0)
        close_img = ImageTk.PhotoImage(Image.open(IMG_PATH / "close.png").resize((20, 20), Image.LANCZOS))

        self.y_pos = y_pos
        self.master = master
        self.width = width
        right_offset = 8
        self.cur_x = self.master.winfo_width()
        self.x = self.cur_x - (self.width + right_offset)

        img_label = tk.Label(self, image=image, bg=bg)
        img_label.image = image
        img_label.pack(side="left", padx=img_pad[0])
        message = tk.Label(self, text=text, font=font, bg=bg, fg="black")
        message.pack(side="left", padx=text_pad[0])

        close_btn = tk.Button(self, image=close_img, bg=bg, relief="flat", command=self.hide_animation, cursor="hand2")
        close_btn.image = close_img
        close_btn.pack(side="right", padx=5)

        self.place(x = self.cur_x, y=y_pos)
        # self.hide_frame()

    def show_animation(self):
        if self.cur_x > self.x:
            self.cur_x -= 1
            self.place(x=self.cur_x, y=self.y_pos)

            self.after(1, self.show_animation)

    def hide_animation(self):
        if self.cur_x < self.master.winfo_width():
            self.cur_x += 1
            self.place(x=self.cur_x, y=self.y_pos)

            self.after(1, self.hide_animation)

# USE EXAMPLE
# if __name__=='__main__':
#     root = tk.Tk()

#     root.title("Notification")
#     root.geometry("500x300")
#     root.configure(bg="black")

#     root.update()

#     img = ImageTk.PhotoImage(Image.open("./images/success.png").resize((25, 25), Image.LANCZOS))

#     cim = ImageTk.PhotoImage(Image.open("./images/close.png").resize((20, 20), Image.LANCZOS))
 
#     img_pad = (5, 0)
#     text_pad = (5, 0)

#     notification = Notification(root, 250, 55, "white", img, "Login Successful.", cim, img_pad, text_pad, "cambria 11", 8)
#     b = tk.Button(
#         root,
#         text="Login",
#         font="cambria 10 bold",
#         fg="white",
#         bg="green",
#         relief="ridge",
#         cursor="hand2",
#         command=notification.show_animation  
#     )

#     b.pack(pady=120)

#     root.mainloop()