import pygame
import time
import threading
import math
class GamepadVibrateTest :
    def __init__ (self ):
        pygame .init ()
        pygame .joystick .init ()
        self .running =True
        if pygame .joystick .get_count ()==0 :
            return
        self .joystick =pygame .joystick .Joystick (0 )
        self .joystick .init ()
        try :
            self .joystick .rumble (0 ,0 ,100 )
            self .vibration_supported =True
        except :
            self .vibration_supported =False
        self .show_menu ()
        self .button_states ={}
    def show_menu (self ):
        pass
    def vibrate_short (self ):
        if not self .vibration_supported :
            return
        self .joystick .rumble (0.7 ,0.7 ,200 )
    def vibrate_long (self ):
        if not self .vibration_supported :
            return
        self .joystick .rumble (0.5 ,0.5 ,1000 )
    def vibrate_pulse (self ):
        if not self .vibration_supported :
            return
        def pulse ():
            for i in range (5 ):
                self .joystick .rumble (0.8 ,0.8 ,150 )
                time .sleep (0.2 )
                self .joystick .rumble (0 ,0 ,50 )
                time .sleep (0.1 )
        threading .Thread (target =pulse ,daemon =True ).start ()
    def vibrate_wave (self ):
        if not self .vibration_supported :
            return
        def wave ():
            duration =2000
            steps =50
            for i in range (steps ):
                intensity =(math .sin (i *0.3 )+1 )/2
                self .joystick .rumble (intensity ,intensity ,duration //steps )
                time .sleep (0.04 )
        threading .Thread (target =wave ,daemon =True ).start ()
    def vibrate_weak (self ):
        if not self .vibration_supported :
            return
        self .joystick .rumble (0.2 ,0.2 ,500 )
    def vibrate_strong (self ):
        if not self .vibration_supported :
            return
        self .joystick .rumble (1.0 ,1.0 ,800 )
    def vibrate_variable (self ,left_intensity ,right_intensity ):
        if not self .vibration_supported :
            return
        if left_intensity >0.1 or right_intensity >0.1 :
            self .joystick .rumble (left_intensity ,right_intensity ,50 )
    def test_all_modes (self ):
        if not self .vibration_supported :
            return
        def test_sequence ():
            modes =[
            ("Слабая вибрация",lambda :self .joystick .rumble (0.3 ,0.3 ,500 )),
            ("Средняя вибрация",lambda :self .joystick .rumble (0.6 ,0.6 ,500 )),
            ("Сильная вибрация",lambda :self .joystick .rumble (1.0 ,1.0 ,500 )),
            ("Левый мотор",lambda :self .joystick .rumble (1.0 ,0 ,500 )),
            ("Правый мотор",lambda :self .joystick .rumble (0 ,1.0 ,500 )),
            ("Пульс",self .vibrate_pulse ),
            ]
            for name ,func in modes :
                func ()
                time .sleep (1 )
        threading .Thread (target =test_sequence ,daemon =True ).start ()
    def handle_button_press (self ,button ,pressed ):
        if button not in self .button_states :
            self .button_states [button ]=False
        if pressed and not self .button_states [button ]:
            if button ==0 :
                self .vibrate_short ()
            elif button ==1 :
                self .vibrate_long ()
            elif button ==2 :
                self .vibrate_wave ()
            elif button ==3 :
                self .vibrate_pulse ()
            elif button ==4 :
                self .vibrate_weak ()
            elif button ==5 :
                self .vibrate_strong ()
            elif button ==6 :
                self .test_all_modes ()
            elif button ==7 :
                self .running =False
        self .button_states [button ]=pressed
    def run (self ):
        if not hasattr (self ,'joystick'):
            return
        clock =pygame .time .Clock ()
        try :
            while self .running :
                pygame .event .pump ()
                for i in range (self .joystick .get_numbuttons ()):
                    button_pressed =self .joystick .get_button (i )
                    if button_pressed or i in self .button_states :
                        self .handle_button_press (i ,button_pressed )
                if self .joystick .get_numaxes ()>=6 :
                    try :
                        left_trigger =max (0 ,(self .joystick .get_axis (4 )+1 )/2 )
                        right_trigger =max (0 ,(self .joystick .get_axis (5 )+1 )/2 )
                        self .vibrate_variable (left_trigger ,right_trigger )
                    except :
                        pass
                clock .tick (60 )
        except KeyboardInterrupt :
            pass
        finally :
            if self .vibration_supported :
                self .joystick .rumble (0 ,0 ,0 )
            pygame .quit ()
def main ():
    try :
        tester =GamepadVibrateTest ()
        tester .run ()
    except Exception as e :
        pass
if __name__ =="__main__":
    main ()