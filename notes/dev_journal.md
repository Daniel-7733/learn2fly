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
- Vertical speed is tan(Theta) x horizontal speed
- final_velocity = initial_velocity + (acceleration x time)

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
 
