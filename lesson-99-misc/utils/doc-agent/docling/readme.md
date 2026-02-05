# [docling](https://pypi.org/project/docling/)

SDK and CLI for parsing PDF, DOCX, HTML, and more, to a unified document representation for powering downstream workflows such as gen AI applications.

## Setup
```
conda activate ag2
pip install docling
cd ~/projects/wgong/py4kids/lesson-99-misc/docling

cp ~/projects/wgong/AG2/ag2/test/agentchat/contrib/graph_rag/Toast_financial_report.pdf data/

```


## Errors

### test-1

```
The following error(s) have occurred:
- Data Ingestion Task Failed, Error 'ascii' codec can't encode character '\u2612' in position 126: ordinal not in range(128): '../test/agentchat/contrib/graph_rag/Toast_financial_report.pdf'
```

### test-2
```
The following error(s) have occurred:
- Data Ingestion Task Failed, Error 'ascii' codec can't encode character '\u2019' in position 3166: ordinal not in range(128): 'https://www.independent.co.uk/space/earth-core-inner-shape-change-b2695585.html'
```