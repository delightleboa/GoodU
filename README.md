# WyzePal bots

This directory contains the source code for the `wyzepal_bots` PyPI package.

The WyzePal documentation has guides on [using WyzePal's bot system](
https://chat.wyzepal.org/api/running-bots)
and [writing your own bots](
https://chat.wyzepal.org/api/writing-bots).

## Directory structure

```shell
wyzepal_bots  # This directory
├───wyzepal_bots  # `wyzepal_bots` package.
│   ├───bots/  # Actively maintained and tested bots.
│   ├───bots_unmaintained/  # Unmaintained, potentially broken bots.
│   ├───game_handler.py  # Handles game-related bots.
│   ├───lib.py  # Backbone of run.py
│   ├───provision.py  # Creates a development environment.
│   ├───run.py  # Used to run bots.
│   ├───simple_lib.py  # Used for terminal testing.
│   ├───test_lib.py  # Backbone for bot unit tests.
│   ├───test_run.py  # Unit tests for run.py
│   └───terminal.py  # Used to test bots in the command line.
└───setup.py  # Script for packaging.
```
