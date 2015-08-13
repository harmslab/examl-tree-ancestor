# Create pilot tree using fasttree
FastTreeMP -fastest alignment-internal.fasta > fasttree.newick

# Create compressed, binary alignment and then run examl

# USE LG MODEL
parse-examl -s alignment-internal.phy -n alignment-internal -q alignment-internal_lg.model
examl -s alignment-internal.binary -m GAMMA -n examl -t fasttree.newick 

# USE BEST AA MODEL.  For some reason, this does not sample LG.
#~/Desktop/ExaML/parser/parse-examl -s alignment-internal.phy -n alignment-internal -m PROT 
#~/Desktop/ExaML/examl/examl -s alignment-internal.binary -m GAMMA -n examl -t fasttree.newick --auto-prot=ml|bic

# remove supports from final tree so paml doesn't choke and then run.  
alpha=`./examl_to_lazarus.py ExaML_modelFile.examl`
lazarus_batch.py --alignment alignment-internal.fasta --tree ExaML_result.examl --model ./examl-matrix-used.dat --branch_lengths fixed --asrv 8 --alpha ${alpha} --codeml &> lazarus-spew.log
