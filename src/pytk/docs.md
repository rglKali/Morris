# PyTk Docs

PyTk is a package created by rglKali on top of the fltk library 
to turn it into an OOP library. 
PyTk package provides 4 classes and several functions.
PyTk library basic class do not require any attributes, 
they take all the attributes from the config file, 
but you still can initialize them, if you want.

In the ``Attributes`` of the classes and ``Arguments`` of the functions you may see
different types of variables and different states: ``required``, ``optional`` and ``default``.

>``required`` means, that if you will not pass it, the library will raise an Error.

>``optional`` means, that if you will not pass it, the library will auto-generate it, if necessary.

>``default`` means, that if you will not pass it, the library will take the default option from the config file.

>

## Class Window.

That's the basic class, which provides you the basic window (subclass of fltk's CustomCanvas) to draw some sprites.

### ~Attributes~

#### width (required, default) ``int``
Represents the width of the window.

#### height (required, default) ``int``
Represents the height of the window.

#### fullscreen (required, default) ``bool``
``True``, if window is in fullscreen mode and ``False``, if not.

#### view (optional) ``View``
Represents the current window View, if any.

### ~Methods~

#### on_update(delta_time: float) -> None
Called automatically each frame. Should contain all the window update processes.
``delta_time`` is time, passed from the previous update.

#### on_draw() -> None
Called automatically each frame. Should contain all the window drawing processes.

#### on_key_press(key: str) -> None
Called automatically, when the user presses some button. Should contain the key's events logic.
``key`` is the key, that user pressed.

#### on_mouse_press(x: int, y: int) -> None
Called automatically, when the user clicks. Should contain the mouse events logic.
``x`` and ``y`` are the coordinates of the mouse, when user clicked.

#### quit() -> None
Called once, when you need to close the window.

>

## class View

Aka-subclass of the Window class. 
You can use it to define different game views for your project (Menu, Settings, Pause, etc..).
Does not contain all the attributes of the basic window, but includes all the methods.

### ~Attributes~

#### window (default) ``Window``
Automatically catches the current window, and creates a reference to it

### ~Methods~

#### on_update(delta_time: float) -> None
Called automatically each frame. Should contain all the window update processes.
``delta_time`` is time, passed from the previous update.

#### on_draw() -> None
Called automatically each frame. Should contain all the window drawing processes.

#### on_key_press(key: str) -> None
Called automatically, when the user presses some button. Should contain the key's events logic.
``key`` is the key, that user pressed.


#### on_mouse_press(x: int, y: int) -> None
Called automatically, when the user clicks. Should contain the mouse events logic.
``x`` and ``y`` are the coordinates of the mouse, when user clicked.

>

## class Sprite

Basic sprite object. 
Requires you to work with objects in a more comfortable way.

### ~Attributes~

#### window (default) ``Window``
Automatically catches the current window, and creates a reference to it

#### x (required) ``int``
Represents the ``x`` coordinate of the sprite in the ``Window``.

#### y (required) ``int``
Represents the ``y`` coordinate of the sprite in the ``Window``.

#### hitbox (optional) ``list[tuple[int, int]]``
Represents the ``Sprite``'s hitbox, according to it's ``x`` and ``y`` coordinates
If not provided, will be created automatically and will contain only 1 pixel: ``Sprites``'s ``x`` and ``y`` coordinates.

### ~Methods~

