from heapq import heappush, _heappop_max, _heapify_max


def addToHeap(heap,community_id, spamminess_value):
    heappush(heap, (spamminess_value, community_id))

def heapify(heap):
    _heapify_max(heap)
def getMaxElement(heap):
    return _heappop_max(heap)