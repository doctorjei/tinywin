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

RELEASE = "2025-07-alpha"

#WIN_CONFIG_PATH = "Windows/System32/config/"
SW_HIVE_PATH = "Windows/System32/config/SOFTWARE"
# "SAM", "SECURITY", "SYSTEM", "ELAM", "DRIVERS", "DEFAULT","COMPONENTS", "BBI"

SHARED_APPX_HIVE = "Microsoft\\Windows\\CurrentVersion\\Appx\\AppxAllUserStore\\Applications"
BAD_INPUT_MSG = "%; please try again."

YN_CHECK = lambda r: None if not len(r) or (r.upper()[0] != 'Y' and r.upper()[0] != 'N') else r[0]


# Unfortunately, the wimlib mount call crashes silently - so use the executable mount call.
wimlib._use_executable_mount = True


def validated_input(prompt, error_msg, validator):
    result = input(prompt)
    while not (result := validator(result)):
        print(error_msg)
        result = input(prompt)
    return result


def terminate(msg="Unspecificed fatal error."):
    logging.fatal(msg)
    exit()


def delete_filesets(base, paths_to_remove):
    for target_path in paths_to_remove:
        full_path = os.path.join(base, target_path)
        # Take ownership and remove the path completely.


def execute_removal(instructions, image, system_path):
    delete_packages(system_path, instructions.get("Packages"))
    delete_filesets(system_path, instructions.get("Delete_File"))
    # Add registry entries
    # Delete registry entries
    if instructions.get("Callable"):
        instructions.get("Callable")(image, system_path)


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


def remove_packages(mount_path):
    logging.info("Beginning application removal...")


    sw_hive_path = os.path.join(mount_path, SW_HIVE_PATH)
    software_hive = Registry.Registry(sw_hive_path)
    appx_hive = software_hive.open(SHARED_APPX_PATH)

    targets = ['Clipchamp.Clipchamp', 'Microsoft.549981C3F5F10', 'Microsoft.BingNews',
               'Microsoft.BingSearch', 'Microsoft.BingWeather', 'Microsoft.GamingApp',
               'Microsoft.GetHelp',
               'Microsoft.Getstarted', 'Microsoft.MicrosoftOfficeHub',
               'Microsoft.MicrosoftSolitaireCollection', 'Microsoft.People',
               'Microsoft.PowerAutomateDesktop', 'Microsoft.Todos',
               'Microsoft.WindowsAlarms', 'microsoft.windowscommunicationsapps',
               'Microsoft.WindowsFeedbackHub', 'Microsoft.WindowsMaps',
               'Microsoft.WindowsSoundRecorder', 'Microsoft.Xbox.TCUI',
               'Microsoft.XboxGamingOverlay', 'Microsoft.XboxGameOverlay',
               'Microsoft.XboxSpeechToTextOverlay', 'Microsoft.YourPhone',
               'Microsoft.ZuneMusic', 'Microsoft.ZuneVideo',
               'MicrosoftCorporationII.MicrosoftFamily',
               'MicrosoftCorporationII.QuickAssist_', 'MicrosoftTeams']

    provisioned = [subkey.name() for subkey in bob.subkeys()]
    to_be_removed = [entry for entry in provisioned if "_" in entry and entry.split("_")[0] in targets]

    packagesToRemove = [] # Get the list of packages to be removed.
    for entry in packagePrefixes:
        pass # if any package has that prefix, add it to the packagesToRemove.
    # $packagesToRemove = $installed_packages | Where-Object {
    #     $packageName = $_
    #     $packagePrefixes -contains ($packagePrefixes | Where-Object { $packageName -like "$_*" })
    # }

    for package in packagesToRemove:
        pass # Remove the package.
    # foreach ($package in $packagesToRemove) {
    #     & 'dism' '/English' "/image:$($ScratchDisk)\scratchdir" '/Remove-ProvisionedAppxPackage' "/>
    # }

    logging.info("AppX not yet implemented!")
    return

