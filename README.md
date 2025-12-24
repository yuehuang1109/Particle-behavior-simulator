# Particle-behavior-simulator

A 2D particle collision simulator built with Python, NumPy, and Matplotlib, featuring elastic collisions and interactive parameter control.

This is a TERM PROJECT written to focus on
- 2D elastic collisions and their physical behavior
- Object-oriented programming (class `particle`)
- Interactive UI

Features
- 2D particle motion and collision simulation
- Elastic collisions between particles, as well as collisions between particles and walls
- Interactive UI implemented using Matplotlib
- Adjustable parameters, including "Radius", "Mass", "Elastic coefficient", "Area size", and "Number of particles"
- Pause and resume functionality
- Reset system with new initial conditions

REQs
- Python
- NumPy
- Matplotlib

Functions and principle
- Create a class called `particle`, including the parameters mass, posit, velo, rad, and e (elastic coefficient),
  with class functions `move` and `turn` (`turn` is an additional function which is not actually used in this project)
- Functions controlling collisions with walls and between particles
- The main function can be separated into several parts
-   Lines 56–85: creating figures, buttons, and sliders in order to control mode toggles and simulation parameters
-   Lines 106–161: particle initialization, designed to initialize particle conditions by assigning all properties.
    First, detecting the modes of radius and mass, then choosing the method to distribute particle properties.Also, assigning particles its random position.Finally setting the boundaries and refresh the interface.
-   Lines 163-180: Respawning particles when the conditions changed.
-   Lines 183-197: Creating buttons and its func.
-   Lines 237-262: Update by refreshing interface a time per 0.05 sec

Developing process
All ideas come from general physics lectures, especially the topic of gass physics.
Thus, this project aims to build a simulator to visualize the behavior of ga particles.
One limitation is that the simulation cannot precisely describe real gas behavior due to limited physics background
and the project deadline.
LLMs were used in this project, but mostly for debugging issues related to constructing interactive interfaces
using Matplotlib.
In addition, LLMs were sometimes used to learn new programming syntax(for me).
However, when dealing with Lines 163–180, there were still some unresolved issues, so I asked ChatGPT to help
complete this part.
All sections where LLMs were used are listed below.
https://chatgpt.com/g/g-p-69311dff84a88191be2624bba940c0d3-term-project/shared/c/694b4e95-c334-8322-bb13-5514788d4331?owner_user_id=user-P1TVWZnKek6SgTqdDbmUyUce
