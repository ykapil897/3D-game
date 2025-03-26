# 🚀 Space Heist - 3D Space Navigation Game

**Space Heist** is a **3D space navigation game** developed using **Python and OpenGL**, where players control a transporter ship to reach a designated space station while avoiding pirate ships.

---

## 🌌 Overview
In this game, you play as a pilot of a transporter ship navigating through space to reach a **golden destination space station**. You must avoid or destroy **enemy pirate ships** that will try to stop you. The game features:

- First-person and third-person **view modes**
- A **navigation system** for guidance
- **Combat mechanics** with laser weapons

---

## 🎮 Features
✅ **3D Space Environment** with planets and space stations  
✅ **First-person & Third-person** camera views  
✅ **Physics-based** acceleration & deceleration  
✅ **Combat System** with laser weapons  
✅ **Enemy AI** that chases the player  
✅ **Minimap Navigation** with directional arrows  
✅ **Collision Detection System**  
✅ **ImGUI-based** menu interface  

---

## 🕹️ How to Play
| **Action**         | **Key/Button**       |
|--------------------|---------------------|
| Pitch up          | `W`                 |
| Pitch down        | `S`                 |
| Yaw left          | `A`                 |
| Yaw right         | `D`                 |
| Roll left         | `Q`                 |
| Roll right        | `E`                 |
| Increase speed    | `SPACE`             |
| Decrease speed    | `LEFT SHIFT`        |
| Fire laser        | `LEFT CLICK`        |
| Toggle camera view | `RIGHT CLICK`       |

🎯 **Objective:** Navigate to the **golden space station** to **win the game**!  

---

## 🔧 Requirements
Ensure you have the following installed:
- **Python 3.x**
- **OpenGL**
- **GLFW**
- **NumPy**
- **PyImGui**

---

## 📦 Installation
```sh
# Clone the repository
git clone https://github.com/your_username/space-heist.git
cd space-heist

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

---

## 📂 Game Structure
The game is organized into multiple **Python modules**:

- `main.py` → Entry point, manages game loop
- `game.py` → Core game mechanics, scene updates
- `graphics.py` → Graphics components, objects, shaders
- `window_manager.py` → Window & input handling
- `objects.py` → 3D object definitions
- `shaders.py` → GLSL shader code for rendering
- `models/` → 3D model files (OBJ format)

---

## 🎮 Game Screens
- **Main Menu** → Start screen with "New Game" button
- **Game Screen** → The main gameplay area
- **Victory Screen** → Displayed when player reaches the destination
- **Game Over Screen** → Displayed when player's ship is destroyed

---

## 🛠️ Development Notes
The game leverages **modern OpenGL techniques** such as:
- **Vertex & Index Buffer Objects (VBOs & IBOs)**
- **Vertex Array Objects (VAOs)**
- **GLSL Shaders** for rendering
- **Matrix-based transformations** for movement
- **ImGui** for UI elements

---

## 🏆 Contribute
Want to contribute? **Fork this repo** and submit a Pull Request! 🚀

---

## 📜 License
This project is licensed under the **MIT License**.

---

⭐ **If you like this project, consider giving it a star!** ⭐
