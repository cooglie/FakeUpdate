#!/usr/bin/env python3
"""FakeUpdate — harmless, clearly simulated macOS-style update screen."""
import tkinter as tk
import random
import math

UPDATE_NAMES = [
    "macOS Sequoia Security Response",
    "System Firmware Optimization",
    "Finder Stability Update",
    "Spotlight Index Refresh",
    "Core Services Maintenance",
    "macOS Compatibility Update",
    "Background Services Refresh",
]

THEMES = {
    "macOS Light": {"bg": "#f5f5f7", "fg": "#1d1d1f", "muted": "#6e6e73", "accent": "#007aff", "track": "#d2d2d7"},
    "Midnight": {"bg": "#111318", "fg": "#f5f5f7", "muted": "#a1a1aa", "accent": "#4f9cff", "track": "#343943"},
    "Classic": {"bg": "#e9edf2", "fg": "#20242a", "muted": "#697386", "accent": "#3478c8", "track": "#cbd3df"},
    "Dark Red": {"bg": "#160f12", "fg": "#fff1f2", "muted": "#d4a6ad", "accent": "#e34b5f", "track": "#49252d"},
}

class FakeUpdate:
    def __init__(self, root):
        self.root = root
        self.root.title("FakeUpdate — Simulation")
        self.root.configure(bg=THEMES["macOS Light"]["bg"])
        self.root.geometry("900x600")
        self.root.minsize(640, 440)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.theme_name = "macOS Light"
        self.progress = 0
        self.running = False
        self.restarting = False
        self.after_id = None
        self.build()
        self.apply_theme()
        self.root.bind("<Escape>", lambda _e: self.close())
        self.root.bind("<F11>", lambda _e: self.toggle_fullscreen())

    def build(self):
        self.top = tk.Frame(self.root)
        self.top.pack(fill="x", padx=28, pady=(18, 0))
        self.brand = tk.Label(self.top, text="FakeUpdate  •  SIMULATION", font=("Helvetica", 10, "bold"))
        self.brand.pack(side="left")
        self.theme_var = tk.StringVar(value=self.theme_name)
        self.theme_menu = tk.OptionMenu(self.top, self.theme_var, *THEMES.keys(), command=lambda _v: self.apply_theme())
        self.theme_menu.pack(side="right")
        self.full_btn = tk.Button(self.top, text="Vollbild", command=self.toggle_fullscreen)
        self.full_btn.pack(side="right", padx=8)

        self.center = tk.Frame(self.root)
        self.center.pack(expand=True, fill="both", padx=50, pady=25)
        self.logo = tk.Label(self.center, text="◌", font=("Helvetica", 62))
        self.logo.pack(pady=(18, 14))
        self.title = tk.Label(self.center, text="Systemupdate wird vorbereitet", font=("Helvetica", 25, "bold"))
        self.title.pack(pady=8)
        self.subtitle = tk.Label(self.center, text=random.choice(UPDATE_NAMES), font=("Helvetica", 14))
        self.subtitle.pack(pady=(0, 26))
        self.percent = tk.Label(self.center, text="0 %", font=("Helvetica", 30, "bold"))
        self.percent.pack(pady=5)
        self.canvas = tk.Canvas(self.center, height=12, width=520, highlightthickness=0)
        self.canvas.pack(fill="x", padx=30, pady=12)
        self.status = tk.Label(self.center, text="Bitte warten …", font=("Helvetica", 12))
        self.status.pack(pady=8)
        self.note = tk.Label(self.center, text="Dies ist eine harmlose Simulation. Dein Mac wird nicht aktualisiert oder neu gestartet.", font=("Helvetica", 10), wraplength=620)
        self.note.pack(pady=(12, 20))
        self.controls = tk.Frame(self.center)
        self.controls.pack(pady=8)
        self.start_btn = tk.Button(self.controls, text="Simulation starten", command=self.start)
        self.start_btn.pack(side="left", padx=6)
        self.reset_btn = tk.Button(self.controls, text="Zurücksetzen", command=self.reset)
        self.reset_btn.pack(side="left", padx=6)
        self.close_btn = tk.Button(self.controls, text="Beenden", command=self.close)
        self.close_btn.pack(side="left", padx=6)
        self.footer = tk.Label(self.root, text="ESC = Beenden   •   F11 = Vollbild umschalten", font=("Helvetica", 9))
        self.footer.pack(side="bottom", pady=12)

    def apply_theme(self):
        self.theme_name = self.theme_var.get()
        c = THEMES[self.theme_name]
        self.root.configure(bg=c["bg"])
        for widget in [self.top, self.center, self.controls]:
            widget.configure(bg=c["bg"])
        for widget in [self.brand, self.logo, self.title, self.subtitle, self.percent, self.status, self.note, self.footer]:
            widget.configure(bg=c["bg"], fg=c["fg"] if widget in [self.logo, self.title, self.percent] else c["muted"])
        self.brand.configure(fg=c["fg"])
        self.canvas.configure(bg=c["bg"])
        for button in [self.start_btn, self.reset_btn, self.close_btn, self.full_btn]:
            button.configure(bg=c["track"], fg=c["fg"], activebackground=c["accent"], activeforeground="white",
                             relief="flat", bd=0, padx=14, pady=8)
        self.theme_menu.configure(bg=c["track"], fg=c["fg"], activebackground=c["accent"], relief="flat", highlightthickness=0)
        self.theme_menu["menu"].configure(bg=c["track"], fg=c["fg"])
        self.draw_bar()

    def draw_bar(self):
        c = THEMES[self.theme_name]
        self.canvas.delete("all")
        w = max(self.canvas.winfo_width(), 300)
        self.canvas.create_rectangle(0, 0, w, 12, fill=c["track"], outline="")
        self.canvas.create_rectangle(0, 0, w*self.progress/100, 12, fill=c["accent"], outline="")

    def start(self):
        if self.running:
            return
        self.progress = 0
        self.running = True
        self.restarting = False
        self.subtitle.configure(text=random.choice(UPDATE_NAMES))
        self.start_btn.configure(state="disabled")
        self.status.configure(text="Update wird installiert …")
        self.tick()

    def tick(self):
        if not self.running:
            return
        self.progress = min(100, self.progress + random.choice([1, 1, 1, 2, 3]))
        self.percent.configure(text=f"{self.progress} %")
        self.draw_bar()
        if self.progress >= 100:
            self.running = False
            self.status.configure(text="Installation abgeschlossen — Neustart wird simuliert …")
            self.title.configure(text="Update abgeschlossen")
            self.logo.configure(text="✓")
            self.after_id = self.root.after(1800, self.restart_animation)
        else:
            self.after_id = self.root.after(random.randint(90, 260), self.tick)

    def restart_animation(self):
        self.restarting = True
        self.title.configure(text="Neustart")
        self.subtitle.configure(text="Dein Mac bleibt unverändert — nur die Animation läuft.")
        self.status.configure(text="Neustart wird simuliert" + "." * (int(self.root.tk.call("clock", "milliseconds")) % 4))
        self.logo.configure(text="⟳")
        self.after_id = self.root.after(500, self.restart_animation_step)

    def restart_animation_step(self):
        self.logo.configure(text=random.choice(["⟳", "◌", "⟲"]))
        self.status.configure(text=random.choice(["Dienste werden gestartet …", "Systemprüfung …", "Fast fertig …"]))
        self.after_id = self.root.after(650, self.finish)

    def finish(self):
        self.title.configure(text="Alles erledigt!")
        self.subtitle.configure(text="Die FakeUpdate-Demo ist beendet.")
        self.status.configure(text="Kein echter Neustart durchgeführt.")
        self.logo.configure(text="✓")
        self.start_btn.configure(state="normal", text="Erneut starten")

    def reset(self):
        self.running = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.progress = 0
        self.restarting = False
        self.title.configure(text="Systemupdate wird vorbereitet")
        self.subtitle.configure(text=random.choice(UPDATE_NAMES))
        self.percent.configure(text="0 %")
        self.status.configure(text="Bereit für die Simulation")
        self.logo.configure(text="◌")
        self.start_btn.configure(state="normal", text="Simulation starten")
        self.draw_bar()

    def toggle_fullscreen(self):
        current = bool(self.root.attributes("-fullscreen"))
        self.root.attributes("-fullscreen", not current)

    def close(self):
        self.running = False
        if self.after_id:
            try: self.root.after_cancel(self.after_id)
            except tk.TclError: pass
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FakeUpdate(root)
    root.mainloop()
