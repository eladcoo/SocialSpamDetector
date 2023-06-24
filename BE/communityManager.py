from heapq import heappush, _heappop_max, _heapify_max


def add_account_to_heap(heap, id, spamminess_value):
    heappush(heap, (spamminess_value, id))

def heapify(heap):
    _heapify_max(heap)
def get_max_element(heap):
    return _heappop_max(heap)