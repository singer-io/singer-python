stitchstream-python
===================

Writes the stitchstream format from Python

Use
---

This library depends on python3 and a to-be-released version of
`transit-python`. The first step is to setup the python environment
and manually install the correct version of that library:

```bash
› mkvirtualenv -p python3 stitch
```

```bash
› workon stitch
› git clone https://github.com/cognitect/transit-python
› cd transit-python
› python setup.py install
```

Next, install this library:

```bash
› workon stitch
› git clone http://github.com/stitchstreams/stitchstream-python
› cd stitchstream-python
› python setup.py install
```

Now, from python code within the same `virtualenv`, you can use the
library:

```python
import stitchstream as ss

records = [{'id': i, 'value': 'abc'} for i in range(0,10)]
ss.write_records('my_table', ['id'], records)
ss.write_bookmark({'my_table': i})
```


License
-------

Copyright © 2016 Stitch

Distributed under the Apache License Version 2.0
