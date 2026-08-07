# Learn2Fly — System Map

> A visual notebook for understanding how the whole project works.

This file is not meant to explain every function.

Its purpose is to answer four questions:

```text
1. What does this class own?
2. What does it need?
3. What does it produce?
4. Where does it sit in the whole system?
```

When I feel lost, I should return here and look at the big picture.

---

# 1. The Main Mental Model

Learn2Fly is built like a pipeline.

```text
WORLD / TIME
     |
     v
SIMULATION
     |
     v
FLIGHT SYSTEM
     |
     v
AIRCRAFT STATE
     |
     v
ANALYZE
     |
     v
UNDERSTAND
     |
     v
DECIDE
     |
     v
COMMAND
     |
     v
CONTROL
     |
     v
PHYSICS
     |
     v
NEW AIRCRAFT STATE
```

The most important idea:

> Information should flow through the system instead of every class knowing everything.

---

# 2. Simulation

## Responsibility

`Simulation` owns the simulated world clock.

It decides:

* When the simulation starts.
* When the simulation stops.
* How much simulated time passes during each update.

It should **not** decide how the aircraft flies.

---

## Needs

```text
FlightSystem
time_step / dt
```

Example:

```text
dt = 0.1 seconds
```

---

## Produces

Simulation mainly produces:

```text
Repeated FlightSystem updates
Elapsed simulated time
```

---

## Pipeline

```text
Simulation starts
      |
      v
Check whether simulation should stop
      |
      v
FlightSystem.update(dt)
      |
      v
time_elapsed += dt
      |
      v
Repeat
```

---

## Mental Picture

```text
SIMULATION = CLOCK + LOOP
```

Simulation manages:

> When things happen.

FlightSystem manages:

> What happens to the aircraft.

---

# 3. FlightSystem

## Responsibility

`FlightSystem` is the main coordinator of the aircraft.

It connects the major aircraft subsystems together.

It should not contain all the logic itself.

Instead, it asks the correct component to do each job.

---

## Needs

It may contain or communicate with:

```text
Plane
FlightAnalyzer
DecisionMaker
AutoPilot
FlightController
```

and receives:

```text
dt
```

from Simulation.

---

## Produces

The final result of one update is:

```text
A new aircraft state
```

---

## Pipeline

The conceptual update pipeline is:

```text
Plane state
    |
    v
FlightAnalyzer
    |
    v
FlightReport
    |
    v
DecisionMaker
    |
    v
Decision
    |
    v
AutoPilot
    |
    v
Controller Targets
    |
    v
FlightController
    |
    v
Plane Physics
    |
    v
New Plane State
```

---

## Mental Picture

```text
FLIGHT SYSTEM = CONDUCTOR
```

Like an orchestra conductor:

It does not play every instrument.

It tells each system when its responsibility should happen.

---

# 4. Plane

## Responsibility

`Plane` owns the physical state of the aircraft.

This is one of the most important ownership boundaries in the project.

The Plane owns things like:

```text
altitude
horizontal_speed
vertical_speed
pitch_angle
bank_angle
throttle
mass
drag
AoA
```

The Plane represents:

> What the aircraft physically is right now.

---

## Needs

To update its physics, Plane may need:

```text
dt
gravity
thrust
lift
drag
mass
current control state
```

---

## Produces

A new physical aircraft state.

For example:

```text
new altitude
new vertical speed
new horizontal speed
new AoA
new position/state
```

---

## Physics Pipeline

```text
Current State
     |
     v
Calculate Forces
     |
     v
Calculate Acceleration
     |
     v
Update Velocity
     |
     v
Update Position / Altitude
     |
     v
Calculate Derived State
     |
     v
New Aircraft State
```

The physics idea is:

```text
FORCE
  ↓
ACCELERATION
  ↓
VELOCITY
  ↓
POSITION
```

---

## Mental Picture

```text
PLANE = PHYSICAL TRUTH
```

If somebody asks:

> "What is the aircraft's altitude?"

Plane should own the answer.

---

# 5. FlightCalculator

## Responsibility

`FlightCalculator` owns reusable mathematical calculations.

It should contain calculations that:

* Do not need to own aircraft state.
* Can be reused in many places.
* Have clear mathematical inputs and outputs.

