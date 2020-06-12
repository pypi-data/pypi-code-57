from collections import defaultdict

import numpy
import pytest

import event_model


def test_run_router(tmp_path):
    bundle = event_model.compose_run()
    docs = []
    start_doc, compose_descriptor, compose_resource, compose_stop = bundle
    docs.append(('start', start_doc))
    bundle = compose_descriptor(
        data_keys={'motor': {'shape': [], 'dtype': 'number', 'source': '...'},
                   'image': {'shape': [512, 512], 'dtype': 'number',
                             'source': '...', 'external': 'FILESTORE:'}},
        name='primary')
    primary_descriptor_doc, compose_primary_event, compose_event_page = bundle
    docs.append(('descriptor', primary_descriptor_doc))
    bundle = compose_descriptor(
        data_keys={'motor': {'shape': [], 'dtype': 'number', 'source': '...'}},
        name='baseline')
    baseline_descriptor_doc, compose_baseline_event, compose_event_page = bundle
    docs.append(('descriptor', baseline_descriptor_doc))
    bundle = compose_resource(
        spec='TIFF', root=str(tmp_path), resource_path='stack.tiff',
        resource_kwargs={})
    resource_doc, compose_datum, compose_datum_page = bundle
    docs.append(('resource', resource_doc))
    datum_doc = compose_datum(datum_kwargs={'slice': 5})
    docs.append(('datum', datum_doc))
    primary_event_doc = compose_primary_event(
        data={'motor': 0, 'image': datum_doc['datum_id']},
        timestamps={'motor': 0, 'image': 0}, filled={'image': False})
    docs.append(('event', primary_event_doc))
    baseline_event_doc = compose_baseline_event(
        data={'motor': 0},
        timestamps={'motor': 0})
    docs.append(('event', baseline_event_doc))
    stop_doc = compose_stop()
    docs.append(('stop', stop_doc))

    # Empty list of factories. Just make sure nothing blows up.
    rr = event_model.RunRouter([])
    for name, doc in docs:
        rr(name, doc)

    # A factory that rejects all runs.
    def null_factory(name, doc):
        return [], []

    rr = event_model.RunRouter([null_factory])
    for name, doc in docs:
        rr(name, doc)

    # A factory that accepts all runs.
    collected = []

    def collector(name, doc):
        if name == 'event_page':
            name = 'event'
            doc, = event_model.unpack_event_page(doc)
        elif name == 'datum_page':
            name = 'datum'
            doc, = event_model.unpack_datum_page(doc)
        collected.append((name, doc))

    def all_factory(name, doc):
        return [collector], []

    rr = event_model.RunRouter([all_factory])
    for name, doc in docs:
        rr(name, doc)

    assert collected == docs
    collected.clear()

    # A factory that returns a subfactory interested in 'baseline' only.
    def subfactory(name, doc):
        if doc.get('name') == 'baseline':
            return [collector]
        return []

    def factory_with_subfactory_only(name, doc):
        return [], [subfactory]

    rr = event_model.RunRouter([factory_with_subfactory_only])
    for name, doc in docs:
        rr(name, doc)

    expected_item = ('event', baseline_event_doc)
    unexpected_item = ('event', primary_event_doc)
    assert expected_item in collected
    assert unexpected_item not in collected
    collected.clear()

    # Test factory that expects old (pre-1.14.0) RunRouter behavior.

    collected_header_docs = {}

    class LocalException3(Exception):
        ...

    def header_collector(name, doc):
        if name in ('start', 'stop', 'descriptor'):
            key = (name, doc['uid'])
            if key in collected_header_docs:
                raise LocalException3
            collected_header_docs[key] = doc

    def all_factory(name, doc):
        header_collector(name, doc)
        return [header_collector], []

    rr = event_model.RunRouter([all_factory])
    with pytest.warns(UserWarning, match='1.14.0'), pytest.raises(LocalException3):
        for name, doc in docs:
            rr(name, doc)

    collected_header_docs.clear()

    # Test subfactory that expects old (pre-1.14.0) RunRouter behavior.

    def factory_with_subfactory_only(name, doc):
        header_collector(name, doc)

        def subfactory(name, doc):
            if doc.get('name') == 'baseline':
                header_collector(name, doc)
                return [header_collector]
            return []

        return [], [subfactory]

    rr = event_model.RunRouter([factory_with_subfactory_only])
    with pytest.warns(UserWarning, match='1.14.0'), pytest.raises(LocalException3):
        for name, doc in docs:
            rr(name, doc)

    collected_header_docs.clear()

    # Test RunRouter with handler_registry.

    class FakeTiffHandler:
        def __init__(self, resource_path):
            assert resource_path == str(tmp_path / "stack.tiff")

        def __call__(self, slice):
            return numpy.ones((5, 5))

    reg = {'TIFF': FakeTiffHandler}

    def check_filled(name, doc):
        if name == 'event_page':
            for is_filled in doc['filled'].values():
                assert all(is_filled)
        elif name == 'event':
            for is_filled in doc['filled'].values():
                assert is_filled

    def check_not_filled(name, doc):
        if name == 'event_page':
            for is_filled in doc['filled'].values():
                assert not any(is_filled)
        elif name == 'event':
            for is_filled in doc['filled'].values():
                assert not is_filled

    def check_filled_factory(name, doc):
        return [check_filled], []

    def check_not_filled_factory(name, doc):
        return [check_not_filled], []

    # If reg is missing our spec (or just not given) docs pass through
    # unfilled.
    rr = event_model.RunRouter([check_not_filled_factory])
    for name, doc in docs:
        rr(name, doc)

    # If fill_or_fail is set to True and reg is missing our spec (or just not
    # given) we raise.
    rr = event_model.RunRouter([check_not_filled_factory], fill_or_fail=True)
    with pytest.raises(event_model.UndefinedAssetSpecification):
        for name, doc in docs:
            rr(name, doc)

    # If spec is provided, docs are filled, regardless of fill_or_fail.
    rr = event_model.RunRouter([check_filled_factory], reg)
    for name, doc in docs:
        rr(name, doc)

    rr = event_model.RunRouter([check_filled_factory], reg, fill_or_fail=True)
    for name, doc in docs:
        rr(name, doc)


