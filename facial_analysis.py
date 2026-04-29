import cv2
import numpy as np
import sys
import os

# Mediapipe check
try:
    import mediapipe as mp
    mp_face_mesh = mp.solutions.face_mesh
except Exception as e:
    # Agar library missing hai toh result Oval|Fair hi aayega
    print(f"RESULT: Oval | Fair")
    sys.exit(0)

def run_analysis(img):
    try:
        h, w = img.shape[:2]
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1) as mesh:
            results = mesh.process(img_rgb)

        if not results.multi_face_landmarks:
            # Face detect nahi hua toh hamesha default results aate hain
            return "Oval", "Fair"

        face = results.multi_face_landmarks[0].landmark
        
        # --- 1. FACE SHAPE LOGIC (Landmarks Improvement) ---
        # Height: Forehead (10) to Chin (152)
        face_height = abs(face[152].y - face[10].y) * h
        # Width: Left cheek (234) to Right cheek (454)
        face_width = abs(face[454].x - face[234].x) * w
        
        ratio = face_height / face_width

        # Widths for Shape check
        forehead_w = abs(face[332].x - face[103].x) * w
        jaw_w = abs(face[361].x - face[132].x) * w

        # Decision Logic (Dynamic Thresholds)
        if ratio > 1.45:
            shape = "Oval"
        elif ratio < 1.22:
            shape = "Round"
        elif forehead_w > jaw_w * 1.15:
            shape = "Heart"
        elif ratio > 1.28 and ratio < 1.45 and jaw_w > forehead_w * 0.95:
            shape = "Square"
        else:
            shape = "Diamond"

        # --- 2. SKIN TONE LOGIC (Cheek Sampling is better) ---
        # Nose bridge (1) ke bajaye Cheek (234 ya 454) ka area zyada accurate hai
        # Hum dono cheeks ka average brightness nikalenge
        cx1, cy1 = int(face[234].x * w), int(face[234].y * h)
        cx2, cy2 = int(face[454].x * w), int(face[454].y * h)
        
        # Safe sampling (boundary checks)
        sample1 = img[max(0, cy1-10):min(h, cy1+10), max(0, cx1-10):min(w, cx1+10)]
        sample2 = img[max(0, cy2-10):min(h, cy2+10), max(0, cx2-10):min(w, cx2+10)]
        
        brightness = (np.mean(sample1) + np.mean(sample2)) / 2

        # Adjusted Thresholds for Indian Skin Tones & Lighting
        if brightness > 195: tone = "Fair"
        elif brightness > 165: tone = "Medium"
        elif brightness > 135: tone = "Olive"
        elif brightness > 105: tone = "Dusky"
        else: tone = "Dark"

        return shape, tone

    except Exception as e:
        # Debugging ke liye terminal check karein
        # print(f"Error: {e}") 
        return "Oval", "Fair"

def capture_from_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened(): return None
    frame_captured = None
    
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        cv2.putText(frame, "Align Face & Press SPACE", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.imshow("Analysis Window", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 32: # SPACE to Capture
            frame_captured = frame.copy()
            break
        elif key == 27: # ESC to Cancel
            break
            
    cap.release()
    cv2.destroyAllWindows()
    return frame_captured

if __name__ == "__main__":
    image = None
    # 1. Path check
    if len(sys.argv) > 1 and sys.argv[1] != "CAMERA":
        if os.path.exists(sys.argv[1]):
            image = cv2.imread(sys.argv[1])
    
    # 2. Webcam check if no image
    if image is None:
        image = capture_from_webcam()

    # 3. Final Output
    if image is not None:
        shape, tone = run_analysis(image)
        # Yeh format app.py ko results redirect karne mein help karta hai
        print(f"RESULT: {shape} | {tone}")
    else:
        print("RESULT: Oval | Fair")
    
    sys.stdout.flush()