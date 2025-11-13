import tkinter as tk
import cv2
from PIL import Image, ImageTk

class CameraApp:
    def __init__(self, root):
        self.root = root
        root.title("HoverCraft3000")

        # video display
        self.video_label = tk.Label(root)
        self.video_label.pack()

        # control buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill="x", pady=8)

        self.start_btn = tk.Button(btn_frame, text="Turn On Camera", width=15, command=self.start_camera)
        self.start_btn.pack(side="left", padx=4)

        self.stop_btn = tk.Button(btn_frame, text="Turn Off Camera", width=15, command=self.stop_camera, state="disabled")
        self.stop_btn.pack(side="left", padx=4)

        self.quit_btn = tk.Button(btn_frame, text="Quit", width=15, command=self.on_close)
        self.quit_btn.pack(side="right", padx=4)

        self.cap = None
        self.running = False

        # handle window close
        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_camera(self):
        if self.running:
            return
        # open default camera (0)
        self.cap = cv2.VideoCapture(0, cv2.CAP_ANY)
        if not self.cap.isOpened():
            tk.messagebox.showerror("Camera error", "Unable to open camera (index 0).")
            self.cap.release()
            self.cap = None
            return

        self.running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self._update_frame()

    def stop_camera(self):
        if not self.running:
            return
        self.running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        # release will be done in on_close or here
        if self.cap:
            self.cap.release()
            self.cap = None
        # clear image
        self.video_label.config(image="")

    def _update_frame(self):
        if not self.running or not self.cap:
            return
        ret, frame = self.cap.read()
        if not ret:
            # camera read failed — stop
            self.stop_camera()
            return
        # convert BGR (OpenCV) to RGB (PIL)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        # keep reference to avoid GC
        self.video_label.imgtk = imgtk
        self.video_label.config(image=imgtk)
        # schedule next frame (approx 30 FPS)
        self.root.after(33, self._update_frame)

    def on_close(self):
        # stop and release camera before exit
        self.running = False
        if self.cap:
            try:
                self.cap.release()
            except Exception:
                pass
            self.cap = None
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()