import tkinter as tk
from tkinter import ttk, filedialog, messagebox, PhotoImage
import subprocess
import threading
import os
from datetime import datetime

class ADBLogCaptureApp:
    """
    ADB Log Capture Tool

    This tool provides a GUI for capturing dmesg, xlog, and logcat logs from an Android device.
    """

    def __init__(self, master):
        self.master = master
        self.master.title("ADB Log Capture")

        # Set the window icon (attempt both .ico and .png for compatibility)
        try:
            self.master.iconbitmap("adb_log_icon.ico")  # Preferred for Windows
        except Exception as e:
            print(f"Error with .ico file: {e}")
            try:
                icon = PhotoImage(file="adb_log_icon.png")  # Fallback for cross-platform
                self.master.iconphoto(True, icon)
            except Exception as e:
                print(f"Error with .png file: {e}")

        # Variables for logging control
        self.stop_requested = False
        self.dmesg_thread = None
        self.xlog_thread = None
        self.logcat_thread = None

        self.dmesg_proc = None
        self.xlog_proc = None
        self.logcat_proc = None

        # User-configurable variables
        self.output_dir = tk.StringVar(value=os.getcwd())
        self.iteration_name = tk.StringVar(value="")
        self.capture_dmesg = tk.BooleanVar(value=True)
        self.capture_xlog = tk.BooleanVar(value=True)
        self.capture_logcat = tk.BooleanVar(value=True)

        self.run_directory = None

        self.setup_menu()
        self.setup_ui()

    def setup_menu(self):
        """Create a top-level menu with an About option."""
        menubar = tk.Menu(self.master)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.master.config(menu=menubar)

    def setup_ui(self):
        """Set up the main user interface."""
        main_frame = ttk.Frame(self.master, padding="20 20 20 20")
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="ADB Log Capture Tool", font=('Segoe UI', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        # Instructions
        instruction_text = ("Use this tool to capture dmesg, xlog, and logcat logs from an Android device.\n"
                            "Ensure the device is connected and adb is available in PATH.")
        instruction_label = ttk.Label(main_frame, text=instruction_text)
        instruction_label.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="w")

        # Output directory
        dir_frame = ttk.Labelframe(main_frame, text="Output Directory")
        dir_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        dir_frame.columnconfigure(0, weight=1)

        dir_label = ttk.Label(dir_frame, textvariable=self.output_dir)
        dir_label.grid(row=0, column=0, sticky="ew")
        browse_button = ttk.Button(dir_frame, text="Browse...", command=self.browse_directory)
        browse_button.grid(row=0, column=1, padx=5)

        # Iteration name
        iteration_frame = ttk.Labelframe(main_frame, text="Iteration Name (optional)")
        iteration_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        iteration_frame.columnconfigure(0, weight=1)

        iteration_entry = ttk.Entry(iteration_frame, textvariable=self.iteration_name, width=40)
        iteration_entry.grid(row=0, column=0, sticky="ew")

        # Checkboxes for logs
        checkbox_frame = ttk.Labelframe(main_frame, text="Select Logs to Capture")
        checkbox_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        dmesg_check = tk.Checkbutton(checkbox_frame, text="dmesg", variable=self.capture_dmesg, onvalue=True, offvalue=False)
        dmesg_check.grid(row=0, column=0, padx=(10, 10), pady=5)

        xlog_check = tk.Checkbutton(checkbox_frame, text="xlog", variable=self.capture_xlog, onvalue=True, offvalue=False)
        xlog_check.grid(row=0, column=1, padx=(10, 10), pady=5)

        logcat_check = tk.Checkbutton(checkbox_frame, text="logcat", variable=self.capture_logcat, onvalue=True, offvalue=False)
        logcat_check.grid(row=0, column=2, padx=(10, 10), pady=5)

        # Start/Stop Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(10, 20), sticky="ew")
        start_button = ttk.Button(button_frame, text="Start Logging", command=self.start_logging)
        start_button.grid(row=0, column=0, padx=10)
        self.start_button = start_button

        stop_button = ttk.Button(button_frame, text="Stop Logging", command=self.stop_logging, state=tk.DISABLED)
        stop_button.grid(row=0, column=1, padx=10)
        self.stop_button = stop_button

        # Status bar
        self.status_label = ttk.Label(main_frame, text="Status: Not started.", anchor="w", font=("Segoe UI", 9, "italic"))
        self.status_label.grid(row=6, column=0, columnspan=2, sticky="ew")

    def show_about(self):
        """Display the about information."""
        messagebox.showinfo("About", "Author: Abhinav Saurabh")

    def browse_directory(self):
        """Open a file dialog to browse for the output directory."""
        directory = filedialog.askdirectory(initialdir=self.output_dir.get())
        if directory:
            self.output_dir.set(directory)

    def start_logging(self):
        """Start capturing selected logs."""
        self.stop_requested = False

        if not (self.capture_dmesg.get() or self.capture_xlog.get() or self.capture_logcat.get()):
            messagebox.showwarning("No Logs Selected", "Please select at least one log type to capture.")
            return

        if not os.path.isdir(self.output_dir.get()):
            messagebox.showerror("Error", "The selected output directory does not exist.")
            return

        self.update_status("Preparing device...")

        custom_name = self.iteration_name.get().strip()
        if custom_name:
            folder_name = f"logs_{custom_name}"
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            folder_name = f"logs_{timestamp}"

        self.run_directory = os.path.join(self.output_dir.get(), folder_name)
        os.makedirs(self.run_directory, exist_ok=True)

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.update_status("Starting logging...")

    def stop_logging(self):
        """Stop logging processes and open the run directory."""
        self.update_status("Stopping logging...")
        self.stop_requested = True

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.update_status("Logging stopped.")

        if self.run_directory and os.path.isdir(self.run_directory):
            os.startfile(self.run_directory)  # Opens folder in Windows

    def update_status(self, msg):
        """Update the status label text."""
        self.status_label.config(text=f"Status: {msg}")
        self.master.update_idletasks()


def main():
    root = tk.Tk()
    app = ADBLogCaptureApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
