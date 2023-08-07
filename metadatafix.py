import os
import platform
import pip
import requests

def is_arm_mac():
    """Return True if the current machine is an ARM Mac."""
    return platform.machine().startswith("arm64")

def install_hachoir():
    """Install the latest version of hachoir for M1 or M2 Macs."""
    try:
        pip.main(["install", "hachoir"])
    except:
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
    url = "https://github.com/metadata-dev/metadata/archive/refs/tags/v0.2.tar.gz"
    filename = "metadata-0.2.tar.gz"
    with requests.get(url, stream=True) as r:
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)

    os.system("tar -xf %s" % filename)
    os.system("cd metadata-0.2 && pip install .")

def main():
    if not is_arm_mac():
        print("This script is only intended for ARM Macs.")
        exit()

    if not os.geteuid() == 0:
        print("This script must be run as root. Please run it with sudo.")
        exit()

    install_hachoir()
    modify_metadata_requirements()
    install_metadata()

if __name__ == "__main__":
    main()
