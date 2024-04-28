Robot Programming Language
This project is the culmination of my computer systems engineering degree.
The final software will be designed to control a robot vehicle through simple commands.
It will read batch files and translate them into commands that drive the robot.
Additionally, it wil retrieve sensor readings and navigation information from the robot.

Current Version Features:
Text Editor: Open, edit, and save text files directly within the GUI
GUI: Graphical user interface functioning as a development environment with a terminal for debugging.
Batch File Processing:  Parse data files, perform syntax checks, tokenize commands,
    and pack data before sending it for execution.
Command Driven Mode: A separate window to write and execute individual commands.
Data interpretation: Interfaces with an Arduino program that reads tokens,
    interprets them into specific functions, and communicates a response back to the GUI.
For Loop Support: The language includes support for FOR loops, allowing execution of commands multiple times.
    However, it does not currently support nested FOR loops.

Final Version Features:
Movement Functionality: Add movement functionality to MOV, TURN and STOP functions.
Sensor Integration: Retrieve sensor readings from the robot for monitoring and analysis.
Syntax: Syntax is explained in a file

Future improvements:
Better error handling using try, except
Variables support
Nestled loops
Conditional statements support
Mathematics Support
Optimise compilation algorithms
In app com port adjustment