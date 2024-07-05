# Git Tips
- how to access 2 github accounts from your PC:
https://code.tutsplus.com/quick-tip-how-to-work-with-github-and-multiple-accounts--net-22574t
  - in .ssh folder, create `config` file, name 2nd account host as `github.com-work`
  - git clone git@`github.com-work`:gongwork/st_rag.git  # use 2nd host

- With two GitHub accounts: wgong, gongwork
  - use two different browsers: e.g wgong in Brave, gongwork in Chrome
  - Use git:
    - git clone git@github.com:wgong/embedchain.git (into wgong account)
    - git clone git@github.com-work:gongwork/embedchain.git (into gongwork account, Note: `-work` suffix configured inside `.ssh` folder)

  - clone:
    - git clone git@github.com-work:gongwork/data-copilot.git
    - git add .
    - git commit -m "init"
    - git push

- how to delete github repo:
https://zapier.com/blog/github-delete-repository/

- how to add SSH key
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
```
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

- how to avoid prompting pwd
https://stackoverflow.com/questions/7773181/git-keeps-prompting-me-for-a-password

  - add SSH key to github.com 
  - ensure local `.git/config` file as
```
[remote "origin"]
        ## url = https://github.com/wgong/py4kids.git
        url = ssh://git@github.com/wgong/py4kids.git
        fetch = +refs/heads/*:refs/remotes/origin/*

```