from tokenizer_tools.utils.batch_iterator import BatchingIterator

def test_batchingIterator():
    data = range(19)

    bi = BatchingIterator(5)
    for i in bi(data):
        print(i)
