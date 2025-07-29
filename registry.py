# File paths to hives, etc.
WIN_CONFIG_PATH = "Windows/System32/config/"
SW_HIVE_PATH = "Windows/System32/config/SOFTWARE"
# "SAM", "SECURITY", "SYSTEM", "ELAM", "DRIVERS", "DEFAULT","COMPONENTS", "BBI"

SHARED_APPX_HIVE = "Microsoft\\Windows\\CurrentVersion\\Appx\\AppxAllUserStore\\Applications"


def load_registrey():
    pass
    # reg load HKLM\zCOMPONENTS $ScratchDisk\scratchdir\Windows\System32\config\COMPONENTS | Out-Null
    # reg load HKLM\zDEFAULT $ScratchDisk\scratchdir\Windows\System32\config\default | Out-Null
    # reg load HKLM\zNTUSER $ScratchDisk\scratchdir\Users\Default\ntuser.dat | Out-Null
    # reg load HKLM\zSOFTWARE $ScratchDisk\scratchdir\Windows\System32\config\SOFTWARE | Out-Null
    # reg load HKLM\zSYSTEM $ScratchDisk\scratchdir\Windows\System32\config\SYSTEM | Out-Null


def unload_registrey():
    pass
    # reg unload HKLM\zCOMPONENTS | Out-Null
    # reg unload HKLM\zDRIVERS | Out-Null
    # reg unload HKLM\zDEFAULT | Out-Null
    # reg unload HKLM\zNTUSER | Out-Null
    # reg unload HKLM\zSCHEMA | Out-Null
    # reg unload HKLM\zSOFTWARE
    # reg unload HKLM\zSYSTEM | Out-Null

