# tiger_versus_python
Script to Convert Pre-Processed TIGER data to OpenStreetMap format

Preprocessed data can be found at https://www.nominatim.org/data/

Works with Python >= 3.6.

Run like this:

```shell
cat path/to/tiger/*.csv | ./tiger_versus_python.py > usa.osc
```
