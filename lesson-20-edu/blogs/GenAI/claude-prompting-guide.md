Claude prompting guide.md
17.80 KB • 413 extracted lines
Formatting may be inconsistent from source.
 # Claude prompting guide

## General tips for effective prompting

### 1. Be clear and specific
   - Clearly state your task or question at the beginning of your message.
   - Provide context and details to help Claude understand your needs.
   - Break complex tasks into smaller, manageable steps.

   Bad prompt:
   <prompt>
   "Help me with a presentation."
   </prompt>

   Good prompt:
   <prompt>
   "I need help creating a 10-slide presentation for our quarterly sales meeting. The presentation should cover our Q2 sales performance, top-selling products, and sales targets for Q3. Please provide an outline with key points for each slide."
   </prompt>

   Why it's better: The good prompt provides specific details about the task, including the number of slides, the purpose of the presentation, and the key topics to be covered.

### 2. Use examples
   - Provide examples of the kind of output you're looking for.
   - If you want a specific format or style, show Claude an example.

   Bad prompt:
   <prompt>
   "Write a professional email."
   </prompt>

   Good prompt:
   <prompt>
   "I need to write a professional email to a client about a project delay. Here's a similar email I've sent before:

   'Dear [Client],
   I hope this email finds you well. I wanted to update you on the progress of [Project Name]. Unfortunately, we've encountered an unexpected issue that will delay our completion date by approximately two weeks. We're working diligently to resolve this and will keep you updated on our progress.
   Please let me know if you have any questions or concerns.
   Best regards,
   [Your Name]'

   Help me draft a new email following a similar tone and structure, but for our current situation where we're delayed by a month due to supply chain issues."
   </prompt>

   Why it's better: The good prompt provides a concrete example of the desired style and tone, giving Claude a clear reference point for the new email.

### 3. Encourage thinking
   - For complex tasks, ask Claude to "think step-by-step" or "explain your reasoning."
   - This can lead to more accurate and detailed responses.

   Bad prompt:
   <prompt>
   "How can I improve team productivity?"
   </prompt>

   Good prompt:
   <prompt>
   "I'm looking to improve my team's productivity. Think through this step-by-step, considering the following factors:
   1. Current productivity blockers (e.g., too many meetings, unclear priorities)
   2. Potential solutions (e.g., time management techniques, project management tools)
   3. Implementation challenges
   4. Methods to measure improvement

   For each step, please provide a brief explanation of your reasoning. Then summarize your ideas at the end."
   </prompt>

   Why it's better: The good prompt asks Claude to think through the problem systematically, providing a guided structure for the response and asking for explanations of the reasoning process. It also prompts Claude to create a summary at the end for easier reading.

### 4. Iterative refinement
   - If Claude's first response isn't quite right, ask for clarifications or modifications.
   - You can always say "That's close, but can you adjust X to be more like Y?"

   Bad prompt:
   <prompt>
   "Make it better."
   </prompt>

   Good prompt:
   <prompt>
   "That’s a good start, but please refine it further. Make the following adjustments:
   1. Make the tone more casual and friendly
   2. Add a specific example of how our product has helped a customer
   3. Shorten the second paragraph to focus more on the benefits rather than the features"
   </prompt>

   Why it's better: The good prompt provides specific feedback and clear instructions for improvements, allowing Claude to make targeted adjustments instead of just relying on Claude’s innate sense of what “better” might be — which is likely different from the user’s definition!

