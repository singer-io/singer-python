singer-python
===================

Writes the Singer format from Python

Use
---

This library depends on python3. We recommend using a `virtualenv`
like this:

```bash
python3 -m venv ~/.virtualenvs/singer-python
```

Next, install this library:

```bash
source ~/.virtualenvs/singer-python/bin/activate
git clone http://github.com/singer-io/singer-python
cd singer-python
make install
```

Now, from python code within the same `virtualenv`, you can use the
library:

```python
import singer

singer.write_schema('my_table',
	            {'properties':{'id': {'type': 'string', 'key': True}}},
		    ['id'])
singer.write_records('my_table',
                     [{'id': 'b'}, {'id':'d'}])
singer.write_state({'my_table': 'd'})
```


License
-------

Copyright © 2017 Stitch

Distributed under the Apache License Version 2.0
