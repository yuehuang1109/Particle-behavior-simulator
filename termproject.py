import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons,Button

"""Particle class and functions for 2D collision simulation"""

#Class of particle
class particle:
    def __init__(self, mass, posit, velo, rad,e=1.0):
        self.mass = mass
        self.posit = np.array(posit, dtype=float)
        self.velo = np.array(velo, dtype=float)
        self.rad = rad  
        self.circle = None #for matplotlib circle patch
        self.e = e

    def move(self, dt):
        self.posit += self.velo * dt

    def turn(self, angle):
        turning_matrix = np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
        self.velo = self.velo.dot(turning_matrix)


def collide_2d(p1, p2):
        r = p1.posit - p2.posit
        dist = np.linalg.norm(r)
        min_dist = p1.rad + p2.rad
        if dist == 0 or dist > min_dist:
            return

        n = r / dist
        v_rel = np.dot(p1.velo - p2.velo, n)
        if v_rel >= 0:
            return

        e = p1.e # coefficient of restitution(in this simulator, all particles have the same e)
        m1, m2 = p1.mass, p2.mass
        J = -(1 + e) * v_rel / (1/m1 + 1/m2)
        
        p1.velo += (J / m1) * n
        p2.velo -= (J / m2) * n

        global bouncecounter
        bouncecounter += 1
        global bounce_text
        bounce_text.set_text(f'Bounces: {bouncecounter}')
    
bouncecounter = 0
bounce_text = None 
        
