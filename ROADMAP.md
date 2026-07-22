# Learn2Fly Roadmap

> **Current Project Philosophy**
>
> Learn2Fly is not simply an autopilot simulator.
>
> It is a long-term engineering project whose goal is to understand and build the complete chain of an intelligent flight-control system, from aircraft physics to autonomous decision making and eventually hardware.
>
> Every phase builds one layer of that system.

---

# Development Principles

Always follow these rules:

1. Physics before control.
2. Control before automation.
3. Automation before intelligence.
4. Simulation before hardware.
5. Correctness before optimization.
6. Simple solutions before complex ones.
7. Every module should have one clear responsibility.

---

# Phase 0 — Foundation ✅

## Goal

Create the project and development environment.

### Completed

* Git repository
* README
* Development journal
* Basic project structure
* Simulation loop
* Initial Plane model

---

# Phase 1 — Aircraft Physics ✅

## Goal

Create a believable aircraft.

### Completed

* Gravity
* Lift
* Drag
* Thrust
* Pitch
* Horizontal speed
* Vertical speed
* Flight Path Angle
* Angle of Attack
* Basic flight dynamics

The aircraft can now physically fly inside the simulation.

---

# Phase 2 — Flight Mathematics ✅

## Goal

Teach the simulator how to measure flight.

### Completed

* FlightCalculator
* Flight path calculations
* AoA calculations
* Rate of change
* Time to stall
* Time to impact
* Kinetic Energy
* Potential Energy
* Total Energy
* Specific Energy
* Energy rate

The simulator can now calculate meaningful flight values.

---

# Phase 3 — Situation Awareness ✅

## Goal

Understand what the aircraft is experiencing.

### Completed

* FlightAnalyzer
* Speed margin
* AoA margin
* Risk levels
* Recoverability
* Threat detection
* Most urgent threat

The simulator now understands whether the aircraft is safe.

---

# Phase 4 — Reporting System ✅

## Goal

Collect aircraft knowledge into one object.

### Completed

* FlightReport
* Aircraft state
* Flight analysis
* Energy information
* Safety information

The rest of the system can now read one report instead of many variables.

---

# Phase 5 — Decision Making ✅

## Goal

Teach the aircraft what it should do.

### Completed

* Decision class
* DecisionMaker
* Flight modes
* Emergency logic
* Priority handling
* Explainable decisions

The simulator now decides *what* should happen.

---

# Phase 6 — Flight Control 🚧 *(Current Phase)*

## Goal

Execute decisions smoothly.

### Current Work

* FlightController
* Pitch controller
* Throttle controller
* Bank controller
* Smooth transitions
* Deadbands
* Controller limits

### Next Goals

* Improve controller stability
* Tune gains
* Prevent oscillation
* Improve energy management
* Refine climb/descent behavior

At the end of this phase, the aircraft should follow commands reliably.

---

# Phase 7 — Integrated Flight System

## Goal

Connect every subsystem into one complete architecture.

### Planned

Create:

```
FlightSystem
```

Responsibilities:

* Coordinate modules
* Update pipeline
* Execute flight loop
* Connect reports, decisions and controller

Pipeline:

```
Plane
↓

FlightCalculator
↓

FlightAnalyzer
↓

FlightReport
↓

DecisionMaker
↓

FlightController
↓

Plane
```

This becomes the aircraft "brain."

---

# Phase 8 — Mission System

## Goal

Give the aircraft objectives.

### Planned

* Mission
* Mission Planner
* Waypoints
* Desired altitude
* Desired speed
* Flight phases

Examples

* Takeoff
* Climb
* Cruise
* Descent
* Landing

The aircraft will begin flying toward missions instead of merely staying alive.

---

# Phase 9 — Navigation System

## Goal

Teach the aircraft where it is.

### Planned

* Position
* Heading
* Wind correction
* Navigation
* Route following

The aircraft should know where it wants to go.

---

# Phase 10 — Sensor System

## Goal

Separate physics from sensing.

### Planned

Sensors such as:

* Airspeed
* Altitude
* IMU
* Vertical speed
* GPS
* Angle of attack

The controller should use sensor information instead of directly reading the Plane object.

---

# Phase 11 — Flight Recorder

## Goal

Record every flight.

### Planned

* Flight logs
* CSV
* JSON
* Graph generation
* Replay support

The simulator becomes a laboratory.

---

# Phase 12 — Visualization

## Goal

Observe the aircraft.

### Planned

* Live graphs
* Flight path
* Energy graphs
* Risk graphs
* Debug overlays
* Flight instruments

The aircraft becomes easier to understand and debug.

---

# Phase 13 — Learning System

## Goal

Teach the aircraft to learn.

### Planned

* Analyze previous flights
* Detect patterns
* Recommend improvements
* Compare flights
* Optimize controller parameters

This is **not** full AI yet.

It is data-driven improvement.

---

# Phase 14 — AI Pilot

## Goal

Introduce intelligent decision making.

Possible future topics

* Reinforcement Learning
* Neural Networks
* Genetic Algorithms
* Adaptive controllers

Only after the rule-based pilot is mature.

---

# Phase 15 — C/C++ Integration

## Goal

Move performance-critical systems to C/C++.

Possible candidates

* Physics
* Controller
* Mathematics
* Sensor processing

Python remains the orchestration layer.

---

# Phase 16 — Hardware

## Goal

Move from simulation to reality.

Possible future work

* Raspberry Pi
* STM32
* Arduino
* IMU
* Servo control
* RC aircraft
* Hardware-in-the-loop simulation

Only after the simulator is highly reliable.

---

# Long-Term Vision

```
Physics
        ↓
Measurements
        ↓
Analysis
        ↓
Reporting
        ↓
Decision
        ↓
Control
        ↓
Mission
        ↓
Navigation
        ↓
Sensors
        ↓
Learning
        ↓
AI
        ↓
Hardware
```

---

# Current Status (July 2026)

```
██████████░░░░░░░░░░░░░░░░░░░░
Foundation               ✅
Aircraft Physics         ✅
Flight Mathematics       ✅
Situation Awareness      ✅
Reporting                ✅
Decision Making          ✅
Flight Control           🚧
Integrated Flight System ⏳
Mission System           ⏳
Navigation               ⏳
Sensors                  ⏳
Visualization            ⏳
Learning                 ⏳
AI Pilot                 ⏳
Hardware                 ⏳
```

---

