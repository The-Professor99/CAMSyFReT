from setuptools import setup, find_packages

setup(
    name="CAMSyFReT",
    version="1.1.1",
    author="Eze Ihechi Festus",
    author_email="festusihechi99@gmail.com",
    description="A class Attendance Management System Using Face Recognition Technology",
    url="https://github.com/The-Professor99/CAMSyFReT",
    license="MIT",
    long_description=open("README.rst", "r").read(),
    keywords="class attendance management system face recognition technology opencv",
    project_urls={
        "Author Website": "https://ihechifestus9.web.app",
        "Source Code": "https://github.com/The-Professor99/CAMSyFReT",
    },
    packages=find_packages(),
    install_requires=[
      "imutils==0.5.4",
      "joblib==1.1.0",
      "numpy==1.22.4",
      "opencv-python==4.6.0.66",
      "pandas==1.5.0",
      "pkg_resources==0.0.0",
      "PyQt6==6.3.1",
      "PyQt6-Qt6==6.3.2",
      "PyQt6-sip==13.4.0",
      "python-dateutil==2.8.2",
      "pytz==2021.3",
      "scikit-learn==1.0.1",
      "scipy==1.7.2",
      "six==1.16.0",
      "threadpoolctl==3.0.0"
    ],
    python_requires=">=3.8",
    package_data={
        "Final_Project.attendance_records": ["*.*"],
        "Final_Project.changes.dataset.unknown": ["*.jpg"],
        "Final_Project.constants": ["*.txt","*.prototxt", "*.caffemodel"],
        "Final_Project.files": ["*.*"],
        "Final_Project.images": ["*.png"],
        "Final_Project.output": ["*.*"],
        "Final_Project": ["*.t7"],
        "": ["*.txt", "*.rst"],
    },
    entry_points={"console_scripts": ["Final_Project = Final_Project.__main__:main"]},
)
