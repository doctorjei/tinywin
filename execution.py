import importlib

import registry import preprocess_entries, delete_keys, update_keys
from utils import get_identifier, delete_paths, copy_paths


def apply_changeset(changes, image, system_path):
    sys_apps = registry.get_provisioned(system_path) # TODO: move this into metadata? Always one list.

    # First, copy any critical files, then delete as necessary.
    if (path_pairs_to_copy := changes.get("copy_path")):
        copy_paths(system_path, path_pairs_to_copy)

    if (paths_to_delete := changes.get("delete_path")):
        delete_paths(system_path, paths_to_delete)

    # Handle registry changes AppX pacakges, key entry addition / update / removal)
    if "registry" in changes:
        # Make a list of keys to remove to get rid of (unprovision) the "bloatware"
        if (bloat := changes["registry"].get("unprovision"):
            targets = [pkg for pkg in sys_apps if "_" in pkg and pkg.split("_")[0] in bloat]
            bloat_keys =  [_PKG_KEYS_APPX + "\\" + bloater for bloater in targets]
            bloat_keys += [_PKG_KEYS_HKCU + "\\" + bloater for bloater in targets]
            bloat_keys += [_PKG_KEYS_HKLM + "\\" + bloater for bloater in targets]

        # Grab a list of keys to be removed; add the bloatware keys to that list.
        if (to_be_deleted := changes["registry"].get("delete")):
            to_be_deleted += bloat_keys
        # Get the list of updates / additions to make.
        if not (to_update := changes["registry"].get("update")):
	            to_update = []

        # Prepare the keys to be changed; opens hives and expands paths, etc.
        target_sets = { "update": to_update, "delete": to_be_deleted }
        hives, action_set = preprocess_entries(system_path, target_sets)

        # Output: { ("HIVENAME": OPENED_HIVE or None)* },
        #         { ("ACTIONTYPE": { ("HIVENAME": [KEY_PATH*]) })* }
        for hive_name, key_path in action_set["delete"]:
            pass
        #    hives[hive_name].open(
        #)

        for hive_name, key_path in action_set["update"]:
            pass

        # Unload / save hive once finished with keys.

    if (last_call := instructions.get("callable"):
        if len(last_call):
            last_call = last_call.decode() if type(last_call) is bytes else last_call
            call_pair = ["", last_call] if type(last_call) is str else last_call

            if len(call_pair) == 2:
                execute_special_function(*call_pair)
            else:
                logging.warn("Callable ({last_call}) should be a string or pair. Ignoring.")
        else:
            logging.warn("Empty callable special function entry; ignoring.")

    # TODO: what about "dependents"?...


def execute_special_function(call_module, call_name):
    if call_name:
        if call_module:
            try:
                call_module = importlib.import_module(call_module)
                if hasattr(call_module, call_name):
                    if not functor := my_module.__get_attribute__(call_name)):
                        call_module = ""
            except ImportError as e:
                print(f"Error loading '{call_module}' module; ignoring. [{e}]")
                call_module = ""

        if not call_module:
            functor = get_identifier(call_name)
    else:
        logging.warn("No call for special function; this should never happen! Ignoring.")
        return
    # If no valid callable object was found, warn and return.
    if not functor:
        logging.warn("Module and call [{call_module}, {call_name}] invalid. Ignoring.")
        return
    # Finally, call the successfully identified special function, then return.
    functor()
