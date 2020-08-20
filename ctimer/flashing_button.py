# source: https://www.raspberrypi.org/forums/viewtopic.php?t=230465
import tkinter as Tk

flash_delay = 500  # msec between colour change
flash_colours = ('black', 'red') # Two colours to swap between

button_flashing = False

def flashColour(object, colour_index):
    global button_flashing

    if button_flashing:
        object.config(foreground = flash_colours[colour_index])
        root.after(flash_delay, flashColour, object, 1 - colour_index)
    else:
        object.config(foreground = flash_colours[0])

def buttonCallback(self):
    global button_flashing

    button_flashing = not button_flashing
    if button_flashing:
        self.config(text = 'Press to stop flashing')
        flashColour(self, 0)
    else:
        self.config(text = 'Press to start flashing',
                    foreground = flash_colours[0])

root = Tk.Tk()
my_button = Tk.Button(root, text = 'Press to start flashing',
                      foreground = flash_colours[0],
                      command = lambda:buttonCallback(my_button))
my_button.pack()

root.mainloop()


# import tkinter as Tk
#
# flash_delay = 500  # msec between colour change
# flash_colours = ('black', 'red') # Two colours to swap between
#
# def flashColour(object, colour_index):
#     object.config(foreground = flash_colours[colour_index])
#     root.after(flash_delay, flashColour, object, 1 - colour_index)
#
# root = Tk.Tk()
# my_label = Tk.Label(root, text = 'I can flash!',
#                       foreground = flash_colours[0])
# my_label.pack()
#
# flashColour(my_label, 0)
#
# root.mainloop()
