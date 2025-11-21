# Launching KiCad and Creating a New Project

Before diving into PCB design, setting up a new project in KiCad is essential.
This foundational step ensures that all your design files are organized and easily accessible.

## Steps

## 1. Open KiCad

- Launch the Application:
  - After installing KiCad, locate the application in your system’s programs menu or desktop shortcut and open it.
  - Upon launching, the KiCad Project Manager window appears, serving as the central hub for managing your PCB projects.

## 2. Create a New Project

- Initiate a New Project:
  - In the Project Manager, navigate to `File > New Project > New Project`.
  
- Choose Project Location:
  - Select a directory on your computer where you want to store your project files.
  - It's advisable to create a dedicated folder for each project to maintain organization.
  
- Name Your Project:
  - Enter a meaningful name for your project, such as `STM32_First_Project`.
  - This name will be used for the project's primary files.
  
- Create the Project:
  - Click Save to create the project. KiCad will generate essential files, including:
    - .pro file: The main project file that keeps track of all components and settings.
    - .sch file: The schematic file where you will draw your circuit diagram.

> Best Practice: Maintain a consistent naming convention and directory structure for your projects. This practice simplifies file management, especially as project complexity increases.
> Practical Example: For instance, store all related files in a folder named `STM32_First_Project` with subfolders like `schematic`, `pcb`, `libraries`, and `docs`.
