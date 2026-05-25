# Learn2Fly

Learn2Fly is a long-term learning project for building a simple flight simulator, then gradually moving toward autopilot logic, data collection, and eventually hardware.

The goal is not to build a perfect airplane immediately. The goal is to learn step by step:

- Python simulation
- C/C++ control logic
- basic physics
- data logging
- autopilot thinking
- AI/learning systems later
- hardware later

## Project Philosophy

This project should be treated as a learning laboratory.

First we build the airplane in software.  
Then we teach it basic stability.  
Then we collect data.  
Then we experiment with learning.  
Only after that do we think about real hardware.

## Phase 1: Python Flight Simulator

Initial goal:

- Create a simple 2D airplane model
- Simulate altitude, speed, angle, gravity, and throttle
- Print flight state in the terminal
- Log simple flight data to CSV

Example output:

```text
Time: 1s | Altitude: 100 | Speed: 20 | Angle: 5
Time: 2s | Altitude: 98  | Speed: 21 | Angle: 4
```

## Phase 2: Basic Autopilot

Goal:

- Keep the plane level
- Prevent crashing
- Maintain altitude
- Use simple rules before AI

Example:

```text
if altitude < target_altitude:
    increase_throttle()
```

## Phase 3: C/C++ Control Module

Goal:

- Move the control logic into C or C++
- Keep Python for simulation, data, and experiments
- Learn how Python and C/C++ can communicate

## Phase 4: Learning Pilot

Goal:

- Use Python to analyze flight logs
- Study what caused crashes
- Improve decisions over time
- Experiment with simple machine learning later

## Phase 5: Hardware

Only after the simulator and control logic are stable.

Possible future hardware:

- microcontroller or flight controller
- IMU sensor
- motor
- servos
- battery
- foam airframe

## Suggested First Task

Create a `Plane` class with:

- altitude
- speed
- angle

Then simulate gravity by reducing altitude over time.

## Suggested Folder Structure

```text
learn2fly/
│
├── main.py
├── plane.py
├── physics.py
├── config.py
├── data/
│   └── flight_log.csv
├── notes/
│   └── dev_journal.md
└── README.md
```

## Status

Project started as a long-term learning journey.
