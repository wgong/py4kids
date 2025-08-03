## Setup

```bash
# setup
$ pip install prefect
```

## create a project 

```bash
$ mkdir hello
$ cd hello
$ prefect init --name hello
```

Write Your First Flow (`my_flow.py`) by defining tasks and flows with decorators

```python
from prefect import flow, task

@task
def my_task():
  return "Hello"

@flow
def main():
  result = my_task()
  print(result)

if __name__ == "__main__":
  main()
```

## Test & Deploy

```bash
# Test 
$ python my_flow.py

# Create deployment config
# You can also make changes to this deployment configuration by making changes to the prefect.yaml file.
$ prefect deploy my_flow.py:main --name my_deployment

$ prefect deploy -n my_deployment

# To execute flow runs from this deployment, start a worker in a separate terminal that pulls work from the 'test_flow' work pool:
$ prefect worker start --pool 'test_flow'

# To schedule a run for this deployment, use the following command:
$ prefect deployment run 'main/my_deployment'

```

## Upgrade to v3

```bash
pip install -U prefect   # 3.4.11
prefect server database upgrade

# optional
pip install -U 'prefect[aws]'
# Prefect database at sqlite+aiosqlite:////home/papagame/.prefect/prefect.db upgraded!
```