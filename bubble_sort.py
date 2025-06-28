import timeit

def bubble(l):
    N = len(l)
    for j in range(1, N + 1):
        swaps = False
        for i in range(N - j):
            k = i + 1
            if l[i] > l[k]:
                l[i], l[k] = l[k], l[i]
                swaps = True
        if not swaps:
            break
    return l

def insertion(l):
    for i in range(1, len(l)):
        k, j = l[i], i - 1
        while j >= 0 and k < l[j]:
            l[j + 1] = l[j]
            j -= 1
        l[j + 1] = k
    return l

def merge(l):
    if len(l) > 1:
        mid = len(l) // 2
        left, right, i, j, k = l[:mid], l[mid:], 0, 0, 0
        merge(left)
        merge(right)

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                l[k] = left[i]
                i += 1
            else:
                l[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            l[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            l[k] = right[j]
            j += 1
            k += 1
    return l

def quicksort(l):
    if len(l) < 2: return l
    pivot = l[0]
    less, greater = [i for i in l[1:] if i <= pivot], [i for i in l[1:] if i > pivot]
    return quicksort(less) + [pivot] + quicksort(greater)

n = [5, 9, 4, 2, 11, 15, 23, 31, 1, 6]

def run_bubble(): return bubble(n.copy())
def run_insertion(): return insertion(n.copy())
def run_merge(): return merge(n.copy())
def run_quicksort(): return quicksort(n.copy())

b_result = run_bubble()
b_time = timeit.timeit(run_bubble, number=1) * 1000

i_result = run_insertion()
i_time = timeit.timeit(run_insertion, number=1) * 1000

m_result = run_merge()
m_time = timeit.timeit(run_merge, number=1) * 1000

q_result = run_quicksort()
q_time = timeit.timeit(run_quicksort, number=1) * 1000

print(f"   Bubble: {b_result} ({b_time:.3f} ms)")
print(f"Insertion: {i_result} ({i_time:.3f} ms)")
print(f"    Merge: {m_result} ({m_time:.3f} ms)")
print(f"QuickSort: {q_result} ({q_time:.3f} ms)")
