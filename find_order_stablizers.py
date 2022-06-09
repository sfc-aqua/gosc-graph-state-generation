#modified based on the source code of heapq
def heappush(heap, item,stablizer_order,stablizer):
    """Push item onto heap, maintaining the heap invariant."""
    heap.append(item)
    stablizer_order.append(stablizer)
    _siftdown(heap, 0, len(heap)-1,stablizer_order)

def _siftdown(heap, startpos, pos, stablizer_order):
    newitem = heap[pos]
    newstablizer = stablizer_order[pos]
    # Follow the path to the root, moving parents down until finding a place
    # newitem fits.
    while pos > startpos:
        parentpos = (pos - 1) >> 1
        parent = heap[parentpos]
        parent_stablizer = stablizer_order[parentpos]
        if newitem < parent:
            heap[pos] = parent
            stablizer_order[pos]=parent_stablizer
            pos = parentpos
            continue
        break
    heap[pos] = newitem
    stablizer_order[pos] = newstablizer

def heappop(heap,stablizer_order):
    """Pop the smallest item off the heap, maintaining the heap invariant."""
    lastelt = heap.pop()    # raises appropriate IndexError if heap is empty
    laststa = stablizer_order.pop()
    if heap:
        returnitem = heap[0]
        returnsta = stablizer_order[0]
        heap[0] = lastelt
        stablizer_order[0] = laststa
        _siftup(heap, 0,stablizer_order)
        return returnitem,returnsta
    return lastelt,laststa

def _siftup(heap, pos,stablizer_order):
    endpos = len(heap)
    startpos = pos
    newitem = heap[pos]
    newsta = stablizer_order[pos]
    # Bubble up the smaller child until hitting a leaf.
    childpos = 2*pos + 1    # leftmost child position
    while childpos < endpos:
        # Set childpos to index of smaller child.
        rightpos = childpos + 1
        if rightpos < endpos and not heap[childpos] < heap[rightpos]:
            childpos = rightpos
        # Move the smaller child up.
        heap[pos] = heap[childpos]
        stablizer_order[pos] = stablizer_order[childpos]
        pos = childpos
        childpos = 2*pos + 1
    # The leaf at pos is empty now.  Put newitem there, and bubble it up
    # to its final resting place (by sifting its parents down).
    heap[pos] = newitem
    stablizer_order[pos] = newsta
    _siftdown(heap, startpos, pos, stablizer_order)