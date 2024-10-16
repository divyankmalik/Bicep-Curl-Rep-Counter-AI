import cv2
import numpy as np
from sklearn.svm import LinearSVC

class Model:
    def __init__(self):
        self.model = LinearSVC(max_iter=1000)
        self.is_trained = False
        self.last_prediction = None
        self.rep_counter = 0

    def train_model(self, counters):
        img_list = []  # List to hold flattened image data
        class_list = []  # List to hold class labels

        # Class 1 images
        for i in range(1, counters[0]):
            img = cv2.imread(f"1/frame{i}.jpg", cv2.IMREAD_GRAYSCALE)
            if img is not None:
                resized_img = cv2.resize(img, (150, 162))  # Resize to a consistent size
                img_flat = resized_img.flatten()
                img_list.append(img_flat)
                class_list.append(1)

        # Class 2 images
        for i in range(1, counters[1]):
            img = cv2.imread(f"2/frame{i}.jpg", cv2.IMREAD_GRAYSCALE)
            if img is not None:
                resized_img = cv2.resize(img, (150, 162))  # Resize to a consistent size
                img_flat = resized_img.flatten()
                img_list.append(img_flat)
                class_list.append(2)

        if img_list:
            img_array = np.array(img_list)
            class_array = np.array(class_list)
            self.model.fit(img_array, class_array)
            self.is_trained = True
            print("Model successfully trained!")
        else:
            print("No images to train on.")

    def predict(self, frame):
        if frame is None:
            print("Failed to capture frame from camera.")
            return None  # Return None if frame is invalid

        try:
            resized_frame = cv2.resize(frame, (150, 162))
            frame_gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
            img_flat = frame_gray.flatten()

            if self.is_trained:
                prediction = self.model.predict([img_flat])
                print(f"Prediction: {prediction}")

                # Increment rep_counter if prediction changes from 1 to 2
                if self.last_prediction == 1 and prediction[0] == 2:
                    self.rep_counter += 1
                    print(f"Rep Count: {self.rep_counter}")

                # Update last prediction
                self.last_prediction = prediction[0]

                # Return the updated rep counter for the GUI to update the label
                return self.rep_counter
            else:
                print("Model not trained. Please train the model first.")
                return None
        except cv2.error as e:
            print(f"OpenCV Error: {e}")
            return None
