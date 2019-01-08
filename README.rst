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
