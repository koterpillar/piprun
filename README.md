piprun
======

`piprun` lets you specify PyPI packages your script needs inline:

```python
#!/usr/bin/env piprun Flask==0.10.1 --

from flask import Flask
app = Flask(__name__)

# ...
```

Optionally, specify the Python interpreter path (e.g. for Python 2) as the
first argument:

```python
#!/usr/bin/env piprun /usr/bin/python2 Flask==0.10.1 --
# ...
```
