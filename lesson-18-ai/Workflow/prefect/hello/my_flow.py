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
  print("Flow executed successfully!")