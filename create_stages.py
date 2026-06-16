import customtkinter as ctk

# Set the overall visual theme and color profile
ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"


class ModernApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure main window properties
        self.title("CustomTkinter Showcase App")
        self.geometry("700x450")

        # Configure a responsive 2-column grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ------------------ SIDEBAR NAVIGATION ------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)  # Pushes bottom elements down

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="My App", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_dashboard = ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=self.button_click)
        self.btn_dashboard.grid(row=1, column=0, padx=20, pady=10)

        self.btn_settings = ctk.CTkButton(self.sidebar_frame, text="Settings", command=self.button_click)
        self.btn_settings.grid(row=2, column=0, padx=20, pady=10)

        # Theme Switcher inside the Sidebar
        self.theme_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.theme_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.theme_optionmenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                  command=self.change_appearance_mode_event)
        self.theme_optionmenu.grid(row=6, column=0, padx=20, pady=(10, 20))
        self.theme_optionmenu.set("System")

        # ------------------ MAIN CONTENT AREA ------------------
        self.main_frame = ctk.CTkScrollableFrame(self, label_text="Control Panel")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Text Input Field
        self.entry = ctk.CTkEntry(self.main_frame, placeholder_text="Type something here...")
        self.entry.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        # Action Button
        self.submit_btn = ctk.CTkButton(self.main_frame, text="Submit Data", fg_color="green", hover_color="darkgreen",
                                        command=self.submit_action)
        self.submit_btn.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Feedback Label
        self.output_label = ctk.CTkLabel(self.main_frame, text="Waiting for input...",
                                         font=ctk.CTkFont(size=13, slant="italic"))
        self.output_label.grid(row=2, column=0, padx=20, pady=10)

        # Checkboxes & Switches Frame
        self.checkbox_frame = ctk.CTkFrame(self.main_frame)
        self.checkbox_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.checkbox_1 = ctk.CTkCheckBox(self.checkbox_frame, text="Enable Logging")
        self.checkbox_1.pack(pady=10, padx=10, anchor="w")

        self.switch_1 = ctk.CTkSwitch(self.checkbox_frame, text="Developer Mode")
        self.switch_1.pack(pady=10, padx=10, anchor="w")

        # Progress Indicator & Slider
        self.slider = ctk.CTkSlider(self.main_frame, from_=0, to=1, command=self.slider_event)
        self.slider.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.slider.set(0.5)

        self.progressbar = ctk.CTkProgressBar(self.main_frame)
        self.progressbar.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        self.progressbar.set(0.5)

    # ------------------ LOGIC & EVENT HANDLERS ------------------
    def button_click(self):
        print("Sidebar navigation button clicked!")

    def submit_action(self):
        user_text = self.entry.get()
        if user_text:
            self.output_label.configure(text=f"Submitted: '{user_text}'", text_color="lightgreen")
        else:
            self.output_label.configure(text="Input cannot be empty!", text_color="red")

    def slider_event(self, value):
        self.progressbar.set(value)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = ModernApp()
    app.mainloop()