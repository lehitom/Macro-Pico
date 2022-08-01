import keypad
import time
import board
import rotaryio
import digitalio
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

km = keypad.KeyMatrix(
    row_pins=(board.GP4, board.GP5, board.GP6, board.GP7, board.GP8),
    column_pins=(board.GP0, board.GP1, board.GP2, board.GP3),
)

button = digitalio.DigitalInOut(board.GP12)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

encoder = rotaryio.IncrementalEncoder(board.GP14, board.GP13)

cc = ConsumerControl(usb_hid.devices)

button_state = None
last_position = encoder.position

# for joystick setting up
x_axis = analogio.AnalogIn(board.GP18)
y_axis = analogio.AnalogIn(board.GP19)

control_key = Keycode.SHIFT

time.sleep(1)

mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

pot_min = 0.8
pot_max = 2.5
step = (pot_max – pot_min) / 20.0

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

def steps(axis):
    """ Maps the potentiometer voltage range to 0-20 """
    result = round((axis – pot_min) / step)
    if result > 8 and result < 12:
        result = 10
    return result

buttons_pressed = False

while True:
    event = km.events.get()
    if event:
        print(event)

    current_position = encoder.position
    position_change = current_position - last_position
    if position_change > 0:
        for _ in range(position_change):
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        print(current_position)
    elif position_change < 0:
        for _ in range(-position_change):
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        print(current_position)
    last_position = current_position
    if not button.value and button_state is None:
        button_state = "pressed"
    if button.value and button_state == "pressed":
        print("Button pressed.")
        cc.send(ConsumerControlCode.PLAY_PAUSE)
        button_state = None

# for Joystick Configuration
    x = get_voltage(x_axis)
    y = get_voltage(y_axis)

    if x > 3.0:
        mouse.click(Mouse.LEFT_BUTTON)
        time.sleep(0.2)  # Debounce delay

# print(steps(x), steps(y))
# time.sleep(0.1)

    if steps(x) == 10 and steps(y) == 10:
        'if cond:' buttons_pressed == True:
            buttons_pressed = False
            keyboard.release_all()
            mouse.release_all()
    else:
        'if not cond:' buttons_pressed == False:
            buttons_pressed = True
            keyboard.press(control_key)
            time.sleep(0.1)
            mouse.press(Mouse.MIDDLE_BUTTON)

        if steps(x) > 11.0:
            # print(steps(x))
            mouse.move(x=1)
        if steps(x) < 9.0:
            # print(steps(x))
            mouse.move(x=–1)

        if steps(x) > 19.0:
            # print(steps(x))
            mouse.move(x=2)
        if steps(x) < 1.0:
            # print(steps(x))
            mouse.move(x=–2)

        if steps(y) > 11.0:
            # print(steps(y))
            mouse.move(y=–1)
        if steps(y) < 9.0:
            # print(steps(y))
            mouse.move(y=1)

        if steps(y) > 19.0:
            # print(steps(y))
            mouse.move(y=–2)
        if steps(y) < 1.0:
            # print(steps(y))
            mouse.move(y=2)

# for Joystick Configuration...
