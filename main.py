import tkinter as tk
from PIL import Image, ImageTk
import database
from stock_window import StockWindow
import os
import sys


class MainApp:
    def __init__(self, root):
        self.fullscreen_state = None
        self.root = root
        root.title("Stoc Club GPL by Ionel Stan")
        root.geometry("1000x700")
        root.state('zoomed')
        database.init_db()

        # Canvas principal
        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.redraw)

        # Încarcă logo
        import os
        import sys
        from PIL import Image, ImageTk

        # Încarcă logo corect, funcționează și în .exe
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        logo_path = os.path.join(base_path, "logo.png")
        self.original_logo = Image.open(logo_path)

        # Butonul STOC (mare și centrat)
        self.stock_button = tk.Button(
            root,
            text="Stoc Club GPL",
            command=lambda: StockWindow(root),
            bg="#ecf0f1",
            activebackground="#2c3e50",
            relief="raised",
            bd=3
        )

        # Font mare și padding
        self.stock_button.configure(font=("Arial", 28, "bold"), padx=40, pady=20)

        # Efect hover
        self.stock_button.bind("<Enter>", lambda e: self.stock_button.config(bg="#ecf0f1"))
        self.stock_button.bind("<Leave>", lambda e: self.stock_button.config(bg="#ecf0f1"))

    def redraw(self, event):
        # Șterge elementele vizuale (logo și gradient)
        self.canvas.delete("logo")
        self.canvas.delete("gradient")

        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()

        # Gradient fundal
        self.draw_gradient("#2c3e50", "#ecf0f1", w, h)

        # Redimensionare logo (80% din lățime)
        new_width = int(w * 1)
        ratio = new_width / self.original_logo.width
        new_height = int(self.original_logo.height * ratio)
        resized = self.original_logo.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(resized)

        # Afișare logo
        self.canvas.create_image(w // 2, h // 2.5, image=self.logo_img, anchor="center", tags="logo")

        # Plasare buton centrat sub logo
        y_pos = int(h * 0.8)
        if not hasattr(self.stock_button, "canvas_window"):
            self.stock_button.canvas_window = self.canvas.create_window(
                w // 2, y_pos, window=self.stock_button, anchor="center"
            )
        else:
            self.canvas.coords(self.stock_button.canvas_window, w // 2, y_pos)

    def draw_gradient(self, color1, color2, width, height):
        r1, g1, b1 = self.hex_to_rgb(color1)
        r2, g2, b2 = self.hex_to_rgb(color2)
        for i in range(height):
            r = int(r1 + (i / height) * (r2 - r1))
            g = int(g1 + (i / height) * (g2 - g1))
            b = int(b1 + (i / height) * (b2 - b1))
            self.canvas.create_line(0, i, width, i, fill=f"#{r:02x}{g:02x}{b:02x}", tags="gradient")

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
