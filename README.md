# Sketches Overview

## Count-Min (CM) Sketch
The Count-Min Sketch is a probabilistic data structure used for frequency estimation. It provides a compact representation of the frequencies of elements in a data stream, allowing for approximate query results with controlled error margins. It is particularly useful for large-scale data processing where exact counting is infeasible due to memory constraints.

### CM Sketch Example Usage

```python
# CM(depth, width, seed = 7727)
cms = CountMinSketch(11, 200)
for word in lines_list:
    # print(int(word))
    cms.increment_counters(int(word), 1)
cm_counts = cms.approximate_count(1650614882)
print(cm_counts)
```

## Flajolet-Martin (FM) Sketch
The Flajolet-Martin Sketch (Probabilistic Counting with Stochastic Averaging) is used for approximating the number of distinct elements in a dataset. It is based on hash functions and provides an efficient way to estimate the cardinality of large datasets with limited memory usage.

```python

from flajolet_martin_sketch import FlajoletMartinSketch

# Sample data
lines_list = [...]  # Replace with your data

# Initialize FM Sketch
fm_bits = 8
fm_n = 3
fm = FlajoletMartinSketch(fm_bits, fm_n)

# Add elements to the sketch
for i in lines_list:
    fm.add_element(int(i))

# Estimate and print the number of distinct elements
print("Approximate number of distinct elements:", fm.estimate_cardinality())

```

#### Note: The random generator that is used in the sketch is the converted prng.c file of the original author. The case that is used and tested based on the original code is the case 2. 

## Reference
The original code and additional details can be found at [DIMACS - Code by Graham Cormode.](https://www.dimacs.rutgers.edu/~graham/code/)