""" Orginial
'Clipchamp.Clipchamp',				42M
'Microsoft.549981C3F5F10',			2M
'Microsoft.BingNews',				30M
'Microsoft.BingSearch',				0.4M
'Microsoft.BingWeather',			0.6M
'Microsoft.GamingApp',				360M
'Microsoft.GetHelp',				244M
'Microsoft.Getstarted',				23M
'Microsoft.MicrosoftOfficeHub',			1M
'Microsoft.MicrosoftSolitaireCollection',	68M
'Microsoft.People',				25M
'Microsoft.PowerAutomateDesktop',		2M
'Microsoft.Todos',				1.2M
'Microsoft.WindowsAlarms',			23M
'Microsoft.windowscommunicationsapps',		211M
'Microsoft.WindowsFeedbackHub',			41M
'Microsoft.WindowsMaps',			45M
'Microsoft.WindowsSoundRecorder',		2M
'Microsoft.Xbox.TCUI',				12M
'Microsoft.XboxGamingOverlay',			26M
'Microsoft.XboxGameOverlay',                    3M
'Microsoft.XboxSpeechToTextOverlay',            1M
'Microsoft.YourPhone',                          2M
'Microsoft.ZuneMusic',                          36M
'Microsoft.ZuneVideo',                          35M
'MicrosoftCorporationII.MicrosoftFamily',       ????
'MicrosoftCorporationII.QuickAssist_',          5M
'MicrosoftTeams'                                300M?

Other possible targets for removal:

Microsoft.Windows.Photos_24.24010.29003.0_neutral_~_8wekyb3d8bbwe		**	523M
Microsoft.Paint_11.2302.20.0_neutral_~_8wekyb3d8bbwe				**	417M
MSTeams_1.0.0.0_x64__8wekyb3d8bbwe						**	300M
Microsoft.ScreenSketch_2022.2307.52.0_neutral_~_8wekyb3d8bbwe			**	212M
MicrosoftWindows.Client.WebExperience_424.1301.270.9_neutral_~_cw5n1h2txyewy	**	167M
MicrosoftWindows.CrossDevice_1.23101.22.0_neutral_~_cw5n1h2txyewy		**	92M
#Microsoft.WindowsStore_22401.1400.6.0_neutral_~_8wekyb3d8bbwe			**	80M
Microsoft.StorePurchaseApp_22312.1400.6.0_neutral_~_8wekyb3d8bbwe		**	47M
Microsoft.OutlookForWindows_1.0.0.0_neutral__8wekyb3d8bbwe			**	45M
Microsoft.SecHealthUI_1000.26100.1.0_x64__8wekyb3d8bbwe				**	24M
Microsoft.WindowsAlarms_2022.2312.2.0_neutral_~_8wekyb3d8bbwe			**	23M
Microsoft.WindowsCamera_2022.2312.3.0_neutral_~_8wekyb3d8bbwe			**	22M
Microsoft.WindowsNotepad_11.2312.18.0_neutral_~_8wekyb3d8bbwe			**	20M
Microsoft.WindowsCalculator_2021.2311.0.0_neutral_~_8wekyb3d8bbwe		**	17M
Microsoft.XboxIdentityProvider_12.110.15002.0_neutral_~_8wekyb3d8bbwe		**	11M
Microsoft.MicrosoftStickyNotes_4.6.2.0_neutral_~_8wekyb3d8bbwe			**	2M
Microsoft.Windows.DevHome_0.100.128.0_neutral_~_8wekyb3d8bbwe *************	**	2M


--- KEEP THESE ---
Microsoft.WindowsTerminal_3001.18.10301.0_neutral_~_8wekyb3d8bbwe		X	19M
Microsoft.HEIFImageExtension_1.0.63001.0_neutral_~_8wekyb3d8bbwe		??	14M
Microsoft.VP9VideoExtensions_1.1.451.0_neutral_~_8wekyb3d8bbwe			??	7M
Microsoft.HEVCVideoExtension_2.0.61931.0_neutral_~_8wekyb3d8bbwe		??	6M
Microsoft.AV1VideoExtension_1.1.61781.0_neutral_~_8wekyb3d8bbwe			??	5M
Microsoft.AVCEncoderVideoExtension_1.0.271.0_neutral_~_8wekyb3d8bbwe		??	4M
Microsoft.RawImageExtension_2.3.171.0_neutral_~_8wekyb3d8bbwe			??	3.3M
Microsoft.ApplicationCompatibilityEnhancements_1.2401.10.0_neutral_~_8wekyb3d8bbwe ??	3M
Microsoft.MPEG2VideoExtension_1.0.61931.0_neutral_~_8wekyb3d8bbwe		--	3M
Microsoft.WebMediaExtensions_1.0.62931.0_neutral_~_8wekyb3d8bbwe		--	2.9M
Microsoft.WebpImageExtension_1.0.62681.0_neutral_~_8wekyb3d8bbwe		--	1.6M




Others from recent updates:
Microsoft.Copilot_				190M
Microsoft.DesktopAppInstaller_			138M
Microsoft.Ink.Handwriting.en-US.1.0_		9M
Microsoft.Microsoft3DViewer_			58M
Microsoft.OfficePushNotificationUtility_	0.1M
Microsoft.OneDriveSync_				0.1M
Microsoft.PowerToys.FileLocksmithContextMenu_ 	?
Microsoft.PowerToys.ImageResizerContextMenu_  	?
Microsoft.PowerToys.PowerRenameContextMenu_   	?
Microsoft.Services.Store.Engagement_          	?
Microsoft.Teams.TxNdi_				?
Microsoft.UI.Xaml.2.7_7.2208.15002.0_		?
Microsoft.WidgetsPlatformRuntime_		?
MicrosoftWindows.Speech.ja-JP.1			?
MicrosoftWindows.Voice.ja-JP.Nanami.1_		?
MicrosoftWindows.WindowsSandbox_		??
"""


