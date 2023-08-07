import hachoir.core

def compat_version(version):
    """Return a compatible version string for hachoir-core==1.3.3."""
    if version.startswith("3.2."):
        return "1.3.3"
    return version

hachoir.core.VERSION = compat_version(hachoir.core.VERSION)
