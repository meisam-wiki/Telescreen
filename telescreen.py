"""
copyright: 2019 Meisam@wikimedia, MichaelSchoenitzer@wikimedia
This file is part of Telescreen: A slideshow script for the WikiMUC

    Telescreen is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Telescreen is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Telescreen. If not, see <https://www.gnu.org/licenses/>.
"""
import argparse
import logging
import sys
from pathlib import Path

from selenium import webdriver

import ci_tests
import configs
from slides import Slides

CLI_PARSER = argparse.ArgumentParser()
CLI_PARSER.add_argument(
    "-dir",
    help="directory of images",
    nargs="?",
    dest="working_directory",
    default=Path.cwd(),
)
CLI_PARSER.add_argument(
    "-w",
    "--wait",
    help="Waiting time between each slide update",
    type=int,
    dest="slides_refresh_time",
    default=30,
)
CLI_PARSER.add_argument(
    "--headless_test", action="store_true", help="Run the functionality tests"
)
ARGS = CLI_PARSER.parse_args()

configs.slides_refresh_time = ARGS.slides_refresh_time
configs.working_directory = Path(ARGS.working_directory)


if ARGS.headless_test:
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    logging.getLogger("").addHandler(console)
    return_code = 0
    return_code += ci_tests.test_list()
    return_code += ci_tests.test_cache_renewal()
    return_code += ci_tests.test_errors()
    sys.exit(return_code)

SLIDESHOW = Slides()
SLIDESHOW.browser = webdriver.Firefox()
SLIDESHOW.browser.fullscreen_window()

while True:
    SLIDESHOW.update_slides()
    SLIDESHOW.play()