---

## Needs

Numbers.

Examples:

```text
target
current
old_value
new_value
dt
altitude
velocity
AoA
AoA rate
```

---

## Produces

Calculated values.

Examples:

```text
error
rate_of_change
specific_energy
energy_rate
time_to_impact
time_to_stall
clamped_value
```

---

## Pipeline

Usually:

```text
INPUT VALUES
     |
     v
FORMULA
     |
     v
RESULT
```

Example:

```text
target + current
      |
      v
error()
      |
      v
target - current
```

---

## Mental Picture

```text
FLIGHT CALCULATOR = TOOLBOX
```

It should calculate.

It should not decide.

---

# 6. FlightAnalyzer

## Responsibility

`FlightAnalyzer` interprets the aircraft state.

Plane gives raw truth.

FlightAnalyzer asks:

> What does this truth mean?

For example:

```text
Plane:
Speed = 52 m/s

Analyzer:
Speed Margin = +2 m/s
```

Or:

```text
Plane:
AoA = 14 degrees

Analyzer:
Aircraft is close to critical AoA.
```

---

## Needs

Usually:

```text
Plane state
FlightCalculator results
Safety limits
```

Examples:

```text
speed
minimum safe speed
AoA
critical AoA
altitude
vertical speed
AoA rate
```

---

## Produces

Meaningful flight information.

Examples:

```text
speed_margin
aoa_margin
time_to_stall
time_to_impact
risk_level
threat_type
recoverability
```

Ultimately:

```text
FlightReport
```

---

## Pipeline

```text
RAW AIRCRAFT STATE
        |
        v
Calculate Margins
        |
        v
Calculate Predictions
        |
        v
Determine Threat
        |
        v
Determine Risk
        |
        v
Determine Recoverability
        |
        v
FlightReport
```

---

## Mental Picture

```text
FLIGHT ANALYZER = INTERPRETER
```

Plane says:

```text
"This is what is happening."
```

Analyzer says:

```text
"This is what it means."
```

---

# 7. FlightReport

## Responsibility

`FlightReport` packages the important analyzed information.

It is primarily a data carrier.

It should not contain large decision systems.

---

## Needs

Information produced by FlightAnalyzer.

For example:

```text
risk
threat
margins
time_to_stall
time_to_impact
recoverability
```

---

## Produces

One structured report.

Conceptually:

```text
FlightReport(
    risk=HIGH,
    threat=STALL,
    time_to_stall=3.2,
    speed_margin=4.0,
    recoverability=GOOD
)
```

---

## Pipeline

```text
FlightAnalyzer
      |
      v
Collect Important Information
      |
      v
FlightReport
      |
      +--------> DecisionMaker
```

---

## Mental Picture

```text
FLIGHT REPORT = MEDICAL REPORT
```

The patient is the Plane.

The analyzer is the doctor examining the patient.

The report contains the diagnosis.

---

# 8. DecisionMaker

## Responsibility

`DecisionMaker` chooses what the aircraft should do next.

It does not physically move the aircraft.

It chooses the strategy.

---

## Needs

Primarily:

```text
FlightReport
Current FlightState
Mission context
```

---

## Produces

```text
Decision
```

Example:

```text
Mode: EMERGENCY
Reason: STALL
Priority: CRITICAL
```

---

## Pipeline

```text
FlightReport
     |
     v
Current State / Context
     |
     v
Evaluate Situation
     |
     v
Choose Priority
     |
     v
Choose Response
     |
     v
Decision
```

---

## Mental Picture

```text
DECISION MAKER = BRAIN
```

It answers:

> What should we do?

Not:

> How do I physically move the elevator?

---

# 9. Decision

## Responsibility

`Decision` stores the result of the decision-making process.

DecisionMaker creates the decision.

Other systems consume it.

---

## Needs

Values selected by the DecisionMaker.

For example:

```text
mode
reason
priority
message
```

---

## Produces

Nothing complicated.

The object itself is the output.

---

## Example

```text
Decision
|
+-- Mode: EMERGENCY
+-- Reason: STALL
+-- Priority: CRITICAL
+-- Message: Recover from stall
```

---

## Mental Picture

```text
DECISION = ORDER
```

