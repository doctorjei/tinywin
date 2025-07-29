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


# Reads and pre-processes registry data; returns open hives & hive:list(key_path) dictionary.
# Input: target_sets = { ( "TYPE" : [TARGET_SHORTCUT_PATH*] )* }
# Output: { ("HIVENAME": OPENED_HIVE or None)* },
#         { ("ACTIONTYPE": { ("HIVENAME": [KEY_PATH*]) })* }
def preprocess_entries(system_path, target_sets, open_hives=True):
    hives = dict() # Dictionary mapping name to open registry hive
    action_set = dict()

    for type, target_list in target_sets.items():
        key_paths = dict() # List of paths

        # Expand paths and get clear list of the hives to open
        for hive_name, key_path in (extract_path(entry) for entry in targets):
            key_paths[hive_name] = (key_paths.get(hive_name) or []) + [key_path]

        # Open hives as necessary (or create a placeholder otherwise).
        for hive_name in key_paths.keys():
            if not hive_name in hives: # Only open the hive if it isn't open yet
                hive_path = __hive_paths[hive_name] # TODO: Need mount path. Object? Passing?
                hives[hive_name] = "Foo" if open_hives else None # TODO: Open the hive file if needed

        # Add the set of key paths to the action type (e.g., "add", "delete", etc.
        action_set[type] = key_paths

    return hives, action_set


def extract_path(original_path):
    # If this operation as two operators (key and value), make sure to extract them.
    if type(original_path) is list and len(original_path) == 2:
        original_path, value = original_path
    else:
        value = None

    # First, get the locations of the delimiters.
    split_indices = find_delimiters(original_path, '\\\\')
    search_start = 0
    new_path = ""

    for split_index in split_indices:
        pivot = original_path[search_start:split_index].rfind('\\') + 1 # Find shortcut start.
        head = original_path[search_start:pivot] # Pre-shortcut head.
        identifier = original_path[pivot:split_index] # Shortcut identifier.

        new_path += head + (registry_shortcuts.get(identifier) or "")
        search_start = split_index + 2 # Move search start to prep for next iteration.

    # Add any remaining path sections to the new path (the "tail") and return.
    new_path += original_path[search_start:]

    if new_path.find('\\') == -1:
        hive, key_path = new_path, None
    else:
        hive, key_path = new_path.split('\\', 1)

    return hive, (key_path, valye if value else key_path) # Add the value back if needed.


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
