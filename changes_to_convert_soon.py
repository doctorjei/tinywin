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
'Clipchamp.Clipchamp',                42M
'Microsoft.549981C3F5F10',            2M
'Microsoft.BingNews',                30M
'Microsoft.BingSearch',                0.4M
'Microsoft.BingWeather',            0.6M
'Microsoft.GamingApp',                360M
'Microsoft.GetHelp',                244M
'Microsoft.Getstarted',                23M
'Microsoft.MicrosoftOfficeHub',            1M
'Microsoft.MicrosoftSolitaireCollection',    68M
'Microsoft.People',                25M
'Microsoft.PowerAutomateDesktop',        2M
'Microsoft.Todos',                1.2M
'Microsoft.WindowsAlarms',            23M
'Microsoft.windowscommunicationsapps',        211M
'Microsoft.WindowsFeedbackHub',            41M
'Microsoft.WindowsMaps',            45M
'Microsoft.WindowsSoundRecorder',        2M
'Microsoft.Xbox.TCUI',                12M
'Microsoft.XboxGamingOverlay',            26M
'Microsoft.XboxGameOverlay',                    3M
'Microsoft.XboxSpeechToTextOverlay',            1M
'Microsoft.YourPhone',                          2M
'Microsoft.ZuneMusic',                          36M
'Microsoft.ZuneVideo',                          35M
'MicrosoftCorporationII.MicrosoftFamily',       ????
'MicrosoftCorporationII.QuickAssist_',          5M
'MicrosoftTeams'                                300M?

Other possible targets for removal:

Microsoft.Windows.Photos_24.24010.29003.0_neutral_~_8wekyb3d8bbwe        **    523M
Microsoft.Paint_11.2302.20.0_neutral_~_8wekyb3d8bbwe                **    417M
MSTeams_1.0.0.0_x64__8wekyb3d8bbwe                        **    300M
Microsoft.ScreenSketch_2022.2307.52.0_neutral_~_8wekyb3d8bbwe            **    212M
MicrosoftWindows.Client.WebExperience_424.1301.270.9_neutral_~_cw5n1h2txyewy    **    167M
MicrosoftWindows.CrossDevice_1.23101.22.0_neutral_~_cw5n1h2txyewy        **    92M
#Microsoft.WindowsStore_22401.1400.6.0_neutral_~_8wekyb3d8bbwe            **    80M
Microsoft.StorePurchaseApp_22312.1400.6.0_neutral_~_8wekyb3d8bbwe        **    47M
Microsoft.OutlookForWindows_1.0.0.0_neutral__8wekyb3d8bbwe            **    45M
Microsoft.SecHealthUI_1000.26100.1.0_x64__8wekyb3d8bbwe                **    24M
Microsoft.WindowsAlarms_2022.2312.2.0_neutral_~_8wekyb3d8bbwe            **    23M
Microsoft.WindowsCamera_2022.2312.3.0_neutral_~_8wekyb3d8bbwe            **    22M
Microsoft.WindowsNotepad_11.2312.18.0_neutral_~_8wekyb3d8bbwe            **    20M
Microsoft.WindowsCalculator_2021.2311.0.0_neutral_~_8wekyb3d8bbwe        **    17M
Microsoft.XboxIdentityProvider_12.110.15002.0_neutral_~_8wekyb3d8bbwe        **    11M
Microsoft.MicrosoftStickyNotes_4.6.2.0_neutral_~_8wekyb3d8bbwe            **    2M
Microsoft.Windows.DevHome_0.100.128.0_neutral_~_8wekyb3d8bbwe *************    **    2M

--- KEEP THESE ---
Microsoft.WindowsTerminal_3001.18.10301.0_neutral_~_8wekyb3d8bbwe        X    19M
Microsoft.HEIFImageExtension_1.0.63001.0_neutral_~_8wekyb3d8bbwe        ??    14M
Microsoft.VP9VideoExtensions_1.1.451.0_neutral_~_8wekyb3d8bbwe            ??    7M
Microsoft.HEVCVideoExtension_2.0.61931.0_neutral_~_8wekyb3d8bbwe        ??    6M
Microsoft.AV1VideoExtension_1.1.61781.0_neutral_~_8wekyb3d8bbwe            ??    5M
Microsoft.AVCEncoderVideoExtension_1.0.271.0_neutral_~_8wekyb3d8bbwe        ??    4M
Microsoft.RawImageExtension_2.3.171.0_neutral_~_8wekyb3d8bbwe            ??    3.3M
Microsoft.ApplicationCompatibilityEnhancements_1.2401.10.0_neutral_~_8wekyb3d8bbwe ??    3M
Microsoft.MPEG2VideoExtension_1.0.61931.0_neutral_~_8wekyb3d8bbwe        --    3M
Microsoft.WebMediaExtensions_1.0.62931.0_neutral_~_8wekyb3d8bbwe        --    2.9M
Microsoft.WebpImageExtension_1.0.62681.0_neutral_~_8wekyb3d8bbwe        --    1.6M

Others from recent updates:
Microsoft.Copilot_                190M
Microsoft.DesktopAppInstaller_            138M
Microsoft.Ink.Handwriting.en-US.1.0_        9M
Microsoft.Microsoft3DViewer_            58M
Microsoft.OfficePushNotificationUtility_    0.1M
Microsoft.OneDriveSync_                0.1M
Microsoft.PowerToys.FileLocksmithContextMenu_     ?
Microsoft.PowerToys.ImageResizerContextMenu_      ?
Microsoft.PowerToys.PowerRenameContextMenu_       ?
Microsoft.Services.Store.Engagement_              ?
Microsoft.Teams.TxNdi_                ?
Microsoft.UI.Xaml.2.7_7.2208.15002.0_        ?
Microsoft.WidgetsPlatformRuntime_        ?
MicrosoftWindows.Speech.ja-JP.1            ?
MicrosoftWindows.Voice.ja-JP.Nanami.1_        ?
MicrosoftWindows.WindowsSandbox_        ??
"""


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

