import cv2
from fer import FER
import pyttsx3
import time
import random
import numpy as np

emotion_detector = FER(
    mtcnn=True,
    scale_factor=0.5  
)

#text-to-speech engine
tts_engine = pyttsx3.init()

# detected emotions with multiple options
compliments = {
    "happy": [
        "Your smile lights up the room!",
        "Your joy is contagious!",
        "You have such a wonderful smile!"
    ],
    "neutral": [
        "Your presence is calm and confident!",
        "You have a wonderful aura about you!",
        "You carry yourself with grace!"
    ],
    "sad": [
        "You've got this, keep going!",
        "Tomorrow will be better!",
        "Your strength is admirable!"
    ],
    "angry": [
        "Take a deep breath and stay calm.",
        "Your passion shows your dedication!",
        "Channel that energy into something positive!"
    ],
    "disgust": [
        "Every emotion is valid. You're doing great.",
        "It's okay to feel what you feel.",
        "Your honesty is refreshing!"
    ],
    "fear": [
        "You are stronger than your fears.",
        "Face your challenges with courage!",
        "You've overcome so much already!"
    ],
    "surprise": [
        "Wow, life is full of exciting moments!",
        "Your expressions are so genuine!",
        "You bring such energy to every moment!"
    ]
}

def get_compliment(emotion):
    """Return a random compliment based on the detected emotion."""
    if emotion.lower() in compliments:
        return random.choice(compliments[emotion.lower()])
    return "You are amazing just as you are!"

def speak_compliment(compliment):
    """Use text-to-speech to say the compliment."""
    try:
        tts_engine.say(compliment)
        tts_engine.runAndWait()
    except Exception as e:
        print(f"Error in text-to-speech: {e}")

def analyze_emotions(frame):
    """
    Detect and return the dominant emotion in the frame with improved accuracy.
    Returns: (emotion, face_box, confidence)
    """
    try:
        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        
        gray_frame = cv2.equalizeHist(gray_frame)
        
        # Detect faces and emotions
        results = emotion_detector.detect_emotions(frame)

        if results:
            # Get the first detected face's emotion
            emotions = results[0]["emotions"]
            
            
            MIN_CONFIDENCE = 0.3
            emotions = {k: v for k, v in emotions.items() if v >= MIN_CONFIDENCE}
            
            if emotions:
                dominant_emotion = max(emotions, key=emotions.get)
                confidence = emotions[dominant_emotion]
                
                box = results[0]["box"]
                
                return dominant_emotion, box, confidence
        return None, None, None
    except Exception as e:
        print(f"Error analyzing emotions: {e}")
        return None, None, None

def draw_privacy_notice(frame):
    """Draw privacy notice on the frame."""
    notice = "Privacy Notice: All processing is done locally"
    cv2.putText(frame, notice, 
                (10, frame.shape[0] - 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, (255, 255, 255), 1)

def main():
    """Main function to run emotion detection."""
    cap = cv2.VideoCapture(0)
    
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    
  
    last_detected_emotion = None
    current_compliment = None
    last_detection_time = None
    detection_interval = 10
    
    
    emotion_history = []
    HISTORY_LENGTH = 2
    
    print("Starting Smart Mirror...")
    print("Press 'q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame to create a mirror effect
        frame = cv2.flip(frame, 1)
        
        # Resize frame for better performance while maintaining quality
        frame = cv2.resize(frame, (640, 480))

        current_time = time.time()

        # Calculate time until next detection
        time_remaining = 0
        if last_detection_time:
            time_remaining = max(0, detection_interval - (current_time - last_detection_time))

        should_detect = (
            last_detection_time is None or 
            current_time - last_detection_time >= detection_interval
        )

        if should_detect:
            current_emotion, face_box, confidence = analyze_emotions(frame)
            
            if current_emotion and confidence:
                # Add to emotion history
                emotion_history.append(current_emotion)
                if len(emotion_history) > HISTORY_LENGTH:
                    emotion_history.pop(0)
                
                # Only update emotion if we have consistent readings
                if len(emotion_history) == HISTORY_LENGTH and \
                   all(e == emotion_history[0] for e in emotion_history):
                    
                    stable_emotion = emotion_history[0]
                    
                    # Draw rectangle around the face
                    if face_box:
                        (x, y, w, h) = face_box
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    # Update emotion and compliment
                    if stable_emotion != last_detected_emotion:
                        current_compliment = get_compliment(stable_emotion)
                        speak_compliment(current_compliment)
                        last_detected_emotion = stable_emotion

                    last_detection_time = current_time
                    
                    # Display confidence score
                    cv2.putText(frame, f"Confidence: {confidence:.2f}", 
                              (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 
                              0.6, (0, 255, 0), 2)

        # Display information
        if last_detected_emotion:
            # Display emotion and confidence
            cv2.putText(frame, f"Emotion: {last_detected_emotion}", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, (255, 255, 255), 2)
            
            # Display compliment
            if current_compliment:
                cv2.putText(frame, current_compliment, 
                            (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                            0.6, (0, 255, 255), 2)

        # Display countdown timer
        cv2.putText(frame, f"Next detection in: {int(time_remaining)}s", 
                    (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, (0, 255, 0), 2)

       
        draw_privacy_notice(frame)

        # Display the video feed
        cv2.imshow("Smart Mirror - Emotion Detection", frame)

        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("Shutting down Smart Mirror...")
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()