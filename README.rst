====================================
 Class Attendance Management System
====================================

Authors
=======
By Eze Ihechi Festus -  https://ihechifestus9.web.app

About
=====

This is a class attendance management system based on face recognition technology. It uses pre-trained opencv caffe models to detect and capture the faces of students which are then saved as images. These images are used to train a support vector machine(SVM) model which is subsequently used, while taking class attendance, to recognize the faces of students present. Upon recognition of a student, the system updates the attendance records accordingly.
Checkout the repository to explore more features of the project.

Installation
============

Please ensure that you're using a pip version of 22.2.2 or greater.

    $ pip install CAMSyFReT

Usage
=====

Simply run `python3 -m Final_Project` from within the project folder and follow in-app prompts.

- Make sure to train models on captured faces before calling on take attendance.


Contributing
============

Submit bugs and patches to the `git repository <https://github.com/The-Professor99/CAMSyFReT>`_.

Notes
=====
Read more on how to use the package `here <https://github.com/The-Professor99/CAMSyFReT>`_

Issues
======
- Trying to take an attendance or capture biometrics may shutdown the app, if this is the case on your system and you receive an error messaging on the terminal stating: "can't open camera by index", please attach a webcam and try again.
- If an error occurs when trying to train the model on captured images, go to the settings page and click on `reset`. After this, capture the images again and try training the model again.
    
