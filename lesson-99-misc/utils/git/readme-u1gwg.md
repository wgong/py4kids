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

- how to delete github repo:
https://zapier.com/blog/github-delete-repository/
