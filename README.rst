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

Any ``ANGRY_SNAKE_CASE`` attributes of a ``BaseConfig`` sub-class will be
intercepted by the meta-class, and checked for in the environment using
``os.getenv``.

Their type will be determined by their annotation in the class, or fall back to
``str``.

Methods will automatically behave like a ``property``, with access to ``self``.

Handling of type casting can be overridden [as it is for bool] by adding it to
the ``__types__`` dict:

.. code-block:: python

    class Config(BaseConfig):
        __types__ = {
            json: lambda v: json.loads(v) if isinstance(v, str) else v,
        }
        
        LOGGING : json = {'version': 1 ...}

All types defined on parent ``Config`` classes will be merged with this dict.

Inheritance
===========

Classes, as usual, inherit from their parents.  If the type of an attribute is
changed, it will raise an ``AssertionError``.

Methods
=======

Method in all-caps will be invoked, and can access ``self`` as usual:

.. code-block:: python

   class Config(BaseConfig):
      DB_ENGINE = 'postgresql'
      DB_HOST = 'localhost'
      DB_PORT : int = 5432
      DB_USER = 'test_user'
      DB_PASS = 'secret'
      DB_NAME = 'test-db'

      def CONNECTION_STRING(self):
          return f'{self.DB_ENGINE}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}/{self.DB_NAME}'


Using in Django
---------------


In your ``settings.py``, put your settings class (or classes), then use the following code to select one to use:

.. code-block:: python

   import os
   MODE = os.getenv('DJANGO_MODE', 'Local')
   globals().update(globals()[f'{ MODE.title() }Settings'].as_dict())


With Python 3.7
===============

In Python 3.7, a new feature was added which allowed you to define
`__getattr__` for a module (See `PEP 562`
<https://www.python.org/dev/peps/pep-0562/>).

The `BaseConfig` metaclass provides a `module_getattr` factory method to
provide a `__getattr__` that will look up the `Config` object.


.. code-block:: python

   from confucius import BaseConfig

   class Config(BaseConfig):
       DB_HOST = 'localhost'
       DB_PORT = 5432

   __getattr__ = Config.module_getattr()


After importing this module, attempts to access attributes will resolve
normally and, if they're not found, call `__getattr__`, just like on an object.
