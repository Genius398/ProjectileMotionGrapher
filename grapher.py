import math
import matplotlib.pyplot as plt
import mplcursors

g = 9.81

thetaDeg = float(input("Enter angle of projection (degrees): "))
u = float(input("Enter velocity of projection (m/s): "))

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
velocities = []
times = []

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

# Adding the equation of the graph
equation_str = r'$x(t) = v_0 \cos(\theta) \cdot t$' '\n' r'$y(t) = v_0 \sin(\theta) \cdot t - \frac{1}{2} g \cdot t^2$'
ax.text(0.05, 0.75, equation_str, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

# Adding interactivity with mplcursors
cursor = mplcursors.cursor(line, hover=True)
@cursor.connect("add")
def on_add(sel):
    index = int(sel.target.index)
    velocity = velocities[index]
    time = times[index]
    vx = horizontalV
    vy = verticalV - g * time
    sel.annotation.set_text(f'Time: {time:.2f} s\n'
                            f'Velocity: {velocity:.2f} m/s\n'
                            f'Horizontal Velocity: {vx:.2f} m/s\n'
                            f'Vertical Velocity: {vy:.2f} m/s')

plt.show()

# Display results in SI units
print("\nResults in SI units:")
print("Time of flight:", round(timeOfFlight, 2), "seconds")
print("Maximum height:", round(heightMax, 2), "meters")
print("Range of projection:", round(rangeProjection, 2), "meters")
print("Horizontal component of initial velocity:", round(horizontalV, 2), "m/s")
print("Vertical component of initial velocity:", round(verticalV, 2), "m/s")
print("Horizontal distance traveled:", round(horizontalDistance, 2), "meters")
