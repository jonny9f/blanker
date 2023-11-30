# Redact

A very simple tool that creates a window on top of all other windows to blank out a certain part of the screen.

To resize drag from the right or bottom of the window.

## Running

Run simply with 
```python redact.py```

## Create .app bundle

- install the deps in requirements.txt with pip
- run
``` make ```
- The bundle will be in ./dist

## Knows Issues

- cannot drag from bottom right corner to resize width and height at the same time
- the bundle will not create a new instance by default. to create multiple instances from from terminal instance