DecisionMaker is the officer who chooses the order.

Decision is the written order.

---

# 10. FlightState

## Responsibility

`FlightState` defines the common structure for aircraft behavior states.

Examples:

```text
TakeoffState
ClimbState
CruiseState
DescentState
LandingState
EmergencyState
```

Each state owns the behavior that belongs specifically to that phase of flight.

---

## Needs

Depending on the design:

```text
FlightReport
Plane state
Mission targets
DecisionMaker context
```

---

## Produces

State-specific decisions or transitions.

Examples:

```text
Remain in CRUISE
Transition to DESCENT
Enter EMERGENCY
```

---

## State Pipeline

```text
Current FlightState
       |
       v
Read Aircraft Situation
       |
       v
Run State-Specific Logic
       |
       v
Decision
       |
       v
Check Transition
       |
       v
Current State or New State
```

---

## Mental Picture

```text
STATE = CURRENT JOB
```

The aircraft may always be the same aircraft.

But its job changes.

```text
TAKEOFF -> Get safely airborne
CLIMB   -> Gain altitude
CRUISE  -> Maintain efficient flight
DESCENT -> Lose altitude safely
LANDING -> Reach ground safely
EMERGENCY -> Survive immediate danger
```

---

# 11. TakeoffState

## Responsibility

Own the logic specific to takeoff.

Main objective:

```text
Become safely airborne.
```

---

## Needs

Things like:

```text
speed
AoA
altitude
thrust
safety information
```

---

## Produces

Takeoff-related decisions.

Possible transition:

```text
TAKEOFF
   |
   | safe altitude reached
   v
CLIMB
```

---

## Important Priorities

```text
Speed
Thrust
AoA
Positive climb
Safe altitude
```

---

# 12. ClimbState

## Responsibility

Own climb behavior.

Main objective:

```text
Reach target altitude safely.
```

---

## Needs

```text
current altitude
target altitude
speed
AoA
energy
risk
```

---

## Produces

Climb decisions.

Possible transition:

```text
CLIMB
  |
  | target altitude reached
  v
CRUISE
```

---

## Mental Model

```text
KE -> PE
```

Climbing exchanges speed for altitude.

Throttle may add energy while the climb consumes kinetic energy.

---

# 13. CruiseState

## Responsibility

Own normal cruise behavior.

Main objectives:

```text
Maintain safe flight
Maintain target altitude
Maintain target speed
Avoid unnecessary energy loss
```

---

## Needs

```text
FlightReport
speed
altitude
energy state
mission information
```

---

## Produces

Cruise decisions.

Possible transitions:

```text
CRUISE -> DESCENT
CRUISE -> EMERGENCY
```

---

# 14. DescentState

## Responsibility

Own controlled descent behavior.

Main objective:

```text
Lose altitude without losing control of energy and speed.
```

---

## Needs

```text
target altitude
vertical speed
speed
AoA
energy
```

---

## Produces

Descent decisions.

Possible transition:

```text
DESCENT
   |
   | landing conditions reached
   v
LANDING
```

---

# 15. LandingState

## Responsibility

Own final landing behavior.

Main objective:

```text
Reach the ground safely.
```

---

## Needs

```text
altitude
vertical speed
speed
AoA
touchdown conditions
```

---

## Produces

Landing decisions.

Possible final state:

```text
LANDING
   |
   | aircraft reaches ground safely
   v
SIMULATION COMPLETE
```

---

# 16. EmergencyState

## Responsibility

EmergencyState owns immediate survival behavior.

Emergency logic can override normal mission objectives.

---

## Needs

```text
Threat
Risk
Aircraft state
Recoverability
```

---

## Produces

Emergency decisions.

Examples:

```text
STALL recovery
IMPACT avoidance
OVERSPEED protection
```

---

## Priority Model

```text
NORMAL MISSION
     |
     | emergency detected
     v
EMERGENCY STATE
     |
     | danger resolved
     v
RETURN TO SAFE FLIGHT
```

---

## Mental Picture

```text
EMERGENCY STATE = SURVIVAL MODE
```

Mission goals become secondary.

---

# 17. AutoPilot

## Responsibility

`AutoPilot` converts decisions into target commands.

Decision says:

```text
Recover from stall.
```

