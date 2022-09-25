 Class Attendance Management System
====================================

About
=====

This is a class attendance management system based on face recognition technology. It uses pre-trained opencv caffe models to detect and capture the faces of students which are then saved as images. This is the enrollment phase. 

In the training phase, these images are passed to a model which extracts the feature vectors(embeddings) that quantify each face in the image, a labelEncoder function is then used to add names to the embeddings which are subsequently used to train a Support Vector Machine (SVM) learning model.
 
When the 'Take Attendance' process is initiated, the system once again captures the faces of students in the class at that point in time and the trained SVM model is used to determine who, by percentage probabilities, is in the new captured images. This percentage probability is compared to a predefined threshold(confidence level) and if it meets it, the labelEncoder is queried for the most likely name. This is the recognition phase.

When a student's face is recognized/authenticated, his/her attendance record is updated accordingly.

Attendance records as well as records of enrolled students can also be viewed and modified on the system.


## Installation

This project can be installed by running the following commands in your preferred directory.

    $ git clone https://github.com/The-Professor99/CAMSyFReT.git

## Requirements

<strong>This assumes you have <i>Python</i> installed on your system</strong>

[Setup a virtual environment and activate it](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)

Run the command below in the project's root folder to install the requirements.

    $ pip install -r requirements.txt
    
However, after installation, trying to run the app may result in errors which states that "This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem". This is because installing opencv4 using pip may not always work. If this is the case on your system, please read this guide on [installing opencv4](https://pyimagesearch.com/2018/08/15/how-to-install-opencv-4-on-ubuntu/).

## How To Use

[Activate the virtual environment](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)

Run the below command to start up the project

    $ python run.py

Upon successful [login](./Images/app_images/1_register_&_login.png), you can enroll a student through the `Enroll Student` tab.

#### [Enroll student(s)](./Images/app_images/2_enroll_student.jpg)

- Fill in the student's details.
- click on `Capture biometrics`
- When the camera comes up, take about 10 pictures of the student. Ensure that the [face is detected](./Images/app_images/3_face_detection.jpg). To take a picture, press `k` and to exit the camera, press `q`.
- [Train the model](./Images/app_images/4_train_model_&_take_attendance.png) on captured faced by pressing the `Train Model` button. You only need to train the model only when you newly enroll a student.

    
#### Take Attendance

- After the above section is completed, whenever you want to take an attendance, place your camera or webcam at a position where it can easily detect the faces of students and press the `Start recognition` or `Take Attendance` button.
- The system will find and update the attendance records of students it detects and [recognize](./Images/app_images/5_face_recognition.jpg).
- At the end of the attendance taking process, press `q` to exit the camera.

    
#### View Attendance Records.

- click the `view attendance tab` buttons to [view all attendace taken records](./Images/app_images/6_view_attendance_records.png).
- Enter `course details` and click on `view course details` button to [find details of all students](./Images/app_images/7_view_registered_students.png) you've enrolled into the course.
- You can make changes to these records and after making the changes, hit the `Save modifications` button to save them.


### Deployment

[Source distributions](https://packaging.python.org/en/latest/glossary/#term-Source-Distribution-or-sdist) and [build distributions](https://packaging.python.org/en/latest/glossary/#term-Built-Distribution) have been generated for publishing to [Pypi](https://pypi.org/). They are located in the [dist](./dist/) folder.
A sample publish to Pypi's test server has been made and can be accessed [here](https://test.pypi.org/project/ClassAttendanceManagementSystem/1.0/). However, as stated on pypi, publishes made to pypi's test server are occasionally deleted so should the link be broken, please make use of the content of this repository instead.

### Issues
I recently discovered an issue. Trying to take an attendance or capture biometrics may shutdown the app, if this is the case on your system and you receive an error messaging on the terminal stating: "can't open camera by index", please attach a webcam and try again.

### Future work

To make a pyinstaller executable of the project, this way, a user has to only install the executable to use it instead of having to go through the stress of installing python and setting up the project themselves. This hasn't been made possible yet as a result of the challenge outlined in the [requirement's section](#requirements).

### Other Details
- Some [UML diagrams](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/what-is-uml/) drafted out in the course of running the project can be accessed [here](./Images/uml_diagrams)

- Make sure to train models on captured faces before calling on take attendance.
- The models determine if a face is present in the image and whose it is by generating percentage probabilities. These percentage probabilities are compared to a predefined threshold(confidence level) which, by default, is set to 0.80. You can increase/decrease these confidence levels in the [settings page](./Images/app_images/8_settings_page.png) to limit the occurrencies of [false positives and negatives](https://en.wikipedia.org/wiki/False_positives_and_false_negatives).

### Useful Resources
- [The fastest way to learn OpenCV, Object Detection, and Deep Learning](https://pyimagesearch.com/)

#### Please note that this is still a work in progress.