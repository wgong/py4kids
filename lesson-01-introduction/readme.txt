### [Tutorial: Setting up Python enviroments with Mambaforge](https://ross-dobson.github.io/posts/2021/01/setting-up-python-virtual-environments-with-mambaforge/)

Use micromamba::

https://mamba.readthedocs.io/en/latest/micromamba-installation.html#umamba-install

use git-bash
"${SHELL}" <(curl -L micro.mamba.pm/install.sh)
micromamba bin folder ~/.local/bin
Prefix location? [~/micromamba]

Setting mamba executable to: "C:\\Users\\p2p2l\\.local\\bin\\micromamba"
Adding (or replacing) the following in your "C:\\Users\\p2p2l\\.bash_profile" file

# >>> mamba initialize >>>
# !! Contents within this block are managed by 'mamba init' !!
export MAMBA_EXE='/c/Users/p2p2l/.local/bin/micromamba';
export MAMBA_ROOT_PREFIX='/c/Users/p2p2l/micromamba';
eval "$("$MAMBA_EXE" shell hook --shell bash --root-prefix "$MAMBA_ROOT_PREFIX")"
# <<< mamba initialize <<<

launch a new gitbash
$ micromamba create -n st

$ micromamba env list
  Name  Active  Path
-------------------------------------------------------
                C:\Users\p2p2l\anaconda3\envs\duck090
                C:\Users\p2p2l\anaconda3\envs\gradio
                C:\Users\p2p2l\anaconda3\envs\st
  base          C:\Users\p2p2l\micromamba
  st            C:\Users\p2p2l\micromamba\envs\st

$ cd ~/lesson-99-misc/benchmark
$ micromamba create -n py311 python=3.11
$ micromamba activate py311
$ python --version
Python 3.11.6
$ python bench.py 
1.8258523999829777 1.8263571000134107 1.8272148000251036 # py3.11
1.8920940999999978 1.8966619999999992 1.901398900000002  # py3.9

$ pip show streamlit
Name: streamlit
Version: 1.25.0

$ edit ~/.bash_profile

$ ln -s ~/.local/bin/micromamba ~/.local/bin/mamba
export PATH=$PATH:~/.local/bin

$ micromamba deactivate
$ micromamba env remove -n ENVNAME`
$ micromamba activate nicegui
$ pip install -r list.txt # install a list of packages
$ pip freeze > list.txt # export a list of packages to a file

$ micromamba env list
  Name  Active  Path
-------------------------------------------------------
                C:\Users\p2p2l\anaconda3\envs\duck090
                C:\Users\p2p2l\anaconda3\envs\gradio
                C:\Users\p2p2l\anaconda3\envs\st
  base          C:\Users\p2p2l\micromamba
  st            C:\Users\p2p2l\micromamba\envs\st

$ micromamba create -n py311 python=3.11

### Installing mamba on a machine with conda
```
## prioritize 'conda-forge' channel
conda config --add channels conda-forge

## update existing packages to use 'conda-forge' channel
conda update -n base --all

## install 'mamba'
conda install -n base mamba

## Now you can use mamba instead of conda.
```
failed

