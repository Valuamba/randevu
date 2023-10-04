from typing import List

"""Code copied from https://www.geeksforgeeks.org/check-if-any-two-intervals-overlap-among-a-given-set-of-intervals/"""


class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end
 
 
def is_intersect(arr: List[Interval], length: int) -> bool:
    arr.sort(key=lambda x: x.start)
 
    for i in range(1, length):
        if (arr[i - 1].end >= arr[i].start):
            return True
 
    return False
 
 
def is_intersect_with(interval: Interval, arr: List[Interval]) -> bool:
    for i in arr:
        if (i.start >= interval.start and i.start <= interval.end) \
            and (i.end > interval.start and i.end <= interval.end):
                continue
        else:
            return False
    return True
        
 