#!/usr/bin/env python3
def get_name(install_path):
    """
    Pass in an installation path string and get back the last folder
    which is the name of the package. Eg. rincewind
    """
    package_name = install_path.split('/')
    return(package_name[-2])