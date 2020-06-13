'''
.. codeauthor:: David Zwicker <david.zwicker@ds.mpg.de>
'''

import numpy as np

from .. import plotting
from ...grids import UnitGrid
from ...fields import ScalarField, FieldCollection
from ...storage import get_memory_storage
from ...tools.misc import skipUnlessModule



@skipUnlessModule("matplotlib")
def test_scalar_field_plot(tmp_path):
    """ test ScalarFieldPlot class"""
    path = tmp_path / "test_scalar_field_plot.png"
            
    # create some data
    state = ScalarField.random_uniform(UnitGrid([16, 16]))
    for scale in [(0, 1), 1, 'automatic', 'symmetric', 'unity']:
        sfp = plotting.ScalarFieldPlot(state, scale=scale)
        sfp.savefig(path)
        assert path.stat().st_size > 0

    sfp = plotting.ScalarFieldPlot(state, quantities={'source': None})
    sfp.savefig(path)
    assert path.stat().st_size > 0



@skipUnlessModule("matplotlib")
def test_scalar_plot(tmp_path):
    """ test Simple simulation """
    path = tmp_path / "test_scalar_plot.png"
    
    # create some data
    state = ScalarField.random_uniform(UnitGrid([16, 16]), label='test')
    with get_memory_storage(state) as storage:
        storage.append(state.data, 0)
        storage.append(state.data, 1)
    
    # check creating an overview image
    plotting.plot_magnitudes(storage, filename=path)
    assert path.stat().st_size > 0

    # check creating an kymograph
    plotting.plot_kymograph(storage, filename=path)
    assert path.stat().st_size > 0



@skipUnlessModule("matplotlib")
def test_collection_plot(tmp_path):
    """ test Simple simulation """
    # create some data
    field = FieldCollection([ScalarField(UnitGrid([8, 8]), label='first'),
                             ScalarField(UnitGrid([8, 8]))])
    with get_memory_storage(field) as storage:
        storage.append(field.data)
    
    path = tmp_path / 'test_collection_plot.png'
    plotting.plot_magnitudes(storage, filename=path)
    assert path.stat().st_size > 0



def test_kymograph_single(tmp_path):
    """ test making kymographs for single fields """
    # create some storage
    field = ScalarField(UnitGrid(8))
    with get_memory_storage(field) as storage:
        for i in range(8):
            storage.append(np.full(8, i), i)
    
    # create single kymograph
    path = tmp_path / 'test1.png'
    plotting.plot_kymograph(storage, colorbar=True, transpose=True,
                            filename=path)
    assert path.stat().st_size > 0
    
    # create multiple kymographs
    path = tmp_path / 'test2.png'
    plotting.plot_kymographs(storage, filename=path)
    assert path.stat().st_size > 0
    
  

def test_kymograph_collection(tmp_path):
    """ test making kymographs for field collections """
    # create some storage
    field = FieldCollection([ScalarField(UnitGrid(8), label='a'),
                             ScalarField(UnitGrid(8), label='b')])
    with get_memory_storage(field) as storage:
        for i in range(8):
            storage.append(np.full((2, 8), i), i)
    
    # create single kymograph
    path = tmp_path / 'test1.png'
    plotting.plot_kymograph(storage, field_index=1, colorbar=True,
                            transpose=True, filename=path)
    assert path.stat().st_size > 0
    
    # create multiple kymographs
    path = tmp_path / 'test2.png'
    plotting.plot_kymographs(storage, filename=path)
    assert path.stat().st_size > 0
    
      
