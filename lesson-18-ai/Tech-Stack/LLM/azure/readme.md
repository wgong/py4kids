# Getting an Azure OpenAI API Key

Getting an Azure OpenAI API key involves a few steps, primarily centered around having an Azure subscription and creating an Azure OpenAI resource.

**Prerequisites:**

1.  **Azure Subscription:** You need an active Azure subscription. If you don't have one, you can sign up for a free Azure account, which often includes free credits. However, be aware that sometimes Azure OpenAI services require a paid account or specific approval.
2.  **Access Approval:** Azure OpenAI Service is often restricted and requires you to fill out a registration form to get access. This is to ensure responsible AI usage. You might need to wait for approval after submitting the form.

**Steps to get your Azure OpenAI Key:**

1.  **Sign in to Azure Portal:**
    Go to the Azure portal: [portal.azure.com](https://portal.azure.com/). Log in with your Microsoft account credentials.

2.  **Create an Azure OpenAI Resource:**

      * In the Azure portal, use the search bar at the top to search for "Azure OpenAI".
      * Select "Azure OpenAI" from the search results.
      * Click on **"Create"** to create a new Azure OpenAI resource.
      * Fill in the required details:
          * **Subscription:** Choose your active Azure subscription.
          * **Resource Group:** Create a new resource group or select an existing one. A resource group helps organize your Azure resources.
          * **Region:** Select a region that is geographically close to you or your users for lower latency. Note that not all models are available in all regions.
          * **Name:** Provide a unique name for your Azure OpenAI resource.
          * **Pricing tier:** Choose a pricing tier (e.g., Standard S0).
      * Review your selections and click **"Create"**. The deployment might take a few minutes.

3.  **Go to the Resource and Find Keys and Endpoint:**

      * Once the deployment is complete, click **"Go to resource"** on the deployment completion screen.
      * On the left-hand navigation menu of your Azure OpenAI resource, under "Resource Management", click on **"Keys and Endpoint"**.

4.  **Copy Your API Key and Endpoint:**

      * On this page, you will see two API keys (Key 1 and Key 2) and your Endpoint URL.
      * **Copy either Key 1 or Key 2.** Both keys are valid, and having two allows for key rotation without service interruption.
      * **Copy the Endpoint URL.** You will need both the key and the endpoint URL to make API calls to your Azure OpenAI models.

**Example of how to use the key and endpoint in code (Python):**

```python
import openai
import os

# Set your Azure OpenAI API key and endpoint
openai.api_key = os.getenv("AZURE_OPENAI_KEY") # It's best practice to use environment variables
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = "azure"
openai.api_version = "2023-05-15" # Or the latest supported API version

# Your deployment name (you'll create this in Azure OpenAI Studio)
deployment_name = "your-deployment-name" # e.g., "gpt-35-turbo-deployment"

response = openai.Completion.create(
    engine=deployment_name,
    prompt="Hello, what is the capital of France?",
    max_tokens=50
)

print(response.choices[0].text)
```

**Next Steps After Getting the Key:**

  * **Deploy Models in Azure OpenAI Studio:** After creating the resource and getting the key, you'll need to go to **Azure OpenAI Studio** (`https://oai.azure.com/`) to deploy specific models (e.g., `gpt-3.5-turbo`, `gpt-4`, `text-embedding-ada-002`). The API key and endpoint you obtained are for accessing the *service*, but you need to *deploy* models within that service to use them.
  * **Secure Your Keys:** Never hardcode your API keys directly into your applications. Use environment variables, Azure Key Vault, or other secure methods to store and access them.
  * **Understand Pricing:** Be aware of the pricing for Azure OpenAI services, as usage incurs costs.


# Multi-Agent-Medical-Assistant

local folder: `~\Multi-Agent-Medical-Assistant`

```
deployment_name=lft-agent
model_name=gpt-4o-mini
azure_endpoint=
openai_api_key=
openai_api_version=2023-05-15
```
