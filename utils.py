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


def delete_filesets(base, paths_to_remove):
    for target_path in paths_to_remove:
        full_path = os.path.join(base, target_path)
        # Take ownership and remove the path completely.
