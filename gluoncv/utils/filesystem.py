"""Filesystem utility functions."""
import os
import errno

def makedirs(path):
    """Create directory recursively if not exists.
    Similar to `makedir -p`, you can skip checking existance before this function.

    Parameters
    ----------
    path : str
        Path of the desired dir
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise

def import_try_install(package, extern_url=None):
    """Try import the specified package.
    If the package not installed, try use pip to install and import if success.

    Parameters
    ----------
    package : str
        The name of the package trying to import.
    extern_url : str or None, optional
        The external url if package is not hosted on PyPI.
        For example, you can install a package using:
         "pip install git+http://github.com/user/repo/tarball/master/egginfo=xxx".
        In this case, you can pass the url to the extern_url.

    Returns
    -------
    <class 'Module'>
        The imported python module.

    """
    try:
        return __import__(package)
    except ImportError:
        try:
            from pip import main as pipmain
        except ImportError:
            from pip._internal import main as pipmain

        # trying to install package
        url = package if extern_url is None else extern_url
        pipmain(['install', '--user', url])  # will raise SystemExit Error if fails

        # trying to load again
        try:
            return __import__(package)
        except ImportError:
            import sys
            import site
            user_site = site.getusersitepackages()
            if user_site not in sys.path:
                sys.path.append(user_site)
            return __import__(package)
    return __import__(package)
