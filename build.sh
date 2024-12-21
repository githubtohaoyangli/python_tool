


python3 -m nuitka --standalone --macos-create-app-bundle --remove-output --enable-plugins=tk-inter --macos-app-name=Python_tool --macos-app-version=1.1.0 --show-progress --output-dir=dist --macos-app-icon=python_tool.icns python_tool.py
#python -m nuitka --clang --remove-output --show-progress --standalone --output-dir=udist --macos-create-app-bundle --macos-app-name=Updater --enable-plugins=tk-inter --macos-app-version=1.0.0 --macos-app-icon=python_tool.icns update.py

