stitchstream-python
===================

Writes the Singer format from Python

Use
---

This library depends on python3. We recommend using a `virtualenv`
like this:

```bash
› mkvirtualenv -p python3 stitch
```

Next, install this library:

```bash
› workon stitch
› git clone http://github.com/singer-io/singer-python
› cd stitchstream-python
› python setup.py install
```

Now, from python code within the same `virtualenv`, you can use the
library:

```python
import singerio as ss

records = [{'id': i, 'value': 'abc'} for i in range(0,10)]
ss.write_schema('my_table',
                {'properties':{'id': {'type': 'string', 'key': True}}})
ss.write_records('my_table',
                 [{'id': 'b'}, {'id':'d'}])
ss.write_state({'my_table': i})
```


License
-------

Copyright © 2016 Stitch

Distributed under the Apache License Version 2.0
