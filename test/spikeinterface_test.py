import spikeinterface as si
import spikeinterface.extractors as se 
import spikeinterface.postprocessing as spost
import spikeinterface.qualitymetrics as sqm
import spikeinterface.exporters as sexp
import spikeinterface.widgets as sw
import spikeinterface_gui as sgui
import sortingview.views as vv

import numpy as np
import kachery_cloud as kcl

import warnings
from numba.core.errors import NumbaWarning, NumbaDeprecationWarning, NumbaPendingDeprecationWarning
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore', category=NumbaWarning)
warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)


### Read in recording and sorting files ###
dirpath = '/Users/jcheng/Documents/Data/20181105/mountains/channel019/'
recording_dir = dirpath + 'dataset'
sorting_file = dirpath + 'output/firings.mda'

recording = se.read_mda_recording(recording_dir, raw_fname='raw_data.mda',)
recording.annotate(is_filtered=True)
sorting = se.read_mda_sorting(sorting_file, 30_000)

### Extract waveforms ###
job_kwargs = dict(n_jobs=10, chunk_duration='1s', progress_bar=True,)
we = si.extract_waveforms(recording, sorting, folder=dirpath+"waveforms", 
                          load_if_exists=False, overwrite=True,
                          max_spikes_per_unit=500,
                          ms_before=1.5, ms_after=2.5,
                          sparse=True,**job_kwargs)

### Compute sorting metrics ###
# Spike amplitudes
amplitudes = spost.compute_spike_amplitudes(we, outputs="by_unit", load_if_exists=True, 
                                            **job_kwargs)
# ISI histograms
isi_histograms, hist_bins = spost.compute_isi_histograms(we)
# Correlograms
ccgs, cor_bins = spost.compute_correlograms(we)
# PCA
pc = spost.compute_principal_components(we, n_components=3,
                                        load_if_exists=False,
                                        n_jobs=job_kwargs["n_jobs"], 
                                        progress_bar=job_kwargs["progress_bar"])
# Unit locations
unit_locs = spost.compute_unit_locations(we)
# Template metrics
metrics = spost.compute_template_metrics(we, metric_names=spost.get_template_metric_names())
# Template similarity
similarity = spost.compute_template_similarity(we)


### Generate GUI for viewing and curation of sorting results ###
kcl.use_sandbox()
w_ss = sw.plot_sorting_summary(we, backend='sortingview')