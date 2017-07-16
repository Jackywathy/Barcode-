import os, appdirs

# 0: default level, None
# 1: can read from products
# 2: can read users
# 4: can write to products
# 5: can write to users
# 10: full permissions
PERMS_NONE = 0
PERMS_READ_PRODUCT = 1
PERMS_READ_USERS = 2
PERMS_WRITE_PRODUCTS = 4
PERMS_WRITE_USERS = 5
PERMS_FULL = 10


AppName = "BarcodeScanner"

def get_app_directory(file_name=None):
    """Gets the app directory, with file_name appended if supplied"""
    path = appdirs.user_data_dir(AppName)
    if file_name is not None:
        return os.path.join(path, file_name)
    else:
        return path


