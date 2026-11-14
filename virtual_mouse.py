
import cv2
import mediapipe as mp
import pyautogui
import time
import math

from pathlib import Path

# =====================================
# 1. CONFIGURATION
# =====================================

MODEL_PATH = Path("models/hand_landmarker.task")

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model topilmadi: {MODEL_PATH}"
    )

# PyAutoGUI safety
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

SCREEN_W, SCREEN_H = pyautogui.size()

CAM_W = 640
CAM_H = 480

SMOOTHING = 5
PINCH_THRESHOLD = 0.045
MARGIN = 0.10

# =====================================
# 2. MEDIAPIPE CONFIGURATION
# =====================================

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=str(MODEL_PATH)
    ),
    running_mode=RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

# =====================================
# 3. CAMERA
# =====================================

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_W)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_H)

if not cap.isOpened():
    raise RuntimeError("Web Camera ochilmadi!")

# =====================================
# 4. VARIABLES
# =====================================

prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0

is_pinching = False
last_timestamp_ms = 0

prev_time = time.perf_counter()

# =====================================
# 5. HELPER FUNCTIONS
# =====================================

def distance(p1, p2):
    return math.hypot(
        p1.x - p2.x,
        p1.y - p2.y
    )


def map_to_screen(x, y):

    # Camera coordinates -> screen coordinates
    x = max(MARGIN, min(1 - MARGIN, x))
    y = max(MARGIN, min(1 - MARGIN, y))

    screen_x = int(
        (x - MARGIN) / (1 - 2 * MARGIN) * SCREEN_W
    )

    screen_y = int(
        (y - MARGIN) / (1 - 2 * MARGIN) * SCREEN_H
    )

    return (
        max(0, min(SCREEN_W - 1, screen_x)),
        max(0, min(SCREEN_H - 1, screen_y))
    )


# =====================================
# 6. MAIN LOOP
# =====================================

try:

    with HandLandmarker.create_from_options(options) as landmarker:

        print("AI Virtual Mouse started!")
        print("Move index finger to control cursor.")
        print("Pinch thumb and index finger to click.")
        print("Press ESC to exit.")

        while cap.isOpened():

            ret, frame = cap.read()

            if not ret:
                break

            # Mirror camera
            frame = cv2.flip(frame, 1)

            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb_frame
            )

            timestamp_ms = max(
                time.monotonic_ns() // 1_000_000,
                last_timestamp_ms + 1
            )
            last_timestamp_ms = timestamp_ms

            result = landmarker.detect_for_video(
                mp_image,
                timestamp_ms
            )

            status = "NO HAND"

            if result.hand_landmarks:

                landmarks = result.hand_landmarks[0]

                # Index finger tip = landmark 8
                index_tip = landmarks[8]

                # Thumb tip = landmark 4
                thumb_tip = landmarks[4]

                # Cursor position
                target_x, target_y = map_to_screen(
                    index_tip.x,
                    index_tip.y
                )

                # Smooth cursor movement
                curr_x = prev_x + (
                    target_x - prev_x
                ) / SMOOTHING

                curr_y = prev_y + (
                    target_y - prev_y
                ) / SMOOTHING

                # Move mouse
                pyautogui.moveTo(
                    int(curr_x),
                    int(curr_y)
                )

                prev_x, prev_y = curr_x, curr_y

                # Pinch detection
                pinch_distance = distance(
                    index_tip,
                    thumb_tip
                )

                pinching = (
                    pinch_distance < PINCH_THRESHOLD
                )

                # Click only once when pinch starts
                if pinching and not is_pinching:
                    pyautogui.click()
                    status = "CLICK"
                elif pinching:
                    status = "PINCH"
                else:
                    status = "MOVING"

                is_pinching = pinching

                # Draw hand landmarks
                h, w, _ = frame.shape

                for point_id in [4, 8]:
                    point = landmarks[point_id]

                    px = int(point.x * w)
                    py = int(point.y * h)

                    cv2.circle(
                        frame,
                        (px, py),
                        10,
                        (0, 255, 0),
                        -1
                    )

                # Draw line between thumb and index
                p1 = (
                    int(thumb_tip.x * w),
                    int(thumb_tip.y * h)
                )

                p2 = (
                    int(index_tip.x * w),
                    int(index_tip.y * h)
                )

                cv2.line(
                    frame,
                    p1,
                    p2,
                    (255, 0, 0),
                    3
                )

            else:
                is_pinching = False

            # FPS
            current_time = time.perf_counter()

            fps = 1 / max(
                current_time - prev_time,
                1e-6
            )

            prev_time = current_time

            cv2.putText(
                frame,
                f"FPS: {fps:.1f}",
                (15, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Status: {status}",
                (15, 65),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

            cv2.imshow(
                "AI Virtual Mouse",
                frame
            )

            if cv2.waitKey(1) & 0xFF == 27:
                break

except pyautogui.FailSafeException:
    print("Emergency stop: mouse moved to top-left corner!")

finally:
    cap.release()
    cv2.destroyAllWindows()

print("AI Virtual Mouse stopped!")
