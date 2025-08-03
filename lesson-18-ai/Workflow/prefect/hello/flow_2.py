from prefect import flow, task

@task
def get_customer_ids():
    return ["customer1", "customer2", "customer3"]

@task
def process_customer(customer_id):
    return f"Processed {customer_id}"

@flow
def main():
    customer_ids = get_customer_ids()
    results = process_customer.map(customer_ids)
    actual_results = [future.result() for future in results]
    return actual_results

if __name__ == "__main__":
    flow_result = main()
    print("Actual results:", flow_result)