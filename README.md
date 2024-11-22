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

The purpose I coded this plugin is to autopilot to help me with the measurement of sink vs time to achive an acurate L/D and flight polar numbers on diferent XPlane 12 gliders

The basic strategy is:
Set the simulator time/weather to a cold early morning flight with zero or minimum convective activity.
Take a tow to a given altitud (6000 feet works for me) , set a given speed on the autopilot, wait for the speed to level.
using a chronometer and your calibrated altimeter measure how long takes to loose a fixed amount of altitud (100 to 500 feet) and record the time it took to do so. 
Change autopilot setting to a new speed (+20 kph for example) and repeat the measurement
Continue with a range of speed while you have altitud, to gather enough info to create an interpolated sink vs speed plot.

For better acuracy in your results, you should take multiple flights to gather more data for your plot therefore averaging any measurement errors. 

Finally, air density / altitud corrections are be needed to get a real number for flight performance. 




Installation

( https://xppython3.readthedocs.io/en/latest/index.html ) This is XPPython3 version 4 and includes both the X-Plane plugin as well as a private version of Python3. Unlike previous versions of XPPython3, you no longer need to install your own copy of Python.

For installation copy the Python files to the X-Plane Resources/plugins/PythonPlugins folder so that the Python plugin can find them.


* I am looking for the original spreadsheet that Dick used to cruch the numbers, but it seems to have vanished on the internet. It probably is stored on a 'floppy disk' somwhere in the clubhouse, have no idea how would I ever read that these days :) 