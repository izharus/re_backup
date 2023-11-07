"""
audio_alerts.py - A module for managing notifications and playing notification
sounds.

This module provides the `NotificationController` class, which enables the
management of notifications and the playback of notification sounds. The
class can use default success, error, and warning notifications or
user-defined notifications if they exist.

External Dependencies:
    - pygame.mixer: A library for working with audio in pygame.
    - pyttsx3: A text-to-speech conversion library.

Classes:
    NotificationController:
        A class for managing notifications and playing notification sounds.

Usage:
    import audio_alerts

    # Create a NotificationController instance with default sound paths and
    # a logging object
    notification_controller = audio_alerts.NotificationController(
        default_success_sound_path='path/to/default_success_sound.wav',
        default_error_sound_path='path/to/default_error_sound.wav',
        default_warning_sound_path='path/to/default_warning_sound.wav',
        log=my_logging_object
    )

    # Play a success notification sound
    notification_controller.alert_success()

    # Play an error notification sound
    notification_controller.alert_error()

    # Play a custom notification sound (if it exists) or the default one
    notification_controller.alert_sound(
        'path/to/custom_notification_sound.wav')
"""


import os
import threading
import time
from typing import Any

import pygame.mixer
import pyttsx3


class NotificationController:
    """
    A class for managing notifications and playing notification sounds.
    Can use default success/error/warning notifications or user-defined
    notificationsif they exist.

    Args:
        default_success_sound_path (str): The path to the default success
            notification sound file.
        default_error_sound_path (str): The path to the default error
            notification sound file.
        default_warning_sound_path (str): The path to the default warning
            notification sound file.
        log (Any): The logging object used for writing log messages.

    Attributes:
        custom_success_sound_path (str): The basename of the user-defined
            success notification sound file.
        custom_warning_sound_path (str): The basename of the user-defined
            warning notification sound file.
        custom_error_sound_path (str): The basename of the user-defined
            error notification sound file.
        default_success_sound_path (str): The path to the default success
            notification sound file.
        default_warning_sound_path (str): The path to the default warning
            notification sound file.
        default_error_sound_path (str): The path to the default error
            notification sound file.
        log (Any): The logging object used for writing log messages.

    Methods:
        alert_msg(message: str) -> None:
            Play a notification message.

        alert_sound(sound_file_path: str) -> bool:
            Play a notification sound.

        alert_success() -> None:
            Play a success notification sound.

        alert_warning() -> None:
            Play a warning notification sound.

        alert_error() -> None:
            Play an error notification sound.
    """

    def __init__(
        self,
        default_success_sound_path: str,
        default_error_sound_path: str,
        default_warning_sound_path: str,
        log: Any,
    ):
        """
        Initialize the NotificationController instance.

        Args:
            default_success_sound_path (str): The path to the default success
                notification file.
            default_error_sound_path (str): The path to the default error
                notification file.
            default_warning_sound_path (str): The path to the default warning
                notification file.
            log (Any): The logging object used for writing log messages.

        Returns:
            None
        """
        self.custom_success_sound_path = os.path.basename(
            default_success_sound_path
        )
        self.custom_warning_sound_path = os.path.basename(
            default_warning_sound_path
        )
        self.custom_error_sound_path = os.path.basename(
            default_error_sound_path
        )

        # Construct the full paths to the default notification files
        self.default_success_sound_path = default_success_sound_path
        self.default_error_sound_path = default_error_sound_path
        self.default_warning_sound_path = default_warning_sound_path
        self.log = log

    def alert_msg(self, message: str) -> None:
        """
        Play a notification message.

        Args:
            message (str): The notification message to play.

        Returns:
            None
        """
        engine = pyttsx3.init()
        engine.say(message)
        engine.runAndWait()

    def alert_sound(self, sound_file_path: str) -> bool:
        """
        Play a notification sound.

        Args:
            sound_file_path (str): Path to the notification sound file.

        Returns:
            bool: True if the sound played successfully, False otherwise.
        """

        try:
            # Initialize pygame audio
            pygame.mixer.init()

            pygame.mixer.music.load(sound_file_path)
            pygame.mixer.music.play()

            # Wait until the music finishes playing
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            pygame.mixer.music.stop()
            pygame.mixer.quit()

            return True
        except Exception:
            # self.log.write_log(
            # f" ERROR Не найден файл уведомления {sound_file_path}")
            return False

    def _alert_success(self) -> bool:
        """
        Play a custom success notification sound if it exists or
        the default one.

        Returns:
            bool: True if the sound played successfully, False otherwise.
        """
        if not self.alert_sound(self.custom_success_sound_path):
            return self.alert_sound(self.default_success_sound_path)
        return True

    def alert_success(self) -> None:
        """
        Play a success notification sound in a separate thread.
        Play a custom success notification sound if it exists or the
        default one.
        """
        threading.Thread(target=self._alert_success).start()
        time.sleep(1)

    def alert_warning(self) -> None:
        """
        Play a warning notification sound in a separate thread.
        Play a custom warning notification sound if it exists or
        the default one.
        """
        threading.Thread(target=self._alert_warning).start()
        time.sleep(1)

    def _alert_warning(self) -> None:
        """
        Play a custom warning notification sound if it exists or
        the default one.
        """
        if not self.alert_sound(self.custom_warning_sound_path):
            self.alert_sound(self.default_warning_sound_path)

    def _alert_error(self) -> bool:
        """
        Play a custom error notification sound if it exists or the default one.

        Returns:
            bool: True if the sound played successfully, False otherwise.
        """
        if not self.alert_sound(self.custom_error_sound_path):
            return self.alert_sound(self.default_error_sound_path)
        return True

    def alert_error(self) -> None:
        """
        Play an error notification sound in a separate thread.
        Play a custom error notification sound if it exists or the default one.
        """
        threading.Thread(target=self._alert_error).start()
        time.sleep(1)
