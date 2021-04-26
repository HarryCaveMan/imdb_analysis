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