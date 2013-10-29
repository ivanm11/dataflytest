PROJECT SETUP
=============

To create new project and setup basic workspace for frontend developer follow
these steps:

1) Create new Bitbucket repo under *df-sean* user (let's call it `new-project.git`) 
[https://bitbucket.org/repo/create](https://bitbucket.org/repo/create)

2) Follow "I'm starting from scratch" Bitbucket guide:  

```bash
  mkdir /path/to/your/project
  cd /path/to/your/project
  git init
  git remote add origin ssh://git@bitbucket.org/df-sean/new-project.git  
```

Copy /frontend folder from DataFly Starter and make initial commit:

```bash
  cp -r starter/new_project/frontend new-project/
  git add .
  git commit -m "Initial commit"
  git push origin master
```

3) Go to "Access management" in Bitbucket repo "Administration", grant access
to developer with "Write" permissions.

4) Send a link to Bitbucket repo and a link to Frontend Developer Guide:  
[http://doc.datafly.net/frontend-guide?password=WeL1C00Me](http://doc.datafly.net/frontend-guide?password=WeL1C00Me)

5) Check results by pulling commits and running app on localhost:

```bash
/path/to/your/project/frontend$ python app.py
```