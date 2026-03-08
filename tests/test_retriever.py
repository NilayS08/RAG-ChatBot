from src.retriever import build_filter
def test_filter_single():
    f = build_filter(region='India')
    assert f == {'region': {'$eq': 'India'}}
def test_filter_multiple():
    f = build_filter(department='HR', region='India')
    assert '$and' in f
    assert len(f['$and']) == 2
def test_filter_none():
    f = build_filter()
    assert f is None

