__title__ = "LCLPy"
__author__ = "Paul Bayfield"
__version__ = "1.0.1"
__description__ = "Une bibliothèque Python pour interagir avec les services bancaires de LCL."

__baseURL__ = "https://monespace.lcl.fr/api"

__headers__ = {
    "User-Agent": f"MoneyTracker/{__version__} (github.com/PaulBayfield/MoneyTracker)"
}

from .client import LCLClient
