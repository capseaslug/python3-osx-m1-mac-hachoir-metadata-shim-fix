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
    """Download the metadata package, extract the metadata, modify it to include hachoir-core==1.3.3, and then save the modified metadata."""

    url = "https://files.pythonhosted.org/packages/8a/2b/3982e589808af51d6e8d3f7ebb6c540005ad3466d1e49"

    # Download the metadata package
    with requests.get(url, stream=True) as r:
        with open("metadata.tar.gz", "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)

    # Extract the metadata from the package
    with gzip.open("metadata.tar.gz", "rb") as f:
        metadata = f.read().decode("utf-8")

    # Modify the metadata to include hachoir-core==1.3.3
    print("Replacing hachoir-core version...")
    metadata = re.sub(r"hachoir-core==\d.\d.\d", "hachoir-core==1.3.3", metadata)

    # Save the modified metadata to a new file
    with open("metadata.tar.gz", "wb") as f:
        f.write(metadata.encode("utf-8"))

    # Install the modified metadata
    print("Installing modified metadata...")
    pip.main(["install", "-r", "metadata.tar.gz"])

    print("Success! The metadata requirements have been modified and installed.")

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

if __name__ == "__main__":
    main()