"""主程式"""
def main():
    global bounce_text
    
    fig = plt.figure(figsize=(8, 8))
    plt.subplots_adjust(left=0.3, bottom=0.25)
    bounce_text = fig.text(0.05, 0.95, f'Bounces: {bouncecounter}', fontsize=12, color='black', va='top')
    
    ax_slider_num = plt.axes([0.55, 0.22, 0.30, 0.01])
    slider_num = Slider(ax_slider_num, "Number of particles", 1, 150, valinit=10)

    ax_slider_Area = plt.axes([0.55, 0.18, 0.30, 0.01])
    slider_Area = Slider(ax_slider_Area, "AREA", 10, 50, valinit=20)

    ax_slider_mass = plt.axes([0.55, 0.14, 0.30, 0.01])
    slider_mass = Slider(ax_slider_mass, "Fixed mass", 0.1, 5.0, valinit=1.0)

    ax_slider_rad = plt.axes([0.55, 0.1, 0.30, 0.01])
    slider_rad = Slider(ax_slider_rad, "Fixed radius", 0.01, 0.5, valinit=0.05)

    ax_slider_E = plt.axes([0.55, 0.06, 0.30, 0.01])
    slider_E = Slider(ax_slider_E,"Elasticity Constant", 0, 1.0, valinit=1.0)

    ax_radio_mass = plt.axes([0.03, 0.60, 0.2, 0.10])
    radio_mass = RadioButtons(ax_radio_mass, ("fixed", "uniform", "normal"))
    ax_radio_mass.set_title("Mass mode")

    ax_radio_rad = plt.axes([0.03, 0.40, 0.2, 0.10])
    radio_rad = RadioButtons(ax_radio_rad, ("fixed", "uniform", "normal"))
    ax_radio_rad.set_title("Radius mode")
    
    ax_main = plt.axes([0.3, 0.3, 0.6, 0.6])
    ax_main.set_facecolor("black")
    ax_main.set_title("Main Simulation Area")
    
    par = []
    paused = False

    def clear_circles():
        ax_main.cla()
        for p in par:
            p.circle = None

    def build_circles():
        for p in par:
            p.circle = plt.Circle(p.posit, radius=p.rad, fill=True, color='cyan', alpha=1)
            ax_main.add_patch(p.circle)
            

    def Eupdate(val,particles):
        e = slider_E.val
        for p in particles:
            p.e = e

    def particle_init():  # create or change the particles based on current settings
        nonlocal par
        ax_main.cla()
        n = int(slider_num.val)
        L = float(slider_Area.val)
        e = float(slider_E.val)

        mass_mode = radio_mass.value_selected
        rad_mode  = radio_rad.value_selected

        # resize particle list if needed
        if len(par) != n:
            par = [particle(1.0, [0, 0], [0, 0], float(slider_rad.val), e=e) for _ in range(n)]

        clear_circles()

        positions = []

        for i in range(len(par)):
            # decide this particle's radius first (IMPORTANT for non-overlap)
            if rad_mode == 'fixed':
                new_rad = float(slider_rad.val)
            elif rad_mode == 'uniform':
                new_rad = float(np.random.uniform(0.01, float(slider_rad.val) * 2))
            else:  # normal
                new_rad = float(max(0.01, np.random.normal(float(slider_rad.val), float(slider_rad.val) / 4)))

            # place without overlap
            max_try = 5000
            for _ in range(max_try):
                posit = np.random.rand(2) * L
                if all(np.linalg.norm(posit - positions[j]) > (new_rad + par[j].rad) for j in range(len(positions))):
                    positions.append(posit)
                    break
            else:
                raise RuntimeError("Cannot place particles: area too crowded")

            par[i].posit = np.array(posit, dtype=float)
            par[i].rad = new_rad

            # mass
            if mass_mode == 'fixed':
                par[i].mass = float(slider_mass.val)
            elif mass_mode == 'uniform':
                par[i].mass = float(np.random.uniform(0.1, float(slider_mass.val) * 2))
            else:  # normal
                par[i].mass = float(max(0.1, np.random.normal(float(slider_mass.val), float(slider_mass.val) / 4)))

            par[i].velo = (np.random.rand(2) - 0.5) * L
            par[i].e = e

        # update axes + draw circles
        ax_main.set_xlim(0, L)
        ax_main.set_ylim(0, L)
        build_circles()
        fig.canvas.draw_idle()

    def respawn_particles(event=None):
        nonlocal paused
        particle_init()
        paused = True # pause after respawn
        
        global bouncecounter 
        bouncecounter = 0
        global bounce_text  
        bounce_text.set_text(f'Bounces: {bouncecounter}')
        

    #respanw when sliders change
    slider_num.on_changed(lambda val: respawn_particles())
    slider_Area.on_changed(lambda val: respawn_particles())
    slider_rad.on_changed(lambda val: respawn_particles())
    slider_mass.on_changed(lambda val: respawn_particles())
    slider_E.on_changed(lambda val: Eupdate(val, par))
    slider_E.on_changed(lambda val: respawn_particles())

    #respawn when radio buttons change
    def on_radio(label):
        respawn_particles()

    radio_mass.on_clicked(on_radio)
    radio_rad.on_clicked(on_radio)
    
    #$button to respawn and pause/resume  
    def toggle_pause(event):
        nonlocal paused
        paused = not paused
        
    button_respawn = Button(plt.axes([0.05, 0.10, 0.2, 0.04]), 'Respawn Particles')
    button_respawn.on_clicked(respawn_particles)
    button_pause = Button(plt.axes([0.05, 0.14, 0.2, 0.04]), 'Pause / Resume')
    button_pause.on_clicked(toggle_pause)
    
    particle_init() 
    
    #moving and collision detection
    def wall_bounce(p, L):
        global bouncecounter, bounce_text

        x, y = p.posit
        vx, vy = p.velo
        r = p.rad
        e = p.e

        bounced = False

        if x - r < 0:
            x = r
            vx = abs(vx) * e
            bounced = True
        elif x + r > L:
            x = L - r
            vx = -abs(vx) * e
            bounced = True

        if y - r < 0:
            y = r
            vy = abs(vy) * e
            bounced = True
        elif y + r > L:
            y = L - r
            vy = -abs(vy) * e
            bounced = True

        if bounced:
            bouncecounter += 1
            bounce_text.set_text(f'Bounces: {bouncecounter}')

        p.posit[:] = (x, y)
        p.velo[:] = (vx, vy)
        
    def update():
        N = len(par)    
        L = float(slider_Area.val)    
        dt = 0.05

        if paused:
            return
        for p in par:
            p.move(dt)
            wall_bounce(p, L)

        for i in range(N):
            for j in range(i+1, N):
                collide_2d(par[i], par[j])
                
        for p in par:
            if p.circle is not None:
                p.circle.center = p.posit

        fig.canvas.draw_idle()
        
    timer = fig.canvas.new_timer(interval=30)
    timer.add_callback(update)
    timer.start()
    
    plt.show()
    
    print("working")


if __name__ == "__main__":
    main()