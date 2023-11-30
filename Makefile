# Define the default target # dep is a redact.py
all: build

# Target to build the application 
build: redact.py
	pyinstaller --onefile --windowed redact.py

# Clean up the generated files
clean:
	rm -rf build dist __pycache__
	rm -f redact.spec
