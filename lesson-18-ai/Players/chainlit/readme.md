

### setup 
```
conda create -n chainlit python=3.11

mkdir ~/Documents/Dad/0_Biz/Duck-AI/AIApps

cd ~/projects/AI

git clone git@github.com:wgong/chainlit.git
git clone git@github.com:wgong/chainlit_cookbook.git


```


### Test

chainlit run app-01.py

```
[2024-11-20 20:20:22] Starting 'chainlit' ...
[2024-11-20 20:20:27] sleeper_0 (S): 	SYNC slept 5 sec 	[2024-11-20 20:20:22] ==> [2024-11-20 20:20:27]
[2024-11-20 20:20:29] sleeper_1 (A): 	ASYNC slept 2 sec 	[2024-11-20 20:20:27] ==> [2024-11-20 20:20:29]
[2024-11-20 20:20:33] sleeper_2 (A): 	ASYNC slept 4 sec 	[2024-11-20 20:20:29] ==> [2024-11-20 20:20:33]
[2024-11-20 20:20:36] sleeper_3 (S): 	ASYNC slept 3 sec 	[2024-11-20 20:20:33] ==> [2024-11-20 20:20:36]
[2024-11-20 20:20:43] sleeper_4 (A): 	SYNC slept 7 sec 	[2024-11-20 20:20:36] ==> [2024-11-20 20:20:43]
[2024-11-20 20:20:43] Done processing !!!
```

https://github.com/Chainlit/chainlit/issues/1538

```
python app-02.py
```

