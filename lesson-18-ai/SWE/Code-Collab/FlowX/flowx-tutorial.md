# FlowX Complete Learning Tutorial

Welcome to the comprehensive tutorial for FlowX - an advanced AI agent orchestration platform developed by Seth Ford. This tutorial will take you from zero to proficient in using FlowX's powerful features.

## Table of Contents
1. [What is FlowX?](#what-is-flowx)
2. [Installation & Setup](#installation--setup)
3. [Core Concepts](#core-concepts)
4. [Getting Started - Your First Project](#getting-started---your-first-project)
5. [Agent Management](#agent-management)
6. [Memory System](#memory-system)
7. [SPARC Methodology](#sparc-methodology)
8. [Monitoring & Dashboards](#monitoring--dashboards)
9. [Advanced Features](#advanced-features)
10. [Real-World Examples](#real-world-examples)
11. [Best Practices](#best-practices)
12. [Troubleshooting](#troubleshooting)

## What is FlowX?

FlowX is an advanced AI agent orchestration platform that revolutionizes software development through:

- **Intelligent Agent Coordination**: 9 specialized agent types working together
- **Neural Pattern Recognition**: Real TensorFlow.js neural networks
- **Sophisticated Memory Systems**: Persistent learning across sessions
- **Real-time Monitoring**: Live dashboards and performance metrics
- **SPARC Methodology**: Structured development workflows

Think of FlowX as your AI-powered development team coordinator that can spawn specialized agents, manage complex workflows, and learn from every interaction.

## Installation & Setup

### Prerequisites
- Node.js >= 18.0.0
- NPM or similar package manager
- Claude AI access (which you already have!)

### Installation Methods

#### Method 1: Global Installation (Recommended for Learning)
```bash
# Install FlowX globally
npm install -g claude-code-flow

which flowx
# ~/.npm-global/bin/flowx

# Verify installation
flowx --version
# Should show version 8.0.3 or higher
```

#### Method 2: Project-Specific Installation
```bash
# Use without installing globally
npx claude-code-flow init MyProject --sparc --advanced

# Or install in specific project
npm install claude-code-flow
npx claude-code-flow init --sparc --advanced
```

## Core Concepts

### 1. Agents
FlowX uses 9 specialized agent types, each with distinct capabilities:

- **Architect**: System design, scalability planning (95% proficiency)
- **Coder**: Software development, clean code practices
- **Tester**: Quality assurance, test automation
- **Security**: Threat modeling, vulnerability assessment
- **Researcher**: Information gathering, pattern recognition
- **Analyst**: Data analysis, statistical modeling
- **Optimizer**: Performance optimization, resource efficiency
- **Documenter**: Technical writing, API documentation
- **Monitor**: System monitoring, health checks

### 2. Neural Memory System
- Powered by real TensorFlow.js neural networks
- Persistent learning across sessions
- Semantic search capabilities
- Pattern recognition and optimization

### 3. SPARC Methodology
Structured development approach:
- **S**pecification: Define requirements
- **P**seudocode: Plan implementation
- **A**rchitecture: Design system structure
- **R**efinement: Iterate and improve
- **C**ompletion: Finalize implementation

## Getting Started - Your First Project

### Step 1: Initialize Your Project

```bash
cd ~/projects/wgong/py4kids/lesson-18-ai/SWE/Code-Collab/FlowX

# Create a new FlowX project with all advanced features
flowx init My1stProject --sparc --advanced --neural-memory

# Navigate to your project
cd My1stProject


flowx init ~/projects/wgong/flowx-tutorials/My2ndProject --sparc --advanced --neural-memory


# find where My2ndProject folder is
find . -name "My2ndProject" -type d 2>/dev/null

# ./.npm-global/lib/node_modules/claude-code-flow/home/papagame/projects/wgong/flowx-tutorials/My2ndProject

cd ~/projects/wgong/flowx-tutorials
mv ~/.npm-global/lib/node_modules/claude-code-flow/home/papagame/projects/wgong/flowx-tutorials/My2ndProject .
rm -rf ~/.npm-global/lib/node_modules/claude-code-flow/home
```

```log

(base) papagame@papa-game:~/projects/wgong/py4kids/lesson-18-ai/SWE/Code-Collab/FlowX$ flowx init My1stProject --sparc --advanced --neural-memory
2025-07-19 23:35:23.075466: I tensorflow/core/platform/cpu_feature_guard.cc:193] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 FMA
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
🚀 Initializing FlowX CLI...
Initializing services with 3000ms timeout...
{"timestamp":"2025-07-20T03:35:23.169Z","level":"INFO","message":"Starting global services initialization","context":{}}
{"timestamp":"2025-07-20T03:35:23.170Z","level":"INFO","message":"Initializing persistence...","context":{}}
Awaiting initialization promise...
Ensured database directory exists: /home/papagame/.npm-global/lib/node_modules/claude-code-flow/.flowx
Created new database at /home/papagame/.npm-global/lib/node_modules/claude-code-flow/.flowx/flowx.db
Database saved to /home/papagame/.npm-global/lib/node_modules/claude-code-flow/.flowx/flowx.db
Persistence initialized successfully at ./.flowx
{"timestamp":"2025-07-20T03:35:23.198Z","level":"INFO","message":"Initializing memory...","context":{}}
{"timestamp":"2025-07-20T03:35:23.198Z","level":"INFO","message":"Global services initialized successfully","context":{}}
Services initialized successfully
✅ Backend services initialized (29ms)
ℹ️ Creating project structure...
Database saved to /home/papagame/.npm-global/lib/node_modules/claude-code-flow/.flowx/flowx.db
ℹ️ Initializing SPARC methodology...
ℹ️ Initializing advanced features...
ℹ️ Creating configuration files...
ℹ️ Initializing git repository...
ℹ️ Installing dependencies...
npm warn deprecated @humanwhocodes/config-array@0.13.0: Use @eslint/config-array instead
npm warn deprecated @babel/plugin-proposal-explicit-resource-management@7.27.4: This proposal has been merged to the ECMAScript standard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-explicit-resource-management instead.
npm warn deprecated rimraf@3.0.2: Rimraf versions prior to v4 are no longer supported
npm warn deprecated jest-fast-check@2.0.0: Replaced by @fast-check/jest
npm warn deprecated @humanwhocodes/object-schema@2.0.3: Use @eslint/object-schema instead
npm warn deprecated eslint@8.57.1: This version is no longer supported. Please see https://eslint.org/version-support for other options.

> claude-code-flow@8.0.3 postinstall
> node scripts/install.js

Installing Claude-Flow...
Claude-Flow installation completed!
You can now use: npx claude-flow or claude-flow (if installed globally)

added 933 packages, changed 2 packages, and audited 1363 packages in 1m

226 packages are looking for funding
  run `npm fund` for details

1 moderate severity vulnerability

Some issues need review, and may require choosing
a different dependency.

Run `npm audit` for details.
ℹ️ Validating initialization...
✅ Initialization validation passed
✅ Successfully initialized Claude Flow project: My1stProject
ℹ️ Next steps:
  cd My1stProject
  flowx start
{"timestamp":"2025-07-20T03:36:30.174Z","level":"INFO","message":"Starting global services shutdown","context":{}}
{"timestamp":"2025-07-20T03:36:30.175Z","level":"INFO","message":"Global services shutdown completed","context":{}}
(base) papagame@papa-game:~/projects/wgong/py4kids/lesson-18-ai/SWE/Code-Collab/FlowX$ ls


```

Issue: My1stProject not created in current folder
found it at `~/.npm-global/lib/node_modules/claude-code-flow/My1stProject`


```bash

# Navigate to where the project was created
cd ~/.npm-global/lib/node_modules/claude-code-flow/

# Move the project to your desired location
mv My1stProject ~/projects/wgong/flowx-tutorials

# Navigate to your project
cd ~/projects/wgong/flowx-tutorials/My1stProject

# Check what was created
ls -la

tree .
```




This creates:
- ✅ Complete project structure with FlowX configuration
- ✅ Neural memory system with SQLite backend
- ✅ Specialized agent behavior registry
- ✅ Real-time monitoring dashboard setup
- ✅ Local `./flowx` wrapper script

### Step 2: Start FlowX

```bash
# Start the orchestration system with UI
flowx start --ui --port 3000
```

### Step 3: Launch Monitoring Dashboard

```bash
# In a new terminal, launch real-time monitoring
flowx monitor --port 3001 --refresh 5
```

Now you should have:
- FlowX orchestrator running on port 3000
- Real-time monitoring dashboard on port 3001

### Step 4: Verify Everything is Working

```bash
# Check system status
flowx status --detailed --performance

# Check health
flowx health --comprehensive
```

## Agent Management


### Quick Demo

```bash

~/projects/wgong/flowx-tutorials/tmp$ flowx swarm create "Build a TODO API with GET, POST, PUT, DELETE endpoints" \
  --strategy development \
  --name todo-api-demo \
  --output ./output/todo-api \
  --verbose
2025-07-20 00:34:50.388384: I tensorflow/core/platform/cpu_feature_guard.cc:193] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 FMA
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
🚀 Initializing FlowX CLI...
Initializing services with 3000ms timeout...
{"timestamp":"2025-07-20T04:34:50.482Z","level":"INFO","message":"Starting global services initialization","context":{}}
{"timestamp":"2025-07-20T04:34:50.482Z","level":"INFO","message":"Initializing persistence...","context":{}}
Awaiting initialization promise...
Ensured database directory exists: /home/papagame/.npm-global/lib/node_modules/claude-code-flow/.flowx
Loaded existing database from /home/papagame/.npm-global/lib/node_modules/claude-code-flow/.flowx/flowx.db
Database saved to /home/papagame/.npm-global/lib/node_modules/claude-code-flow/.flowx/flowx.db
Persistence initialized successfully at ./.flowx
{"timestamp":"2025-07-20T04:34:50.506Z","level":"INFO","message":"Initializing memory...","context":{}}
{"timestamp":"2025-07-20T04:34:50.506Z","level":"INFO","message":"Global services initialized successfully","context":{}}
Services initialized successfully
✅ Backend services initialized (24ms)
ℹ️ 🚀 Launching Claude Code with swarm coordination...
Database saved to /home/papagame/.npm-global/lib/node_modules/claude-code-flow/.flowx/flowx.db
ℹ️ ✅ MCP configuration found in Claude settings (flowx)
✅ 🛡️ Enhanced swarm with security context (3 templates)
ℹ️ 🔒 Security Level: critical
ℹ️ 📋 Compliance: OWASP_TOP_10_2023, GDPR, SOX
⚠️ 🔓 Using --dangerously-skip-permissions for seamless swarm execution
ℹ️ 🔗 Using Claude settings: /home/papagame/.npm-global/lib/node_modules/claude-code-flow/.claude/settings.json
ℹ️ Launching Claude Code with swarm coordination...
✅ ✓ Claude Code launched with swarm coordination
ℹ️   The swarm will coordinate task execution using MCP tools
ℹ️   Use BatchTool for parallel operations
ℹ️   Memory will be shared between agents
error: unknown option '--temperature'
❌ Claude Code exited with code 1
{"timestamp":"2025-07-20T04:34:52.166Z","level":"INFO","message":"Starting global services shutdown","context":{}}
{"timestamp":"2025-07-20T04:34:52.166Z","level":"INFO","message":"Global services shutdown completed","context":{}}

```

### Spawning Your First Agent

```bash
# Spawn an architect agent
flowx agent spawn architect --name "System Designer" --priority 9

Database saved to /home/papagame/.npm-global/lib/node_modules/claude-code-flow/.flowx/flowx.db
✅ ✅ Agent spawned successfully: System Designer (agent-1752985058283-dyspijar5)
ℹ️ Process ID: 707452
ℹ️ Status: running
ℹ️ Type: architect
ℹ️ Working Directory: default
✅ 🛡️ Security Level: high
ℹ️ 🔒 OWASP Compliance: TOP_10_2023
ℹ️ 🏗️ Clean Architecture: true


# Spawn a coder agent
flowx agent spawn coder --name "Senior Developer" --priority 8


✅ ✅ Agent spawned successfully: Senior Developer (agent-1752985280486-7fehr0lr6)
ℹ️ Process ID: 710673
ℹ️ Status: running
ℹ️ Type: coder
ℹ️ Working Directory: default


# Spawn a tester agent
flowx agent spawn tester --name "QA Engineer" --priority 7
```

### Managing Agents

```bash
# List all active agents with status
flowx agent list --status --performance


✅ Backend services initialized (25ms)
ℹ️ No agents found


# List with real-time updates
flowx agent list --status --performance --real-time

# Kill a specific agent
flowx agent kill agent-123
```

### Multi-Agent Coordination (Swarms)

```bash
# Coordinate multiple agents for a task
flowx swarm "Build a REST API with authentication" \
  --agents 3 \
  --strategy development \
  --monitor


2025-07-20 00:22:19.560641: I tensorflow/core/platform/cpu_feature_guard.cc:193] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 FMA
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
🚀 Initializing FlowX CLI...
Initializing services with 3000ms timeout...
{"timestamp":"2025-07-20T04:22:19.653Z","level":"INFO","message":"Starting global services initialization","context":{}}
{"timestamp":"2025-07-20T04:22:19.654Z","level":"INFO","message":"Initializing persistence...","context":{}}
Awaiting initialization promise...
Ensured database directory exists: /home/papagame/.npm-global/lib/node_modules/claude-code-flow/.flowx
Loaded existing database from /home/papagame/.npm-global/lib/node_modules/claude-code-flow/.flowx/flowx.db
Database saved to /home/papagame/.npm-global/lib/node_modules/claude-code-flow/.flowx/flowx.db
Persistence initialized successfully at ./.flowx
{"timestamp":"2025-07-20T04:22:19.678Z","level":"INFO","message":"Initializing memory...","context":{}}
{"timestamp":"2025-07-20T04:22:19.678Z","level":"INFO","message":"Global services initialized successfully","context":{}}
Services initialized successfully
✅ Backend services initialized (25ms)
ℹ️ 🚀 Launching Claude Code with swarm coordination...
Database saved to /home/papagame/.npm-global/lib/node_modules/claude-code-flow/.flowx/flowx.db
ℹ️ ✅ MCP configuration found in Claude settings (flowx)
✅ 🛡️ Enhanced swarm with security context (3 templates)
ℹ️ 🔒 Security Level: critical
ℹ️ 📋 Compliance: OWASP_TOP_10_2023, GDPR, SOX
⚠️ 🔓 Using --dangerously-skip-permissions for seamless swarm execution
ℹ️ 🔗 Using Claude settings: /home/papagame/.npm-global/lib/node_modules/claude-code-flow/.claude/settings.json
ℹ️ Launching Claude Code with swarm coordination...
✅ ✓ Claude Code launched with swarm coordination
ℹ️   The swarm will coordinate task execution using MCP tools
ℹ️   Use BatchTool for parallel operations
ℹ️   Memory will be shared between agents
error: unknown option '--temperature'
❌ Claude Code exited with code 1


# Advanced swarm with neural coordination
flowx swarm "Build e-commerce platform with microservices" \
  --agents 4 \
  --strategy development \
  --monitor \
  --neural-coordination
```

## Memory System

FlowX's neural memory system is one of its most powerful features.

### Storing Information

```bash
# Store project context with neural enhancement
flowx memory store "project-requirements" \
  "E-commerce platform with microservices architecture, React frontend, Node.js backend" \
  --neural --priority high --tags "project,architecture,requirements"

# Store technical decisions
flowx memory store "tech-stack" \
  "React, Node.js, PostgreSQL, Redis, Docker, Kubernetes" \
  --neural --namespace "architecture" --priority high

# Store coding patterns
flowx memory store "authentication-pattern" \
  "JWT tokens with refresh mechanism, OAuth2 integration" \
  --neural --tags "security,authentication" --priority high
```

### Querying Memory

```bash
# Semantic search for patterns
flowx memory query "authentication patterns" --neural --similarity 0.8

# Query with specific parameters
flowx memory query "microservices authentication patterns" \
  --neural --similarity 0.8 --limit 10

# Query by tags
flowx memory query --tags "security,authentication" --neural
```

### Memory Learning and Optimization

```bash
# Trigger learning cycle for development patterns
flowx memory learn --pattern "development" --optimize-retrieval

# Learn from specific domain
flowx memory learn --pattern "security" --optimize

# Analyze memory performance
flowx memory stats --neural-metrics --performance-analysis
```

## SPARC Methodology

SPARC provides a structured approach to development tasks.

### Architecture Phase

```bash
# Design system architecture
flowx sparc architect "Design e-commerce microservices architecture" \
  --detailed --documentation --save-patterns

# Architect with specific focus
flowx sparc architect "User authentication system design" \
  --security-focused --scalability-analysis
```

### Coding Phase

```bash
# Implement with TDD
flowx sparc code "User authentication service" \
  --tdd --security-review --performance-optimized

# Code with specific requirements
flowx sparc code "Payment processing module" \
  --secure --tested --documented
```

### Testing Phase

```bash
# Comprehensive testing
flowx sparc test "Payment processing module" \
  --comprehensive --security-testing --load-testing

# Focused testing
flowx sparc test "API endpoints" --unit --integration
```

### Optimization Phase

```bash
# Performance optimization
flowx sparc optimize "Database queries and API performance" \
  --benchmarking --monitoring --alerts

# General optimization
flowx sparc optimize "Application performance" --comprehensive
```

## Monitoring & Dashboards

### Real-time Dashboard

```bash
# Launch dashboard with custom refresh rate
flowx monitor-dashboard --port 3001 --refresh 5

# Dashboard features:
# ✅ Live agent status and performance metrics
# ✅ Task progress tracking with completion rates
# ✅ Resource usage monitoring (CPU, memory, network)
# ✅ System health indicators and alerts
# ✅ Auto-refresh with configurable intervals
```

### Status and Health Monitoring

```bash
# Detailed status overview
flowx status --detailed --performance

# Health check with comprehensive report
flowx health --comprehensive

# Agent-specific monitoring
flowx agent list --status --performance --real-time
```

## Advanced Features

### Task Management

```bash
# Create high-priority research task
flowx task create research "Market analysis for mobile app" --priority high

# Create development task
flowx task create development "Implement user registration" --priority medium

# List all tasks
flowx task list --status --priority
```

### Configuration Management

```bash
# Show current configuration
flowx config show --detailed

# Update configuration
flowx config set neural-memory.enabled true
flowx config set monitoring.auto-refresh 3
```

### Neural Pattern Recognition

The neural system automatically:
- Recognizes development patterns with 95%+ accuracy
- Optimizes memory retrieval by 70%
- Provides contextual understanding for natural language queries
- Learns continuously across sessions

## Real-World Examples

### Example 1: Building an E-commerce Platform

```bash
# 1. Initialize project
flowx init EcommercePlatform --sparc --advanced --neural-memory
cd EcommercePlatform

# 2. Start systems
flowx start --ui --port 3000
flowx monitor-dashboard --port 3001 --refresh 5

# 3. Store project context
flowx memory store "project-context" \
  "E-commerce platform: user management, product catalog, shopping cart, payment processing, order management" \
  --neural --priority high --tags "project,ecommerce"

# 4. Spawn development team
flowx agent spawn architect --name "Lead Architect" --priority 9
flowx agent spawn coder --name "Senior Developer" --priority 8
flowx agent spawn tester --name "QA Engineer" --priority 7
flowx agent spawn security --name "Security Analyst" --priority 8

# 5. Architecture phase
flowx sparc architect "E-commerce microservices architecture" \
  --detailed --documentation --save-patterns

# 6. Implementation coordination
flowx swarm "Build user authentication microservice" \
  --agents 3 --strategy development --monitor

# 7. Store architectural decisions
flowx memory store "microservices-pattern" \
  "API Gateway + User Service + Product Service + Order Service + Payment Service" \
  --neural --namespace "architecture"

# 8. Continue with other services
flowx sparc code "Product catalog service" --tdd --performance-optimized
flowx sparc test "User authentication" --comprehensive --security-testing
```

### Example 2: AI Research Project

```bash
# 1. Initialize research project
flowx init AIResearchProject --sparc --advanced
cd AIResearchProject

# 2. Spawn research team
flowx agent spawn researcher --name "AI Researcher" --priority 9
flowx agent spawn analyst --name "Data Analyst" --priority 8
flowx agent spawn documenter --name "Technical Writer" --priority 7

# 3. Store research context
flowx memory store "research-topic" \
  "Natural Language Processing for code generation, focus on transformer architectures" \
  --neural --priority high --tags "research,nlp,transformers"

# 4. Coordinate research
flowx swarm "Research transformer architectures for code generation" \
  --agents 3 --strategy research --monitor

# 5. Query related patterns
flowx memory query "transformer architectures code generation" \
  --neural --similarity 0.8 --limit 15
```

## Best Practices

### 1. Memory Management
- Use descriptive keys and tags for better searchability
- Set appropriate priority levels (high for critical context)
- Use namespaces to organize different domains
- Trigger learning cycles regularly

### 2. Agent Coordination
- Match agent types to task requirements
- Use appropriate priority levels for agents
- Monitor agent performance and adjust as needed
- Use swarms for complex, multi-faceted tasks

### 3. SPARC Methodology
- Always start with architecture for complex projects
- Use iterative refinement cycles
- Document patterns for future reuse
- Integrate testing throughout the process

### 4. Monitoring
- Keep monitoring dashboard running during active development
- Review performance metrics regularly
- Set up health checks for critical systems
- Use real-time updates for dynamic situations

## Troubleshooting

### Common Issues

#### FlowX Won't Start
```bash
# Check Node.js version
node --version  # Should be >= 18.0.0

# Check port availability
lsof -i :3000  # Default FlowX port
lsof -i :3001  # Default monitoring port

# Force kill if needed
pkill -f flowx
```

#### Memory System Issues
```bash
# Reset memory system
flowx memory reset --confirm

# Rebuild neural patterns
flowx memory learn --pattern "all" --rebuild
```

#### Agent Communication Problems
```bash
# Kill all agents and restart
flowx agent kill --all
flowx start --ui --port 3000

# Check agent registry
flowx agent list --detailed --debug
```

### Performance Optimization

```bash
# Check system performance
flowx status --performance --detailed

# Optimize memory usage
flowx memory stats --optimize-storage

# Agent performance tuning
flowx agent optimize --all --performance-mode
```

### Getting Help

```bash
# General help
flowx --help

# Command-specific help
flowx agent --help
flowx memory --help
flowx sparc --help

# Version and system info
flowx --version
flowx status --system-info
```

## Next Steps

Now that you've learned the basics of FlowX:

1. **Practice with Small Projects**: Start with simple workflows to get comfortable
2. **Explore Neural Memory**: Experiment with different query patterns and learning cycles
3. **Try Different Agent Combinations**: See how different agent types work together
4. **Monitor Performance**: Use the dashboard to understand system behavior
5. **Join the Community**: Contribute to the project on GitHub
6. **Read the Source**: Explore the codebase to understand advanced features

## Additional Resources

- **GitHub Repository**: https://github.com/sethdford/flowx
- **NPM Package**: https://www.npmjs.com/package/claude-code-flow
- **Test Suite**: Run `npm test` to see comprehensive testing examples
- **Contributing Guide**: Check the repository for contribution guidelines

## Summary

FlowX is a powerful platform that combines:
- ✅ AI agent orchestration with 9 specialized agent types
- ✅ Neural memory systems with real TensorFlow.js integration
- ✅ SPARC methodology for structured development
- ✅ Real-time monitoring and performance analytics
- ✅ Cross-session learning and pattern recognition

With this tutorial, you now have the knowledge to leverage FlowX for your development projects. Start small, experiment with different features, and gradually build up to more complex orchestrations.

Happy coding with FlowX! 🚀