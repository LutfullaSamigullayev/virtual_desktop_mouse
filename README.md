# 🖱️ AI Virtual Mouse

A real-time AI-powered virtual mouse that allows users to control their computer cursor using hand gestures captured through a webcam.

The project uses **Python**, **OpenCV**, and **MediaPipe Hand Landmarker** to detect hand landmarks and translate hand movements into mouse actions.

## ✨ Features

- Real-time hand tracking using webcam.
- Hand landmark detection with MediaPipe.
- Cursor movement using index finger.
- Pinch gesture detection for mouse clicking.
- Smooth cursor movement.
- Webcam-based interaction without a physical mouse.

## 🛠️ Technologies

- Python 3.12
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy

## 📁 Project Structure

```text
VIRTUAL_DESKTOP_MOUSE/
│
├── models/
│   └── hand_landmarker.task
│
├── virtual_mouse.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/virtual-desktop-mouse.git
```

### 2. Navigate to the project directory

```bash
cd virtual-desktop-mouse
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows (Git Bash):**

```bash
source .venv/Scripts/activate
```

**Windows (CMD):**

```cmd
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Usage

Run the application:

```bash
python virtual_mouse.py
```

Make sure your webcam is connected and accessible.

## 🖐️ Hand Gestures

| Gesture | Action |
|---|---|
| Index finger movement | Move cursor |
| Thumb and index finger pinch | Mouse click |
| Hand tracking | Real-time cursor control |

*Note: Actual gesture behavior depends on the implementation in `virtual_mouse.py`.*

## 📦 Requirements

- Python 3.12
- Webcam
- Windows operating system
- Internet connection for initial dependency installation

## 🔧 Troubleshooting

**1. Webcam not detected**

- Check whether your webcam is connected.
- Close other applications that may be using the camera.

**2. ModuleNotFoundError**

Run:

```bash
pip install -r requirements.txt
```

**3. MediaPipe model not found**

Make sure the model file exists:

```text
models/hand_landmarker.task
```

## 🔮 Future Improvements

- Left and right mouse click gestures.
- Double-click gesture.
- Scroll control using hand gestures.
- Drag and drop functionality.
- Gesture-based keyboard shortcuts.
- Improved cursor smoothing and tracking accuracy.

## 👨‍💻 Author

Developed as an AI and Computer Vision learning project.

---

**AI Virtual Mouse — Control your computer with hand gestures.**