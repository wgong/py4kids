## Prompt
### Description
```markdown

My team is an early adopter of GenAI, has built a product called Developer Assist, which empowers developer role to use various tools such as role/access request, product search, jira integration in one place,

now our company wants to expand this product to support Product manager role by using best practice, methodology, and tools in the area of product discovery, analysis, solution, prototyping and release,

You are an expert in Software Development Life Cycle and Product Management Life Cycle areas, can you articulate a clear road map vision, in order to take Developer Assist to next level or even beyond to support additional persona or use-cases in the area of Data Analyst, Business Analyst where GenAI will be utilized to boost their productivity

Please provide clear description of your vision for leveraging GenAI to support Developer,
Product Manager, Data and Business Analyst,
and supplement with mermaid diagram if needed
```

### Solution Architecture

```markdown
can you create a solution architecture diagram as follows:

1) horizontal layers
with shared components like LLM models, knowledge vector store, memory, planning, tool-use (via MCP), query parsing and routing, agent orchestration

2) vertical columns (each column represents a use-case or persona)
developer
product manager
data analyst
business analyst
...

so the horizontal layers provide platform with various common and shared services, 
vertical tier/column represents custom solution for specific use-case and/or persona
```