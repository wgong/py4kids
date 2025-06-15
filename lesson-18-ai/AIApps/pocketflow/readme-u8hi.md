## Setup

```bash
cd ~/projects/wgong
git clone git@github.com:The-Pocket/Tutorial-Codebase-Knowledge.git

conda create -n zinets python=3.11
conda activate zinets  # git-tutor

pip install -r requirements.txt
```

### AI Studio by Google


### Cleanup

```bash
conda env remove --name agent
conda clean --all  # remove unused env space
```

## Usage

```
# Analyze a GitHub repository
python main.py --repo https://github.com/username/repo --include "*.py" "*.js" --exclude "tests/*" --max-size 50000

# Or, analyze a local directory
python main.py --dir /path/to/your/codebase --include "*.py" --exclude "*test*"



# Or, generate a tutorial in Chinese
python main.py --repo https://github.com/username/repo --language "Chinese"
```

### Vanna.AI

```
$ python main.py --dir /home/papagame/projects/digital-duck/ssadata --include "*.py" 

Starting tutorial generation for: /home/papagame/projects/digital-duck/ssadata in English language
Crawling directory: /home/papagame/projects/digital-duck/ssadata...
Fetched 66 files.
Identifying abstractions using LLM...
Identified 7 abstractions.
Analyzing relationships using LLM...
Generated project summary and relationship details.
Determining chapter order using LLM...
Determined chapter order (indices): [5, 0, 2, 6, 1, 3, 4]
Preparing to write 7 chapters...
Writing chapter 1 for: Flask API/App (Web Interface)
 using LLM...
Writing chapter 2 for: VannaBase (Core Interface)
 using LLM...
Writing chapter 3 for: LLM Connector (Reasoning Engine)
 using LLM...
Writing chapter 4 for: Prompt Engineering (Guiding the LLM)
 using LLM...
Writing chapter 5 for: Vector Store (Knowledge Storage)
 using LLM...
Writing chapter 6 for: Database Connector (Execution Layer)
 using LLM...
Writing chapter 7 for: Training Data Management (Learning Material)
 using LLM...
Finished writing 7 chapters.
Combining tutorial into directory: output/ssadata
  - Wrote output/ssadata/index.md
  - Wrote output/ssadata/01_flask_api_app__web_interface__.md
  - Wrote output/ssadata/02_vannabase__core_interface__.md
  - Wrote output/ssadata/03_llm_connector__reasoning_engine__.md
  - Wrote output/ssadata/04_prompt_engineering__guiding_the_llm__.md
  - Wrote output/ssadata/05_vector_store__knowledge_storage__.md
  - Wrote output/ssadata/06_database_connector__execution_layer__.md
  - Wrote output/ssadata/07_training_data_management__learning_material__.md

Tutorial generation complete! Files are in: output/ssadata

```

### OctoTools
using LLM=Claude 3.7 Sonnet  # encounter rate-limit issue of 20,000 input tokens per minute

using LLM=gemini-2.5-pro

```
$ python main.py --repo https://github.com/octotools/octotools --include "*.py" "*.js" --exclude "tests/*" --max-size 50000
# rate limit exceeded

$ python main.py --dir ~/projects/wgong/octotools --include "*.py" "*.js" --exclude "tests/*" "examples/*"

Starting tutorial generation for: /home/papagame/projects/wgong/octotools in English language
Crawling directory: /home/papagame/projects/wgong/octotools...
Fetched 62 files.
Identifying abstractions using LLM...
Identified 10 abstractions.
Analyzing relationships using LLM...
use LLM model: Google / gemini-2.5-pro-exp-03-25
Generated project summary and relationship details.
Determining chapter order using LLM...
use LLM model: Google / gemini-2.5-pro-exp-03-25
Determined chapter order (indices): [0, 1, 5, 8, 2, 3, 6, 4, 7, 9]
Preparing to write 10 chapters...
Writing chapter 1 for: Solver Framework
 using LLM...
use LLM model: Google / gemini-2.5-pro-exp-03-25
Writing chapter 2 for: Planning-Execution Cycle
 using LLM...
use LLM model: Google / gemini-2.5-pro-exp-03-25
Writing chapter 3 for: Query Analysis
 using LLM...
use LLM model: Google / gemini-2.5-pro-exp-03-25
Writing chapter 4 for: Multimodal Processing
 using LLM...
use LLM model: Google / gemini-2.5-pro-exp-03-25
Writing chapter 5 for: Tool Architecture
 using LLM...
use LLM model: Google / gemini-2.5-pro-exp-03-25
Writing chapter 6 for: LLM Engine Integration
 using LLM...
use LLM model: Google / gemini-2.5-pro-exp-03-25
Writing chapter 7 for: Tool Command Generation
 using LLM...
use LLM model: Google / gemini-2.5-pro-exp-03-25
Writing chapter 8 for: Memory Management
 using LLM...
use LLM model: Google / gemini-2.5-pro-exp-03-25
Writing chapter 9 for: Context Verification
 using LLM...
use LLM model: Google / gemini-2.5-pro-exp-03-25
Writing chapter 10 for: Task Evaluation System
 using LLM...
use LLM model: Google / gemini-2.5-pro-exp-03-25
Finished writing 10 chapters.
Combining tutorial into directory: output/octotools
  - Wrote output/octotools/index.md
  - Wrote output/octotools/01_solver_framework_.md
  - Wrote output/octotools/02_planning_execution_cycle_.md
  - Wrote output/octotools/03_query_analysis_.md
  - Wrote output/octotools/04_multimodal_processing_.md
  - Wrote output/octotools/05_tool_architecture_.md
  - Wrote output/octotools/06_llm_engine_integration_.md
  - Wrote output/octotools/07_tool_command_generation_.md
  - Wrote output/octotools/08_memory_management_.md
  - Wrote output/octotools/09_context_verification_.md
  - Wrote output/octotools/10_task_evaluation_system_.md

Tutorial generation complete! Files are in: output/octotools
```