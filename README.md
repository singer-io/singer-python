singer-python
===================

Writes the Singer format from Python

Use
---

This library depends on python3. We recommend using a `virtualenv`
like this:

```bash
› mkvirtualenv -p python3 singer
```

Next, install this library:

```bash
› workon singer
› git clone http://github.com/singer-io/singer-python
› cd singer-python
› python setup.py install
```

Now, from python code within the same `virtualenv`, you can use the
library:

```python
import singer

singer.write_schema('my_table',
                {'properties':{'id': {'type': 'string', 'key': True}}})
singer.write_records('my_table',
                 [{'id': 'b'}, {'id':'d'}])
singer.write_state({'my_table': 'd'})
```


License
-------

Copyright © 2017 Stitch

Distributed under the Apache License Version 2.0
