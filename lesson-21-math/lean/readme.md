```bash
elan default stable

lean --help

cd ~/projects/AI-Tools/

git clone git@github.com:wgong/mathematics_in_lean.git

cd mathematics_in_lean
cd MIL/C01_Introduction
lean S01_Getting_Started.lean



# lake env lean --run MIL/C01_Introduction/S02_Overview.lean 

```

```output
2 + 2 : ℕ
f (x : ℕ) : ℕ
2 + 2 = 4 : Prop
FermatLastTheorem : Prop
easy : 2 + 2 = 4
MIL/C01_Introduction/S02_Overview.lean:27:8: warning: declaration uses `sorry`
hard : FermatLastTheorem
(interpreter) unknown declaration 'main'
```