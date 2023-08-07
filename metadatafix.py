import hachoir.core
import os
import platform
import pip

def compat_version(version):
    """Return a compatible version string for hachoir-core==1.3.3."""
    if version.startswith("3.2."):
        return "1.3.3"
    return version

def is_arm_mac():
    """Return True if the current machine is an ARM Mac."""
    return platform.machine().startswith("arm64")

def install_hachoir():
    """Install the latest version of hachoir for M1 or M2 Macs."""
    if not is_arm_mac():
        raise Exception("This script is only intended for ARM Macs.")
    pip.main(["install", "hachoir-parser"])

def modify_metadata_requirements():
    """Modify the metadata package requirements to be compatible with hachoir-core==1.3.3."""
    requirements_file = os.path.join(os.path.dirname(__file__), "metadata", "requirements.txt")
    with open(requirements_file, "r") as f:
        requirements = f.readlines()

    for index, requirement in enumerate(requirements):
        if requirement.startswith("hachoir-core=="):
            requirements[index] = "hachoir-core==1.3.3"

    with open(requirements_file, "w") as f:
        f.writelines(requirements)

def install_metadata():
    """Install the metadata package."""
    pip.main(["install", "metadata==0.2"])

def main():
    if not is_arm_mac():
        print("This script is only intended for ARM Macs.")
        print("Do you want to continue (Y/N)?")
        choice = input()
        if choice != "Y":
            exit()

    install_hachoir()
    modify_metadata_requirements()
    install_metadata()

if __name__ == "__main__":
    main()
