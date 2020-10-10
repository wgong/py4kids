import os
import shutil
import re

basedir = '.'

len1 = 8
pat1 = re.compile("^[0-9]{8}")

len2 = 6
pat2 = re.compile("^[0-9]{6}")

len3 = 4
pat3 = re.compile("^[0-9]{4}")

pat4 = re.compile(r"^(([0-9]{4}-[0-9]{2}-[0-9]{2})|([0-9]{4}-[0-9]{2}))")

def refmt_date(fn0):
  global len1,len2,len3,pat1,pat2,pat3,pat4
  if re.match(pat4, fn0):
    return fn0
    
  m = re.match(pat1, fn0)
  if m:
    if len(fn0)> len1:
      fn = f"{m[0][:4]}-{m[0][4:6]}-{m[0][6:len1]}-{fn0[len1:]}"
    else:
      fn = f"{m[0][:4]}-{m[0][4:6]}-{m[0][6:len1]}"
  else:
    m = re.match(pat2, fn0)
    if m:
      if len(fn0)> len2:
        fn = f"{m[0][:4]}-{m[0][4:len2]}-{fn0[len2:]}"
      else:
        fn = f"{m[0][:4]}-{m[0][4:len2]}"
    else:
      m = re.match(pat3, fn0)
      if m:
        if len(fn0)> len3:
          fn = f"{m[0][:len3]}-{fn0[len3:]}"
        else:
          fn = f"{m[0][:len3]}"
      else:
        fn = fn0
  return fn

for fn in os.listdir(basedir):
  if not os.path.isdir(os.path.join(basedir, fn)):
    continue # Not a directory
  fn2 = refmt_date(fn)
  if fn == fn2:
    continue

  from_dir = os.path.join(basedir, fn)
  to_dir = os.path.join(basedir, fn2) 
  print(f"cp -rf {from_dir} {to_dir}\n")

  os.system(f"cp -rf {from_dir} {to_dir}")
  os.system(f"rm -rf {from_dir}")
