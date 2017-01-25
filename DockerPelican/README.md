# blog
A pelican based blog: [http://doctimjones.org](http://doctimjones.org)

## Running 

### development
```
git@github.com:doctimjones/blog.git
cd blog
docker build -t blog .
docker run --rm -i -t -p 8888:8000 --name blog-latest blog
```

### production
```
git clone https://github.com/doctimjones/blog.git
cd blog/blog
sed -i.bak 's/http:\/\/localhost:18888\//http:\/\/doctimjones.org\//' pelicanconf.py
sed -i.bak 's/http:\/\/localhost:18888\//http:\/\/doctimjones.org\//' publishconf.py
cd ..
docker build -t blog-prod .
docker run --rm -d -p 80:8000 --name blog-live blog-prod
```

```
git submodule init
git submodule update
virtualenv -p python3 venv
python /Users/d7082791602/Git/blog/DockerPelican/pip/venv/bin/pelican content -s publishconf.py
```