def remove_edge_browser(image, mount_path):
    # TODO: Use removal_steps to delete files.
    architecture = image.architecture
    if (architecture == 'x86_64' or architecture == 'amd64'):
        architecture = 'x64'

    if not architecture:
        logging.warning("Architecture information not found.")

    elif archtecture == 'x64': # Should result in a list (probably of one)
        arch_paths = ["Windows/WinSxS/amd64_microsoft-edge-webview_31bf3856ad364e35*"]

    elif architecture == 'arm64':
        arch_paths = ["Windows/WinSxS/arm64_microsoft-edge-webview_31bf3856ad364e35*"]

    else:
        logging.warning(f"Unknown architecture: {architecture}")
        arch_paths = []

    delete_filesets(arch_paths)


def remove_onedrive(mount_path):
    delete_filesets(mount_path, "Windows/System32/OneDriveSetup.exe")


def load_registrey():
    pass
    # reg load HKLM\zCOMPONENTS $ScratchDisk\scratchdir\Windows\System32\config\COMPONENTS | Out-Null
    # reg load HKLM\zDEFAULT $ScratchDisk\scratchdir\Windows\System32\config\default | Out-Null
    # reg load HKLM\zNTUSER $ScratchDisk\scratchdir\Users\Default\ntuser.dat | Out-Null
    # reg load HKLM\zSOFTWARE $ScratchDisk\scratchdir\Windows\System32\config\SOFTWARE | Out-Null
    # reg load HKLM\zSYSTEM $ScratchDisk\scratchdir\Windows\System32\config\SYSTEM | Out-Null


def disable_sponsored_apps():
    pass
    # & 'reg' 'add' 'HKLM\zNTUSER\SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'OemPreInstalledAppsEnabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'OemPreInstalledAppsEnabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'PreInstalledAppsEnabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'SilentInstalledAppsEnabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zSOFTWARE\Policies\Microsoft\Windows\CloudContent' '/v' 'DisableWindowsConsumerFeatures' '/t' 'REG_DWORD' '/d' '1' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'ContentDeliveryAllowed' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zSOFTWARE\Microsoft\PolicyManager\current\device\Start' '/v' 'ConfigureStartPins' '/t' 'REG_SZ' '/d' '{"pinnedList": [{}]}' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'ContentDeliveryAllowed' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'ContentDeliveryAllowed' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'FeatureManagementEnabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'OemPreInstalledAppsEnabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'PreInstalledAppsEnabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'PreInstalledAppsEverEnabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'SilentInstalledAppsEnabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'SoftLandingEnabled' '/t' 'REG_DWORD' '/d' '0' '/f'| Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'SubscribedContentEnabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'SubscribedContent-310093Enabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'SubscribedContent-338388Enabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'SubscribedContent-338389Enabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'SubscribedContent-338393Enabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'SubscribedContent-353694Enabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'SubscribedContent-353696Enabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'SubscribedContentEnabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' '/v' 'SystemPaneSuggestionsEnabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zSOFTWARE\Policies\Microsoft\PushToInstall' '/v' 'DisablePushToInstall' '/t' 'REG_DWORD' '/d' '1' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zSOFTWARE\Policies\Microsoft\MRT' '/v' 'DontOfferThroughWUAU' '/t' 'REG_DWORD' '/d' '1' '/f' | Out-Null
    # & 'reg' 'delete' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager\Subscriptions' '/f' | Out-Null
    # & 'reg' 'delete' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager\SuggestedApps' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zSOFTWARE\Policies\Microsoft\Windows\CloudContent' '/v' 'DisableConsumerAccountStateContent' '/t' 'REG_DWORD' '/d' '1' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zSOFTWARE\Policies\Microsoft\Windows\CloudContent' '/v' 'DisableCloudOptimizedContent' '/t' 'REG_DWORD' '/d' '1' '/f' | Out-Null