### 5. Leverage Claude's knowledge
   - Claude has broad knowledge across many fields. Don't hesitate to ask for explanations or background information
   - Be sure to include relevant context and details so that Claude’s response is maximally targeted to be helpful

   Bad prompt:
   <prompt>
   "What is marketing? How do I do it?"
   </prompt>

   Good prompt:
   <prompt>
   "I'm developing a marketing strategy for a new eco-friendly cleaning product line. Can you provide an overview of current trends in green marketing? Please include:
   1. Key messaging strategies that resonate with environmentally conscious consumers
   2. Effective channels for reaching this audience
   3. Examples of successful green marketing campaigns from the past year
   4. Potential pitfalls to avoid (e.g., greenwashing accusations)

   This information will help me shape our marketing approach."
   </prompt>

   Why it's better: The good prompt asks for specific, contextually relevant  information that leverages Claude's broad knowledge base. It provides context for how the information will be used, which helps Claude frame its answer in the most relevant way.

### 6. Use role-playing
   - Ask Claude to adopt a specific role or perspective when responding.

   Bad prompt:
   <prompt>
   "Help me prepare for a negotiation."
   </prompt>

   Good prompt:
   <prompt>
   "You are a fabric supplier for my backpack manufacturing company. I'm preparing for a negotiation with this supplier to reduce prices by 10%. As the supplier, please provide:
   1. Three potential objections to our request for a price reduction
   2. For each objection, suggest a counterargument from my perspective
   3. Two alternative proposals the supplier might offer instead of a straight price cut

   Then, switch roles and provide advice on how I, as the buyer, can best approach this negotiation to achieve our goal."
   </prompt>

   Why it's better: This prompt uses role-playing to explore multiple perspectives of the negotiation, providing a more comprehensive preparation. Role-playing also encourages Claude to more readily adopt the nuances of specific perspectives, increasing the intelligence and performance of Claude’s response.


## Task-specific tips and examples

### Content Creation

1. **Specify your audience**
   - Tell Claude who the content is for.

   Bad prompt:
   <prompt>
   "Write something about cybersecurity."
   </prompt>

   Good prompt:
   <prompt>
   "I need to write a blog post about cybersecurity best practices for small business owners. The audience is not very tech-savvy, so the content should be:
   1. Easy to understand, avoiding technical jargon where possible
   2. Practical, with actionable tips they can implement quickly
   3. Engaging and slightly humorous to keep their interest

   Please provide an outline for a 1000-word blog post that covers the top 5 cybersecurity practices these business owners should adopt."
   </prompt>

   Why it's better: The good prompt specifies the audience, desired tone, and key characteristics of the content, giving Claude clear guidelines for creating appropriate and effective output.

2. **Define the tone and style**
   - Describe the desired tone.
   - If you have a style guide, mention key points from it.

   Bad prompt:
   <prompt>
   "Write a product description."
   </prompt>

   Good prompt:
   <prompt>
   "Please help me write a product description for our new ergonomic office chair. Use a professional but engaging tone. Our brand voice is friendly, innovative, and health-conscious. The description should:
   1. Highlight the chair's key ergonomic features
   2. Explain how these features benefit the user's health and productivity
   3. Include a brief mention of the sustainable materials used
   4. End with a call-to-action encouraging readers to try the chair

   Aim for about 200 words."
   </prompt>

   Why it's better: This prompt provides clear guidance on the tone, style, and specific elements to include in the product description.

3. **Define output structure**
   - Provide a basic outline or list of points you want covered.

   Bad prompt:
   <prompt>
   "Create a presentation on our company results."
   </prompt>

   Good prompt:
   <prompt>
   "I need to create a presentation on our Q2 results. Structure this with the following sections:
   1. Overview
   2. Sales Performance
   3. Customer Acquisition
   4. Challenges
   5. Q3 Outlook

   For each section, suggest 3-4 key points to cover, based on typical business presentations. Also, recommend one type of data visualization (e.g., graph, chart) that would be effective for each section."
   </prompt>

   Why it's better: This prompt provides a clear structure and asks for specific elements (key points and data visualizations) for each section.

### Document summary and Q&A

1. **Be specific about what you want**
   - Ask for a summary of specific aspects or sections of the document.
   - Frame your questions clearly and directly.
   - Be sure to specify what kind of summary (output structure, content type) you want

2. **Use the document names**
   - Refer to attached documents by name.

