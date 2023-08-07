import os
import platform
import requests
import gzip
import pip

def is_apple_silicon_mac():
    """Return True if the current machine is an Apple Silicon Mac."""
    return platform.machine().startswith("arm64")

def install_hachoir():
    """Install the latest version of hachoir for Apple Silicon Macs."""
    try:
        pip.main(["install", "hachoir"])
    except:
        pip.main(["install", "hachoir-parser"])

def modify_metadata_requirements():
    """Modify the metadata package requirements to be compatible with hachoir-core==1.3.3."""

    # Download the metadata package
    url = "https://github.com/metadata-dev/metadata/archive/refs/tags/v0.2.tar.gz"
    filename = "metadata-0.2.tar.gz"

    with requests.get(url, stream=True) as r:
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)

    # Uncompress the metadata package
    os.system("gzip -d %s" % filename)

    # Download the entire library
    url = "https://hachoir.org/files/hachoir-full-1.3.3.tar.gz"
    filename = "hachoir-full-1.3.3.tar.gz"

    with requests.get(url, stream=True) as r:
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)

    # Uncompress the library
    os.system("tar -xf %s" % filename)

    # Modify the requirements file
    with open("metadata-0.2/requirements.txt", "r") as f:
        requirements = f.readlines()

    for index, requirement in enumerate(requirements):
        if requirement.startswith("hachoir-core=="):
            requirements[index] = "hachoir==1.3.3"

    with open("metadata-0.2/requirements.txt", "w") as f:
        f.writelines(requirements)

def update_metadata_package():
    """Update the metadata package to be compatible with hachoir."""

    # Install the modified requirements file
    os.system("cd metadata-0.2 && pip install -r requirements.txt")

def main():
    """Check if the current machine is an Apple Silicon Mac.
    If it is, install hachoir and modify the metadata package requirements.
    If not, print a message and exit.
    """

    if not is_apple_silicon_mac():
        print("This script is only intended for Apple Silicon Macs.")
        exit()


    install_hachoir()
    modify_metadata_requirements()
    update_metadata_package()

if __name__ == "__main__":
    main()
