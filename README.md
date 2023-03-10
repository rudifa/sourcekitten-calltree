# generate a calltree for a swift file

```
sourcekitten-calltree % sourcekitten_calltree.py -h                                        [main|✔]
usage: sourcekitten_calltree.py [-h] [--file FILE] [-x EXCLUDE]

Process a json file generated by sourcekitten --structure and generate a calltree.

optional arguments:
  -h, --help            show this help message and exit
  --file FILE           the file to process
  -x EXCLUDE, --exclude EXCLUDE
                        exclude identifiers from the call tree

How to generate a calltree for a Swift file:
1. sourcekitten structure --file <file>.swift | python3 sourcekitten_calltree.py
2. or, in two steps:
    2.1. sourcekitten structure --file <file>.swift > <file>.json
    2.2. python3 sourcekitten_calltree.py <file>.json
3. this script generates two calltree files in subdirectory graphviz-output/:
    3.1 <file>.calltree.gv
    3.2 <file>.calltree.gv.pdf and opens it in Preview.
4. if needed, install sourcekitten first:
    brew install sourcekitten
5. You can exclude uninteresting functions from the calltree by passing them as a comma-separated list, e.g.:
   ./sourcekitten_calltree.py --file <file>.json -x print,String,Int

```

### issues

- none known
