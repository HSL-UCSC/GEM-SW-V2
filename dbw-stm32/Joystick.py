"""
Holds the code to allow for the use of a joystick to drive the simulations as opposed to the current slider inputs.
This should all be relatively automatic, and require no tweaking from the students to make it work (caveat: you might need to reassign
the correct channels and buttons for your own particular joystick).

Also see ece163/Contants/JoystickConstants.py for the parameters that define the axes and buttons.
"""

# 4/18/2023 - Alex, Bailin, Gabe - first attempt at adding in the code
# 4/21/2023 - Documenting and folding into the main branch
# 5/02/2023 - Elkaim - All patched into code for 3-axis and 4-axis controllers, need to make sliders live for Chapter2


import time
import pygame

AXES = [0, 1, 2, 3]
BUTTONS = [10]

REVERSED = [False, True, False, False]
SCALE = [1.0, 1.0, 1.0, 1.0]
BIAS = [0.0, 0.0, 0.0, 0.0]


class Joystick:
    """
    Class which implements the joystick controls for the simulation. Should be fairly automatic for the students.
    Might need to re-map the axes and buttons for the joystick controller that you have. Mapping is held in the
    ece163/Contants/JoystickConstants.py file. Uses pygame library (installed automatically if you used bootstrap.py)
    """

    device = None

    def __init__(self):
        """
        Scans for valid joystick at startup. Note that this is only done once, and is not "live." Requires a minimum of
        three axes and 2 buttons to be valid.
        """
        pygame.joystick.init()

        # Search for a joystick with atleast 4 axises
        for stick_i in range(pygame.joystick.get_count()):
            self.device = pygame.joystick.Joystick(stick_i)
            if self.device.get_numaxes() < len(
                AXES
            ) or self.device.get_numbuttons() < len(BUTTONS):
                self.device.quit()
                self.device = None
            else:
                break

        # Check if a device connected
        if self.device == None:
            print("No compatible joysticks found, use the sliders.")
            self.active = False
        else:
            self.active = True
            # Display device name and number of axes
            print(
                "Found " + self.device.get_name(),
                "\n\tAxes: " + str(self.device.get_numaxes()),
                "\n\tButtons: " + str(self.device.get_numbuttons()),
            )

        pygame.init()

    def get_joystick_values(self):
        """
        Function to map the raw axis and button readings from the joystick to joystickValues type.

        :return: joystickValues class
        """
        pygame.event.get(pygame.JOYAXISMOTION)

        # Data is returned in a datatype to store relevant controller information
        if self.device and self.device.get_numaxes() > len(AXES):
            return {
                "axes": tuple(
                    (self.device.get_axis(i) * (-1.0 if REVERSED[i] else 1.0))
                    * SCALE[i]
                    + BIAS[i]
                    for i in AXES
                ),
                "buttons": tuple(self.device.get_button(i) for i in BUTTONS),
            }

        else:
            return None


if __name__ == "__main__":
    j = Joystick()
    while True:
        print(j.get_joystick_values())
        time.sleep(0.5)
