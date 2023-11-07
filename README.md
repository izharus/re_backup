# Re_backup Module

The Re_backup module is designed to help you ensure the safety of your backups in case the disk storing them becomes corrupted or fails. It provides a convenient way to copy and manage backup files, keeping them synchronized between two locations.

## Main Purpose

The main purpose of the Re_backup module is to offer a solution for safeguarding your backups by continuously monitoring and copying files from a source directory to a destination directory without overwriting existing files. It also removes any files in the destination directory that are no longer present in the source directory.

## Features

- Continuous synchronization: Re_backup continuously checks the source directory for new files and copies them to the destination directory without replacing existing files.

- Automatic removal: Files in the destination directory that no longer exist in the source directory are automatically removed to maintain consistency.

- Customizable time intervals: You can specify the time interval for checking and copying files, allowing you to balance synchronization frequency and resource usage.

- Audio alert on errors: Re_backup includes an audio alert feature to notify you in case of errors during the backup process, ensuring prompt attention to any issues.


## Usage

To use the Re_backup module, follow these simple steps:

1. Import the module: `from Re_backup import make_re_backup`.

2. Call the `make_re_backup` function, passing the desired time interval in minutes as an argument. This function will continuously monitor and synchronize the source and destination directories.

```python
from Re_backup import make_re_backup

# Set the desired time interval in minutes (e.g., 60 minutes)
make_re_backup(time_interval_minutes=60)
```

## Getting Started
1. Ensure you have the required dependencies installed, including Python and any additional libraries your project depends on.

2. Configure the SRC_DIRECTORY and DIST_DIRECTORY variables in the backuper.py module to specify the source and destination directories for your backups.

3. Import the make_re_backup function and call it with your desired time interval to start the synchronization process.

## License
This project is licensed under the Apache License, Version 2.0 - see the LICENSE file for details.

## Contact
For any questions or feedback, feel free to contact me at ruslan.izhakovskij@gmail.com.