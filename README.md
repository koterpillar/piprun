piprun
======

`piprun` lets you specify PyPI packages your script needs inline:

```python
#!/usr/bin/env piprun Flask==0.10.1 --

from flask import Flask
app = Flask(__name__)

# ...
```
