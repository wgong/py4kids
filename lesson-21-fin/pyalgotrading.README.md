## GitHub

https://github.com/wgong/pyalgotrade

https://www.algobulls.com/

https://algobulls.github.io/pyalgotrading/introduction/

## Documentation

https://gbeced.github.io/pyalgotrade/docs/v0.20/html/index.html

### Tutorial

https://gbeced.github.io/pyalgotrade/docs/v0.20/html/tutorial.html

### Sample

pyalgotrade/samples/tutorial-2-wg.py

#### datafeed

```
python -m "pyalgotrade.tools.quandl" --source-code="WIKI" --table-code="ORCL" --from-year=2000 --to-year=2000 --storage=. --force-download --frequency=daily [--auth-token=<Quandl-API-Token>]

```

which will save quotes into file ``WIKI-ORCL-2000-quandl.csv`` in current folder