3. **Ask for citations**
   - Request that Claude cites specific parts of the document in its answers.

Here is an example that combines all three of the above techniques:

   Bad prompt:
   <prompt>
   "Summarize this report for me."
   </prompt>

   Good prompt:
   <prompt>
   "I've attached a 50-page market research report called 'Tech Industry Trends 2023'. Can you provide a 2-paragraph summary focusing on AI and machine learning trends? Then, please answer these questions:
   1. What are the top 3 AI applications in business for this year?
   2. How is machine learning impacting job roles in the tech industry?
   3. What potential risks or challenges does the report mention regarding AI adoption?

   Please cite specific sections or page numbers when answering these questions."
   </prompt>

   Why it's better: This prompt specifies the exact focus of the summary, provides specific questions, and asks for citations, ensuring a more targeted and useful response. It also indicates the ideal summary output structure, such as limiting the response to 2 paragraphs.

### Data analysis and visualization

1. **Specify the desired format**
   - Clearly describe the format you want the data in.

   Bad prompt:
   <prompt>
   "Analyze our sales data."
   </prompt>

   Good prompt:
   <prompt>
   "I've attached a spreadsheet called 'Sales Data 2023'. Can you analyze this data and present the key findings in the following format:

   1. Executive Summary (2-3 sentences)

   2. Key Metrics:
      - Total sales for each quarter
      - Top-performing product category
      - Highest growth region

   3. Trends:
      - List 3 notable trends, each with a brief explanation

   4. Recommendations:
      - Provide 3 data-driven recommendations, each with a brief rationale

   After the analysis, suggest three types of data visualizations that would effectively communicate these findings."
   </prompt>

   Why it's better: This prompt provides a clear structure for the analysis, specifies key metrics to focus on, and asks for recommendations and visualization suggestions for further formatting.

### Brainstorming
 1. Use Claude to generate ideas by asking for a list of possibilities or alternatives.
     - Be specific about what topics you want Claude to cover in its brainstorming

   Bad prompt:
   <prompt>
   "Give me some team-building ideas."
   </prompt>

   Good prompt:
   <prompt>
   "We need to come up with team-building activities for our remote team of 20 people. Can you help me brainstorm by:
   1. Suggesting 10 virtual team-building activities that promote collaboration
   2. For each activity, briefly explain how it fosters teamwork
   3. Indicate which activities are best for:
      a) Ice-breakers
      b) Improving communication
      c) Problem-solving skills
   4. Suggest one low-cost option and one premium option."
   </prompt>

   Why it's better: This prompt provides specific parameters for the brainstorming session, including the number of ideas, type of activities, and additional categorization, resulting in a more structured and useful output.

2. Request responses in specific formats like bullet points, numbered lists, or tables for easier reading.

   Bad Prompt:
   <prompt>
   "Compare project management software options."
   </prompt>

   Good Prompt:
   <prompt>
   "We're considering three different project management software options: Asana, Trello, and Microsoft Project. Can you compare these in a table format using the following criteria:
   1. Key Features
   2. Ease of Use
   3. Scalability
   4. Pricing (include specific plans if possible)
   5. Integration capabilities
   6. Best suited for (e.g., small teams, enterprise, specific industries)"
   </prompt>

   Why it's better: This prompt requests a specific structure (table) for the comparison, provides clear criteria, making the information easy to understand and apply.
  
## Troubleshooting, minimizing hallucinations, and maximizing performance

1. **Allow Claude to acknowledge uncertainty**
   - Tell Claude that it should say it doesn’t know if it doesn’t know. Ex. “If you're unsure about something, it's okay to admit it. Just say you don’t know.”

2. **Break down complex tasks**
   - If a task seems too large and Claude is missing steps or not performing certain steps well, break it into smaller steps and work through them with Claude one message at a time.

3. **Include all contextual information for new requests**
   - Claude doesn't retain information from previous conversations, so include all necessary context in each new conversation.

