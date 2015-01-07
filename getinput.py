'''
Created on 07.01.2015

@author: dddsnn
'''

import os
if os.name == 'posix':
    import pyxhook as hooklib
elif os.name == 'nt':
    import pyHook as hooklib
    import pythoncom
import time

def kb_down(ev):
    global key_states
    if ev.Key in key_states:
        key_states[ev.Key] = 1

def kb_up(ev):
    global key_states
    if ev.Key in key_states:
        key_states[ev.Key] = 0

def mouse_down(ev):
    button = ev.MessageName.replace(' down', '')
    global mouse_states
    if button in mouse_buttons:
        mouse_states[button] = 1

def mouse_up(ev):
    button = ev.MessageName.replace(' up', '')
    global mouse_states
    if button in mouse_buttons:
        mouse_states[button] = 0

if __name__ == '__main__':
    keys = ['Control_L', 'Shift_L', 'a', 's', 'd', 'w', 'f', 'e', 'r', 'space']
    mouse_buttons = ['mouse left', 'mouse right', 'mouse 8']
    key_states = dict([(k, 0) for k in keys])
    mouse_states = dict([(k, 0) for k in mouse_buttons])

    hm = hooklib.HookManager()

    hm.KeyDown = kb_down
    hm.KeyUp = kb_up
    hm.MouseAllButtonsDown = mouse_down
    hm.MouseAllButtonsUp = mouse_up

    hm.HookKeyboard()
    hm.HookMouse()

    hm.start()

    # seconds between samples
    step = 0.05
    # duration of sampling (seconds)
    duration = 10
    output = ''
    for i in range(int(duration / step)):
        time.sleep(step)
        for k in sorted(key_states.keys()):
            output += str(key_states[k])
        for k in sorted(mouse_states.keys()):
            output += str(mouse_states[k])
    print(output)

    hm.cancel()
