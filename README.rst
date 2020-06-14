========
ctimer
========


.. image:: https://img.shields.io/pypi/v/ctimer.svg
        :target: https://pypi.python.org/pypi/ctimer

.. image:: https://img.shields.io/travis/zztin/ctimer.svg
        :target: https://travis-ci.com/zztin/ctimer

.. image:: https://readthedocs.org/projects/ctimer/badge/?version=latest
        :target: https://ctimer.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




This is a python implementation of a time management tool. Designed for MacOSX at the moment. CTimer is a free timer\
tool to help you keep track of your productivity during the day, and help you set realistic goals for your day. \
Contributions are welcome!




Features
--------

* Provide a Tkinter GUI window for the ease of use for users.
* Set 25 mins for focus time, and 5 mins for break time.
* Set 8 clocks as aim for a day.

* TODO BUGFIX:
        - self.display.config updates appears after the voice_messages (os.subprocess("say ...")
        - 00:00 does not show.
* TODO NEW FEATURES:
        - Allowing setting customize time inteval, aim clock counts, goals for today (prompt text) on entry.
        - Visual representation of clocks accomplished today (1. block representation of time similar to gantt chart.\
          Compare across the week. 2. Histogram over time over the year-- this requires storage of data locally).
        - Allows notes taking during the clock (note interruption, how many pauses you took etc.)
        - Add tick-tock sound when clocks start.


Installation
------------

```
python setup.py develop
```

Launch the Application
----------------------

```
ctimer
```

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

These links provided immense help for a head start for this project.
1. stackoverflow: https://stackoverflow.com/questions/47824017/starting-and-pausing-with-a-countdown-timer-in-tkinter
2. stackexchange: https://apple.stackexchange.com/questions/3454/say-in-different-language
3. tkinter tutorial
