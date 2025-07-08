import customtkinter as ctk
import random, requests, pyttsx3
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw, ImageFont
import pyperclip

# AMOLED Mode
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")  # Keep base dark theme

class QuoteGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🧠 Quote Generator Pro Max")
        self.geometry("600x540")
        self.configure(fg_color="#000000")  # AMOLED BG
        self.resizable(False, False)

        self.favorites = []
        self.local_quotes = {
            "Motivation": [
                "Push yourself, because no one else is going to do it for you.",
                "Great things never come from comfort zones.",
            ],
            "Funny": [
                "I'm not lazy, I'm on energy-saving mode.",
                "If life gives you lemons, add vodka.",
            ],
            "Productivity": [
                "Success doesn’t come from what you do occasionally.",
                "Schedule your priorities.",
            ]
        }

        self.tts = pyttsx3.init()
        self.build_ui()

    def build_ui(self):
        # Title
        ctk.CTkLabel(self, text="💬 Quote Generator", font=("Poppins", 22, "bold"), text_color="#FF4B4B", fg_color="#000000").pack(pady=(10, 4))

        # Dropdown menu - AMOLED style
        self.category_menu = ctk.CTkOptionMenu(
            self,
            values=["Motivation", "Funny", "Productivity", "API"],
            fg_color="#000000",
            text_color="#FF4B4B",
            button_color="#000000",
            button_hover_color="#220000",
            dropdown_fg_color="#000000",
            dropdown_text_color="#FF4444",
            dropdown_hover_color="#330000"
        )
        self.category_menu.set("Motivation")
        self.category_menu.pack(pady=4)

        # Quote box - also AMOLED black
        self.quote_box = ctk.CTkTextbox(
            self,
            height=140,
            width=480,
            font=("Poppins", 15),
            wrap="word",
            fg_color="#000000",
            text_color="#FFEEEE",
            border_color="#FF4444",
            border_width=2,
        )
        self.quote_box.pack(pady=8)
        self.quote_box.insert("1.0", "Click below to get your quote ✨")
        self.quote_box.configure(state="disabled")

        # Red Glow Button Style
        def red_glow_style(widget):
            widget.configure(
                fg_color="#000000",
                border_color="#FF4444",
                border_width=2,
                hover_color="#220000",
                text_color="#FF4444"
            )

        # Frame for Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="#000000")
        btn_frame.pack(pady=4)

        btn_style = {
            "font": ("Poppins", 13),
            "corner_radius": 15,
            "height": 38,
            "width": 200
        }

        self.btn1 = ctk.CTkButton(btn_frame, text="🎯 Get Quote", command=self.display_quote, **btn_style)
        self.btn2 = ctk.CTkButton(btn_frame, text="💾 Save", command=self.save_favorite, **btn_style)
        self.btn3 = ctk.CTkButton(btn_frame, text="➕ Add", command=self.add_custom_quote, **btn_style)
        self.btn4 = ctk.CTkButton(btn_frame, text="🖼️ Export", command=self.export_image, **btn_style)
        self.btn5 = ctk.CTkButton(btn_frame, text="🔊 Speak", command=self.speak_quote, **btn_style)
        self.btn6 = ctk.CTkButton(btn_frame, text="📋 Copy", command=self.copy_clipboard, **btn_style)

        for b in [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn6]:
            red_glow_style(b)

        # Grid layout (compact, symmetric)
        self.btn1.grid(row=0, column=0, padx=6, pady=4)
        self.btn2.grid(row=0, column=1, padx=6, pady=4)
        self.btn3.grid(row=1, column=0, padx=6, pady=4)
        self.btn4.grid(row=1, column=1, padx=6, pady=4)
        self.btn5.grid(row=2, column=0, padx=6, pady=4)
        self.btn6.grid(row=2, column=1, padx=6, pady=4)

        # Footer
        ctk.CTkLabel(self, text="🔎 Powered by Y7X 💗", font=("Poppins", 12, "italic"), text_color="#888888", fg_color="#000000").pack(pady=8)

    def get_random_quote(self):
        category = self.category_menu.get()
        if category == "API":
            try:
                res = requests.get("https://api.quotable.io/random")
                return res.json()["content"]
            except:
                return "⚠️ Could not fetch quote from API."
        else:
            return random.choice(self.local_quotes[category])

    def display_quote(self):
        quote = self.get_random_quote()
        self.quote_box.configure(state="normal")
        self.quote_box.delete("1.0", "end")
        self.quote_box.insert("1.0", quote)
        self.quote_box.configure(state="disabled")

    def speak_quote(self):
        quote = self.quote_box.get("1.0", "end").strip()
        self.tts.say(quote)
        self.tts.runAndWait()

    def save_favorite(self):
        quote = self.quote_box.get("1.0", "end").strip()
        if quote and quote not in self.favorites:
            self.favorites.append(quote)
            messagebox.showinfo("Saved", "✅ Quote added to favorites.")
        else:
            messagebox.showinfo("Info", "Already saved or empty.")

    def copy_clipboard(self):
        quote = self.quote_box.get("1.0", "end").strip()
        pyperclip.copy(quote)
        messagebox.showinfo("Copied", "📋 Quote copied to clipboard!")

    def add_custom_quote(self):
        dialog = ctk.CTkInputDialog(title="Add Quote", text="Enter your quote:")
        quote = dialog.get_input()
        if quote:
            category = self.category_menu.get()
            if category not in self.local_quotes:
                self.local_quotes[category] = []
            self.local_quotes[category].append(quote)
            messagebox.showinfo("Added", "✅ Your quote has been added.")

    def export_image(self):
        quote = self.quote_box.get("1.0", "end").strip()
        if not quote:
            return
        img = Image.new("RGB", (800, 400), color=(0, 0, 0))  # AMOLED
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 24)
        draw.text((50, 100), quote, font=font, fill=(255, 0, 0))
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if path:
            img.save(path)
            messagebox.showinfo("Exported", "🖼️ Quote saved as image!")

if __name__ == "__main__":
    app = QuoteGeneratorApp()
    app.mainloop()