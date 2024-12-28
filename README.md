# Smart Mirror Emotion Detection System

## Overview
This project implements a Smart Mirror feature that detects users' facial expressions in real-time and provides personalized compliments based on their emotional state. The system uses computer vision and emotion recognition technologies to create an interactive and uplifting experience.

### Key Features
- Real-time facial detection and emotion analysis
- Personalized compliments based on detected emotions
- Text-to-speech feedback
- Privacy-focused local processing
- 20-second interval emotion detection
- Confidence score display
- User-friendly interface with countdown timer

## Libraries and Tools Used
- **OpenCV**: For facial detection and image processing
- **FER (Facial Emotion Recognition)**: For emotion detection
- **pyttsx3**: For text-to-speech functionality
- **NumPy**: For numerical computations
- **Python 3.x**: As the primary programming language

## Installation

### Prerequisites
- Python 3.x
- Webcam
- Internet connection (only for initial package installation)

### Setup Instructions
1. Clone the repository:   ```bash
   git clone https://github.com/VinayakPaka/Smart-Mirror-Objective.git
   cd Smart-Mirror-Objective   ```

2. Create and activate a virtual environment:   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Linux/Mac
   # or
   myenv\Scripts\activate  # On Windows   ```

3. Install required packages:   ```bash
   pip install -r requirements.txt   ```

## Usage
1. Ensure your webcam is connected and functioning
2. Run the main script:   ```bash
   python main.py   ```
3. Position yourself in front of the camera
4. The system will:
   - Detect your face
   - Analyze your emotion every 20 seconds
   - Display the detected emotion and confidence score
   - Provide a personalized compliment
   - Speak the compliment through audio output

4. Press 'q' to quit the application

## Technical Challenges and Solutions

### 1. Emotion Detection Accuracy
**Challenge**: Initial emotion detection was not accurate enough for practical use.
**Solution**: 
- Implemented histogram equalization for better contrast
- Added confidence threshold filtering
- Introduced emotion stability tracking
- Optimized camera settings and frame processing

### 2. Performance Optimization
**Challenge**: Processing every frame was resource-intensive.
**Solution**: 
- Implemented interval-based detection (20 seconds)
- Optimized frame resizing
- Added efficient memory management

### 3. User Experience
**Challenge**: Feedback wasn't clear enough for users.
**Solution**: 
- Added visual countdown timer
- Implemented confidence score display
- Enhanced visual feedback with face detection rectangle
- Added multiple compliment variations for each emotion

## Privacy Considerations
- All processing is done locally on the user's machine
- No data is stored or transmitted
- No cloud services are used for processing
- Clear privacy notice displayed during operation

## Best Practices for Usage
1. Ensure good lighting conditions
2. Face the camera directly
3. Maintain a distance of 2-3 feet from the camera
4. Avoid rapid movements
5. Make clear expressions for better detection

## Troubleshooting
1. If emotion detection is not working:
   - Check lighting conditions
   - Ensure face is clearly visible
   - Verify webcam permissions

2. If audio is not working:
   - Check system audio settings
   - Verify pyttsx3 installation


## License
This project is licensed under the MIT License - see the LICENSE file for details. 