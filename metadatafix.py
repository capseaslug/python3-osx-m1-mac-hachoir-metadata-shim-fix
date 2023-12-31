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
    try:
        with requests.get(url, stream=True) as r:
            with open("metadata.tar.gz", "wb") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading metadata package: {e}")
        return

    # Extract the metadata from the package
    try:
        with gzip.open("metadata.tar.gz", "rb") as f:
            metadata = f.read().decode("utf-8")
    except Exception as e:
        print(f"Error extracting metadata from package: {e}")
        return

    # Modify the metadata to include hachoir-core==1.3.3
    try:
        metadata = re.sub(r"hachoir-core==\d.\d.\d", "hachoir-core==1.3.3", metadata)
    except Exception as e:
        print(f"Error modifying metadata: {e}")
        return

    # Save the modified metadata to a new file
    try:
        with open("metadata.tar.gz", "wb") as f:
            f.write(metadata.encode("utf-8"))
    except Exception as e:
        print(f"Error saving modified metadata: {e}")
        return

    # Install the modified metadata
    try:
        pip.main(["install", "-r", "metadata.tar.gz"])
    except Exception as e:
        print(f"Error installing modified metadata: {e}")
        return

    print("Success! The metadata requirements have been modified and the metadata python library has been installed.")

def main():
    """Check if the current machine is an Apple Silicon Mac.
    If it is, install hachoir and modify the metadata package requirements.
    If not, print a warning and continue.
    """

    is_apple_silicon = is_apple_silicon_mac()
    if not is_apple_silicon:
        print("Warning: This script was made for Apple Silicon Macs. It may not cause any problems on other machines, but it is not guaranteed to work.")
        answer = input("Are you sure you want to continue? (y/N): ")
        if answer != "y":
            print("Exiting...")
            exit()


    try:
        install_hachoir()
        modify_metadata_requirements()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