AutoPilot translates that into something actionable:

```text
target_pitch = -5°
target_throttle = 1.0
```

---

## Needs

```text
Decision
Plane
Flight safety information
Mission targets
```

---

## Produces

Control targets.

Examples:

```text
target_pitch
target_throttle
target_bank_angle
target_vertical_speed
```

---

## Pipeline

```text
Decision
   |
   v
Safety Protection
   |
   v
Mission Objective
   |
   v
Calculate Targets
   |
   v
Controller Targets
```

---

## Priority Layers

```text
1. Emergency
2. Safety protections
3. Normal mission objectives
```

For example:

```text
STALL?
  |
 YES
  |
  +----> Pitch Down + Throttle Up

NO
 |
 v
LOW SPEED?
 |
YES
 |
 +----> Protect Speed

NO
 |
 v
NORMAL MISSION CONTROL
```

---

## Mental Picture

```text
AUTOPILOT = STRATEGY -> COMMAND
```

---

# 18. FlightController

## Responsibility

`FlightController` moves the actual controls toward the targets requested by AutoPilot.

AutoPilot may instantly request:

```text
target_pitch = +5°
```

But the physical aircraft cannot teleport its pitch.

FlightController applies movement gradually.

---

## Needs

```text
Plane
dt
AutoPilot targets
maximum control rates
```

---

## Produces

Updated control state.

Examples:

```text
new pitch
new throttle
new bank
```

---

## Pipeline

```text
Target
   |
   v
Calculate Error
   |
   v
Apply Rate Limit
   |
   v
Move Control
   |
   v
Updated Plane Control State
```

---

## Example

```text
Current Pitch = 0°
Target Pitch = 5°
Maximum Pitch Rate = 2°/s
dt = 0.5 s
```

Maximum change this frame:

```text
2 × 0.5 = 1°
```

So:

```text
0° -> 1°
```

Not:

```text
0° -> 5°
```

---

## Mental Picture

```text
AUTOPILOT:
"Go there."

CONTROLLER:
"I will move us there safely."
```

---

# 19. Enums

Enums represent a limited set of meaningful states.

Examples:

```text
ThreatType
RiskLevel
Recoverability
FlightMode
```

---

## Why Enums Matter

Instead of:

```text
"high"
"High"
"HIGH"
"very high maybe"
```

I can have:

```text
RiskLevel.HIGH
```

This makes the system clearer and safer.

---

## Mental Picture

```text
ENUM = CONTROLLED VOCABULARY
```

Everyone in the system speaks the same language.

---

# 20. The Complete Application Pipeline

Here is the whole system in one flow.

```text
┌──────────────────────┐
│      SIMULATION      │
│                      │
│ owns time + loop     │
└──────────┬───────────┘
           │ dt
           v
┌──────────────────────┐
│     FLIGHT SYSTEM    │
│                      │
│ coordinates aircraft │
└──────────┬───────────┘
           │
           v
┌──────────────────────┐
│        PLANE         │
│                      │
│ physical truth       │
└──────────┬───────────┘
           │ state
           v
┌──────────────────────┐
│   FLIGHT ANALYZER    │
│                      │
│ interprets state     │
└──────────┬───────────┘
           │
           v
┌──────────────────────┐
│    FLIGHT REPORT     │
│                      │
│ packaged information │
└──────────┬───────────┘
           │
           v
┌──────────────────────┐
│   DECISION MAKER     │
│                      │
│ chooses strategy     │
└──────────┬───────────┘
           │
           v
┌──────────────────────┐
│     FLIGHT STATE     │
│                      │
│ mode-specific logic  │
└──────────┬───────────┘
           │
           v
┌──────────────────────┐
│       DECISION       │
│                      │
│ chosen action        │
└──────────┬───────────┘
           │
           v
┌──────────────────────┐
│      AUTOPILOT       │
│                      │
│ chooses targets      │
└──────────┬───────────┘
           │ targets
           v
┌──────────────────────┐
│  FLIGHT CONTROLLER   │
│                      │
│ moves controls       │
└──────────┬───────────┘
           │
           v
┌──────────────────────┐
│        PLANE         │
│                      │
│ physics update       │
└──────────┬───────────┘
           │
           v

        NEW STATE
           │
           └───────────────┐
                           │
                           v
                    NEXT SIMULATION
                        UPDATE
```

