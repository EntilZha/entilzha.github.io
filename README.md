# Building Website

To build my website there are two commands to run.
For my sanity, I've encoded all the dependencies in a Dockerfile so the website can be fully built from that.

1. To build the docker container run `docker build -t pelican .`
2. To run pelican commands, use `./penguin` instead of `pelican`
3. To run the publishing script, run `./publish.sh`