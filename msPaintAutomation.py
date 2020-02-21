import pyautogui
import time
import cv2 as cv
from PIL import Image

print( cv.__version__)
image_file = 'C:\\Users\\1151244\\Pictures\\rtn_logo.jpg'
# Basic usage:
# 1. Find the variable called image_file (line above) and replace it with a valid path to an image
# 2. Start MS Paint in the background
# 3. Start this from the command line and within 5 seconds:
# 4. Put your mouse pointer in the top left corner of the canvas (the giant white part) in Paint
# 5. Wait forever

# If you want it to stop press CTRL + ALT + DEL and put your mouse in the top left corner of the screen. It should stop.


pyautogui.PAUSE = 0  # adjust this like crazy
original_speed = pyautogui.PAUSE
pyautogui.FAILSAFE = True
TESTING = False

if not TESTING:
    time.sleep(5)

start_time = time.time()


def color_comp(color_number, component):
    """
    Quick way to change the color in the custom color menu
    :param color_number: 0-255 value
    :param component: the key to get to the color. r=red, g=green, u=blue
    :return: None
    """
    pyautogui.hotkey('altleft', component)
    pyautogui.typewrite(str(color_number))


def color(color_numbers):
    """
    Take a list of color values (RGB), open the custom colors, and apply values.
    :param color_numbers: List (Red, Green, Blue) values
    :return: None
    """

    # If there is an alpha channel discard it as there is no opacity in paint
    if len(color_numbers) > 3:
        color_numbers.pop()

    # print("Color Numbers: ", color_numbers)

    assert len(color_numbers) == 3, "{}".format(len(color_numbers))

    for num in color_numbers:
        assert 0 <= num <= 255, str(num)
    if not TESTING:
        pyautogui.typewrite(['altleft', 'h', 'e', 'c', ], interval=0.1)
        color_comp(color_numbers[0], 'r')
        color_comp(color_numbers[1], 'g')
        color_comp(color_numbers[2], 'u')
        pyautogui.press('enter')


def fix_list(num_list):
    """
    Hack to ensure my rounding didn't put values outside of 0-255
    :param num_list: List of numbers.
    :return: The same number list.
    """
    for index in range(len(num_list)):
        if num_list[index] > 255:
            num_list[index] = 255
        elif num_list[index] < 0:
            num_list[index] = 0
    return num_list


# manually determined with the menu turned off the start of the canvas is at 25, 83. otherwise use .position()
# start_x, start_y = 25, 83
start_x, start_y = pyautogui.position()

# read image file
image = Image.open(image_file)

# make dictionary with pixels using RGB as key
pixel_dictionary = dict()
for x in range(image.width):
    for y in range(image.height):
        rgb = image.getpixel((x, y))  # get the pixel value in a tuple
        rgb_rounded = list(map(lambda num: round(num, -1), rgb))  # round it because doing every color takes forever
        rgb_rounded = fix_list(rgb_rounded)  # ensure rounding didn't push anything over 255 (it will)
        rgb_list = list(map(str, rgb_rounded))  # convert it to a list of strings
        rgb_key = ':'.join(rgb_list)  # separate with : to split later

        # if the dictionary doesn't have any pixel list yet, create it.
        if pixel_dictionary.get(rgb_key) is None:
            pixel_dictionary[rgb_key] = list()
        pixel_dictionary[rgb_key].append((x, y))  # compile a list of pixels using this RGB

# from pprint import pprint
# pprint(pixel_dictionary)

pyautogui.click(start_x, start_y)  # clicking before doing all the work to ensure we're focused in the paint

# sorted the RGBs by the lengths of the associated list. this way we can see the image form earlier on
for rgb in sorted(pixel_dictionary.keys(), key=lambda z: len(pixel_dictionary[z]), reverse=True):
    pyautogui.PAUSE = original_speed + 0.1  # when the color form comes up do it slowly or else there are problems.
    # set color to current RGB key
    color_map = map(int, rgb.split(':'))
    color_list = list(color_map)
    # print('changing to', rgb, color_list)
    time.sleep(0.1)  # this sleep is to allow the gui to catch up...i think. this eliminates some but not all problems
    color(color_list)
    pyautogui.PAUSE = original_speed  # return to quickly painting
    for pixel_x, pixel_y in pixel_dictionary.get(rgb):
        if not TESTING:
            # print("drawing", rgb)  # funny enough, this slows it down just enough to be quick with no errors
            pyautogui.click(start_x + pixel_x, start_y + pixel_y)
        else:
            print(list(map(int, rgb.split(':'))), end=' ')
            print(start_x + pixel_x, start_y + pixel_y)

print("Took {} seconds!".format(time.time() - start_time))
