Confucius
---------

.. rubric:: A simpler, clearer approach to configuration.


Quick Start
===========

.. code-block:: python
   :name: config.py

   from confucius import BaseConfig

   class Config(BaseConfig)
       HOST = '127.0.0.1'
       PORT : int = 8000

       DEBUG : bool = False

.. code-block:: python
   :name: app.py

   from myapp import Server
   from config import Config


   server = Server(Config.HOST, Config.PORT)


.. code-block:: sh

   $ python app.py
   - Starting server: 127.0.0.1:8000

   $ PORT=80 python app.py
   - Starting server: 127.0.0.1:80

   $ DEBUG=y python app.py
   - Starting debug server: 127.0.0.1:80


Types
=====

Any `ANGRY_SNAKE_CASE` attributes of a `BaseConfig` sub-class will be intercepted by the meta-class, and checked for in the environment using `os.getenv`.

Their type will be determined by their annotation in the class, or fall back to `str`.

Methods will automatically behave like `property`s, with access to `self`.

Handling of type casting can be overridden [as it is for bool] by adding it to the `__types__` dict:

.. code-block:: python

    class Config(BaseConfig):
        __types__ = {
            json: lambda v: json.loads(v) if isinstance(v, str) else v,
        }
        
        LOGGING : json = {'version': 1 ...}

All types defined on parent `Config` classes will be merged with this dict.

Inheritance
===========

Classes, as usual, inherit from their parents.  If the type of an attribute is changed, it will raise an `AssertionError`.
