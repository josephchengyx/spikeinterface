# 8/31/22
# https://figurl.org/f?v=gs://figurl/spikesortingview-8&d=sha1://428301bc920d206a927143a924165a0a91dc8a63&label=Mountain%20layout%20example

import sortingview.views as vv
import spikeinterface.extractors as se
import spikeinterface as si
import kachery_cloud as kcl
import os
import sys

# Append to the path so we can import from examples directory
current_path = os.getcwd()
path = os.path.join(current_path, '..')
if path not in sys.path:
    sys.path.insert(0, path)
path = os.path.abspath(os.path.join(current_path, '..', 'examples'))
if path not in sys.path:
    sys.path.insert(0, path)

from example_autocorrelograms import example_autocorrelograms
from example_cross_correlograms import example_cross_correlograms
from example_raster_plot import example_raster_plot
from example_average_waveforms import example_average_waveforms
from example_units_table import example_units_table
from example_unit_similarity_matrix import example_unit_unit_similarity_matrix
from example_spike_amplitudes import example_spike_amplitudes

def main():
    kcl.use_sandbox()
    R = se.read_mda_recording('/Users/jcheng/Documents/Data/20181105/mountains/channel019/dataset',  raw_fname='raw_data.mda')
    S = se.read_mda_sorting('/Users/jcheng/Documents/Data/20181105/mountains/channel019/output/firings.mda', 30000)

    view = example_mountain_layout(recording=R, sorting=S)

    url = view.url(
        label='Mountain layout example'
    )
    print(url)

def example_mountain_layout(recording: si.BaseRecording, sorting: si.BaseSorting, height=800):
    R = recording
    S = sorting

    v_units_table = example_units_table(recording=R, sorting=S)
    v_average_waveforms = example_average_waveforms(recording=R, sorting=S)
    v_raster_plot = example_raster_plot(recording=R, sorting=S)
    v_spike_amplitudes = example_spike_amplitudes(recording=R, sorting=S)
    v_autocorrelograms = example_autocorrelograms(sorting=S)
    v_cross_correlograms = example_cross_correlograms(sorting=S, hide_unit_selector=True)
    v_unit_similarity_matrix = example_unit_unit_similarity_matrix(recording=R, sorting=S)
    

    view = vv.MountainLayout(
        height=height,
        items=[
            vv.MountainLayoutItem(
                label='Units',
                view=v_units_table
            ),
            vv.MountainLayoutItem(
                label='Avg. waveforms',
                view=v_average_waveforms
            ),
            vv.MountainLayoutItem(
                label='Raster plot',
                view=v_raster_plot
            ),
            vv.MountainLayoutItem(
                label='Spike amplitudes',
                view=v_spike_amplitudes
            ),
            vv.MountainLayoutItem(
                label='Autocorrelograms',
                view=v_autocorrelograms
            ),
            vv.MountainLayoutItem(
                label='Cross correlograms',
                view=v_cross_correlograms
            ),
            vv.MountainLayoutItem(
                label='Unit similarity matrix',
                view=v_unit_similarity_matrix,
                is_control=True,
                control_height=300
            )
        ]
    )

    return view

if __name__ == '__main__':
    main()
