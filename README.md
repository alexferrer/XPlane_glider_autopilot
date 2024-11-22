# XPlane_glider_autopilot
Auto speed and roll control for D. Johnson Sailplane Performance Flight Test Method [ SSA April 1968 ]

This plugin provides auto speed and auto roll control for gliders. 

It is based on Austin Mayer's (October 15 2021) article at:

https://austinsnerdythings.com/2021/10/15/creating-an-autopilot-in-x-plane-using-python-part-1/

For PID control it uses Caner Durmusoglu Simple PID implementation , which is based on 

# Copyright (C) 2015 Ivmech Mechatronics Ltd. <bilgi@ivmech.com>
Ivmech PID Controller is simple implementation of a Proportional-Integral-Derivative (PID) Controller in the Python Programming Language.  More information about PID Controller: http://en.wikipedia.org/wiki/PID_controller


Three PID controls are used , one for pitch, one for roll and a pitch governor to control speed. 
PID controlers are not easy to fine tune, The settings are programable adjustable, the default are the parameters I found to work best on my CPU , your results may vary. 

You can read about Dick johnsons Sailplane Performance Flight Test Method on April 1968 edition of the SSA magazine . (look on the wayback machine for a free copy)

For many years Dick's glider flight test evaluations regularly published on the SSA magazine were considered the gold standart of flight testing for gliders. 

