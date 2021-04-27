# IMDB Movie Analyzer

Welcome All! This is my IMDB Analyzer

## Usage

```sh
git clone https://github.com/HarryCaveMan/imdb_analysis
cd imdb_analysis/src/python/imdb_analyzer
pip3 install -r analyzer-reqs.txt
pytest --cov=analyzer test/analyzer/
python3 -m analyzer
```

Minus pip, this should an out very similar to the following:

`pytest --cov=analyzer test/analyzer/`:
```txt
platform linux -- Python 3.6.9, pytest-6.2.3, py-1.10.0, pluggy-0.13.1
rootdir: /home/harris/Documents/RedHat/imdb_roi_analysis/src/python/imdb_analyzer
plugins: cov-2.11.1
collected 3 items

test/analyzer/test_analyzer.py .                                                                                          [ 33%]
test/analyzer/test_file_utils.py .                                                                                        [ 66%]
test/analyzer/test_main.py .                                                                                              [100%]

----------- coverage: platform linux, python 3.6.9-final-0 -----------
Name                        Stmts   Miss  Cover
-----------------------------------------------
analyzer/__init__.py            2      0   100%
analyzer/__main__.py           21      2    90%
analyzer/analyzer_core.py      23      0   100%
analyzer/file_utils.py         29      3    90%
-----------------------------------------------
TOTAL                          75      5    93%


========================== 3 passed in 0.76s ==========================
```

`python3 -m analyzer`:
```txt
                        gross       budget  gross_profit
actor_name
Gloria Stuart     658672302.0  200000000.0   458672302.0
Peter Cushing     460935665.0   11000000.0   449935665.0
Niketa Calame     422783777.0   45000000.0   377783777.0
Anthony Reynolds  205253180.5   78000000.0   329999255.0
Stefan Kapicic    363024263.0   58000000.0   305024263.0
Bob Peck          356784000.0   63000000.0   293784000.0
Keir O'Donnell    350123553.0   58800000.0   291323553.0
Conrad Vernon     436471036.0  150000000.0   286471036.0
Sam Anderson      329691196.0   55000000.0   274691196.0
Anthony Daniels   290158751.0   18000000.0   272158751.0
                           gross        budget  gross_profit
actor_name
Harrison Ford       3.479593e+09  1.446377e+09  2.033216e+09
Scarlett Johansson  4.231205e+09  2.376500e+09  1.854705e+09
Robert Downey Jr.   4.162541e+09  2.407000e+09  1.755541e+09
Tom Hanks           3.612647e+09  1.884000e+09  1.728647e+09
Steve Carell        2.154597e+09  8.900000e+08  1.264597e+09
Morgan Freeman      3.938459e+09  2.703900e+09  1.234559e+09
Bradley Cooper      2.056793e+09  8.258000e+08  1.230993e+09
Jennifer Lawrence   2.367856e+09  1.182150e+09  1.185706e+09
John Ratzenberger   2.509861e+09  1.365000e+09  1.144861e+09
Robert Pattinson    1.841497e+09  7.120000e+08  1.129497e+09
```

# Bonus Server

The bonus question I was most excited about was the api server. I decided to use fastapi/uvicorn, with gunicorn as the process manager and an nginx reverse proxy. I started by setting up just a single test endpoint to verify the stack. Then I realized it did not say which information to get, so I just had pandas return all the rows that actor was in either the `actor_1_name` `actor_2_name` or `actor_3_name` column as an html table (pretty neat it does that for you). I also implemented the first 2 questions path-parameterized endpoints to return thr top `n` genres and actors.

## Building the server

From the repo-s root, just run 

```sh
# You can use any tag you like
docker build -t imdb_analyzer .
```

## Running the server

I chose not to pack the entire data file into the container to simulate how it might read in a file from a remote or even distributed file store, so you can attach the data volume to the default data dir for the application, which is `/opt/imdb_analyzer/data`. Here's an example run command that would work from repo root if you tagged your container with `imdb_analyzer` as shown above:

```sh
# run as daemon (-d instead -it) if you don't want app logs
# use -p 80:8080 because nginx configured to listen http on 80 (see /etc/ngix/nginx.conf in repo)
docker run -it -v `pwd`/data:/opt/imdb_analyzer/data -p 80:8080 imdb_analyzer
```


## Notes on possible improvements:

- Better server logging
- Use generators more instead of in-memory iterables
- Integration tests for server (or even mock unit tests)
- Deploy to openshift