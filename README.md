# AutoPP (Pixel People Automation)

Automation scripts for the Android game **Pixel People** powered by [adbutils](https://github.com/openatx/adbutils) and [OpenCV](https://opencv.org/).

---

## Features

- **Utopium Harvester (`utopium.py`)**:
  - Automatically navigates across the city by swiping left and right.
  - Detects tree notification bubbles on the screen using multi-scale OpenCV template matching (`notification_tree.png`).
  - Clicks and pops bubbles to harvest Utopium, automatically handling accidental dialog popups.

- **Heart & Animal Collector (`animals.py`)**:
  - Monitors the screen to detect when a heart is ready for collection.
  - Opens the heart mini-game, identifies heart positions using edge detection (Gaussian blur + Canny filter), and collects them to obtain new animals.

- **Fast Computer Vision (`screen.py`)**:
  - Pre-scaled template matching with morphological local peak detection for efficient and duplicate-free bubble targeting.
  - Configurable matching thresholds and scale factors.

---

## Prerequisites

1. **Android Device or Emulator**:
   - Pixel People installed and open.
   - **USB Debugging** enabled in Developer Options.
   - Device connected to your computer via USB (or wireless ADB).
   - Default coordinates and scaling are calibrated for **2340x1080** screen resolution.
2. **ADB (Android Debug Bridge)**:
   - Ensure ADB is installed and your device shows up when running:
     ```bash
     adb devices
     ```
3. **Python 3.10+** (tested on Python 3.12).

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/autopp.git
   cd autopp
   ```

2. **Create and activate a virtual environment:**
   - **Linux / macOS:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```

3. **Install the package and dependencies:**
   ```bash
   pip install -e .
   ```

---

## Usage

Make sure your device is connected via ADB and the *Pixel People* game is open on screen.

### Harvest Utopium
Runs an infinite loop swiping across the town and popping tree notification bubbles:
```bash
python utopium.py
```

### Collect Hearts and Animals
Monitors and claims hearts as soon as they appear:
```bash
python animals.py
```

---

## Configuration & Tuning

If you are using a device with a different screen resolution or scale:
- **Bubble Template Scale**: Adjust `SCALES` in `screen.py` (e.g. `[0.78, 0.80]` for 2340x1080).
- **Coordinates**: Update the tap / swipe coordinates in `actions.py` and `screen.py` (`check_heart`, `close_notification`, etc.) to match your device resolution.

---

## Project Structure

```text
autopp/
├── actions.py             # Basic swipe actions
├── animals.py             # Heart collection loop
├── notification_tree.png  # Template image for tree bubble matching
├── screen.py              # Screenshot taking, template matching, and heart detection
├── utopium.py             # Utopium harvesting loop
├── pyproject.toml         # Build configuration and dependency specifications
├── .gitignore             # Git ignore file for Python, IDEs, and environments
└── README.md              # Project documentation
```

---

## License

This project is open source and available under the [MIT License](LICENSE).
