# Installation

The following steps will guide you through installing KiCad for your STM32 hardware design project. In the folder `\STM32_HW_Design_KiCAD\utils`, there are two scripts available for installation: one for Windows PowerShell (`install_kicad.ps1`) and one for Linux-based systems using Bash (`install_kicad.sh`). Here's how to use them:

---

## 1. **Install the Software**

### **For Linux Users (Bash Script)**

The provided script `install_kicad.sh` can be used to automate the installation process on Linux-based systems. 

#### Steps:

1. Open a terminal and navigate to the folder containing the script:
    ```bash
    cd /path/to/STM32_HW_Design_KiCAD/utils
    ```

2. Make the script executable if it is not already:
    ```bash
    chmod +x install_kicad.sh
    ```

3. Run the installation script:
    ```bash
    ./install_kicad.sh
    ```

4. The script will use your package manager (e.g., apt for Debian-based systems) to install KiCad.

Alternatively, you can manually install KiCad using your package manager:

#### **Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install kicad
```

### **For Windows Users (PowerShell Script)**

The script `install_kicad.ps1` can be used to automate the installation process on Windows via PowerShell.

#### Steps:

1. Open PowerShell as an administrator.

2. Navigate to the folder containing the script:
    ```powershell
    cd C:\path\to\STM32_HW_Design_KiCAD\utils
    ```

3. Run the PowerShell script:
    ```powershell
    .\install_kicad.ps1
    ```

The script will guide you through downloading and installing KiCad on Windows.

Alternatively, you can manually download and install KiCad:

- Go to the [KiCad official website](https://www.kicad.org/download/) and download the Windows installer.
- Follow the instructions on the website to install KiCad on your system.

---

## 2. **Post-Installation**

Once KiCad is installed, open the software and ensure it is working correctly. You can verify the installation by checking the version number:

- **Linux**: 
    ```bash
    kicad --version
    ```
  
- **Windows**: Open KiCad, and the version will be displayed in the "Help" -> "About" section.

You are now ready to proceed with your STM32 hardware design project in KiCad!

Let me know if you need additional details or clarification for any specific steps!


---

