import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors
import tkinter as tk
from tkinter import ttk, messagebox

# Constants
g = 9.81
timeOfFlight = 0  # Initialize timeOfFlight as a global variable
times = []  # Global variable to store times
velocities = []  # Global variable to store velocities
canvas = None  # Global variable to store the FigureCanvasTkAgg instance

# Functions for calculations and plotting
def calculate_and_plot():
    global timeOfFlight, times, velocities, canvas  # Declare global variables
    try:
        thetaDeg = float(angle_entry.get())
        u = float(velocity_entry.get())

        thetaRad = math.radians(thetaDeg)
        timeOfFlight = (2 * u * math.sin(thetaRad)) / g
        heightMax = (u**2 * (math.sin(thetaRad))**2) / (2 * g)
        rangeProjection = (u**2 * math.sin(2 * thetaRad)) / g

        horizontalV = u * math.cos(thetaRad)
        verticalV = u * math.sin(thetaRad)

        horizontalDistance = horizontalV * timeOfFlight

        # Calculate positions for plotting
        t = 0
        dt = 0.01
        x_values = []
        y_values = []

        times = []  # Reset times list
        velocities = []  # Reset velocities list

        while t <= timeOfFlight:
            x = horizontalV * t
            y = verticalV * t - 0.5 * g * t**2
            vx = horizontalV
            vy = verticalV - g * t
            velocity = math.sqrt(vx**2 + vy**2)
            x_values.append(x)
            y_values.append(y)
            velocities.append(velocity)
            times.append(t)
            t += dt

        # Clear previous plot if canvas exists
        if canvas:
            canvas.get_tk_widget().destroy()

        # Plotting the trajectory
        fig, ax = plt.subplots(figsize=(10, 5))
        line, = ax.plot(x_values, y_values, label='Trajectory', color='blue', linewidth=1)

        # Adding titles and labels
        ax.set_title('Projectile Motion')
        ax.set_xlabel('Horizontal Distance (m)')
        ax.set_ylabel('Vertical Distance (m)')
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.grid(color='gray', linestyle='--', linewidth=0.5)

        # Set scientific notation for axes
        ax.ticklabel_format(style='sci', axis='both', scilimits=(0, 0))

        # Displaying calculated values on the plot
        textstr = '\n'.join((
            f'Time of flight: {timeOfFlight:.2f} s',
            f'Maximum height: {heightMax:.2f} m',
            f'Range of projection: {rangeProjection:.2f} m',
            f'Horizontal component of initial velocity: {horizontalV:.2f} m/s',
            f'Vertical component of initial velocity: {verticalV:.2f} m/s',
            f'Horizontal distance traveled: {horizontalDistance:.2f} m'
        ))

        # Positioning the text box
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=props)

        # Adding interactivity with mplcursors
        cursor = mplcursors.cursor(line, hover=True)
        @cursor.connect("add")
        def on_add(sel):
            index = int(sel.index)
            velocity = velocities[index]
            time = times[index]
            vx = horizontalV
            vy = verticalV - g * time
            sel.annotation.set_text(f'Time: {time:.2f} s\n'
                                    f'Velocity: {velocity:.2f} m/s\n'
                                    f'Horizontal Velocity: {vx:.2f} m/s\n'
                                    f'Vertical Velocity: {vy:.2f} m/s')

        # Embedding the plot in Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.draw()

    except ValueError:
        messagebox.showerror("Error", "Invalid input for angle or velocity.")

# Search function
def search():
    global timeOfFlight, times, velocities  # Ensure global variables are used
    search_type = search_type_var.get()
    tolerance = 0.1  # Tolerance level for comparing velocities
    if search_type == 'time':
        try:
            time_input = float(time_entry.get())
            if 0 <= time_input <= timeOfFlight:
                idx = min(range(len(times)), key=lambda i: abs(times[i] - time_input))
                messagebox.showinfo("Result", f"At time {times[idx]:.2f} s, the velocity is {velocities[idx]:.2f} m/s")
            else:
                messagebox.showerror("Error", "Time is out of range.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input for time.")
    elif search_type == 'velocity':
        try:
            velocity_input = float(velocity_search_entry.get())
            idx = min(range(len(velocities)), key=lambda i: abs(velocities[i] - velocity_input))
            if abs(velocities[idx] - velocity_input) <= tolerance:
                messagebox.showinfo("Result", f"At velocity {velocities[idx]:.2f} m/s, the time is {times[idx]:.2f} s")
            else:
                messagebox.showerror("Error", "No such velocity within tolerance range.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input for velocity.")
    else:
        messagebox.showerror("Error", "Invalid search type.")

# Initialize Tkinter window
root = tk.Tk()
root.title("Projectile Motion")

# Input frame
input_frame = ttk.Frame(root)
input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

# Angle input
angle_label = ttk.Label(input_frame, text="Enter angle of projection (degrees):")
angle_label.grid(row=0, column=0, padx=5, pady=5)
angle_entry = ttk.Entry(input_frame)
angle_entry.grid(row=0, column=1, padx=5, pady=5)

# Velocity input
velocity_label = ttk.Label(input_frame, text="Enter velocity of projection (m/s):")
velocity_label.grid(row=1, column=0, padx=5, pady=5)
velocity_entry = ttk.Entry(input_frame)
velocity_entry.grid(row=1, column=1, padx=5, pady=5)

# Plot button
plot_button = ttk.Button(input_frame, text="Plot", command=calculate_and_plot)
plot_button.grid(row=2, column=0, columnspan=2, pady=10)

# Plot frame
plot_frame = ttk.Frame(root)
plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Search frame
search_frame = ttk.Frame(root)
search_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

search_type_var = tk.StringVar(value='time')

# Time search
time_label = ttk.Label(search_frame, text="Enter time (seconds):")
time_label.grid(row=0, column=0, padx=5, pady=5)
time_entry = ttk.Entry(search_frame)
time_entry.grid(row=0, column=1, padx=5, pady=5)
time_button = ttk.Radiobutton(search_frame, text='Search by Time', variable=search_type_var, value='time')
time_button.grid(row=0, column=2, padx=5, pady=5)

# Velocity search
velocity_search_label = ttk.Label(search_frame, text="Enter velocity (m/s):")
velocity_search_label.grid(row=1, column=0, padx=5, pady=5)
velocity_search_entry = ttk.Entry(search_frame)
velocity_search_entry.grid(row=1, column=1, padx=5, pady=5)
velocity_button = ttk.Radiobutton(search_frame, text='Search by Velocity', variable=search_type_var, value='velocity')
velocity_button.grid(row=1, column=2, padx=5, pady=5)

# Search button
search_button = ttk.Button(search_frame, text="Search", command=search)
search_button.grid(row=2, column=0, columnspan=3, pady=10)

# Run Tkinter main loop
root.mainloop()