def disable_chat():
    logging.info("Disabling Chat icon:")
    # & 'reg' 'add' 'HKLM\zSOFTWARE\Policies\Microsoft\Windows\Windows Chat' '/v' 'ChatIcon' '/t' 'REG_DWORD' '/d' '3' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced' '/v' 'TaskbarMn' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null


def delete_edge_registry():
    logging.info("Removing Edge related registries")
    # reg delete "HKEY_LOCAL_MACHINE\zSOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Microsoft Edge" /f | Out-Null
    # reg delete "HKEY_LOCAL_MACHINE\zSOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Microsoft Edge Update" /f | Out-Null


def disable_onedrive_registry():
    logging.info("Disabling OneDrive folder backup")
    # & 'reg' 'add' "HKLM\zSOFTWARE\Policies\Microsoft\Windows\OneDrive" '/v' 'DisableFileSyncNGSC' '/t' 'REG_DWORD' '/d' '1' '/f' | Out-Null


def disable_devhome_outlook():
    logging.info("Prevents installation or DevHome and Outlook:")
    # & 'reg' 'add' 'HKLM\zSOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Orchestrator\UScheduler\OutlookUpdate' '/v' 'workCompleted' '/t' 'REG_DWORD' '/d' '1' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zSOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Orchestrator\UScheduler\DevHomeUpdate' '/v' 'workCompleted' '/t' 'REG_DWORD' '/d' '1' '/f' | Out-Null
    # & 'reg' 'delete' 'HKLM\zSOFTWARE\Microsoft\WindowsUpdate\Orchestrator\UScheduler_Oobe\OutlookUpdate' '/f' | Out-Null
    # & 'reg' 'delete' 'HKLM\zSOFTWARE\Microsoft\WindowsUpdate\Orchestrator\UScheduler_Oobe\DevHomeUpdate' '/f' | Out-Null


def delete_miscelaneous():
    logging.info('Deleting Application Compatibility Appraiser')
    # reg delete "HKEY_LOCAL_MACHINE\zSOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tasks\{0600DD45-FAF2-4131-A006-0B17509B9F78}" /f | Out-Null

    logging.info('Deleting Customer Experience Improvement Program')
    # reg delete "HKEY_LOCAL_MACHINE\zSOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tasks\{4738DE7A-BCC1-4E2D-B1B0-CADB044BFA81}" /f | Out-Null
    # reg delete "HKEY_LOCAL_MACHINE\zSOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tasks\{6FAC31FA-4A85-4E64-BFD5-2154FF4594B3}" /f | Out-Null
    # reg delete "HKEY_LOCAL_MACHINE\zSOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tasks\{FC931F16-B50A-472E-B061-B6F79A71EF59}" /f | Out-Null
    logging.info('Deleting Program Data Updater')
    # reg delete "HKEY_LOCAL_MACHINE\zSOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tasks\{0671EB05-7D95-4153-A32B-1426B9FE61DB}" /f | Out-Null
    logging.info('Deleting autochk proxy')
    # reg delete "HKEY_LOCAL_MACHINE\zSOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tasks\{87BF85F4-2CE1-4160-96EA-52F554AA28A2}" /f | Out-Null
    # reg delete "HKEY_LOCAL_MACHINE\zSOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tasks\{8A9C643C-3D74-4099-B6BD-9C6D170898B1}" /f | Out-Null
    logging.info('Deleting QueueReporting')
    # reg delete "HKEY_LOCAL_MACHINE\zSOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tasks\{E3176A65-4E44-4ED3-AA73-3283660ACB9C}" /f | Out-Null
    logging.info("Tweaking complete!")
    #$regKey.Close()


