# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#   This is a document about gits
#   You can learn:
#   1, Basic commands for pushing code to origin
#   2, Further step in command
#   3, Setup gits server in linux
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # #


# easy work flow
$ git remote add origin git@github.com:michaelliao/learngit.git
$ git add .
$ git commit -m 'reason to commit'
$ git push origin master

# create global storage for secret order
$ git config --global credential.helper store

# basic configure after you installed gits
$ git config --global user.name "Your Name"
$ git config --global user.email "email@example.com"
$ ssh-keygen -t rsa -C "youremail@example.com"