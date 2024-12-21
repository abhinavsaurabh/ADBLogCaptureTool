# ADB Log Capture Tool

A modern, user-friendly Python-based GUI application for capturing logs from Android devices using **ADB (Android Debug Bridge)**. This tool simplifies the process of collecting critical logs for debugging and diagnostics, making it suitable for developers, testers, and engineers.

---

## **Features**

- **Log Capture**: Supports capturing the following logs:
  - **`dmesg`**: Kernel logs for hardware and driver-level diagnostics.
  - **`xlog`**: System-level logs (e.g., SDE_EVT buffer logs).
  - **`logcat`**: User-space logs for debugging apps and services.
- **GUI Interface**: Intuitive controls for starting, stopping, and managing log capture sessions.
- **Customizable Output**:
  - Select the output directory for storing logs.
  - Name each logging session for better organization.
- **Multi-threaded Execution**: Ensures smooth performance without freezing the application.
- **Automatic Folder Management**: Automatically creates timestamped or custom-named folders for each session.
- **Cross-Platform Compatibility**: Runs on Windows, macOS, and Linux (requires ADB to be installed).
- **Developer Metadata**: Embeds version information, developer name, and copyright details into the executable file.
- **Integrated Icon**: Professional icon included for taskbar and title bar.
- **Log Viewing Convenience**: Opens the log folder automatically after stopping the session.

---

## **Why Use ADB Log Capture Tool?**

- **Efficiency**: Automates the tedious process of running ADB commands manually.
- **User-Friendly**: GUI-based interface eliminates the need for command-line expertise.
- **Debugging Made Easy**: Helps developers and QA teams quickly gather logs for analysis.
- **Session Organization**: Each session is neatly stored in its own folder for easy access.
- **Professional Design**: Built for engineers and management to simplify Android device diagnostics.

---

## **Installation**

### **Prerequisites**

1. **Python**: Ensure Python 3.6 or later is installed on your system.
2. **ADB**: Install ADB (Android Debug Bridge) and ensure it is available in your system's PATH.

### **Steps**

1. Clone the repository:
   ```bash
   git clone https://github.com/YourUsername/ADBLogCaptureTool.git
   cd ADBLogCaptureTool
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python adb_log_capture.py
   ```

---

## **Building the Executable**

To distribute the tool as a standalone `.exe`:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Create the executable:
   ```bash
   pyinstaller --onefile --windowed --icon=adb_log_icon.ico adb_log_capture.py
   ```

3. The executable will be in the `dist` folder.

---

## **Usage**

1. **Launch the Application**: Double-click the executable or run the Python script.

2. **Set Output Directory**: Choose the folder where logs will be saved.

3. **Name Your Session (Optional)**: Enter a custom name for the session folder or leave it blank to use a timestamp.

4. **Select Logs**: Check the boxes for `dmesg`, `xlog`, and/or `logcat` as required.

5. **Start Logging**: Click the **Start Logging** button to begin capturing logs.

6. **Stop Logging**: Click **Stop Logging** when done. The log folder will automatically open.

---

## **Screenshots**

### Main Interface
![Main Interface](path/to/main_interface.png)

### Output Directory Selection
![Output Directory](path/to/output_directory.png)

### Capturing Logs
![Capturing Logs](path/to/capturing_logs.png)

---

## **Technical Details**

### **Core Functionality**

The application uses the `subprocess` module to execute ADB commands for capturing logs:

- **`dmesg`**:
  ```bash
  adb root
  adb shell dmesg -w
  ```
- **`xlog`**:
  ```bash
  adb root
  adb shell mount -t debugfs none /sys/kernel/debug
  adb shell while true; do cat /d/dri/0/debug/dump; echo "newdump"; done; > xlog_out.txt
  ```
- **`logcat`**:
  ```bash
  adb root
  adb remount
  adb logcat -c
  adb logcat -G 256M
  adb logcat > logcat.txt
  ```

### **Multi-threading**

Each log capture process runs in its own thread to ensure the GUI remains responsive.

### **Error Handling**

- **Missing ADB**: The application alerts the user if ADB is not found.
- **Invalid Output Directory**: Warns the user if the selected directory is not writable.

---

## **Customization**

1. **Adding New Log Types**: Extend the application by adding new ADB commands in the `start_logging` function.
2. **Changing UI Layout**: Modify the `setup_ui` function to customize the interface.
3. **Embedding Metadata**: Use the `version_info.txt` file to embed version details in the `.exe`.

---

## **Known Limitations**

- Requires ADB to be installed and accessible via PATH.
- Designed primarily for Android devices with debugging enabled.
- `xlog` functionality depends on device-specific kernel features.

---

## **Planned Features**

- **Log Analysis**: Add built-in tools for analyzing captured logs.
- **Device Detection**: Automatically detect connected devices.
- **Cross-Platform Improvements**: Enhance compatibility with macOS and Linux.

---

## **Contributing**

We welcome contributions from the community! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with detailed descriptions of your changes.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Credits**

- **Developer**: Abhinav Saurabh

---

## **Contact**

For questions, feedback, or support, please contact:

- **Email**: abhinav20127@iiitd.ac.in
- **LinkedIn**: [Abhinav Saurabh](https://linkedin.com/in/abhinavsaurabh)

---

Thank you for using the ADB Log Capture Tool! We look forward to your feedback and contributions.

