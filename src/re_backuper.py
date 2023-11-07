# Copyright 2023 izharus
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Continuous backup and synchronization script.
"""
import os
import shutil
import time
import traceback

from log_wizard import DefaultConfig, log

from .utillity.audio_alerts import NotificationController

DefaultConfig(log_dir="logs")
log = log()


SRC_DIRECTORY = "..\\..\\backups"
DIST_DIRECTORY = "A:\\minecraft_servers\\server_tfc_halloween\\backup"


def make_re_backup(timeaut_minutes: int) -> None:
    """
    Continuously copy new files from the source directory to the destination
    directory without replacing existing files, and remove files from the
    destination directory that no longer exist in the source directory.

    Args:
        timeaut_minutes (int): The time interval in minutes for checking and
            copying files.

    Returns:
        None

    This function monitors the source directory for new files and copies
    them to the destination directory without overwriting existing files.
    It also removes files from the destination directory that no longer
    exist in the source directory.

    An audio alert is triggered in case of errors during the backup process.

    Args:
        - timeaut_minutes (int): The time interval in minutes for checking and
          copying files.

    Example:
    ```python
    from backuper import make_re_backup

    # Set the desired time interval in minutes (e.g., 60 minutes)
    make_re_backup(time_interval_minutes=60)
    ```
    """
    audio_alert_path = "data/bad.mp3"
    audio_alert = NotificationController(
        audio_alert_path,
        audio_alert_path,
        audio_alert_path,
        log,
    )
    while True:
        # Make dist dir if it not exist
        if not os.path.exists(DIST_DIRECTORY):
            os.makedirs(DIST_DIRECTORY)

        # Get a files set form src and dist dirs
        src_files = set(os.listdir(SRC_DIRECTORY))
        dist_files = set(os.listdir(DIST_DIRECTORY))

        was_error = False
        # Копируем файлы из src в dist без замены
        for file in src_files:
            src_path = os.path.join(SRC_DIRECTORY, file)
            dist_path = os.path.join(DIST_DIRECTORY, file)
            if file not in dist_files:
                log.info(f"Copying file: {file}...")
                try:
                    shutil.copy(src_path, dist_path)
                except Exception as error:
                    log.error(f"Failed to copy file: {file}, {error}")
                    log.debug(traceback.format_exc())
                    was_error = True
            log.info(f"File skipped: {file}...")

        # Удаляем файлы из dist, которых нет в src
        for file in dist_files:
            dist_path = os.path.join(DIST_DIRECTORY, file)
            if file not in src_files:
                log.info(f"Removing old file: {file}...")
                try:
                    os.remove(dist_path)
                except Exception as error:
                    log.error(f"Failed to remove file: {file}, {error}")
                    log.debug(traceback.format_exc())
                    was_error = True
        if was_error:
            # Errors was
            audio_alert.alert_error()
            audio_alert.alert_msg("backup error")
        time.sleep(timeaut_minutes * 60)
