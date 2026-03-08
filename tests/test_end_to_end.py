from src.retriever import load_vectorstore, build_filter
from src.chain import build_qa_chain, ask
def test_full_pipeline():
    vs = load_vectorstore()
    filters = build_filter(department='HR', region='India')
    chain = build_qa_chain(vs, filters)
    result = ask(chain, 'How many days of annual leave do I get?')
    assert 'answer' in result
    assert len(result['answer']) > 20, 'Answer should be substantive'
    assert len(result['sources']) > 0, 'Should return source documents'
# Verify all sources match the filter
    for doc in result['sources']:
        assert doc.metadata.get('region') == 'India'
        assert doc.metadata.get('department') == 'HR'