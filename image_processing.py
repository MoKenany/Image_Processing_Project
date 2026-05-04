import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageFilter, ImageEnhance, ImageTk
import cv2
import numpy as np

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AdvancedVisionApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Vision Pro - Advanced Multi-Layer Editor")
        self.geometry("1350x800")

        # Image Data
        self.original_pil = None
        self.current_processed_pil = None
        self.history = [] 
        
        # UI Assets
        self.input_tk = None
        self.output_tk = None

        # --- Layout ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Sidebar (Scrollable to fit all options)
        self.sidebar = ctk.CTkScrollableFrame(self, width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="CONTROL PANEL", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        self.btn_import = ctk.CTkButton(self.sidebar, text="IMPORT IMAGE", fg_color="#27ae60", command=self.load_image)
        self.btn_import.pack(pady=10, padx=20, fill="x")

        self.btn_undo = ctk.CTkButton(self.sidebar, text="UNDO LAST STEP", fg_color="#e67e22", command=self.undo_last)
        self.btn_undo.pack(pady=5, padx=20, fill="x")

        self.btn_save = ctk.CTkButton(self.sidebar, text="SAVE RESULT", state="disabled", command=self.save_image)
        self.btn_save.pack(pady=5, padx=20, fill="x")

        # Geometric Section (Section 7 & 10)
        self.add_section("GEOMETRIC OPERATIONS")
        self.create_edit_btn("Flip Horizontal", "flip_h")
        self.create_edit_btn("Flip Vertical", "flip_v")
        self.create_edit_btn("Center Crop (25%)", "crop")

        # Noise Cancellation (Section 10)
        self.add_section("NOISE CANCELLATION")
        self.create_edit_btn("Median Blur", "median")
        self.create_edit_btn("Gaussian Blur", "gaussian")

        # Coloring (Section 6, 7, 10 & NumPy)
        self.add_section("COLORING & INVERSION")
        self.create_edit_btn("Grayscale", "gray")
        self.create_edit_btn("Invert (Bitwise)", "invert_bit")
        self.create_edit_btn("Invert (NumPy)", "invert_np")
        self.create_edit_btn("Boost Saturation", "boost")

        # Filters (Section 7 & 10)
        self.add_section("FILTERS")
        self.create_edit_btn("Detail Enhance", "detail")
        self.create_edit_btn("Edge Detection", "canny")

        # 2. Viewport
        self.view_container = ctk.CTkFrame(self, fg_color="transparent")
        self.view_container.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.view_container.grid_columnconfigure((0, 1), weight=1)
        self.view_container.grid_rowconfigure(0, weight=1)

        self.input_label = self.create_image_slot(self.view_container, "ORIGINAL", 0)
        self.output_label = self.create_image_slot(self.view_container, "CURRENT RESULT", 1, color="#1abc9c")

    def add_section(self, txt):
        ctk.CTkLabel(self.sidebar, text=txt, font=ctk.CTkFont(size=12, weight="bold"), text_color="#3498db").pack(pady=(20, 5))

    def create_edit_btn(self, txt, mode):
        btn = ctk.CTkButton(self.sidebar, text=txt, command=lambda: self.apply_cumulative_filter(mode), fg_color="#34495e")
        btn.pack(pady=2, padx=30, fill="x")

    def create_image_slot(self, parent, title, col, color="#34495e"):
        frame = ctk.CTkFrame(parent, border_width=2, border_color=color)
        frame.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(weight="bold")).pack(pady=5)
        lbl = ctk.CTkLabel(frame, text="Import an image to display")
        lbl.pack(expand=True, fill="both")
        return lbl

    def load_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.original_pil = Image.open(path).convert("RGB") #
            self.current_processed_pil = self.original_pil.copy()
            self.history = [self.original_pil.copy()]
            self.update_view(is_input=True)
            self.update_view(is_input=False)
            self.btn_save.configure(state="normal")

    def undo_last(self):
        if len(self.history) > 1:
            self.history.pop()
            self.current_processed_pil = self.history[-1].copy()
            self.update_view(is_input=False)

    def save_image(self):
        path = filedialog.asksaveasfilename(defaultextension=".png")
        if path:
            self.current_processed_pil.save(path) #

    def apply_cumulative_filter(self, mode):
        if not self.current_processed_pil: return

        # OpenCV Conversion
        cv_img = cv2.cvtColor(np.array(self.current_processed_pil), cv2.COLOR_RGB2BGR)

        # 1. Geometric
        if mode == "flip_h":
            res = cv2.flip(cv_img, 1) # Horizontal flip
            self.current_processed_pil = Image.fromarray(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
        elif mode == "flip_v":
            res = cv2.flip(cv_img, 0) # Vertical flip
            self.current_processed_pil = Image.fromarray(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
        elif mode == "crop":
            w, h = self.current_processed_pil.size
            # Center crop 25% from edges
            box = (w*0.25, h*0.25, w*0.75, h*0.75)
            self.current_processed_pil = self.current_processed_pil.crop(box)

        # 2. Noise & Filters
        elif mode == "median":
            res = cv2.medianBlur(cv_img, 7) #
            self.current_processed_pil = Image.fromarray(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
        elif mode == "canny":
            res = cv2.Canny(cv_img, 100, 200) #
            self.current_processed_pil = Image.fromarray(res)
        elif mode == "detail":
            self.current_processed_pil = self.current_processed_pil.filter(ImageFilter.DETAIL) #

        # 3. Coloring & Inversion
        elif mode == "gray":
            res = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY) #
            self.current_processed_pil = Image.fromarray(res)
        elif mode == "invert_bit":
            res = cv2.bitwise_not(cv_img) # OpenCV Inversion
            self.current_processed_pil = Image.fromarray(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
        elif mode == "invert_np":
            # Manual NumPy Inversion (255 - pixel)
            res_array = 255 - np.array(self.current_processed_pil)
            self.current_processed_pil = Image.fromarray(res_array)
        elif mode == "boost":
            enhancer = ImageEnhance.Color(self.current_processed_pil) #
            self.current_processed_pil = enhancer.enhance(1.5)

        self.history.append(self.current_processed_pil.copy())
        self.update_view(is_input=False)

    def update_view(self, is_input=True):
        img = self.original_pil if is_input else self.current_processed_pil
        temp = img.copy()
        temp.thumbnail((500, 500), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(temp)

        if is_input:
            self.input_tk = tk_img
            self.input_label.configure(image=self.input_tk, text="")
        else:
            self.output_tk = tk_img
            self.output_label.configure(image=self.output_tk, text="")

if __name__ == "__main__":
    app = AdvancedVisionApp()
    app.mainloop()