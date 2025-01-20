# Installation Guide

This comprehensive guide provides step-by-step instructions for installing KiCad, a powerful open-source PCB design tool, tailored for STM32 hardware design projects. Whether you are using a Linux-based system or Windows, this documentation ensures a smooth installation process, complete with practical examples and best practices.

## Installation Overview

To facilitate the installation of KiCad for your STM32 project, two scripts are provided in the `\STM32_HW_Design_KiCAD\utils` directory:

- Windows Users: `install_kicad.ps1` (PowerShell Script)
- Linux Users: `install_kicad.sh` (Bash Script)

These scripts automate the installation process, streamlining setup and ensuring consistency across different environments.

---

## 1. Installing KiCad

### For Linux Users (Using Bash Script)

Linux users can leverage the `install_kicad.sh` script to automate the installation of KiCad. This method simplifies the process, especially for those unfamiliar with command-line operations.

#### Steps to Install KiCad on Linux:

1. Open Terminal and Navigate to the Script Directory

   Begin by opening your terminal application. Navigate to the directory containing the installation script using the `cd` command. Replace `/path/to/` with the actual path to your project directory.

   ```bash
   cd /path/to/STM32_HW_Design_KiCAD/utils
   ```

2. Make the Script Executable

   Ensure that the script has the necessary execution permissions. This step is crucial for security and functionality.

   ```bash
   chmod +x install_kicad.sh
   ```

   Best Practice: Always review scripts before executing them to understand their actions and ensure they come from a trusted source.

3. Run the Installation Script

   Execute the script to initiate the installation process.

   ```bash
   ./install_kicad.sh
   ```

   The script utilizes your system's package manager (e.g., `apt` for Debian-based systems) to install KiCad and its dependencies automatically.

4. Verification

   After the installation completes, verify that KiCad is installed correctly by checking its version.

   ```bash
   kicad --version
   ```

   Expected Output:
   ```
   KiCad Version 6.x.x
   ```

#### Alternative Manual Installation

If you prefer not to use the provided script, you can manually install KiCad using your system's package manager.

##### For Ubuntu/Debian-Based Systems:

1. Update Package Lists

   ```bash
   sudo apt update
   ```

2. Install KiCad

   ```bash
   sudo apt install kicad
   ```

3. Verify Installation

   ```bash
   kicad --version
   ```

   Note: Manual installation provides more control over the installation process but requires familiarity with package management.

### For Windows Users (Using PowerShell Script)

Windows users can utilize the `install_kicad.ps1` PowerShell script to automate the KiCad installation process, ensuring all necessary components are correctly set up.

#### Steps to Install KiCad on Windows:

1. Open PowerShell as Administrator

   - Click on the Start menu.
   - Search for PowerShell.
   - Right-click on Windows PowerShell and select Run as administrator.

   Best Practice: Running PowerShell with administrative privileges ensures that the script has the necessary permissions to install software.

