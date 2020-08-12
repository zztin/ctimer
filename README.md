# ctimer

This is a python implementation of a time management tool. Designed for MacOSX at the moment. CTimer is a free timer\
tool to help you keep track of your productivity during the day, and help you set realistic goals for your day. \
Contributions are welcome!

## Features

* Provide a Tkinter GUI window for the ease of use for users.
* Set 25 mins for focus time, and 5 mins for break time.
* Set 8 clocks as aim for a day.
* Goals / feedback of each clock & time span per day is kept in a local SQL database (named ctimer.db).


## Getting Started (How to use ctimer?)

1. Go to a folder where you want to save this package and `git clone https://github.com/zztin/ctimer.git`
2. `cd ctimer`
3. `python setup.py develop`
4. launch the app:`ctimer`
5. Enjoy the Ctimer GUI!
6. Optional: try `ctimer --help` for several launching options
7. Wondering how your work proficiency is over the past period? try `ctimer --overall`

## Credits

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

These repositories and links provided ideas for implementations for this project.
1. stackoverflow: https://stackoverflow.com/questions/47824017/starting-and-pausing-with-a-countdown-timer-in-tkinter
2. stackexchange: https://apple.stackexchange.com/questions/3454/say-in-different-language
3. tkinter tutorial
4. https://github.com/rougier/calendar-heatmap
5. https://github.com/MarvinT/calmap

## Notes: 
### Easy way to check your sqlite database (the ctimer.db file) 
A. drag and drop: https://inloop.github.io/sqlite-viewer/
B. in command line
1. `sqlite3 ./data/ctimer.db`
2. `select * from clock_details;` <---remember the ";" in the end
3. The entries should show! If not, try`.tables` to check the table names if there is a table call "clock_details"
