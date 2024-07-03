# import random

# def isPrime(n, k=5):
#     if n <= 1:
#         return False
#     elif n <= 3:
#         return True
#     elif n % 2 == 0 or n % 3 == 0:
#         return False
#     i = 5
#     while i * i <= n and k > 0:
#         if n % i == 0 or n % (i + 2) == 0:
#             return False
#         i += 6
#         k -= 1
#     return True

# def get_random_hash_function(m, is4UHash = False):
#     n = random.getrandbits(32)
#     if n < 0: 
#         n = -n 
#     if n % 2 == 0:
#         n = n + 1
#     while not isPrime(n, 20):
#         n = n + 1
#     a = random.randint(2, n-1)
#     b = random.randint(2, n-1)
#     if is4UHash:
#         c = random.randint(2, n-1)
#         d = random.randint(2, n-1)
#         return (n, a, b, c, d, m)
#     else:
#         return (n, a, b, m)

# # 2 universal hash function
# def hashfun(hfun_rep, num):
#     if len(hfun_rep) > 5:
#         (p, a, b, c, d, m) = hfun_rep
#         return (((a * (num ** 3)) + (b * (num ** 2)) + (c * num) + d) % p) % m
#     else:
#         (p, a, b, m) = hfun_rep
#         return ((a * num + b) % p) % m

# # hash function for a string.
# def hash_string(hfun_rep, hstr):
#     n = hash(hstr)
#     return hashfun(hfun_rep, n)

# class CountMin:
#     def __init__ (self, num_counters):
#         self.m = num_counters
#         self.hash_fun_rep = get_random_hash_function(num_counters)
#         self.counters = [0]*self.m

#     # function: increment 
#     # given a word, increment its count in the countmin sketch
#     def increment_plength(self, word, packet_length):
#         self.counters[hash_string(self.hash_fun_rep, word)%self.m] = self.counters[hash_string(self.hash_fun_rep, word)%self.m] + packet_length
        
#     def increment(self, word):
#         self.counters[hash_string(self.hash_fun_rep, word)%self.m] = self.counters[hash_string(self.hash_fun_rep, word)%self.m] + 1

#         #return None
    
#     def approximateCount(self, word):   
#         return self.counters[hash_string(self.hash_fun_rep, word)%self.m]

# # Count-Min Sketch    
# class CountMinSketch:
#     # Initialize k different counters
#     def __init__(self, k ,m):
#         self.count_min_sketches = [CountMin(m) for i in range(k)]
#     # Function increment_counters
#     # increment each of the individual counters with the word
#     def increment_counters(self, word, packet_length = None):
#         if packet_length != None:
#             for i in range(len(self.count_min_sketches)):
#                 self.count_min_sketches[i].increment_plength(word,packet_length)    
#         else:
#             for i in range(len(self.count_min_sketches)):
#                 self.count_min_sketches[i].increment(word)      
#     def approximate_count(self, word):
#         return min([cms.approximateCount(word) for cms in self.count_min_sketches])

# # Flajolet-Martin Sketch
# class FlajoletMartinSketch:
#     def __init__(self, k, m):
#         self.k = k # bit
#         self.m = m #array
#         self.bitmaps = [[0] * k for _ in range(m)]  # Initialize m k-bit wide bitmaps to all zeros
#         self.hash_fun_reps = [get_random_hash_function(m) for _ in range(k)]
#         self.max_trailing_zeros = [0] * k
    
#     def add_element(self, element):
#         for i in range(self.k):
#             h = hash_string(self.hash_fun_reps[i], element)
#             bitmap_index = self.get_bitmap_index(h)
#             run_length = self.run_of_zeros(h)
#             if bitmap_index < self.m and run_length < self.k:  # Check bounds before assignment
#                 self.bitmaps[bitmap_index][run_length] = 1
#                 self.max_trailing_zeros[i] = max(self.max_trailing_zeros[i], run_length)
    
#     def get_bitmap_index(self, h):
#         return h & ((1 << self.m) - 1)
    
#     def run_of_zeros(self, h):
#         mask = (1 << self.m) - 1
#         trailing_zeros = 0
#         while (h & 1) == 0 and mask > 0:
#             trailing_zeros += 1
#             h >>= 1
#             mask >>= 1
#         return min(trailing_zeros, self.k)
    
#     def estimate_cardinality(self):
#         phi = 0.77351  # A constant factor used in the estimation
#         sum_least_sig_bits = sum(self.least_sig_bit(bitmap) for bitmap in self.bitmaps)
#         avg_trailing_zeros = sum_least_sig_bits / float(self.m)
#         return self.m / phi * 2 ** avg_trailing_zeros
    
#     def least_sig_bit(self, bitmap):
#         return next((i for i, bit in enumerate(bitmap) if bit == 1), 0)
    
#     def print_bitmaps(self):
#         print("Bitmaps:")
#         for i, bitmap in enumerate(self.bitmaps):
#             formatted_bitmap = ' '.join(map(str, bitmap))  # Convert each bit to string and join with space
#             print(f"Bitmap {i}: {formatted_bitmap.rjust(self.k * 2)}")  # Right-align each bitmap

import random
import numpy as np
from .prng import PRNG


