# Dynamic Energy-Aware Emotion Recognition System (Hybrid R + Python)

## 📌 Project Overview
This project implements an intelligent **Hybrid AI System** that dynamically adjusts its computational load based on the device's real-time energy status. It combines the statistical power of **R** with the deep learning capabilities of **Python**.

### 🚀 Key Features
- **Hybrid Architecture**: 
  - **R (The Brain)**: Monitors system health (Battery, CPU), determines operational modes, and orchestrates the workflow.
  - **Python (The Muscles)**: Executes heavy computer vision and deep learning tasks using OpenCV and DeepFace.
- **Dynamic Energy Adaptation**:
  - **High Power Mode (>30% Battery)**: Activates full Deep Learning emotion recognition (DeepFace) for high accuracy.
  - **Low Power Mode (<30% Battery)**: Switches to lightweight face tracking only, disabling neural networks to conserve battery.
- **Real-Time Processing**: Processes webcam feed in real-time with visual feedback on detected emotions and power modes.

---

## 🛠️ Architecture
The system follows a master-slave architecture:
1.  **Controller (R)**: 
    - Checks battery status via WMI (Windows Management Instrumentation).
    - Decides whether to run in `high` or `low` power mode.
    - Calls the Python engine via `reticulate`.
2.  **Vision Engine (Python)**:
    - Initialized once to load heavy models (DeepFace, PyTorch) into memory.
    - Exposes a `get_frame_analysis(mode)` method.
    - Performs face detection (Haar Cascades) and Emotion Recognition (DeepFace).

---

## 💻 Tech Stack
- **R**: Logic control, System monitoring (`reticulate`).
- **Python 3.12**: Computer Vision & AI (`opencv-python`, `deepface`, `torch`, `tf-keras`, `numpy`).
- **Hardware Acceleration**: Supports CUDA (NVIDIA GPU) for deep learning inference if available.

---

## ⚙️ Installation & Setup

### Prerequisites
- **R** (4.0+) installed.
- **Python 3.10+** installed.
- **Git** installed.

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/energy-aware-emotion-recognition.git
cd energy-aware-emotion-recognition
```

### 2. Set up Python Environment
The project requires specific Python libraries. You can install them manually or let the system use the pre-configured environment if you have one.

**Recommended: Create a Virtual Environment**
```bash
# Windows
python -m venv energy_env
.\energy_env\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Application
You can run the system directly using R. The script is designed to automatically link to the `energy_env` folder if it exists in the project root.

**Option A: Command Line**
```bash
Rscript main_controller.R
```

**Option B: RStudio**
1. Open `main_controller.R`.
2. Click **Source** or press `Ctrl+Shift+S`.

---

## 🎮 Usage
- **Start**: Run the script. The webcam window will open.
- **High Power**: If your battery is >30%, you will see emotion labels (e.g., "Happy 90%") and a green box.
- **Low Power**: If your battery drops below 30%, the AI turns off. You will see an orange box and "Energy Saver" text.
- **Stop**: Press `Esc` or `Ctrl+C` in the terminal to shut down the system safely.

---

## 📂 Project Structure
```
├── main_controller.R    # Main entry point (R Logic)
├── vision_engine.py     # Python Computer Vision Class
├── requirements.txt     # Python dependencies
├── .gitignore          # Git exclusion rules
└── README.md           # Project documentation
```

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License
[MIT](https://choosealicense.com/licenses/mit/)