#### update() -> None
Called manually (usually during ``Window``'s or ``View``'s ``on_update`` or using ``SpriteList``'s ``update`` method). 
Should contain all the sprite update process.

#### draw() -> None
Called manually (usually during ``Window``'s or ``View``'s ``on_update`` or using ``SpriteList``'s ``update`` methods). 
Should contain all the sprite drawing process.

#### collides_with_point(x: int, y: int) -> bool
Called manually (usually, using ``Window``'s or ``View``'s ``on_mouse_press`` methods)
Returns ``True``, if the sprite's hitbox contains point (``x`` and ``y``) and ``False`` if not.

>

## Class SpriteList

The basic list to contain your sprites. Not requires subclassing. 
That's basically a subclass of a Python's ``list`` object, so it also supports all the ``list``'s methods. 

### ~Methods~

#### update() -> None
Called manually (usually during ``Window``'s or ``View``'s ``on_update`` methods). 
Draws all containing sprites.

#### draw() -> None
Called manually (usually during ``Window``'s or ``View``'s ``on_update`` methods). 
Updates all containing sprites.

>

### class palette
A palette, containing recommended colors to use with PyTk

>

## function run_pytk() -> None
The heart of the PyTk library, runs the main process.
Requires a ``Window``, created before calling this function.
Note, that this function starts the ``while True`` cycle, and 
the code, written above it will execute only when the window will be closed

>

## function hitbox_circle() -> list[tuple(int, int)]
Creates the circle hitbox.
Usually is used for dynamic ``Sprite``s with circle texture (Points, etc..).

### ~Arguments~

#### radius (required) ``int``
The radius of the current hitbox.


## function hitbox-rect() -> list[tuple(int, int)]
Creates the rectangular hitbox.
Usually is used for dynamic ``Sprite``s with rectangular texture (Buttons, etc..).

### ~Arguments~

#### width (required) ``int``
The width of the current hitbox.

#### height (required) ``int``
The height of the current hitbox.

>

## function draw_line() -> None
Draws the line.
Usually is used in ``on_draw`` method of a ``Window`` or a ``View``, sometimes in the ``draw`` method of the ``Sprite``

### ~Arguments~

#### ax (required) ``int``
The ``x`` coordinate of the start of the line.

#### ay (required) ``int``
The ``y`` coordinate of the start of the line.

#### bx (required) ``int``
The ``x`` coordinate of the end of the line.

#### by (required) ``int``
The ``y`` coordinate of the end of the line.

#### color (required, default) ``str``
The color of the line.
By default, it's the ``black`` from the palette.

#### thickness (required, default) ``int``
The thickness (width) of the line.


## function draw_circle() -> None
Draws the circle.

### ~Arguments~

#### x (required) ``int``
The ``x`` coordinate of the circle's center.

#### y (required) ``int``
The ``y`` coordinate of the circle's center.

#### radius (required) ``int``
The radius of the current circle.

#### color (required, default) ``str``
The color of the circle's body.
By default, it's the ``light_gray`` from the palette.

#### outline (required, default) ``str``
The color of the circle's outline.
By default, it's the ``black`` from the palette.

#### thickness (required, default) ``int``
The thickness (width) of the circle's outline.


## function draw_rect() -> None
Draws the rectangle.

### ~Arguments~

#### x (required) ``int``
The ``x`` coordinate of the rectangle's center.

#### y (required) ``int``
The ``y`` coordinate of the rectangle's center.

#### width (required) ``int``
The width of the current rectangle.

#### height (required) ``int``
The height of the current rectangle.

#### color (required, default) ``str``
The color of the rectangle's body.
By default, it's the ``black`` from the palette.

#### outline (required, default) ``str``
The color of the rectangle's outline.
By default, it's the ``black`` from the palette.

#### thickness (required, default) ``int``
The thickness (width) of the rectangle's outline.


## function draw_text() -> None
Draws the text.

### ~Arguments~

#### x (required) ``int``
The ``x`` coordinate of the text's center.

#### y (required) ``int``
The ``y`` coordinate of the text's center.

#### text (required) ``str``
The body of the current text.

#### font_name (required, default) ``str``
The name of the text's font.
It's strongly recommended to use only Mono-typed fonts.

#### font_size (required, default) ``int``
The size of the text's font.

#### color (required, default) ``str``
The color of the text.
By default, it's the ``black`` from the palette.

#### location (required, default) ``str``
Aka-offset. The location of the text, according to it's ``x`` and ``y`` coordinates.
By default, it's ``center``
The map of all possible locations:

>``nw`` ``n`` ``ne``
>
> ``w`` ``center`` ``e``
>
> ``sw`` ``s`` ``se``


### function get_random_color() -> str
Returns a random color.

### ~Arguments~

#### colors (optional) ``list[str]``
The list of the colors to choose.
If not provided, default palette from the config will be used.


> ## Buttons extension

## class Button

Basic button object.
Subclass of the Sprite object.
Allows you to create rectangular buttons.

### ~Attributes~

#### x (required) ``int``
Represents the ``x`` coordinate.

#### y (required) ``int``
Represents the ``y`` coordinate.

#### width (required) ``int``
Represents the width.

#### height (required) ``int``
Represents the height

#### text (optional, default) ``str``
The text of the button. 
If not provided, would be blank.

#### color (optional, default) ``str``
Hex value of the button's color. 
Recommended to use one of ``palette`` colors.
Default value: ``palette.white``.

### ~Methods~

#### update() -> None
Same as ``Sprite``

#### draw() -> None
Same as ``Sprite``

#### click(x: int, y: int, *args) -> on_click(*args) or None
Function, used in main code to check, if the button was clicked.
If yes, calls ``on_click`` function.
Different arguments passed to this function would be also passed to ``on_click`` function.

#### on_click(*args) -> None
Function, used for subclassing. 
Called automatically after ``click``.
Here should be all button's logic.

>

## class CheckBox

Basic checkbox object.
Subclass of the Sprite object.
Allows you to create square checkboxes.

### ~Attributes~

#### x (required) ``int``
Represents the ``x`` coordinate.

#### y (required) ``int``
Represents the ``y`` coordinate.

#### size (required) ``int``
Represents the size.

#### color (optional, default) ``str``
Hex value of the button's color. 
Recommended to use one of ``palette`` colors.
Default value: ``palette.white``.
Note, that, when ``CheckBox`` is clicked, the color would change to ``palette.red`` or ``palette.yellow``. 

#### value (default): ``bool``
Value that represents the checkbox status.
Could be ejected using built-in ``bool(CheckBox)``

### ~Methods~

#### update() -> None
Same as ``Sprite``

#### draw() -> None
Same as ``Sprite``

#### click(x: int, y: int) -> None
Function, used in main code to check, if the button was clicked.
If yes, calls changes ``value``.

>

## class InputField
too much text, sorry...
Just see the ``buttons.py`` in samples.