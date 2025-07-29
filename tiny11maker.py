#!/usr/bin/env python3
from Registry import Registry # python-registry on PyPi
import locale
import logging
import os
import shutil

import wimlib # python-wimlib

from wimlib import file as wimfile
from wimlib import image
from wimlib.compression import set_default_compression_level
from wimlib.compression import COMPRESSION_TYPE_LZMS

import tiny_configurer as configurer
from utils import YN_CHECK, valited_input, terminate

RELEASE = "2025-07-alpha"
BAD_INPUT_MSG = "%; please try again."

# HACK: Unfortunately, the wimlib mount call crashes silently - so use executable mount call.
wimlib._use_executable_mount = True


def main():
    # Load all configuration values (runtime and file-based)
    runtime, config = configurer.initialize()
    set_default_compression_level(COMPRESSION_TYPE_LZMS, 100)
    wimlib.set_error_printing(True) # Error logging... tweak later?

    # TODO: check for any access barriers? Maybe not needed?
    logging.info(f"Welcome to the tiny11 image creator! (Release: {RELEASE}).")

    # Set up the build directory (if not provided)
    if not runtime.build_path:
        runtime.build_path = os.path.join(os.environ.get('TMPDIR', '/tmp/'), "tiny11")

    logging.info(f"Buildpath / workspace set to {runtime.build_path}.")
    os.makedirs(prep_path := os.path.join(runtime.build_path, "prep"), exist_ok=True)
    prepare_build(prep_path, runtime.media_path, runtime.yes)

    # Here, the user chooses the base image.
    logging.info("Image Records\n-------------")
    wim_file = wimfile.WimFile.from_file(os.path.join(prep_path, "sources/install.wim"))
    logging.info(wim_file.images.get_listing())
    check = lambda k: None if not int(k) in wim_file.images.keys() else int(k)
    prompt = "Select a base image: "
    img_index = validated_input(prompt, BAD_INPUT_MSG % "Invalid index", check)

    # Prepare the directories and mount the image.
    logging.info(f"Mounting image {img_index}...")
    os.makedirs(mount_path := os.path.join(runtime.build_path, "mount"), exist_ok=True)
    os.makedirs(staging_path := os.path.join(runtime.build_path, "staging"), exist_ok=True)

    base_image = wim_file.images[img_index]
    base_image.mount(mount_path, flags=image.MOUNT_READWRITE, staging=staging_path)
    logging.info(f"Successfully mounted at {mount_path}.")

    # Fetch some critical image information (with user input as needed).
    language_index, language_code = select_language(base_image, runtime.yes)
    logging.info(f"Successfully identified language '{language_code}' (#{language_index}).")
    exit()

    logging.info("Removing Edge and connected packages...")
    remove_edge_browser(image, mount_path)

    # Remove packages and applications.
    logging.info("Removing packages...")
    remove_packages(mount_path)
    logging.info("Removing OneDrive...")
    remove_onedrive(image, mount_path)
    logging.info("Application removal complete!")

    # Update the registry.
    logging.info("Loading registry...")
    load_registry()
    logging.info("Bypassing system requirements on the system image")
    bypass_requirements()
    logging.info("Disabling Sponsored Apps")
    disable_sponsored_apps()
    logging.info("Disabling Chat icon")
    disable_chat()
    logging.info("Removing Edge related registries")
    delete_edge_registry()
    logging.info("Disabling OneDrive folder backup")
    disable_onedrive_registry()
    logging.info("Prevents installation or DevHome and Outlook:")
    disable_devhome_outlook()
    logging.info('Deleting Application Compatibility Appraiser')
    delete_miscelaneous()
    logging.info("Disabling Reserved Storage")
    disable_reserved()
    logging.info("Enabling Local Accounts on OOBE")
    enable_oobe()
    logging.info("Disabling User Telemetry:")
    disable_user_telemetry()
    logging.info("Disabling System Telemetry:")
    disable_system_telemetry()
    logging.info("Disabling BitLocker Device Encryption")
    disable_bitlocker()
    logging.info("Owner changed to Administrators.")
    reset_ownership()
    logging.info("Unmounting Registry...")
    unload_registry()

    logging.info("Cleaning up image and unmounting base...")
    #Repair-WindowsImage -Path $ScratchDisk\scratchdir -StartComponentCleanup -ResetBase
    #Dismount-WindowsImage -Path $ScratchDisk\scratchdir -Save

    logging.info("Exporting image...")
    # Compressiontype Recovery is not supported with PShell https://learn.microsoft.com/en-us/powershell/module/dism/export-windowsimage?view=windowsserver2022-ps#-compressiontype
    # Export-WindowsImage -SourceImagePath $ScratchDisk\tiny11\sources\install.wim -SourceIndex $index -DestinationImagePath $ScratchDisk\tiny11\sources\install2.wim -CompressionType Fast
    # Remove-Item -Path "$ScratchDisk\tiny11\sources\install.wim" -Force | Out-Null
    # Rename-Item -Path "$ScratchDisk\tiny11\sources\install2.wim" -NewName "install.wim" | Out-Null

    logging.info("Windows image completed.\n")
    #Start-Sleep -Seconds 2
    #Clear-Host

    logging.info("Mounting boot image:")
    #$wimFilePath = "$ScratchDisk\tiny11\sources\boot.wim"
    # & takeown "/F" $wimFilePath | Out-Null
    # & icacls $wimFilePath "/grant" "$($adminGroup.Value):(F)"
    #Set-ItemProperty -Path $wimFilePath -Name IsReadOnly -Value $false
    #Mount-WindowsImage -ImagePath $ScratchDisk\tiny11\sources\boot.wim -Index 2 -Path $ScratchDisk\scratchdir

    logging.info("Loading registry...")
    # reg load HKLM\zCOMPONENTS $ScratchDisk\scratchdir\Windows\System32\config\COMPONENTS
    # reg load HKLM\zDEFAULT $ScratchDisk\scratchdir\Windows\System32\config\default
    # reg load HKLM\zNTUSER $ScratchDisk\scratchdir\Users\Default\ntuser.dat
    # reg load HKLM\zSOFTWARE $ScratchDisk\scratchdir\Windows\System32\config\SOFTWARE
    # reg load HKLM\zSYSTEM $ScratchDisk\scratchdir\Windows\System32\config\SYSTEM

    logging.info("Bypassing system requirements (on the setup image):")
    # & 'reg' 'add' 'HKLM\zDEFAULT\Control Panel\UnsupportedHardwareNotificationCache' '/v' 'SV1' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zDEFAULT\Control Panel\UnsupportedHardwareNotificationCache' '/v' 'SV2' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Control Panel\UnsupportedHardwareNotificationCache' '/v' 'SV1' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Control Panel\UnsupportedHardwareNotificationCache' '/v' 'SV2' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zSYSTEM\Setup\LabConfig' '/v' 'BypassCPUCheck' '/t' 'REG_DWORD' '/d' '1' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zSYSTEM\Setup\LabConfig' '/v' 'BypassRAMCheck' '/t' 'REG_DWORD' '/d' '1' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zSYSTEM\Setup\LabConfig' '/v' 'BypassSecureBootCheck' '/t' 'REG_DWORD' '/d' '1' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zSYSTEM\Setup\LabConfig' '/v' 'BypassStorageCheck' '/t' 'REG_DWORD' '/d' '1' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zSYSTEM\Setup\LabConfig' '/v' 'BypassTPMCheck' '/t' 'REG_DWORD' '/d' '1' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zSYSTEM\Setup\MoSetup' '/v' 'AllowUpgradesWithUnsupportedTPMOrCPU' '/t' 'REG_DWORD' '/d' '1' '/f' | Out-Null
    logging.info("Tweaking complete!")
    logging.info("Unmounting Registry...")
    #$regKey.Close()
    # reg unload HKLM\zCOMPONENTS | Out-Null
    # reg unload HKLM\zDRIVERS | Out-Null
    # reg unload HKLM\zDEFAULT | Out-Null
    # reg unload HKLM\zNTUSER | Out-Null
    # reg unload HKLM\zSCHEMA | Out-Null
    #$regKey.Close()
    # reg unload HKLM\zSOFTWARE
    # reg unload HKLM\zSYSTEM | Out-Null
    logging.info("Unmounting image...")
    #Dismount-WindowsImage -Path $ScratchDisk\scratchdir -Save
    #Clear-Host

    logging.info("The tiny11 image is now completed. Proceeding with the making of the ISO...")
    logging.info("Copying unattended file for bypassing MS account on OOBE...")
    #Copy-Item -Path "$PSScriptRoot\autounattend.xml" -Destination "$ScratchDisk\tiny11\autounattend.xml" -Force | Out-Null
    logging.info("Creating ISO image...")
    #$hostArchitecture = $Env:PROCESSOR_ARCHITECTURE
    #$ADKDepTools = "C:\Program Files (x86)\Windows Kits\10\Assessment and Deployment Kit\Deployment Tools\$hostarchitecture\Oscdimg"
    #$localOSCDIMGPath = "$PSScriptRoot\oscdimg.exe"

    if True: # ([System.IO.Directory]::Exists($ADKDepTools)) {
        logging.info("Will be using oscdimg.exe from system ADK.")
    #    $OSCDIMG = "$ADKDepTools\oscdimg.exe"
    else:
        logging.info("ADK folder not found. Will be using bundled oscdimg.exe.")
        url = "https://msdl.microsoft.com/download/symbols/oscdimg.exe/3D44737265000/oscdimg.exe"

        if not False: # actual condition: (Test-Path -Path $localOSCDIMGPath)
            logging.info("Downloading oscdimg.exe...")
            # Invoke-WebRequest -Uri $url -OutFile $localOSCDIMGPath

            if True: # (Test-Path $localOSCDIMGPath) {
                logging.info("oscdimg.exe downloaded successfully.")
            else:
                logging.error("Failed to download oscdimg.exe.")
                exit()
        else:
            logging.info("oscdimg.exe already exists locally.")

        # $OSCDIMG = $localOSCDIMGPath
    # & "$OSCDIMG" '-m' '-o' '-u2' '-udfver102' "-bootdata:2#p0,e,b$ScratchDisk\tiny11\boot\etfsboot.com#pEF,e,b$ScratchDisk\tiny11\efi\microsoft\boot\efisys.bin" "$ScratchDisk\tiny11" "$PSScriptRoot\tiny11.iso"

    # Finishing up
    logging.info("Creation completed! Press any key to exit the script...")
    #Read-Host "Press Enter to continue"
    logging.info("Performing Cleanup...")
    # Remove-Item -Path "$ScratchDisk\tiny11" -Recurse -Force | Out-Null
    # Remove-Item -Path "$ScratchDisk\scratchdir" -Recurse -Force | Out-Null

    # Stop the transcript
    #Stop-Transcript


