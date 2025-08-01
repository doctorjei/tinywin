#!/usr/bin/env python3
import argparse
import configparser
import logging
import os
import sys
import saneyaml

from configparser import DEFAULTSECT as _ROOT_
#import configparser.UNNAMED_SECTION as _ROOT_


DEFAULT_LOG_FILE = "./tiny.log"
DEFAULT_CONFIG_FILE = "./tiny11.ini"
DEFAULT_CHANGESETS = "./changesets.yml"

DEFAULT_CONFIG = {_ROOT_ : {}}

#DEFAULT_CONFIG = {_ROOT_ : {'logfile': './tiny11.log'}}

LOG_FORMATS = { logging.INFO:     "%(message)s",
                logging.DEBUG:    "%(levelname)s: %(message)s",
                logging.WARNING:  "%(levelname)s: %(message)s",
                logging.ERROR:    "***%(levelname)s***: %(message)s",
                logging.CRITICAL: "***%(levelname)s***: %(message)s" }


# Customize log messages by level.
class __CustomFormatter(logging.Formatter):
    def __init__(self, handler_list):
        self.refresh_handlers(handler_list)
        super().__init__()

    def refresh_handlers(self, handler_list):
        for handler in handler_list:
            handler = handler() if callable else handler
            handler.setFormatter(self)

    def format(self, record):
        og_fmt = self._fmt
        self._fmt = LOG_FORMATS[record.levelno]
        result = logging.Formatter.format(self, record)
        self._fmt = og_fmt
        return result


def parse_arguments():
    err_map = {"FATAL": logging.FATAL, "ERROR": logging.ERROR,
               "WARN": logging.WARN, "INFO": logging.INFO, "DEBUG": logging.DEBUG}

    desc =  'Program to build a tiny11 image'
    last = ('Error Severity (log indicated level & up):\n'
            '  FATAL     Only log critical / fatal errors     [Highest]\n'
            '  ERROR     Only log errors (no warnings)\n'
            '  WARN      Log warnings and errors\n'
            '  INFO      Log general info messages            [Default]\n'
            '  DEBUG     Include debugging information        [Lowest]')

    formatter = lambda prog: argparse.RawTextHelpFormatter(prog,width=80,max_help_position=45)
    parser = argparse.ArgumentParser(description=desc, epilog=last, formatter_class=formatter)

    parser.add_help = True
    parser.add_argument('media_path', nargs='?', default=None, help='installation media path')
    parser.add_argument('build_path', nargs='?', default=None, help='temporary (build) path')
    parser.add_argument('-y', '--yes', action='store_true', help='overwrite existing data')
    parser.add_argument('--run_conf', default=None, help='runtime configuration file')
    parser.add_argument('--changesets', default=DEFAULT_CHANGES, help='changesets file (YAML)')
    parser.add_argument('--log_level', choices=err_map.keys(), help="set logging level")
    parser.add_argument('--log_file', default='', nargs='?', help='log to file')
    rt = parser.parse_args(sys.argv[1:])

    # Simplify the config file information before returning.
    rt.log_level = err_map[rt.log_level.upper()] if rt.log_level else logging.INFO
    rt.log_file = DEFAULT_LOG_FILE if rt.log_file == None else rt.log_file
    return rt


def initialize():
    # Parse the runtime configuration (command line) and set up logging.
    runtime = parse_arguments()
    logging.basicConfig(level=runtime.log_level)
    formatter = __CustomFormatter(logging._handlerList)
    config = None

    # If there's a config file provided, open and parse it.
    if not runtime.run_conf and os.path.isfile(DEFAULT_CONFIG_FILE):
        runtime.run_conf = DEFAULT_CONFIG_FILE

    if runtime.run_conf:
        try:
            logging.info(f"Loading config file: [{runtime.run_conf}]")
            with open(runtime.run_conf, "r") as conf_file:
#            conf_file = open(runtime.conf_file, "r")
                config = configparser.ConfigParser()
                config.read(conf_file)

        # If there's an error, log it, then load the default config.
        except Exception as e: # TODO: Remove? We have "with" now...
            logging.warning(f"Couldn't read config file: [{type(e).__name__}]")
            config = None


    # If we didn't get the configuration from the file, start from defaults.
    if not config:
        config = configparser.ConfigParser()
        config.read_dict({sec: pairs for sec, pairs in DEFAULT_CONFIG.items()})

    # Make sure the config has no missing sections
    for key, value in DEFAULT_CONFIG.items():
        if key != _ROOT_ and not config.has_section(key):
            config.add_section(key)

    # Ensure values for all 'root' elements (using defaults as necessary)
    for key, value in config[_ROOT_].items():
        if runtime.__getattribute__(key):
            config[_ROOT_][key] = runtime.__getattribute__(key)
        elif not config[_ROOT_][key]:
            config[_ROOT_][key] = DEFAULT_CONFIG[_ROOT_][key]
            runtime.__setattr__(config[_ROOT_][key])

    # If a log filename was provided, start the file-based logging.
    if runtime.log_file:
        logging.info(f"Log file: [{runtime.log_file}]")
        logging.basicConfig(filename=runtime.log_file, level=runtime.log_level)
        formatter.refresh_handlers(logging._handlerList) # Reprocess handlers.

    if runtime.changesets:
        with open(runtime.run_conf, "r") as changes_file:
            runtime.changesets = saneyaml.load(changes_file.read())
    else:
        logging.warn("Warning: no changesets detected. This will result in no image changes.")

    return runtime, config
