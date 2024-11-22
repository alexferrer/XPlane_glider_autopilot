"""
  XPlane Autopilot plugin that keeps glider flight speed and roll constant
  Created to facilitate R. Johnson flight test method ( SSA April 1968 )
  Author: Alex Ferrer @2024
  License: GPL v3
  
"""
import xp
from XPPython3.xp_typing import *
from XPPython3 import xp_imgui # type: ignore
import imgui  # type: ignore
from ivPID import PID 
aboutWindow   = 1
activatePlugin = 2

class PythonInterface:      
    pid_roll  = PID( 2, 1  , 0.001)
    pid_pitch = PID( 2, 1, 0.01)

    pid_speed = PID(.5, .15, 0.01) 
    #pid_speed = PID(.31, .15, 0.01) 80.15
    #pid_speed = PID(.11, .15, 0.01) #30s .445kph   82-160

    def __init__(self):

        self.CGMenuItem = 0
        self.StatsWindowItem = 0
        self.AboutMenuItem = 0
        global myMenu      

        self.sim_time = 0
        self.CALLBACKTIME = .001   
        self.PLUGIN_ENABLED = True
        self.AUTOPILOT_ENABLED = False
        self.AUTOPILOT_WINDOW_OPEN = True
        self.ABOUT_WINDOW = None

        self.auto_pitch = True
        self.pid_pitch.SetPoint = 1
        self.TARGET_PITCH_ANGLE = 1

        self.auto_speed = True
        self.pid_speed.SetPoint = 70
        self.TARGET_SPEED = 70
        self.current_speed = 0

        self.speed_count = 90

        self.auto_roll = True
        self.pid_roll.SetPoint=0.0

    def XPluginStart(self):
        self.Name = "Auto Speed"
        self.Sig = "AlexFerrer.Python.AutoSpeed"
        self.Desc = "Aautopilot plugin that keeps glider flight speed constant"

        # Define an XPlane command 
        # It may be called from a menu item, a key stroke, or a joystick button
        #self.commandRef = xp.createCommand('alexferrer/xplane/auto_speed', 'Engage auto speed control')
        #xp.registerCommandHandler(self.commandRef, self.CommandHandler)
        
        # ----- Menu stuff --------------------------
        mySubMenuItem = xp.appendMenuItem(
            xp.findPluginsMenu(), "Auto Speed", 0, 1)
        self.MyMenuHandlerCB = self.MyMenuHandlerCallback
        self.myMenu = xp.createMenu("Auto Speed", xp.findPluginsMenu(), mySubMenuItem, self.MyMenuHandlerCB, 0)
        xp.appendMenuItem(self.myMenu, "Autopilot", aboutWindow, 1)
        xp.appendMenuItem(self.myMenu, "Plugin On/Off", activatePlugin, 1)    
        # -----------Drefs --------------------------------------
        self.PlaneRol   = xp.findDataRef("sim/flightmodel/position/phi")  # plane roll
        self.PlanePitch = xp.findDataRef("sim/flightmodel/position/theta")  # plane pitch
        self.roll_Dref = xp.findDataRef('sim/flightmodel/forces/L_plug_acf')
        self.pitch_Dref = xp.findDataRef('sim/flightmodel/forces/M_plug_acf')
        self.runningTime = xp.findDataRef("sim/time/total_running_time_sec")                                     
        self.airspeed = xp.findDataRef("sim/flightmodel/position/indicated_airspeed")
        #----------------------------------------------
        self.create_Autopilot_Window()
        xp.registerFlightLoopCallback(self.FlightLoopCallback, 1.0, 0)
        return self.Name, self.Sig, self.Desc

    def XPluginStop(self):    # Unregister the callbacks
        xp.unregisterFlightLoopCallback(self.FlightLoopCallback, 0)
        xp.destroyMenu(self.myMenu)

    def XPluginEnable(self):
           return 1

    def XPluginDisable(self):
        pass

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        pass

    def FlightLoopCallback(self, elapsedMe, elapsedSim, counter, refcon):      
        # is the plugin enabled? , then skip
        if not self.PLUGIN_ENABLED:
            return 1
        
        # is the sim paused? , then skip
        runtime = xp.getDataf(self.runningTime)
        if self.sim_time == runtime:
            print("p ", end='')
            return 1
        self.sim_time = runtime
        self.current_speed = xp.getDataf(self.airspeed) * 1.852
        current_pitch = xp.getDataf(self.PlanePitch) 
        current_roll = xp.getDataf(self.PlaneRol)
        if self.AUTOPILOT_ENABLED:
            if self.auto_speed:
                if self.speed_count > 10:  
                    self.speed_count = 0    
                    self.pid_speed.update(self.current_speed)
                    self.TARGET_PITCH_ANGLE = self.pid_speed.output * -1
                    #update pitch PID
                    self.pid_pitch.clear()
                    self.pid_pitch.SetPoint = self.TARGET_PITCH_ANGLE

                self.speed_count += 1
                #Pitch PID control
                self.pid_pitch.update(current_pitch)
                new_pitch = self.pid_pitch.output * 250 # pitch scale 250
                xp.setDataf(self.pitch_Dref, new_pitch )

            if self.auto_roll:
                self.pid_roll.update(current_roll)
                new_roll = self.pid_roll.output * 300 # roll scale 300
                xp.setDataf(self.roll_Dref, new_roll)

        return self.CALLBACKTIME

    # --------------------------------------------------------------------------------------------------
    #                     UI &  M E N U   S T U F F
    # --------------------------------------------------------------------------------------------------

    def MyMenuHandlerCallback(self, inMenuRef, inItemRef):

        if (inItemRef == aboutWindow):
            self.create_Autopilot_Window()
        
        if (inItemRef == activatePlugin):
            self.PLUGIN_ENABLED = not self.PLUGIN_ENABLED
    #-----------------------------------------------------------------

    def create_Autopilot_Window(self):
        self.AUTOPILOT_WINDOW_OPEN = True
        title = 'Autopilot Plugin'
        l, t, r, b = xp.getScreenBoundsGlobal()
        width = 350
        height = 250
        left_offset = 110
        top_offset = 410

        self.ABOUT_WINDOW = xp_imgui.Window(
            left=l + left_offset,
            top=t - top_offset,
            right=l + left_offset + width,
            bottom=t - (top_offset + height),
            visible=1,
            draw=self.draw_About_Window,
            refCon=self.ABOUT_WINDOW
        )
        self.ABOUT_WINDOW.setTitle(title)
        return

    def draw_About_Window(self, windowID, refCon):
        if not self.AUTOPILOT_WINDOW_OPEN or not self.PLUGIN_ENABLED:
            return

        imgui.text("Target Cruise Speed")
        changed, self.TARGET_SPEED = imgui.slider_int("##Cruise Speed", self.TARGET_SPEED, 70, 200)
        if changed:
            self.pid_speed.clear()
            self.pid_speed.SetPoint=self.TARGET_SPEED

        imgui.text("Current speed: " + str(round(self.current_speed,3)) + " kph")
        imgui.text("Current Error: " + str(round(self.pid_speed.SetPoint-self.current_speed,3)) + " kph")
        imgui.text("")

        imgui.separator()
        changed, self.AUTOPILOT_ENABLED = imgui.checkbox("Enable Autopilot",self.AUTOPILOT_ENABLED)

        if self.AUTOPILOT_ENABLED:        
            changed, self.auto_speed = imgui.checkbox("Auto Speed",self.auto_speed)
            if changed:
                self.pid_speed.clear()
                if self.auto_speed:
                    self.speed_count = 0    
                    self.pid_speed.SetPoint=self.TARGET_SPEED

            changed, self.auto_roll = imgui.checkbox("Auto Roll",self.auto_roll)
            if changed:
                self.pid_roll.clear()
                if self.auto_roll:
                    self.pid_roll.SetPoint=0.0
