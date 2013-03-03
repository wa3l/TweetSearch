#!/usr/bin/python
import math
from collections import Counter

print "hi\a\a"
# l = "spade heart".split()
# l1 = "spade spade spade heart diamond".split()
# l2 = "spade club".split()
# l3 = "spade spade heart heart".split()
# l4 = "club heart heart".split()

# def get_vector(counter, terms, idfs):
#   vector = []
#   for k in terms:
#     if counter[k] == 0: vector.append(0)
#     else:
#       tf  = 1 + math.log(counter[k], 2)
#       idf = math.log(float(4)/idfs[k], 2)
#       vector.append(tf * idf)
#   return vector

# def buildVector(query, docs):
#   for t in query:
#     if t not in terms: return

#   idfs = {'club': 2, 'heart': 3, 'diamond': 1, 'spade': 3}
#   qcounter = Counter(query)
#   counters = []
#   for d in docs: counters.append(Counter(d))

#   terms = set()
#   for c in counters: terms = terms.union(set(c.keys()))

#   vector1 = get_vector(qcounter, terms, idfs)
#   vectors = []
#   for c in counters: vectors.append(get_vector(c, terms, idfs))
#   return vector1, vectors


# def cosim(v1, v2):
#   dot_product = sum(n1 * n2 for n1, n2 in zip(v1, v2))
#   magnitude1  = math.sqrt(sum(n ** 2 for n in v1))
#   magnitude2  = math.sqrt(sum(n ** 2 for n in v2))
#   return dot_product / (magnitude1 * magnitude2)


# v, vs = buildVector(l, [l1, l2, l3, l4])

# print cosim(v, vs[0])
# print cosim(v, vs[1])
# print cosim(v, vs[2])
# print cosim(v, vs[3])
