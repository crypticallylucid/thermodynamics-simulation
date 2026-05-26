# Piston & Particle Simulation

## Overview
This is a python simulation that displays the motion of particles as they undergo isothermic, isobaric, and isovolumetric processes by moving pistons and adding heat. This simulation additionally graphs pressure vs volume as well as pressure vs temperature during all processes.

## Dependencies
Ensure that Python 3.x is installed. This project uses the `tkinter` library as well as `matplotlib` to display the particles, buttons, and graphs. `tkinter` is included with standard python installations, but `matplotlib` will need to be installed.

You can install matplotlib using pip
```bash
pip install matplotlib
```

## Installation and Running the Simulation  
1. Clone the repository.
```bash
git clone https://github.com/crypticallylucid/physicsfinal.git
cd physicsfinal
```
2. If necessary, ensure that `start-gui.sh` is executable. `start-gui.sh` is used to display the simulation through noVNC on ports 5900 and 6080, often needed if the simulation is being run on a displayless virtual machine.
```bash
chmod +x start-gui.sh
```
3. If necessary, setup noVNC.
```bash
./start-gui.sh
export DISPLAY=:1
```
4. Run the simulation.
```bash
python main.py
```

## Demo
https://github.com/user-attachments/assets/75018646-fb78-493e-9c61-0da5e24cef24


## Codebase Overview
### `main.py`
This controls the main simulation. It controls the following 4 things:
1. **Display Loop:** Manages the tkinter canvas, keeping the simulation running.
2. **Calculations and Graphing:** Calculates and graphs the temperatures, pressures, and volumes at each point on the graph.
3. **Collision:** Ensures that particles properly collide with each other, simulating perfectly elastic collisions.
4. **Buttons:** Creates the functionality for all the buttons to interact with the simualation

### `ball.py`
This is the ball object. It is the foundation for each individual particle handles the following 2 things:
1. **Moving:** Redraws itself based on its xvelocity and yvelocity, as well as ensuring that the particles stay within the bounding box.
2. **Temperature Scaling:** Adjusts the ball's velocity based on either a multiplicative scalar or an additive scalar, allowing for the simulation to increase the velocity of each particle, increasing the temperature.

### `piston.py`
This is the piston object. It creates the piston that moves up and down, constraining the particles. It controlls the following 2 things:
1. **Moving:** Contains event functions to move the piston up and down.
2. **Collision:** Ensures that particles are moved if they were in the path of the piston moving and ensures that particles correctly bounce off the bottom of the piston.
