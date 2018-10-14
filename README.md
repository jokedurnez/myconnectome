# MyConnectome meets Joy Division

Figure of MyConnectome global signals.  Only _loosely_ based on the cover of Unknown Pleasures (Joy Division).

Preprocessing from BIDS (included in code): cut off first 10 timepoints, apply mask, center

- `unknownpleasures.sh` contains constants and call to extract script
- `unknownpleasures_extract.py` extracts the global signal from each session with a resting state scan and writes all gs's to a csv.
- `unknownpleasures_figure.ipynb` creates the figure.

*Dependencies:* [singularity container for fmriprep-1.1.5](https://hub.docker.com/r/poldracklab/fmriprep/tags/)

*Data:* MyConnectome preprocessed with fmriprep (available on openfmri)

![myconnectome](unknown_pleasures_myconnectome.jpg)
