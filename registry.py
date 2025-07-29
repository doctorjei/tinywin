import Registry

from utils import find_delimiters

# File paths to hives, etc.
_SYSTEM_HIVE_PATH = "Windows/System32/config/"
_COMMON_HIVES = ["COMPONENTS", "DEFAULT", "DRIVERS", "SOFTWARE", "SYSTEM" ]
_SECURITY_HIVES = ["ELAM", "SAM", "SECURITY"]
_UNCOMMON_HIVES = ["BBI", "BCD-Template", "userdiff", "VSMIDK"]
_SYSTEM_HIVES = _COMMON_HIVES + _SECURITY_HIVES + _UNCOMMON_HIVES

# Special registry paths
_PKG_PATH_HKCR = "Local Settings\\Software\\_$WinCurrent_\\\\AppModel\\Repository\\Packages"
_PKG_KEYS_APPX = "SOFTWARE\\_$WinCurrent_\\\\Appx\\AppxAllUserStore\\Applications"
_PKG_KEYS_HKCU = "NTUSER\\Software\\Classes\\" + PKG_PATH_HKCR
_PKG_KEYS_HKLM = "SOFTWARE\\Classes\\" + _PKG_PATH_HKCR

# Internal shortcuts (dictionary-based)
__hive_paths = {"": SYSTEM_HIVE_PATH, "NTUSER": "Users/Default/ntuser.dat" }
__hive_paths.update({hive: os.path.join(hive_paths[""], hive) for hive in _SYSTEM_HIVES}

# Registry path shortcut - map to a hive and/or key path. (No nested shortcuts!)
registry_shortcuts = {
    "_$WinCurrent_": "Microsoft\\Windows\\CurrentVersion\\",
    "_$WOW64Current_": "WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\"
}


def get_provisioned(system_path):
    hive_name, key_path = extract_path(_PKG_KEYS_APPX)
    sw_hive_path = os.path.join(system_path, __hive_paths[hive_name])
    hive = Registry.Registry(sw_hive_path)

    appx_key = hive.open(key_path)
    provisioned = [subkey.name() for subkey in appx_hive.subkeys()]
    hive.close()

    return provisioned


def delete_keys(hives, key_paths):
    for hive_name, paths in key_paths.items()):
        if not hives[hive_name]:
            # Load the hive into hives[hive_name]
            pass
        for key_path in path_list:
            # delete key_path from hives[hive_name]
            pass


def update_keys(hives, key_paths):
    for hive_name, paths in key_paths.items()):
        if not hives[hive_name]:
            # Load the hive into hives[hive_name]
            pass
        for key_path, value in path_list:
            # set storage at key_path to value in hives[hive_name]
            pass


def load():
    # reg load HKLM\zCOMPONENTS $ScratchDisk\scratchdir\Windows\System32\config\COMPONENTS | Out-Null
    # reg load HKLM\zDEFAULT $ScratchDisk\scratchdir\Windows\System32\config\default | Out-Null
    # reg load HKLM\zNTUSER $ScratchDisk\scratchdir\Users\Default\ntuser.dat | Out-Null
    # reg load HKLM\zSOFTWARE $ScratchDisk\scratchdir\Windows\System32\config\SOFTWARE | Out-Null
    # reg load HKLM\zSYSTEM $ScratchDisk\scratchdir\Windows\System32\config\SYSTEM | Out-Null


def unload():
    # reg unload HKLM\zCOMPONENTS | Out-Null
    # reg unload HKLM\zDRIVERS | Out-Null
    # reg unload HKLM\zDEFAULT | Out-Null
    # reg unload HKLM\zNTUSER | Out-Null
    # reg unload HKLM\zSCHEMA | Out-Null
    # reg unload HKLM\zSOFTWARE
    # reg unload HKLM\zSYSTEM | Out-Null