2. Navigate to the Script Directory

   Use the `cd` command to navigate to the directory containing the installation script. Replace `C:\path\to\` with the actual path to your project directory.

   ```powershell
   cd C:\path\to\STM32_HW_Design_KiCAD\utils
   ```

3. Run the PowerShell Script

   Execute the script to begin the installation.

   ```powershell
   .\install_kicad.ps1
   ```

   The script will guide you through downloading and installing KiCad, handling dependencies and configurations automatically.

4. Verification

   After installation, open KiCad to confirm it was installed successfully.

   - Steps:
     - Click on the Start menu.
     - Search for KiCad and launch the application.
     - Navigate to Help > About to view the version information.

   Expected Output:
   ```
   KiCad Version 6.x.x
   ```

#### Alternative Manual Installation

If you prefer to install KiCad manually, follow these steps:

1. Download the Installer

   - Visit the [KiCad official download page](https://www.kicad.org/download/).
   - Select the Windows installer appropriate for your system (32-bit or 64-bit).

2. Run the Installer

   - Locate the downloaded installer file (e.g., `kicad-6.x.x-installer.exe`).
   - Double-click the installer to launch the setup wizard.

3. Follow Installation Prompts

   - Accept the license agreement.
   - Choose the installation directory.
   - Select additional components if necessary.
   - Complete the installation by following the on-screen instructions.

4. Verification

   - Open KiCad from the Start menu.
   - Navigate to Help > About to verify the installed version.

   Tip: Regularly check the KiCad website for updates to ensure you have the latest features and security patches.

---

## 2. Post-Installation Verification

After successfully installing KiCad, it's essential to verify that the installation was successful and that the software is functioning correctly. This step ensures that your development environment is ready for PCB design tasks.

### Verification Steps

#### For Linux Users:

1. Open Terminal

2. Check KiCad Version

   ```bash
   kicad --version
   ```

   Expected Output:
   ```
   KiCad Version 6.x.x
   ```

3. Launch KiCad

   To further verify, launch KiCad from the terminal or application menu.

   ```bash
   kicad
   ```

   Outcome: The KiCad GUI should open without errors, allowing you to start a new project or open existing ones.

#### For Windows Users:

1. Open KiCad

   - Click on the Start menu.
   - Search for KiCad and launch the application.

2. Check Version Information

   - In KiCad, navigate to Help > About.
   - The version number should be displayed, confirming the installation.

   Example:
   ```
   KiCad Version 6.x.x
   ```

3. Create a Test Project

   - Click on File > New Project.
   - Follow the prompts to create a new PCB design.

   Outcome: Successfully creating a new project indicates that KiCad is functioning correctly.

### Troubleshooting Common Issues

Despite following installation steps meticulously, you might encounter issues. Below are common problems and their solutions.

#### Issue 1: Script Execution Policy Restriction (Windows)

Symptom: Unable to run `install_kicad.ps1` due to execution policy restrictions.

Solution:

1. Check Current Execution Policy

   ```powershell
   Get-ExecutionPolicy
   ```

2. Set Execution Policy Temporarily

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

3. Run the Installation Script Again

   ```powershell
   .\install_kicad.ps1
   ```

   Note: After installation, the execution policy reverts to its original setting when you close PowerShell.

#### Issue 2: Missing Dependencies (Linux)

Symptom: KiCad fails to launch or exhibits missing features.

Solution:

1. Ensure All Dependencies Are Installed

   Re-run the installation script or manually install dependencies.

   ```bash
   sudo apt update
   sudo apt install kicad
   ```

2. Check for Errors During Installation

   Review terminal output for any errors and address them accordingly.

#### Issue 3: Version Mismatch

Symptom: The installed KiCad version does not match the expected version for your project.

Solution:

1. Uninstall Current KiCad Version

   ```bash
   sudo apt remove kicad
   ```

   For Windows, use Add or Remove Programs in the Control Panel.

2. Download the Correct Version

   Visit the [KiCad download page](https://www.kicad.org/download/) and select the version compatible with your project.

3. Reinstall KiCad

   Follow the installation steps outlined above.

### Best Practices for Post-Installation

- Regular Updates: Keep KiCad updated to benefit from the latest features and security patches.
- Backup Configurations: Save your KiCad configurations and preferences to facilitate easy restoration in case of system changes.
- Community Engagement: Participate in KiCad forums and communities to stay informed about best practices and troubleshooting tips.
- Documentation: Maintain documentation of your installation process and any custom configurations for future reference.

---

## Conclusion

Installing KiCad for STM32 hardware design projects involves a straightforward process, whether you are using a Linux-based system or Windows. By following the steps outlined in this guide, you ensure a reliable setup that leverages automated scripts for efficiency and consistency. Post-installation verification and adherence to best practices further guarantee a stable and productive PCB design environment.

For additional support and resources, refer to the [KiCad Documentation](https://docs.kicad.org/) and engage with the KiCad community to enhance your design projects.