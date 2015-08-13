## The pipeline:

`fastree` is used to generate an first-guess tree, followed by `ExaML` to create
a large ML tree, followed by lazarus (which wraps PAML) to do ancestral sequence
reconstruction.

An example pipeline run is shown in `run-me.sh`

### hacks/notes:
* `alignment-internal_lg.model`needs to be tweaked so it has the right protein
length. 
* the `examl -s ...` command below is implemented in `examl-on-cluster.pbs`
* to find the best protein model, you should probably use the "best" option in
examl, as well as trying LG manually (which is not part of "best" option for
some reason). 

### software used:
# fasttree: http://www.microbesonline.org/fasttree/
# examl: http://sco.h-its.org/exelixis/web/software/examl/index.html
# lazarus: https://code.google.com/p/project-lazarus/
# paml: http://abacus.gene.ucl.ac.uk/software/paml.html