def disable_reserved():
    pass
    # & 'reg' 'add' 'HKLM\zSOFTWARE\Microsoft\Windows\CurrentVersion\ReserveManager' '/v' 'ShippedWithReserves' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null


def enable_oobe():
    pass
    # & 'reg' 'add' 'HKLM\zSOFTWARE\Microsoft\Windows\CurrentVersion\OOBE' '/v' 'BypassNRO' '/t' 'REG_DWORD' '/d' '1' '/f' | Out-Null
    # **************Copy-Item -Path "$PSScriptRoot\autounattend.xml" -Destination "$ScratchDisk\scratchdir\Windows\System32\Sysprep\autounattend.xml" -Force | Out-Null


def disable_bitlocker():
    logging.info("Disabling BitLocker Device Encryption")
    # & 'reg' 'add' 'HKLM\zSYSTEM\ControlSet001\Control\BitLocker' '/v' 'PreventDeviceEncryption' '/t' 'REG_DWORD' '/d' '1' '/f' | Out-Null


def disable_user_telemetry():
    logging.info("Disabling User Telemetry:")
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo' '/v' 'Enabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Windows\CurrentVersion\Privacy' '/v' 'TailoredExperiencesWithDiagnosticDataEnabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Speech_OneCore\Settings\OnlineSpeechPrivacy' '/v' 'HasAccepted' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Input\TIPC' '/v' 'Enabled' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\InputPersonalization' '/v' 'RestrictImplicitInkCollection' '/t' 'REG_DWORD' '/d' '1' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\InputPersonalization' '/v' 'RestrictImplicitTextCollection' '/t' 'REG_DWORD' '/d' '1' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\InputPersonalization\TrainedDataStore' '/v' 'HarvestContacts' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zNTUSER\Software\Microsoft\Personalization\Settings' '/v' 'AcceptedPrivacyPolicy' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null
    # & 'reg' 'add' 'HKLM\zSOFTWARE\Policies\Microsoft\Windows\DataCollection' '/v' 'AllowTelemetry' '/t' 'REG_DWORD' '/d' '0' '/f' | Out-Null


def disable_system_telemetry():
    logging.info("Disabling System Telemetry:")
    # & 'reg' 'add' 'HKLM\zSYSTEM\ControlSet001\Services\dmwappushservice' '/v' 'Start' '/t' 'REG_DWORD' '/d' '4' '/f' | Out-Null
    ## Prevents installation or DevHome and Outlook


def bypass_requirements():
    pass
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


def reset_ownership():
    enable_privilege('SeTakeOwnershipPrivilege')
    #$regKey = [Microsoft.Win32.Registry]::LocalMachine.OpenSubKey("zSOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tasks",[Microsoft.Win32.RegistryKeyPermissionCheck]::ReadWriteSubTree,[System.Security.AccessControl.RegistryRights]::TakeOwnership)
    #$regACL = $regKey.GetAccessControl()
    #$regACL.SetOwner($adminGroup)
    #$regKey.SetAccessControl($regACL)
    #$regKey.Close()

    logging.info("Owner changed to Administrators.")
    #$regKey = [Microsoft.Win32.Registry]::LocalMachine.OpenSubKey("zSOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tasks",[Microsoft.Win32.RegistryKeyPermissionCheck]::ReadWriteSubTree,[System.Security.AccessControl.RegistryRights]::ChangePermissions)
    #$regACL = $regKey.GetAccessControl()
    #$regRule = New-Object System.Security.AccessControl.RegistryAccessRule ($adminGroup,"FullControl","ContainerInherit","None","Allow")
    #$regACL.SetAccessRule($regRule)
    #$regKey.SetAccessControl($regACL)
    logging.info("Permissions modified for Administrators group.")
    logging.info("Registry key permissions successfully updated.")
    #$regKey.Close()


def unload_registry():
    pass
    # reg unload HKLM\zCOMPONENTS | Out-Null
    # reg unload HKLM\zDRIVERS | Out-Null
    # reg unload HKLM\zDEFAULT | Out-Null
    # reg unload HKLM\zNTUSER | Out-Null
    # reg unload HKLM\zSCHEMA | Out-Null
    # reg unload HKLM\zSOFTWARE
    # reg unload HKLM\zSYSTEM | Out-Null


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
#    prepare_build(prep_path, runtime.media_path, runtime.yes)

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


