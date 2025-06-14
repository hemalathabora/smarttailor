import cv2
import mediapipe as mp
import numpy as np

def estimate_measurements(image_path):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True)
    mp_drawing = mp.solutions.drawing_utils

    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if not results.pose_landmarks:
        return None  # No landmarks detected

    landmarks = results.pose_landmarks.landmark

    # Example calculation: pixel distance between shoulders (landmarks 11 and 12)
    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]

    image_height, image_width, _ = image.shape
    shoulder_width_px = abs((right_shoulder.x - left_shoulder.x) * image_width)

    # Assume avg shoulder width in real life is 16 inches → calculate pixels-to-inches scale
    pixel_to_inch_scale = 16.0 / shoulder_width_px if shoulder_width_px > 0 else 1

    def pixel_distance(p1, p2):
        return np.sqrt(
            (p1.x - p2.x) ** 2 +
            (p1.y - p2.y) ** 2
        ) * image_width  # Assuming width ≈ height scale

    # Estimate other measurements
    chest_width = pixel_distance(landmarks[11], landmarks[12]) * pixel_to_inch_scale
    waist_width = pixel_distance(landmarks[23], landmarks[24]) * pixel_to_inch_scale
    hip_width = pixel_distance(landmarks[25], landmarks[26]) * pixel_to_inch_scale
    height_estimate = (landmarks[0].y - landmarks[32].y) * image_height * pixel_to_inch_scale * 0.5

    return {
        'shoulder': round(shoulder_width_px * pixel_to_inch_scale, 2),
        'chest': round(chest_width, 2),
        'waist': round(waist_width, 2),
        'hip': round(hip_width, 2),
        'height': round(height_estimate, 2)
    }
