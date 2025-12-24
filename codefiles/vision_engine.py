import cv2
from deepface import DeepFace
import torch
import numpy as np

class EmotionSystem:
    def __init__(self):
        print("--- Python Engine Starting ---")
        
        # 1. Check GPU Status
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Processor: {self.device.upper()}")
        
        # 2. Load Face Detection Model (using OpenCV's built-in Haarcascade for speed)
        # This is much lighter on battery than the deep learning detectors
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # 3. Open Webcam
        self.cap = cv2.VideoCapture(0)
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def get_frame_analysis(self, power_mode):
        ret, frame = self.cap.read()
        if not ret:
            return ["No Camera", 0.0]

        top_emotion = "Neutral"
        score = 0.0
        
        # Detect faces (Fast method)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

        if power_mode == "high":
            # HIGH POWER: Run Deep Learning Emotion Analysis
            for (x, y, w, h) in faces:
                # Extract face area
                face_img = frame[y:y+h, x:x+w]
                
                try:
                    # Run DeepFace analysis (The heavy AI part)
                    # We turn off 'enforce_detection' to prevent crashes if face is blurry
                    results = DeepFace.analyze(face_img, actions=['emotion'], 
                                             enforce_detection=False, silent=True)
                    
                    # DeepFace returns a list, we take the first result
                    result = results[0]
                    emotions = result['emotion']
                    
                    # Sort emotions by score descending
                    sorted_emotions = sorted(emotions.items(), key=lambda item: item[1], reverse=True)
                    
                    top_emotion = sorted_emotions[0][0]
                    score = sorted_emotions[0][1]
                    
                    # Compound Emotion Logic: Check if 2nd best is close (within 15%)
                    if len(sorted_emotions) > 1:
                        second_emotion = sorted_emotions[1][0]
                        second_score = sorted_emotions[1][1]
                        
                        if (score - second_score) < 15.0:
                            top_emotion = f"{top_emotion}-{second_emotion}"

                    # Draw Box & Label
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, f"{top_emotion} ({int(score)}%)", (x, y-10), 
                                self.font, 0.8, (0, 255, 0), 2)
                except:
                    pass # Skip if analysis fails momentarily

            cv2.putText(frame, "MODE: HIGH PERFORMANCE (DeepFace AI)", (10, 30), 
                        self.font, 0.7, (0, 255, 0), 2)

        elif power_mode == "low":
            # LOW POWER: Only track faces, DO NOT run emotion AI
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 165, 255), 2)
            
            # Grayscale effect to visualize power saving
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            
            top_emotion = "Paused"
            cv2.putText(frame, "MODE: ENERGY SAVER (AI OFF)", (10, 30), 
                        self.font, 0.7, (0, 165, 255), 2)

        cv2.imshow("Hybrid R+Python System", frame)
        cv2.waitKey(1)
        
        return [top_emotion, score]

    def release_camera(self):
        self.cap.release()
        cv2.destroyAllWindows()