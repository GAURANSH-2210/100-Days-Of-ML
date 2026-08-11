DT = 0.02          # 50 Hz control loop
MASS = 1.2         # kg
GRAVITY = 9.81     # m/s^2
TARGET = 10.0      # metres
SIM_TIME = 12.0    # seconds


class PID:
    def __init__(self, kp, ki, kd):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.integral = 0.0
        self.prev_error = 0.0

    def update(self, error, dt):
        # P: react to how wrong we are right now
        p = self.kp * error

        # I: past error
        self.integral += error * dt
        i = self.ki * self.integral

        # D: how fast error changes
        derivative = (error - self.prev_error) / dt
        d = self.kd * derivative
        self.prev_error = error

        return p + i + d


def simulate(kp, ki, kd, label):
    pid = PID(kp, ki, kd)
    altitude = velocity = 0.0
    history = []

    for _ in range(int(SIM_TIME / DT)):
        error = TARGET - altitude
        thrust = pid.update(error, DT)

        acceleration = (thrust - MASS * GRAVITY) / MASS
        velocity += acceleration * DT
        altitude += velocity * DT

        if altitude < 0:                    # ground collision
            altitude = velocity = 0.0

        history.append(altitude)

    return label, history


def ascii_plot(label, history, height=14, width=60):
    sampled = [history[int(i * len(history) / width)] for i in range(width)]
    top = max(max(sampled), TARGET) * 1.15

    print(f"\n  {label}")
    for row in range(height, 0, -1):
        level = top * row / height
        line = "".join("#" if v >= level else " " for v in sampled)
        marker = " <- target" if abs(level - TARGET) < top / height / 2 else ""
        print(f"  {level:5.1f}m |{line}|{marker}")
    print(f"        +{'-' * width}+")
    print(f"         final altitude: {history[-1]:.2f} m")


print("=" * 68)
print("PID ALTITUDE HOLD — tuning comparison")
print("=" * 68)

ascii_plot(*simulate(8.0, 0.0, 0.0, "P only — steady-state error, oscillates"))
ascii_plot(*simulate(8.0, 0.0, 4.0, "PD — damped, but never reaches 10m"))
ascii_plot(*simulate(8.0, 3.0, 4.0, "PID — locks onto target"))