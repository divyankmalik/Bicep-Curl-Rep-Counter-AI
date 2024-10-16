# Bicep-Curl-Rep-Counter-AI
This AI-powered model, developed in Python, accurately tracks and counts repetitions by analyzing image-based predictions of extension and contraction movements. Using advanced image recognition and prediction techniques, the model identifies each completed rep, providing a precise count to support your training or exercise regimen.

![Screenshot 2024-10-15 231008](https://github.com/user-attachments/assets/96fb21d8-3f42-4510-a4d2-0f8975d7099e)
Extension
![Screenshot 2024-10-15 231028](https://github.com/user-attachments/assets/62b671b0-5438-4014-abd1-38c821ffe61d)
Contraction
![Screenshot 2024-10-15 231123](https://github.com/user-attachments/assets/fcf359a9-15cd-4619-9527-33ed7bfce9c6)
Model Trained

![Screenshot 2024-10-15 231146](https://github.com/user-attachments/assets/429fed59-533f-4127-b91b-7cd23edc4daf)
Starts Counting Reps with Prediction for each frame

Model Training: I built a Model class using the LinearSVC classifier from Scikit-Learn. I trained this model on grayscale images representing two classes: extended and contracted bicep states. Each image was resized to a consistent shape, flattened, and then fed into the SVM model for classification. I added a button in the GUI to trigger the training process, and after training, the model was ready to make predictions.

Real-Time Prediction: In my prediction function, I captured frames from the camera, resized them, converted them to grayscale, and flattened them to match the input format expected by the model. The model tracks the last prediction, so when it detects a transition from class 1 (extended) to class 2 (contracted), it increments the repetition counter. This prediction process runs in real-time, updating with each frame processed.

GUI with Tkinter: I used the App class to design a simple, functional GUI with Tkinter, including buttons for:

Toggle Counting: This button enables or disables the counting mode, allowing me to control when to start and stop rep counting.
Save Class Images: These buttons capture frames and save them as images in separate folders for each class, making it easy to collect training data for the model.
Train Model: This button triggers the model training, using the saved images from each class.
Reset Counter: This resets the repetition counter displayed on the GUI.
The main display shows the live camera feed, and the repetition counter updates in real-time as the model detects complete reps.

Frame Capture and Display: I used OpenCV to capture frames from the camera and display them on the Tkinter canvas. The repetition counter on the GUI updates whenever the model detects a rep (from extended to contracted).

Through this project, I successfully combined image processing, machine learning, artificial intelligence and GUI design to create an interactive bicep curl rep counter. It was a great learning experience, and I’m pleased with the final result!


