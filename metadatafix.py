import os
import platform
import requests
import gzip
import re
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
    url = "https://files.pythonhosted.org/packages/8a/2b/3982e589808af51d6e8d3f7ebb6c540005ad3466d1e4939e57d25cd1d3c0/metadata-0.2.tar.gz"
    filename = "metadata-0.2.tar.gz"

    with requests.get(url, stream=True) as r:
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)

    # Check if the file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File '{filename}' does not exist.")

    # Uncompress the metadata package
    os.system("gzip -d %s" % filename)

    # Search for the requirements file
    for root, directories, files in os.walk("metadata-0.2"):
        for file in files:
            if re.match("requirements\.txt", file):
                filename = os.path.join(root, file)
                break

    # Modify the requirements file
    with open(filename, "r") as f:
        requirements = f.readlines()

    for index, requirement in enumerate(requirements):
        if requirement.startswith("hachoir-core=="):
            requirements[index] = "hachoir==1.3.3"

    with open(filename, "w") as f:
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
