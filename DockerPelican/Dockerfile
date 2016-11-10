FROM ubuntu:15.10
MAINTAINER Tim Jones (tdj28@github)

# docker build -t blog .

# interactive:
# docker run --rm -i -t -p 8888:8000 --name blog-latest blog

# docker run -d -p 80:8000 --restart=always --name blog-latest blog

ENV DEBIAN_FRONTEND noninteractive

# R 
RUN sh -c 'echo "deb http://cran.rstudio.com/bin/linux/ubuntu trusty/" >> /etc/apt/sources.list'
RUN gpg --keyserver keyserver.ubuntu.com --recv-key E084DAB9
RUN gpg -a --export E084DAB9 | apt-key add -

# Debian packages
COPY ./apt/packages.txt /usr/local/packages.txt
RUN apt-get update && cat /usr/local/packages.txt | xargs apt-get install -yq

# Pip packages
WORKDIR /usr/local/
RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python get-pip.py
COPY ./pip/requirements.txt /usr/local/requirements.txt
RUN pip --no-cache-dir install -r /usr/local/requirements.txt

# Set up supervisor
RUN mkdir -p /var/log/supervisor
RUN mkdir -p /var/log/supervisor/conf.d
COPY ./supervisor/pelican.conf /etc/supervisor/conf.d/pelican.conf

# Set up blog content

RUN mkdir -p /usr/local/blog/plugins
WORKDIR /usr/local/blog/plugins
RUN git clone https://github.com/danielfrg/pelican-ipynb.git ipynb
WORKDIR /usr/local/blog
#RUN git clone --recursive https://github.com/getpelican/pelican-themes/octopress
RUN git clone https://github.com/duilio/pelican-octopress-theme.git
RUN mkdir pelican-themes
RUN mv pelican-octopress-theme pelican-themes/octopress
# Need jquery for BokehJS to work
RUN sed -i.bak 's/<\/head>/<script src="http:\/\/ajax.googleapis.com\/ajax\/libs\/jquery\/1.11.0\/jquery.min.js"><\/script><\/head>/' /usr/local/blog/pelican-themes/octopress/templates/base.html

COPY ./blog/content /usr/local/blog/content
COPY ./blog/pelicanconf.py /usr/local/blog/pelicanconf.py
COPY ./blog/publishconf.py /usr/local/blog/publishconf.py
WORKDIR /usr/local/blog
RUN /usr/bin/python /usr/local/bin/pelican content -s publishconf.py

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf", "-n"]
