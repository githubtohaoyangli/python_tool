xattr -cr python_tool.app
codesign --force --deep --sign - python_tool.app
codesign --verify --deep --strict python_tool.app