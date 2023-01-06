### 13.12.2022 - Release 1.0
``PyTk Souces``: Development.
1. Created 4 Basic classes: ``Window`` and ``View``, ``Sprite`` and ``SpriteList``.
2. Created main ``run`` function, 4 ``draw`` functions, 2 ``hitbox`` functions and 1 ``misc`` function.

``PyTk Samples``: Development.
1. Created a simple sample App, using ``Window`` and ``Sprite`` classes, ``drawing`` and ``hitbox`` functions.


### 15.12.2022 - Release 1.1
``PyTk Sources``: Small fixes & refactors.

1. Removed ``setup`` method for ``Window`` and ``View`` classes.
2. Added ``offset`` attribute for the ``Window``. Experimental Feature. 


``PyTk Docs``: Development.
1. Created docs for PyTk library to provide basic understanding of the OOP and the library.
2. Created changelog file, to manage different versions of the library.


``PyTk Samples``: Minor Hotfix.
1. Removed ``setup`` for ``SampleWindow`` class, according to the sources changes.


### 22.12.2022 - Release 1.2
``PyTk Sources``: Update.
1. Removed Offset feature (useless)
2. Added resizing algorithms, according to the user's parameters and config info
3. Added division between Right and Left mouse clicks

``PyTk Docs``: Hotfix.
1. Removed offset information

``PyTk Samples``: Refactor.
1. Updated sample2.py according to new resizing feature
2. Removed sample.py (doesn't support the new version)
3. Added features from sample.py to sample2.py
4. Renamed sample2.py to sample.py


### 26.12.2022 - Beta 1.2ext
``PyTk Sources``: Small refactor.
1. Changed function ``run()`` to ``run_pytk()``

``PyTk Docs``: Small fix.
1. Small fix, according to the latest sources update.

``Pytk Extensions``: Development.
1. Created a separate directory for different extensions for PyTk library.
2. Created ``buttons.py`` with ``Button``, ``CheckBox`` and ``InputField`` templates.

``PyTk Samples``: Refactor & Update.
1. Moved all the samples to a separate directory.
2. Renamed ``sample.py`` to ``basic.py``
3. Created ``buttons.py`` to demonstrate how to use ``buttons`` extension.


### 29.12.2022 - Release 1.4
``PyTk Sources``: Major update & refactor.
1. Included config files to PyTk and updated all the necessary sources.
2. The library now can work without any extra files, fully automatically.

``PyTK Docs``: No changes.

``PyTk Extensions``: No changes.

``PyTk Samples``: No changes.

### 06.01.2023 - Release 1.5 final
``PyTk Sources``: Bug fix.
1. Minor bug fixes + refactor.

``PyTk Docs``: Update.
1. Added docs for buttons extension.

``PyTk Extensions``: Bug fix.
1. Minor bug fixes.
2. Removed ``action`` argument from ``Button`` class. Subclass instead.

``PyTk Samples``: Refactor.
1. Removed ``sub`` sample, due to extension update.