---

# 21. Information Flow

Another way to see the architecture:

```text
RAW DATA
   |
   v
Plane
   |
   v
MEANING
   |
   v
FlightAnalyzer
   |
   v
INFORMATION
   |
   v
FlightReport
   |
   v
UNDERSTANDING
   |
   v
DecisionMaker / FlightState
   |
   v
DECISION
   |
   v
AutoPilot
   |
   v
COMMAND
   |
   v
FlightController
   |
   v
ACTION
   |
   v
Plane Physics
```

Or even shorter:

```text
DATA
 ↓
INFORMATION
 ↓
KNOWLEDGE
 ↓
DECISION
 ↓
COMMAND
 ↓
ACTION
 ↓
NEW DATA
```

This is one of the most important diagrams in the project.

---

# 22. Ownership Map

When confused, look here.

```text
WHO OWNS WHAT?
```

| Information / Responsibility    | Owner                       |
| ------------------------------- | --------------------------- |
| Altitude                        | Plane                       |
| Speed                           | Plane                       |
| Vertical Speed                  | Plane                       |
| Pitch                           | Plane                       |
| Bank                            | Plane                       |
| Throttle state                  | Plane                       |
| Aircraft physics                | Plane                       |
| Reusable equations              | FlightCalculator            |
| Speed margin                    | FlightAnalyzer              |
| AoA margin                      | FlightAnalyzer              |
| Time to stall                   | FlightAnalyzer / Calculator |
| Time to impact                  | FlightAnalyzer / Calculator |
| Risk level                      | FlightAnalyzer              |
| Threat                          | FlightAnalyzer              |
| Recoverability                  | FlightAnalyzer              |
| Analysis package                | FlightReport                |
| Current flight behavior         | FlightState                 |
| Choosing what should happen     | DecisionMaker               |
| Decision result                 | Decision                    |
| Target pitch                    | AutoPilot                   |
| Target throttle                 | AutoPilot                   |
| Target bank                     | AutoPilot                   |
| Physical control movement       | FlightController            |
| Simulation time                 | Simulation                  |
| Aircraft subsystem coordination | FlightSystem                |

---

# 23. Control Hierarchy

The project also has a hierarchy.

```text
MISSION
   |
   v
FLIGHT MODE
   |
   v
DECISION
   |
   v
AUTOPILOT TARGET
   |
   v
CONTROLLER ACTION
   |
   v
PHYSICAL AIRCRAFT
```

Example:

```text
Mission:
Reach destination

        ↓

Flight State:
CLIMB

        ↓

Decision:
Continue climb

        ↓

AutoPilot:
Target pitch = +4°
Target throttle = 0.8

        ↓

Controller:
Move pitch toward +4°
Move throttle toward 0.8

        ↓

Plane:
Acceleration changes
Speed changes
Altitude changes
```

---

# 24. Emergency Hierarchy

Safety overrides normal goals.

```text
MISSION OBJECTIVE
      |
      v
NORMAL FLIGHT
      |
      | threat detected
      v
SAFETY PROTECTION
      |
      | severe threat
      v
EMERGENCY
```

Think:

```text
MISSION
   <
SAFETY
   <
SURVIVAL
```

Survival has the highest authority.

---

# 25. State Machine Map

A simplified normal flight path:

```text
             ┌─────────┐
             │ TAKEOFF │
             └────┬────┘
                  │
                  v
              ┌───────┐
              │ CLIMB │
              └───┬───┘
                  │
                  v
             ┌────────┐
             │ CRUISE │
             └────┬───┘
                  │
                  v
            ┌─────────┐
            │ DESCENT │
            └────┬────┘
                 │
                 v
            ┌─────────┐
            │ LANDING │
            └─────────┘
```

Emergency can interrupt almost anything:

```text
TAKEOFF ----┐
CLIMB ------|
CRUISE -----+----> EMERGENCY
DESCENT ----|
LANDING ----┘
```

After recovery, later I may design rules for deciding which safe state the aircraft should return to.

---

# 26. The Three Important Loops

I can think of Learn2Fly as three loops.

## Loop 1 — Physics Loop