class FlajoletMartinSketch:
    # def __init__(self, distinct_width,fmsize,seed = 7727):
    #     self.fmsize = fmsize
    #     self.distinct_width = distinct_width
    #     self.fm = [0] * fmsize
    #     random.seed(seed)
    #     self.hasha = [random.randint(0, 2**32 - 1) for _ in range(fmsize)]
    #     self.hashb = [random.randint(0, 2**32 - 1) for _ in range(fmsize)]
    def __init__(self, distinct_width,fmsize,seed = 7727):
            self.fmsize = fmsize
            self.distinct_width = distinct_width
            self.fm = [0] * fmsize
            prng = PRNG(seed=seed, usenric=2)
            # self.hasha = [prng.prng_int() for _ in range(fmsize)]
            # self.hashb = [prng.prng_int() for _ in range(fmsize)]
            self.hasha = []
            self.hashb = []
            for _ in range(fmsize):
                hasha_value = prng.prng_int() & 0xFFFFFFFF
                hashb_value = prng.prng_int() & 0xFFFFFFFF
                
                # print(f'hasha[{_}] = {hasha_value}')
                # print(f'hashb[{_}] = {hashb_value}')
                
                self.hasha.append(hasha_value)
                self.hashb.append(hashb_value)
        
    def zeros_slow(self, test):
        bits = 32
        if test == 0:
            return bits
        for i in range(bits):
            if (test & 1) == 1:
                break
            test >>= 1
        return i
        
    def hash31(self, a, b, x):
        # Calculate the hash
        result = (a * x) + b
        result = ((result >> 31) + result) & (2**31 - 1)
        return result
    # def hash31(self, a, b, x):
    #     return ((a * x + b) % (2**31 - 1))

    def add_element(self, item):
        item = item
        for i in range(self.fmsize):
            hash_value = self.hash31(self.hasha[i], self.hashb[i], item)
            self.fm[i] |= (1 << self.zeros_slow(hash_value))

    def estimate_cardinality(self):
        bits = self.distinct_width
        result = 0.0
        for i in range(self.fmsize):
            max_val = bits
            bitmap = self.fm[i]
            for j in range(bits - 1, -1, -1):
                if ((bitmap >> j) & 1) == 0:
                    max_val = j
            result += float(max_val)
        result = result / self.fmsize
        result = 1.2928 * pow(2.0, result)
        return result

    def fm_destroy(self):
        del self.fm


class CountMinSketch:
    def __init__(self, depth, width, seed = 7727):
        self.width = width
        self.depth = depth
        self.count = 0
        self.counts = np.zeros((depth, width), dtype=int)
        # random.seed(seed)
        # self.hasha = [random.randint(0, 2**31 - 1) for _ in range(depth)]
        # self.hashb = [random.randint(0, 2**31 - 1) for _ in range(depth)]
        prng = PRNG(seed= (-abs(seed)), usenric=2)
        self.hasha = []
        self.hashb = []
        for _ in range(depth):
            hasha_value = prng.prng_int()
            hashb_value = prng.prng_int()
            
            # print(f'hasha[{_}] = {hasha_value}')
            # print(f'hashb[{_}] = {hashb_value}')
            
            self.hasha.append( (hasha_value & (2**31 - 1) ) )
            self.hashb.append( (hashb_value & (2**31 - 1) ))
        
    
    # def hash31(self, a, b, x):
    #     return ((a * x + b) % (2**31 - 1))
    def hash31(self, a, b, x):
        # Calculate the hash
        result = (a * x) + b
        result = ((result >> 31) + result) & (2**31 - 1)
        #print(result,a,b,x)
        return result
        
    def increment_counters(self, item, diff):
        # item = hash(item)
        self.count += diff
        for j in range(self.depth):
            self.counts[j][self.hash31(self.hasha[j], self.hashb[j], item) % self.width] += diff

    def approximate_count(self, query):
        # query = hash(query)
        ans = self.counts[0][self.hash31(self.hasha[0], self.hashb[0], query) % self.width]
        for j in range(1, self.depth):
            ans = min(ans, self.counts[j][self.hash31(self.hasha[j], self.hashb[j], query) % self.width])
        return ans

    def size(self):
        counts = self.width * self.depth * np.dtype(int).itemsize
        hashes = self.depth * 2 * np.dtype(int).itemsize
        return counts + hashes

    def copy(self):
        cm_copy = CountMinSketch(self.width, self.depth, 0)
        cm_copy.counts = np.copy(self.counts)
        cm_copy.hasha = self.hasha[:]
        cm_copy.hashb = self.hashb[:]
        cm_copy.count = self.count
        return cm_copy
    
    def unique_row_count(self, row):
        return np.sum(self.counts[row] > 0)


    @staticmethod
    def compatible(cm1, cm2):
        if cm1.width != cm2.width or cm1.depth != cm2.depth:
            return False
        if cm1.hasha != cm2.hasha or cm1.hashb != cm2.hashb:
            return False
        return True

    @staticmethod
    def inner_product(cm1, cm2):
        if not CountMinSketch.compatible(cm1, cm2):
            return 0
        result = np.dot(cm1.counts[0], cm2.counts[0])
        for j in range(1, cm1.depth):
            tmp = np.dot(cm1.counts[j], cm2.counts[j])
            result = min(tmp, result)
        return result

    def residue(self, Q):
        bitmap = np.zeros(self.width, dtype=bool)
        estimate = 0
        for j in range(self.depth):
            nextest = 0
            bitmap.fill(False)
            for i in range(1, Q[0]):
                bitmap[hash31(self.hasha[j], self.hashb[j], Q[i]) % self.width] = True
            for i in range(self.width):
                if not bitmap[i]:
                    nextest += self.counts[j][i]
            estimate = max(estimate, nextest)
        return estimate

