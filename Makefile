
NP        := 8
BUILD_DIR := $(shell pwd)
DIRS := $(wildcard P*)
BUILD_FILE := $(foreach adir, $(DIRS), $(adir)/$(adir)_out.root)

FILE_LOCATION := /exo/scratch1/ReconEfficiency

.FORCE:

.PHONY: $(DIRS) .depend 
all: $(BUILD_FILE)

$(BUILD_FILE): 
	@echo "$(dir $@)"
	@cd $(dir $@) && mpirun -np $(NP) python $(BUILD_DIR)/root_to_pkl.py $(FILE_LOCATION)/$(dir $@)nfs/slac/g/exo_data3/exo_data/data/WIPP/masked/*/*.root
	@cd $(dir $@) && mpirun -np $(NP) python $(BUILD_DIR)/pkl_to_hists.py masked000*.pkl 
	@python assemble_hists.py $(dir $@)*_proc.root $@ 

.depend depend: .FORCE
	@echo "Making dependencies"
	@touch $@
	@for var in $(BUILD_FILE); do \
          python make_dependency.py $$var \
          "$(FILE_LOCATION)/@REPL@/nfs/slac/g/exo_data3/exo_data/data/WIPP/masked/*/*.root" >> $@; \
         done 

-include .depend