```text
FORCE
  ↓
ACCELERATION
  ↓
VELOCITY
  ↓
POSITION
  ↓
NEW STATE
```

---

## Loop 2 — Control Loop

```text
TARGET
  ↓
ERROR
  ↓
CONTROL COMMAND
  ↓
AIRCRAFT RESPONSE
  ↓
NEW ERROR
```

---

## Loop 3 — Intelligence Loop

```text
STATE
  ↓
ANALYSIS
  ↓
PREDICTION
  ↓
DECISION
  ↓
ACTION
  ↓
NEW STATE
```

These loops run together.

---

# 27. My Debugging Map

When something goes wrong, do not randomly change code.

Follow the pipeline.

Ask:

```text
1. Is Plane state correct?
        ↓
2. Are Calculator equations correct?
        ↓
3. Is Analyzer interpreting correctly?
        ↓
4. Is FlightReport carrying correct data?
        ↓
5. Is the correct FlightState active?
        ↓
6. Is DecisionMaker choosing correctly?
        ↓
7. Is AutoPilot creating correct targets?
        ↓
8. Is Controller moving toward those targets correctly?
        ↓
9. Is Plane physics responding correctly?
        ↓
10. Is Simulation updating with correct dt?
```

This gives me a debugging path instead of guessing.

---

# 28. My Design Questions

Before adding a new class or feature, ask:

```text
WHAT is its responsibility?

WHO should own it?

WHICH layer does it belong to?

WHAT information does it need?

WHAT does it produce?

WHO is allowed to change its data?

WHAT comes before it?

WHAT comes after it?
```

If I cannot answer these questions, I probably do not understand the feature well enough yet.

---

# 29. Big Picture vs Small Picture

When working, switch between two views.

## Big Picture

Ask:

```text
Where does this belong?

Why does it exist?

Who talks to it?

What comes before it?

What comes after it?
```

## Small Picture

Ask:

```text
Is this formula correct?

Is this function correct?

Are the units correct?

Is dt used correctly?

Is this variable owned by the correct class?
```

Good systems require both views.

---

# 30. The Golden Rule

When I feel lost:

Do not immediately write more code.

Return to:

```text
RESPONSIBILITY
     ↓
OWNERSHIP
     ↓
INPUT
     ↓
PROCESS
     ↓
OUTPUT
     ↓
NEXT OWNER
```

Every component should fit somewhere in this chain.

---

# 31. One-Page Cheat Sheet

```text
SIMULATION
Owns: Time and loop
Needs: FlightSystem + dt
Returns: Repeated updates

        ↓

FLIGHT SYSTEM
Owns: Coordination
Needs: Aircraft subsystems
Returns: Updated aircraft

        ↓

PLANE
Owns: Physical state
Needs: Forces + controls + dt
Returns: New physical state

        ↓

FLIGHT ANALYZER
Owns: Interpretation
Needs: Plane state
Returns: FlightReport

        ↓

FLIGHT REPORT
Owns: Structured analysis
Needs: Analyzer results
Returns: Information package

        ↓

DECISION MAKER
Owns: Choosing strategy
Needs: FlightReport + state
Returns: Decision

        ↓

FLIGHT STATE
Owns: Mode-specific behavior
Needs: Situation + context
Returns: State logic / transitions

        ↓

DECISION
Owns: Chosen action
Needs: DecisionMaker result
Returns: Structured decision

        ↓

AUTOPILOT
Owns: Control targets
Needs: Decision + Plane
Returns: Target pitch/throttle/bank

        ↓

FLIGHT CONTROLLER
Owns: Control movement
Needs: Targets + dt
Returns: Updated controls

        ↓

PLANE PHYSICS

        ↓

NEW STATE

        ↓

REPEAT
```

---

# Final Mental Picture

Learn2Fly is not one giant autopilot.

It is a collection of small systems with clear responsibilities.

```text
      OBSERVE
         ↓
      UNDERSTAND
         ↓
       PREDICT
         ↓
       DECIDE
         ↓
       COMMAND
         ↓
       CONTROL
         ↓
        MOVE
         ↓
      OBSERVE AGAIN
```

The goal is not to make every class intelligent.

The goal is to make the **whole system intelligent because every class does its own job well.**
