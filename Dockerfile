FROM python:3.7.4

RUN apt update
RUN apt install -y git
RUN apt install -y nodejs npm
RUN npm install -g uglify-js
RUN npm install -g babel-cli@6 babel-preset-react-app
ENV PYTHONPATH "${PYTHONPATH}:/pelican-plugins"
RUN git clone https://github.com/getpelican/pelican-plugins.git /pelican-plugins
WORKDIR /pelican-plugins
RUN git checkout 0b9e66ee
RUN git submodule update --recursive
RUN mkdir /entilzha.github.io
WORKDIR /entilzha.github.io
ADD requirements.txt .
RUN pip install -r requirements.txt

CMD ["pelican"]