def prepare_build(workspace, source_media, overwrite=False):
    # Get the media path if we don't have it yet.
    if not source_media:
        check = lambda p: None if not os.path.isdir(p) else p
        prompt = "Please enter path for Windows media: "
        source_media = validated_input(prompt, BAD_INPUT_MSG % "Invalid path", check)

    if os.path.exists(workspace) and not overwrite:
        prompt = f"{workspace} exists. Overwrite [y/N]? "
        result = validated_input(prompt, BAD_INPUT_MSG % "Answer 'Y' or 'N'", YN_CHECK)
        # Permissions are read only. Find a way to turn off attribs?

        if not (result.upper() == 'Y'):
            logging.info(f"Directory {runtime.build_path} is not empty; aborting.")
            exit()

    shutil.rmtree(workspace)

    logging.info(f"Searching for install files in {source_media}...")
    boot_image_path = os.path.join(source_media, "sources/boot.wim")
    image_path = os.path.join(source_media, "sources/install.wim")
    esd_path = os.path.join(source_media, "sources/install.esd")

    # Handle error cases - no boot images and/or no installation images.
    if not os.path.isfile(boot_image_path):
        terminate("No boot images found; terminating.")

    if not os.path.isfile(image_path) and not os.path.isfile(esd_path):
        terminate(f"No installation images found; terminating.")

    # If there's no WIM but there is an ESD file, attempt conversion/
    if not os.path.isfile(image_path) and os.path.isfile(esd_path):
        logging.info("Converting installation ESD into WIM; this may take a while...")
        target_wim = wimfile.WimFile(os.path.join(workspace, "sources/install.wim"))

        # Set parameters for export, then create the new image.
        logging.info('NOTE: unable to check integrity (not implemented).')
        esd_file = wimfile.WimFile.from_file(esd_path)
        esd_file.set_output_compression_type(COMPRESSION_TYPE_LZMS)
        esd_file.images[img_index].export_image(target_wim)
        logging.info("Conversion successful.\n") # Sleep for 2 seconds? Clear screen?

    # Copy installation media files (excluding install.esd, if present) to prep directory.
    logging.info("Copying Windows installation media...")
    copy_filter = shutil.ignore_patterns('install.esd')
    shutil.copytree(source_media, workspace, dirs_exist_ok=True, ignore=copy_filter)
    logging.info("Copy complete!\n") # Sleep for 2 seconds? Clear screen?


