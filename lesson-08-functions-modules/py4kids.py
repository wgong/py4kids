# useful functions created for py4kids class
version = 1.0

g_lang_dic = {'chn':'您好', 'eng':'Hello'}

# this function does nothing
def dummy_function():
    pass

def greeting(name):
    print('Hi, %s' % name)

# this function creates a list of integer numbers
def create_integer_list(start, stop, stride=1):
    return list(range(start, stop, stride))

def create_real_list(start, stop, stride):
    import numpy as np
    return np.arange(start, stop, stride)

# this function has error handling to avoid crash
def create_real_list2(start, stop, stride):
    import numpy as np
    if stride != 0.0:
        return np.arange(start, stop, stride)
    else:
        print('[ERROR] stride is zero')
        return None
  
# this function is useful to detect if a string is written in Chinese
def is_chinese(s):
    return all(u'\u4e00' <= c <= u'\u9fff' for c in s)

def greeting2(name):
    lang_dic = {'chn':'你好', 'eng':'Hello'}
    if is_chinese(name):
        print(lang_dic['chn'], ', ', name)
    else:
        print(lang_dic['eng'], ', ', name)
  
def greeting3(name):
    if is_chinese(name):
        print(g_lang_dic['chn'], ', ', name)
    else:
        print(g_lang_dic['eng'], ', ', name)
        
def pythagorean(a,b,c):
    import math
    if c is None and a is not None and b is not None:
        return math.sqrt(a**2 + b**2)
    elif a is None and b is not None and c is not None and c >= b:
        return math.sqrt(c**2 - b**2)
    elif b is None and a is not None and c is not None and c >= a:
        return math.sqrt(c**2 - a**2)
    else:
        return "No solution"

def quad_eq(a, b, c):
    """
    Solving a quadratic equation:
        https://www.wikiwand.com/en/Quadratic_equation
    """
    if a == 0.0:
        if b == 0.0:
            print('Both a and b are zero, no solution')
            return None
        else:
            x = - c/b
            return x
    else:
        import math
        x1 = (-b + math.sqrt(b**2 - 4*a*c)) / (2.0*a) 
        x2 = (-b - math.sqrt(b**2 - 4*a*c)) / (2.0*a) 
        return [x1, x2]
