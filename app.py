import tkinter as tk
import os
import PIL.Image, PIL.ImageTk
import camera
import model
import cv2
import numpy as np

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Biceps Rep Counter")

        self.counters = [1, 1]
        self.rep_counter = 0
        self.last_prediction = 0
        self.counting_enabled = False
        self.camera = camera.Camera()
        self.model = model.Model()

        self.init_gui()

        self.delay = 15
        self.update()

        self.window.attributes("-topmost", True)
        self.window.mainloop()

    def init_gui(self):
        self.canvas = tk.Canvas(self.window, width=self.camera.width, height=self.camera.height)
        self.canvas.pack()

        self.btn_toggleauto = tk.Button(self.window, text="Toggle Counting", command=self.counting_toggle)
        self.btn_toggleauto.pack(anchor=tk.CENTER, expand=True)

        self.btn_class_one = tk.Button(self.window, text="Extended", width=50, command=lambda: self.save_for_class(1))
        self.btn_class_one.pack(anchor=tk.CENTER, expand=True)

        self.btn_class_two = tk.Button(self.window, text="Contracted", width=50, command=lambda: self.save_for_class(2))
        self.btn_class_two.pack(anchor=tk.CENTER, expand=True)

        self.btn_train = tk.Button(self.window, text="Train Model", width=50, command=lambda: self.model.train_model(self.counters))
        self.btn_train.pack(anchor=tk.CENTER, expand=True)

        self.btn_reset = tk.Button(self.window, text="Reset", width=50, command=self.reset)
        self.btn_reset.pack(anchor=tk.CENTER, expand=True)

        self.counter_label = tk.Label(self.window, text=f"{self.rep_counter}", font=("Arial", 24))
        self.counter_label.pack(anchor=tk.CENTER, expand=True)

    def update(self):
        if self.counting_enabled:
            if self.model.is_trained:
                ret, frame = self.camera.get_frame()
                if ret and frame is not None:
                    self.predict(frame)
                else:
                    print("Failed to capture a valid frame from the camera.")
            else:
                print("Train the model first!")

        self.counter_label.config(text=f"{self.rep_counter}")

        ret, frame = self.camera.get_frame()
        if ret and frame is not None:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def predict(self, frame):
        if self.counting_enabled:
            if self.model.is_trained:
                prediction = self.model.predict(frame)
                if prediction:
                    self.rep_counter = self.model.rep_counter
            else:
                print("Train the model first!")

    def counting_toggle(self):
        self.counting_enabled = not self.counting_enabled

    def save_for_class(self, class_num):
        ret, frame = self.camera.get_frame()
        if not ret:
            print("Error: Frame capture failed.")
            return

        if not os.path.exists("1"):
            os.mkdir("1")
        if not os.path.exists("2"):
            os.mkdir("2")

        filename = f"{class_num}/frame{self.counters[class_num - 1]}.jpg"

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        cv2.imwrite(filename, gray_frame)

        img = PIL.Image.open(filename)
        img.thumbnail((150,150), PIL.Image.LANCZOS)
        img.save(filename)
        self.counters[class_num - 1] += 1

    def reset(self):
        self.rep_counter = 0
        self.counter_label.config(text=f"{self.rep_counter}")

if __name__ == "__main__":
    App()