def select_language(image, automated=False):
    # Fetch the local language and list of languages from the image
    languages = image.get_languages()
    local_code = locale.getlocale()[0]
    local_index = languages.index(local_code) if local_code in languages else -1

    # If there are no languges, return error values that can be gracefully handled..
    if len(languages) == 0:
        return -1, ""

    # Separate default language from rest of list; track offset.
    if not languages[0]:
        default_language = -1
        offset = 1

    elif not type(languages[0]) is int:
        default_language = 0
        offset = 0

    else:
        default_language = languages[0]
        offset = 1

    # If there's only one language of the system is in automation mode, go with the default.
    if (len(languages) - offset) == 0 or automated:
        language_index = default_language if default_language >= offset else offset

        if automated and default_language < offset:
            logging.warn("No default language, but in automated mode; defaulting to first.")

    # If we get here, it means that we have multiple languages, so the user should select one.
    else:
        logging.info("Languages Available:\n--------------------")
        for count in range(offset, len(languages)):
            logging.info(f"{count}. {languages[count]}")

        check = lambda k: None if (int(k) > len(languages) or int(k) < offset) else int(k)
        prompt = "Select a language for image: "
        language_index = validated_input(prompt, BAD_INPUT_MSG % "Invalid index", check)

    return language_index, str(languages[language_index])


if __name__ == "__main__":
    main()

