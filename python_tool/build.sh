

pyinstaller -F -w -i python_tool.icns --name "python_tool" ./python_tool/python_tool.py
#python -m nuitka --standalone --macos-create-app-bundle --remove-output --enable-plugins=tk-inter --macos-app-name=Python_tool --macos-app-version=1.1.0 --show-progress --macos-app-icon=python_tool.icns python_tool.py

