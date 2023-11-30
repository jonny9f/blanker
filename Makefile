# Define the default target
all: build

# Target to build the application
build:
	pyinstaller --onefile --windowed redact.py

# Clean up the generated files
clean:
	rm -rf build dist __pycache__
	rm -f redact.spec
