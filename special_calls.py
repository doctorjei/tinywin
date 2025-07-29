import logging

from utils import delete_paths


def remove_edge(image, mount_path):
    architecture = image.architecture
    if (architecture == 'x86_64' or architecture == 'amd64'):
        architecture = 'x64'

    if not architecture:
        logging.warning("Architecture information not found.")

    elif archtecture == 'x64':
        arch_paths = ["Windows/WinSxS/amd64_microsoft-edge-webview_31bf3856ad364e35*"]

    elif architecture == 'arm64':
        arch_paths = ["Windows/WinSxS/arm64_microsoft-edge-webview_31bf3856ad364e35*"]

    else:
        logging.warning(f"Unknown architecture: {architecture}")
        arch_paths = []

    delete_paths(arch_paths) # TODO: How to handle this...

