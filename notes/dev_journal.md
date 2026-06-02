# Development Journal

## Day 1

Today I started the Learn2Fly project.

Main idea:

- Build a flight simulator first
- Learn Python, C/C++, and real-world engineering step by step
- Avoid rushing to hardware too early

First goal:

Make a simple plane fall because of gravity.


## Day 2

Today I use Physics and Geometric Flight for fall calculation:

Main goal:
- To calculate the fall of plan realistically.


Plane has two kind of speed:
1. vertical speed
2. horizontal speed
```
          ^
          |
          | vertical_speed
          |
----------+-------->
       horizontal_speed
```

Formula:
- For Geometric -> Vertical speed is tan(Theta) x horizontal speed
- For Physic -> final_velocity = initial_velocity + (acceleration x time)

Plane has 4 forse: 
1. Lift
2. weight
3. Thrust
4. Drag

The picture:
```
        Lift
          ^
          |
Drag <--- P ---> Thrust
          |
          v
        Weight
```

There are two different speed in a plane: Vertical and horizontal (Groundspeed) speed. To calculate Vertical speed I use ```Vv = Vg.tan(θ) or Vertical speed = Groundspeed x tan(θ)```, then I use ```Vf = Vi + a.t``` to add the gravity. This formula make the fall more realistic. At the end, I update the altitude by this formula: ```altitude += Vertical speed x time```.

in simple term:
Physics Flight: Forse -> acceleration -> Velocity -> Position


## Day 3

Main idea was to calculate horizontal speed also becsaue like vertical speed, horizontal speed is not fix and it need to be calculate every time.

Formula was same but this time I calculate acceleration by introducing mass to the formula becsaue previously, for simplicity, I calculate the force and use it instead of acceleration. However, this time I make it more realistic. These are the formulas:
```
f = ma
vf = vi + at
```
keep in mind that thrust and drag are force (N) and need the first formula: ```thrust - drag = ma```we can fine the acceleration and use it in second formula to calculate the final horizontal Velocity. 

for vertical speed we need to consider another think. Gravity is acceleration (m/s^2). Therefore, I use really simple formula ```angle x horizontal speed x 0.01```. Now, we have the lift. In order to calculate the net acceleration, I use two more formula:
  ```
  1. lift acceleration = lift force / mass
  2. net accceleration = gravity + lift acceleration # Gravity is negetive number -> -9.81
  ```


