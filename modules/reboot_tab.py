
import customtkinter as ctk
from modules.ui_theme import CARD_BG, CARD_BORDER, TEXT_MUTED

class RebootTab(ctk.CTkFrame):
    def __init__(self, master, adb_manager):
        super().__init__(master, fg_color="transparent")
        self.adb_manager = adb_manager

        self.grid_columnconfigure(0, weight=1)
        
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(10, 4))

        self.header = ctk.CTkLabel(self.header_frame, text="Reboot", font=("Roboto Medium", 20))
        self.header.pack(anchor="w")

        self.header_sub = ctk.CTkLabel(self.header_frame, text="Quick reboot modes for different scenarios", font=("Roboto", 12), text_color=TEXT_MUTED)
        self.header_sub.pack(anchor="w", pady=(2, 0))
        
        self.options_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.options_frame.pack(fill="both", expand=True, padx=20, pady=(6, 10))
        
        # Helper to create buttons
        def create_btn(text, cmd_arg, desc):
            frame = ctk.CTkFrame(self.options_frame, corner_radius=12, fg_color=CARD_BG, border_width=1, border_color=CARD_BORDER)
            frame.pack(fill="x", pady=6)
            
            btn = ctk.CTkButton(frame, text=text, command=lambda: self.reboot(cmd_arg), width=180)
            btn.pack(side="left", padx=10)
            
            lbl = ctk.CTkLabel(frame, text=desc, text_color=TEXT_MUTED, anchor="w")
            lbl.pack(side="left", padx=10, fill="x", expand=True)

        create_btn("Normal Reboot", [], "Standard system restart.")
        create_btn("Reboot Recovery", ["recovery"], "Boot into Stock Recovery or TWRP.")
        create_btn("Reboot Bootloader", ["bootloader"], "Boot into Fastboot mode.")
        create_btn("Reboot EDL", ["edl"], "Emergency Download Mode (Requires auth/older devices).")
        create_btn("Reboot Fastboot", ["fastboot"], "Alias for bootloader (works on many Xiaomis).")

        self.status_label = ctk.CTkLabel(self, text="", text_color=TEXT_MUTED)
        self.status_label.pack(pady=(0, 10))

    def reboot(self, mode_args):
        if not self.adb_manager.connected_device:
            self.status_label.configure(text="No device connected.", text_color="red")
            return
            
        cmd = ["-s", self.adb_manager.connected_device, "reboot"] + mode_args
        self.status_label.configure(text=f"Executing reboot {' '.join(mode_args)}...", text_color="yellow")
        
        # Execute in thread? Reboot is usually fast to return, but device goes offline.
        self.adb_manager.run_command(cmd)
        
        self.status_label.configure(text=f"Reboot command sent.", text_color="#2CC985")
