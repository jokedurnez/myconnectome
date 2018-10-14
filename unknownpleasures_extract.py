from nipype.utils.filemanip import split_filename
from argparse import ArgumentParser
from nipype.interfaces import fsl
import datetime as dt
import nibabel as nib
import pandas as pd
import numpy as np
import pytz
import os

parser = ArgumentParser(description = 'Extract global signal from MyConnectome resting sessions.')
parser.add_argument('--basedir', help = 'Path to the bids directory of MyConnectome.')

# get basedir from options
opts = parser.parse_args()
basedir = opts.basedir
prepdir = os.path.join(basedir,'derivatives/fmriprep_1.0.0/fmriprep')
prepsessions = os.listdir(prepdir)

# initiate dataframe
results = pd.DataFrame({})

# a logger for pretty logs
def logger(text,level=1):
    time = dt.datetime.now(pytz.timezone('America/Los_Angeles')).strftime("%Y-%m-%dT%H:%M:%S")
    prefix = "\n༼ つ ◕_◕ ༽つ" if level==0 else "    -- "
    print("%s %s: %s"%(prefix,time,text))

# loop over all sessions
for index,session in enumerate(prepsessions):
    logger('Grabbing global signal from session %s'%session,level=0)

    # get files
    funcdir = os.path.join(prepdir,session,'func')
    key = 'sub-01_%s_task-rest_run-001_bold_space-MNI152NLin2009cAsym'%session
    infile = os.path.join(funcdir,'%s_preproc.nii.gz'%key)
    maskfile = os.path.join(funcdir,'%s_brainmask.nii.gz'%key)
    outfile = os.path.join(funcdir,"%s_preproc_removed_first10.nii.gz"%key)
    if not os.path.exists(infile) or not os.path.exists(maskfile):
        logger("Can't find nifti or mask for session %s"%session)
        continue

    # cut of first 10 timepoints
    logger('Cutting off first timepoints...')
    totaltp = nib.load(infile).shape[3]
    fslcom = "fslroi %s %s %d %d"%(infile,outfile,10,totaltp-10)
    os.popen(fslcom).read()

    # apply mask
    logger('Applying mask...')
    infile = outfile
    _,base,_ = split_filename(infile)
    outfile = os.path.join(funcdir,"%s_masked.nii.gz"%key)
    masker = fsl.maths.ApplyMask()
    masker.inputs.in_file = infile
    masker.inputs.mask_file = maskfile
    masker.inputs.out_file = outfile
    masker.run()

    # read in new nifti and compute global signal
    logger('Grab GS...')
    data = nib.load(outfile).get_data()
    globalts = pd.Series(np.mean(data,axis=(0,1,2)), name=session)
    results = pd.concat([results,globalts],axis=1, sort=False)

logger('Writing global signals to file...',level=0)
results.to_csv(os.path.join(basedir,'derivatives','globalsignal.csv'))