## Example good vs. bad prompt examples

These are more examples that combine multiple prompting techniques to showcase the stark difference between ineffective and highly effective prompts.

### Example 1: Marketing strategy development

Bad prompt:
<prompt>
"Help me create a marketing strategy."
</prompt>

Good prompt:
<prompt>
"As a senior marketing consultant, I need your help developing a comprehensive marketing strategy for our new eco-friendly smartphone accessory line. Our target audience is environmentally conscious millennials and Gen Z consumers. Please provide a detailed strategy that includes:

1. Market Analysis:
   - Current trends in eco-friendly tech accessories
   - 2-3 key competitors and their strategies
   - Potential market size and growth projections

2. Target Audience Persona:
   - Detailed description of our ideal customer
   - Their pain points and how our products solve them

3. Marketing Mix:
   - Product: Key features to highlight
   - Price: Suggested pricing strategy with rationale
   - Place: Recommended distribution channels
   - Promotion: 
     a) 5 marketing channels to focus on, with pros and cons for each
     b) 3 creative campaign ideas for launch

4. Content Strategy:
   - 5 content themes that would resonate with our audience
   - Suggested content types (e.g., blog posts, videos, infographics)

5. KPIs and Measurement:
   - 5 key metrics to track
   - Suggested tools for measuring these metrics

Please present this information in a structured format with headings and bullet points. Where relevant, explain your reasoning or provide brief examples.

After outlining the strategy, please identify any potential challenges or risks we should be aware of, and suggest mitigation strategies for each."
</prompt>

Why it's better: This prompt combines multiple techniques including role assignment, specific task breakdown, structured output request, brainstorming (for campaign ideas and content themes), and asking for explanations. It provides clear guidelines while allowing room for Claude's analysis and creativity.

### Example 2: Financial report analysis

Bad prompt:
<prompt>
"Analyze this financial report."
</prompt>

Good prompt:
<prompt>
"I've attached our company's Q2 financial report titled 'Q2_2023_Financial_Report.pdf'. Act as a seasoned CFO and analyze this report and prepare a briefing for our board of directors. Please structure your analysis as follows:

1. Executive Summary (3-4 sentences highlighting key points)

2. Financial Performance Overview:
   a) Revenue: Compare to previous quarter and same quarter last year
   b) Profit margins: Gross and Net, with explanations for any significant changes
   c) Cash flow: Highlight any concerns or positive developments

3. Key Performance Indicators:
   - List our top 5 KPIs and their current status (Use a table format)
   - For each KPI, provide a brief explanation of its significance and any notable trends

4. Segment Analysis:
   - Break down performance by our three main business segments
   - Identify the best and worst performing segments, with potential reasons for their performance

5. Balance Sheet Review:
   - Highlight any significant changes in assets, liabilities, or equity
   - Calculate and interpret key ratios (e.g., current ratio, debt-to-equity)

6. Forward-Looking Statements:
   - Based on this data, provide 3 key predictions for Q3
   - Suggest 2-3 strategic moves we should consider to improve our financial position

7. Risk Assessment:
   - Identify 3 potential financial risks based on this report
   - Propose mitigation strategies for each risk

8. Peer Comparison:
   - Compare our performance to 2-3 key competitors (use publicly available data)
   - Highlight areas where we're outperforming and areas for improvement

Please use charts or tables where appropriate to visualize data. For any assumptions or interpretations you make, please clearly state them and provide your reasoning.

After completing the analysis, please generate 5 potential questions that board members might ask about this report, along with suggested responses.

Finally, summarize this entire analysis into a single paragraph that I can use as an opening statement in the board meeting."
</prompt>

Why it's better: This prompt combines role-playing (as CFO), structured output, specific data analysis requests, predictive analysis, risk assessment, comparative analysis, and even anticipates follow-up questions. It provides a clear framework while encouraging deep analysis and strategic thinking.