# PyQt XBox Controller Input Reader

Python package adding pyqtSignals from XBox controller to your PyQt5 application.

Simply create instance of **QtXBoxInput** class defined in **pyqt_xbox.py**.

Take a look at the example usage in **main.py**.

This project has been used for reading XBox controller actions:

https://github.com/r4dian/Xbox-Controller-for-Python/tree/master

### params

Instance of **QtXBoxInput** can be created with those params:

 - vibrations: (bool) controller will vibrate while left or right trigger is pressed

### signals

 - button_change - (int, int)
 - axis_change - (str, float)
 - confirm - ()
 - cancel - ()
 - left - ()
 - right - ()
 - up - ()
 - down - ()

Those signals are accessible using for example this:

> QtXBoxInput_instance.axis_change.connect(your_function)