## this function allows PowerShell to take ownership of the Scheduled Tasks registry key from TrustedInstaller. Based on Jose Espitia's script.
# example from above: enable_privilege('SeTakeOwnershipPrivilege')
def enable_privilege(parameter): # ?
    pass
    # param(
    #  [ValidateSet(
    #   "SeAssignPrimaryTokenPrivilege", "SeAuditPrivilege", "SeBackupPrivilege",
    #   "SeChangeNotifyPrivilege", "SeCreateGlobalPrivilege", "SeCreatePagefilePrivilege",
    #   "SeCreatePermanentPrivilege", "SeCreateSymbolicLinkPrivilege", "SeCreateTokenPrivilege",
    #   "SeDebugPrivilege", "SeEnableDelegationPrivilege", "SeImpersonatePrivilege", "SeIncreaseBasePriorityPrivilege",
    #   "SeIncreaseQuotaPrivilege", "SeIncreaseWorkingSetPrivilege", "SeLoadDriverPrivilege",
    #   "SeLockMemoryPrivilege", "SeMachineAccountPrivilege", "SeManageVolumePrivilege",
    #   "SeProfileSingleProcessPrivilege", "SeRelabelPrivilege", "SeRemoteShutdownPrivilege",
    #   "SeRestorePrivilege", "SeSecurityPrivilege", "SeShutdownPrivilege", "SeSyncAgentPrivilege",
    #   "SeSystemEnvironmentPrivilege", "SeSystemProfilePrivilege", "SeSystemtimePrivilege",
    #   "SeTakeOwnershipPrivilege", "SeTcbPrivilege", "SeTimeZonePrivilege", "SeTrustedCredManAccessPrivilege",
    #   "SeUndockPrivilege", "SeUnsolicitedInputPrivilege")]
    # $Privilege,
      ## The process on which to adjust the privilege. Defaults to the current process.
    # $ProcessId = $pid,
    ## Switch to disable the privilege, rather than enable it.
    #  [Switch] $Disable
    # )
    # $definition = @'
    # using System;
    # using System.Runtime.InteropServices;
    #
    # public class AdjPriv
    # {
    #  [DllImport("advapi32.dll", ExactSpelling = true, SetLastError = true)]
    #  internal static extern bool AdjustTokenPrivileges(IntPtr htok, bool disall,
    #   ref TokPriv1Luid newst, int len, IntPtr prev, IntPtr relen);

    #  [DllImport("advapi32.dll", ExactSpelling = true, SetLastError = true)]
    #  internal static extern bool OpenProcessToken(IntPtr h, int acc, ref IntPtr phtok);
    #  [DllImport("advapi32.dll", SetLastError = true)]
    #  internal static extern bool LookupPrivilegeValue(string host, string name, ref long pluid);
    #  [StructLayout(LayoutKind.Sequential, Pack = 1)]
    #  internal struct TokPriv1Luid
    #  {
    #   public int Count;
    #   public long Luid;
    #   public int Attr;
    #  }
    #
    #  internal const int SE_PRIVILEGE_ENABLED = 0x00000002;
    #  internal const int SE_PRIVILEGE_DISABLED = 0x00000000;
    #  internal const int TOKEN_QUERY = 0x00000008;
    #  internal const int TOKEN_ADJUST_PRIVILEGES = 0x00000020;
    #  public static bool EnablePrivilege(long processHandle, string privilege, bool disable)
    #  {
    #   bool retVal;
    #   TokPriv1Luid tp;
    #   IntPtr hproc = new IntPtr(processHandle);
    #   IntPtr htok = IntPtr.Zero;
    #   retVal = OpenProcessToken(hproc, TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, ref htok);
    #   tp.Count = 1;
    #   tp.Luid = 0;
    #   if(disable)
    #   {
    #    tp.Attr = SE_PRIVILEGE_DISABLED;
    #   }
    #   else
    #   {
    #    tp.Attr = SE_PRIVILEGE_ENABLED;
    #   }
    #   retVal = LookupPrivilegeValue(null, privilege, ref tp.Luid);
    #   retVal = AdjustTokenPrivileges(htok, false, ref tp, 0, IntPtr.Zero, IntPtr.Zero);
    #   return retVal;
    #  }
    # }
    #'@
    #
    # $processHandle = (Get-Process -id $ProcessId).Handle
    # $type = Add-Type $definition -PassThru
    # $type[0]::EnablePrivilege($processHandle, $Privilege, $Disable)
    #}


if __name__ == "__main__":
    main()

