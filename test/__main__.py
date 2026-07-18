import os
import sys
import argparse
import traceback
import importlib.util

from typing import Literal
from datetime import datetime

from colorama import Fore, Style, init
from dotenv import load_dotenv

cur_dir = os.path.dirname(__file__)
project_root = os.path.dirname(cur_dir)
sys.path.insert(0, project_root)

test_dir = os.path.join(cur_dir, "units")

init()

load_dotenv()

class TestFunc:
    def __init__(self):
        self.test_functions = []
    
    def unit(self, func):
        self.test_functions.append(func)
    
    def run_units(self):
        test_errors = []
        success_count = 0

        for func in self.test_functions:
            try:
                result = func()
                if type(result) is str:
                    test_errors.append((func.__name__, result))
                    continue
                
                success_count += 1
            except Exception:
                test_errors.append((func.__name__, traceback.format_exc()))

        return (success_count, test_errors)

class TestModule:
    def __init__(self, name: str):
        self.name = name
        self.file = os.path.join(test_dir, f"{name}.py")
        self.module = None

        self.test = TestFunc()

        if not os.path.exists(self.file):
            return
        
        load_dotenv()

        spec = importlib.util.spec_from_file_location(
            name,
            self.file
        )
        self.module = importlib.util.module_from_spec(spec)
        self.module.test = self.test
        time_format = (
            f"{Style.DIM}{Fore.WHITE}%Y-%m-%d{Style.RESET_ALL} "
            f"{Style.BRIGHT}{Fore.CYAN}%H{Fore.RESET}:"
            f"{Fore.CYAN}%M{Fore.RESET}:"
            f"{Fore.CYAN}%S{Fore.RESET}{Style.RESET_ALL}"
        )

        create_prefix = lambda timestamp, level, color: (
            f"{Fore.WHITE}[ {timestamp}{Fore.WHITE}  {name.ljust(12)} {Fore.WHITE}| "
            f"{color}{level}{Fore.WHITE} >{Fore.RESET}"
        )
        def new_print(*values: object,
                        sep: str | None = " ",
                        end: str | None = "\n",
                        file = None,
                        flush: Literal[False] = False):
            timestamp = datetime.now().strftime(time_format)
            prefix = create_prefix(timestamp, "INFO", Fore.LIGHTGREEN_EX)
            print(prefix, *values, f"{Fore.RESET}", sep=sep, end=end, file=file, flush=flush)
        
        def warn(*values: object,
                        sep: str | None = " ",
                        end: str | None = "\n",
                        file = None,
                        flush: Literal[False] = False):
            timestamp = datetime.now().strftime(time_format)
            prefix = create_prefix(timestamp, "WARNING", Fore.LIGHTYELLOW_EX)
            print(prefix, *values, f"{Fore.RESET}", sep=sep, end=end, file=file, flush=flush)

        self.module.print = new_print
        self.module.warn = warn
        spec.loader.exec_module(self.module)
    
    def run(self):
        success_count, errors = self.test.run_units()

        for name, stack in errors:
            print(f"[{Fore.RED}!{Style.RESET_ALL}] {self.name}.{name} failed:")
            print(Style.BRIGHT + Fore.RED + stack + Style.RESET_ALL)

        return (success_count, errors)

def list_units():
    return [dir[:-3] for dir in os.listdir(test_dir) if dir[-3:] == ".py"]

def run_unit(name: str):
    module = TestModule(name)
    if not module.module:
        return (0, [])

    return module.run()


parser = argparse.ArgumentParser(
    prog="test",
    description="Run tests for the api",
)

parser.add_argument("unit", nargs="?", choices=list_units(), default=None,
                    help="Specific unit to run. Leave empty to run all units.")

args = parser.parse_args()

init()

units_to_run = [args.unit] if args.unit else list_units()

total_success = 0
total_errors = []

for unit in units_to_run:
    success_count, errors = run_unit(unit)
    total_success += success_count
    total_errors += errors

plural = lambda norm, alt, count: f"{norm if count == 1 else alt}"

print(f"Finished with {Fore.GREEN}{total_success}{Style.RESET_ALL} successful {plural('unit', 'units', total_success)}, and {Fore.RED}{len(total_errors)}{Style.RESET_ALL} {plural('unit ending in a error', 'units ending in errors', len(total_errors))}.")

sys.exit(1 if total_errors else 0)