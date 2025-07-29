import logging
import os
import os.path
import shutil


# Quick and dirty lambda to loop until the input starts with upper or lower "y" or "n"
YN_CHECK = lambda r: None if not len(r) or (r.upper()[0] != 'Y' and r.upper()[0] != 'N') else r[0]


# Loop on a prompt until the validator returns a non-None result; then, return that result.
def validated_input(prompt, error_msg, validator):
    result = input(prompt)
    while not (result := validator(result)):
        print(error_msg)
        result = input(prompt)
    return result


# Log a fatal error and terminate.
def terminate(msg="Unspecificed fatal error."):
    logging.fatal(msg)
    exit()


# Get a variable's value from the Pyhton VM.
def get_identifier(name):
    try:
        return locals()[name]
    except:
        pass
    try:
        return globals()[name]
    except:
        return None


def delete_paths(base, paths_to_remove):
    for target_path in paths_to_remove:
        # Take ownership and remove the path completely.
        full_path = os.path.join(base, target_path)


def copy_paths(base, copy_pairs):
    for src, dest in copy_pairs:
        src = os.path.abspath(src) if not os.path.isabs(src) else src
        dest = os.path.join(base, dest) if not os.path.isabs(dest) else dest
        shutil.copytree(src, dest)