def test_subfactory():
    # this test targeted the bug described in issue #170
    factory_documents = defaultdict(list)
    subfactory_documents = defaultdict(list)

    def factory(name, start_doc):
        def collect_factory_documents(name, doc):
            factory_documents[name].append(doc)

        def collect_subfactory_documents(name, doc):
            subfactory_documents[name].append(doc)

        def subfactory(name, descriptor_doc):
            return [collect_subfactory_documents]

        return [collect_factory_documents], [subfactory]

    rr = event_model.RunRouter([factory])

    run_bundle = event_model.compose_run()
    rr("start", run_bundle.start_doc)
    assert len(factory_documents) == 1
    assert len(factory_documents["start"]) == 1
    assert factory_documents["start"] == [run_bundle.start_doc]
    assert len(subfactory_documents) == 0

    descriptor_bundle = run_bundle.compose_descriptor(
        data_keys={"motor": {"shape": [], "dtype": "number", "source": "..."}},
        name="primary",
    )
    rr("descriptor", descriptor_bundle.descriptor_doc)
    assert len(factory_documents) == 2
    assert len(factory_documents["start"]) == 1
    assert factory_documents["start"] == [run_bundle.start_doc]
    assert len(factory_documents["descriptor"]) == 1
    assert factory_documents["descriptor"] == [descriptor_bundle.descriptor_doc]

    assert len(subfactory_documents) == 2
    assert len(subfactory_documents["start"]) == 1
    assert subfactory_documents["start"] == [run_bundle.start_doc]
    assert len(subfactory_documents["descriptor"]) == 1
    assert subfactory_documents["descriptor"] == [descriptor_bundle.descriptor_doc]

    stop_doc = run_bundle.compose_stop()
    rr("stop", stop_doc)

    assert len(rr._start_to_start_doc) == 0
