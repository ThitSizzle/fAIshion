import cv2
import mediapipe as mp
import numpy as np
from sklearn.cluster import KMeans

mediapipePose = mp.solutions.pose

bodyTracker = mediapipePose.Pose(
    static_image_mode=True, 
    min_detection_confidence=0.5, 
    model_complexity=1
)

def analyzeImage(image):
    results = {
        "ratio": None, 
        "verticalRatio": None, 
        "bodyShape": "Unknown", 
        "proportion": "Unknown", 
        "skin_rgb": None, 
        "error": None
    }
    
    img = cv2.imread(image)
    if img is None:
        results["error"] = f"File not found at {image}"
        return results

    target_h = 800
    h, w = img.shape[:2]
    scale = target_h / h
    img = cv2.resize(img, (int(w * scale), target_h))
    
    h, w = img.shape[:2]
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    poseResults = bodyTracker.process(img_rgb)
    
    if not poseResults.pose_landmarks:
        results["error"] = "No human body detected, submit another image."
        return results
    
    bodyParts = poseResults.pose_landmarks.landmark

    def distance(p1, p2):
        return np.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)
        
    shoulderWidth = distance(bodyParts[11], bodyParts[12])
    hipWidth = distance(bodyParts[23], bodyParts[24])

    if hipWidth > 0:
        results["ratio"] = round(shoulderWidth/hipWidth, 2)
        if results["ratio"] > 1.05:
            results["bodyShape"] = "Inverted Triangle"
        elif results["ratio"] < 0.95:
            results["bodyShape"] = "Pear"
        else:
            results["bodyShape"] = "Rectangle/Hourglass"

    torsoLength = distance(bodyParts[11], bodyParts[23])
    legLength = distance(bodyParts[23], bodyParts[27])

    if torsoLength > 0:
        verticalRatio = round(legLength/torsoLength, 2)
        results["verticalRatio"] = verticalRatio
        if verticalRatio > 1.2:
            results["proportion"] = "Short torso with long legs"
        elif verticalRatio < 0.9:
            results["proportion"] = "Long torso with short legs"
        else:
            results["proportion"] = "Balanced Proportion"

    nose = bodyParts[0]
    noseX, noseY = int(nose.x * w), int(nose.y * h)

    y1, y2 = max(0, noseY-15), min(h, noseY+15)
    x1, x2 = max(0, noseX-15), min(w, noseX+15)
    
    croppedRegion = img_rgb[y1:y2, x1:x2]
    
    if croppedRegion.size > 0:
        pixels = croppedRegion.reshape(-1,3)
        kmeans = KMeans(n_clusters=1, n_init='auto')
        kmeans.fit(pixels)
        results["skin_rgb"] = kmeans.cluster_centers_[0].astype(int).tolist()

    return results
