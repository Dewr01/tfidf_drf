FROM gitpod/workspace-python

RUN sudo apt-get update && sudo apt-get install -y redis-server