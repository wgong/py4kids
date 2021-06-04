def fib(n):
    old, new = 0, 1
    for _ in range(n):
        old, new = new, old + new
    return old


def max(values):
  _max = values[0]
  for val in values[1:]:
      if val > _max:
          _max = val
  return _max


def min(values):
  _min = values[0]
  for val in values[1:]:
      if val < _min:
          _min = val
  return _min


def sel_sort(data):
  if not isinstance(data, list):
      vals = list(data)
  else:
      vals = data

  size = len(vals)
  for i in range(size):
      for j in range(i+1, size):
          if vals[j] < vals[i]:
              _min = vals[j]
              vals[j] = vals[i]
              vals[i] = _min
  return vals

def is_palindrome(val):
    return val == val[::-1]