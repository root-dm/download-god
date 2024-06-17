import threading
from tkinter import Canvas, Entry, Button, PhotoImage, messagebox

from gui.utils import relative_to_assets


class MainWindow:
    def __init__(self, window, start_download, browse_destination, pause_event, stop_event, config):
        self.window = window
        self.start_download = start_download
        self.browse_destination = browse_destination
        self.pause_event = pause_event
        self.stop_event = stop_event
        self.config = config

        self.window.geometry("1075x547")
        self.window.configure(bg="#181C2A")
        self.window.iconbitmap(relative_to_assets("logo.ico"))
        self.window.title("Download God")

        self.canvas = Canvas(
            self.window,
            bg="#181C2A",
            height=547,
            width=1075,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)

        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            537.0,
            273.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(
            553.0,
            355.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(
            347.0,
            354.0,
            image=self.image_image_3
        )

        self.current_file_label = self.canvas.create_text(
            515.0,
            312.0,
            anchor="nw",
            text="",
            fill="#FFFFFF",
            font=("NunitoSans Regular", 16 * -1)
        )

        self.current_file_progress_label = self.canvas.create_text(
            680.0,
            312.0,
            anchor="nw",
            text="",
            fill="#FFFFFF",
            font=("NunitoSans Regular", 16 * -1)
        )

        self.canvas.create_rectangle(
            519.0,
            342.0,
            817.0,
            355.0,
            fill="#D9D9D9",
            outline="",
            tags="progress_bg")

        self.progress_rectangle = self.canvas.create_rectangle(
            519.0,
            342.0,
            520.0,
            355.0,
            fill="#292879",
            outline="",
            tags="progress_fg")

        self.status_label = self.canvas.create_text(
            600.0,
            280.0,
            anchor="center",
            text="Not started",
            fill="#FFFFFF",
            font=("NunitoSans Bold", 16 * -1)
        )

        self.total_progress_label = self.canvas.create_text(
            345.0,
            370.0,
            anchor="center",
            text="0/0",
            fill="#FFFFFF",
            font=("NunitoSans Regular", 14 * -1)
        )

        self.total_percentage_label = self.canvas.create_text(
            345.0,
            345.0,
            anchor="center",
            text="0%",
            fill="#8D94AF",
            font=("NunitoSans Regular", 32 * -1)
        )

        self.entry_1 = Entry(
            bd=0,
            bg="#0E1116",
            fg="#FFFFFF",  # Set text color to white
            highlightthickness=0,
            insertwidth=0  # Hide the blinking cursor
        )
        self.entry_1.place(
            x=245.0,
            y=183.0,
            width=616.0,
            height=46.0
        )
        self.entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            553.0,
            207.0,
            image=self.entry_image_1
        )

        self.entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(
            553.0,
            140.0,
            image=self.entry_image_2
        )
        self.entry_2 = Entry(
            bd=0,
            bg="#0E1116",
            fg="#FFFFFF",
            highlightthickness=0
        )
        self.entry_2.place(
            x=245.0,
            y=116.0,
            width=616.0,
            height=46.0
        )

        self.entry_1.bind("<Button-1>", lambda e: self.browse_destination(self.entry_1))

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))

        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.start(),
            relief="flat"
        )
        self.button_1.place(
            x=332.0,
            y=487.0,
            width=118.0,
            height=34.0
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.pause,
            relief="flat"
        )
        self.button_2.place(
            x=710.0,
            y=487.0,
            width=115.0,
            height=34.0
        )

        self.canvas.create_text(
            372.0,
            491.0,
            anchor="nw",
            text="Start",
            fill="#8381D9",
            font=("NunitoSans Bold", 16 * -1)
        )

        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        self.button_3 = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.stop,
            relief="flat"
        )
        self.button_3.place(
            x=517.0,
            y=487.0,
            width=125.0,
            height=34.0
        )

    def start(self):
        folder_id = self.entry_2.get()
        destination = self.entry_1.get()
        if not folder_id or not destination:
            messagebox.showerror("Error", "Both Folder ID and Destination are required.")
            return
        self.config['SETTINGS']['folder_id'] = folder_id
        self.config['SETTINGS']['destination'] = destination
        threading.Thread(target=self.start_download, args=(folder_id, destination, self.canvas, self.get_labels())).start()

    def pause(self):
        if self.pause_event.is_set():
            self.pause_event.clear()  # Resume
        else:
            self.pause_event.set()  # Pause

    def stop(self):
        self.stop_event.set()

    def get_labels(self):
        return {
            'status_label': self.status_label,
            'total_progress_label': self.total_progress_label,
            'total_percentage_label': self.total_percentage_label,
            'current_file_label': self.current_file_label,
            'current_file_progress_label': self.current_file_progress_label
        }

    def load_settings(self):
        self.entry_2.insert(0, self.config['SETTINGS'].get('folder_id', ''))
        self.entry_1.insert(0, self.config['SETTINGS'].get('destination', ''))
