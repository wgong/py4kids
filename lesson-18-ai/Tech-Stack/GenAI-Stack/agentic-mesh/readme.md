# References

How we enabled Agents at Scale in the Enterprise with the Agentic AI Mesh

https://medium.com/quantumblack/how-we-enabled-agents-at-scale-in-the-enterprise-with-the-agentic-ai-mesh-architecture-baf4290daf48


ACP

https://research.ibm.com/blog/agent-communication-protocol-ai

A2A

https://medium.com/@elisowski/what-every-ai-engineer-should-know-about-a2a-mcp-acp-8335a210a742

MCP 

https://modelcontextprotocol.io/introduction



# 1

This is an excellent architectural diagram! You've done a brilliant job translating McKinsey's enterprise AI concepts through the lens of data mesh principles. Here's my feedback:

## Strong Design Elements

**Layered Architecture** - The clean separation from personas down to infrastructure is very well thought out. It shows clear abstraction boundaries while maintaining traceability.

**People-Product-Process Integration** - Your circular diagram perfectly captures the synergy concept. This should be the north star that guides all design decisions.

**Pathfinder Strategy** - Highlighting the green boxes shows exactly how you're building from proven success. This de-risks the expansion significantly.

**Data Mesh Influence** - The federated approach across personas while maintaining common services is spot-on. Each persona can own their domain while sharing infrastructure.

## Observations & Suggestions

**Agentic Orchestration Layer** - This is the heart of your mesh. Consider adding workflow orchestration patterns (like Prefect concepts we discussed) to show how agents coordinate across domains.

**Common Services** - Love how you've pulled out Auth/SSO, Observability, etc. Consider adding:
- Agent Registry/Discovery (like a service mesh)
- Policy Engine (for governance)
- Event Bus (for agent-to-agent communication)

**Metadata Layer** - Great to see Collibra and Glue Catalog. This becomes your "data product catalog" equivalent for the agentic mesh.

**Missing Connections** - Consider showing how agents in different personas interact. For example, how does the Product Manager agent coordinate with the Developer SDLC agent?

## Strategic Questions

1. **Agent Lifecycle Management** - How do you deploy, version, and retire agents across this mesh?

2. **Cross-Persona Workflows** - What happens when a business process spans multiple personas? (e.g., product launch involving PM, Dev, Security)

3. **Governance Model** - How do you ensure agents follow enterprise policies while maintaining domain autonomy?

This architecture positions you perfectly for the expansion you're planning. The Product Manager persona addition should be straightforward given your foundation.

What's your timeline for rolling this out beyond the current developer use case?



# 2

That's a smart approach! You're already building those cross-persona capabilities organically within your Developer Assist product. Using A2A or MCP to expose those common functionalities is exactly the right pattern - it creates reusable agent building blocks that other personas can leverage.

**Your incremental strategy is perfect:**
- Prove value with Developer persona ✓
- Build common capabilities that naturally extend to Product Managers ✓  
- Use standards (A2A/MCP) to create composable agent services ✓
- Expand methodically based on proven patterns ✓

**For management buy-in**, your diagram tells a compelling story:
- Shows current investment (green boxes) isn't just for developers
- Demonstrates clear expansion path with shared infrastructure
- Positions the organization for broader AI transformation
- Reduces risk by building on proven foundation

The fact that you're already solving real problems for developers while building toward this broader vision is exactly what executives want to see - practical value today with strategic positioning for tomorrow.

Good luck with the refinements tomorrow! The architecture is solid, and your phased approach should make the business case much easier to make. Having that concrete developer success story plus a clear technical roadmap is a powerful combination.

Let me know how the management discussions go - this could be a real game-changer for your organization's AI strategy.

# 3

I need to search for information about ACP (Agent Communication Protocol) to give you accurate details about this initiative and how it compares to MCP and A2A.Great question! Based on my research, here's how ACP differentiates itself from MCP and A2A:

## ACP (Agent Communication Protocol)

**Core Focus**: Agent-to-agent communication within local or shared environments, designed as "the HTTP of agent communication"

**Key Differentiators:**
- RESTful HTTP-based with simple endpoints, uses MIME types for content identification
- Local-first, real-time agent orchestration with minimal network overhead
- Supports multimodal messages, session continuity, and trajectory metadata for tracking multi-step reasoning
- Structured message envelope with task delegation, routing, and stateful sessions

## How They Compare:

**MCP (Model Context Protocol)**:
- Connects agents to their tools and knowledge - the "tool access layer"
- JSON-RPC client-server for secure tool invocation
- Focus: Agent ↔ Tool/Data integration

**A2A (Agent-to-Agent)**:
- Addresses horizontal interoperability over the open web, treating agents as interoperable services
- Uses "Agent Cards" for capability discovery
- Focus: Cross-vendor, internet-scale agent coordination

**ACP (Agent Communication Protocol)**:
- Connects agents to agents - complements MCP
- Designed for local-first environments with lightweight, stateless services
- Focus: Local/enterprise agent orchestration and coordination

## Strategic Positioning for Your Architecture:

**ACP would be ideal for your agentic mesh because:**
- Perfect for enterprise environments where agents operate within your infrastructure
- Transforms fragmented landscape into interconnected teammates with easier integration
- Provides connective tissue for heterogeneous agents to behave like a tight microservice cluster
- Works well with your AWS-based architecture

**Complementary Use**: ACP and MCP can be used together - MCP for tool access, ACP for agent coordination

For your enterprise agentic mesh, ACP seems like the most relevant choice since you're building within your organization's boundaries rather than across the open internet.

# 4

Absolutely, you're right - they are all very new protocols! The timeline shows just how rapidly this space is evolving:

- **MCP**: Launched by Anthropic late 2024
- **ACP**: IBM contributed BeeAI to Linux Foundation in March 2025
- **A2A**: Google unveiled A2A a few weeks after ACP was shown at AI Dev 25 conference

It's great that you've already prototyped MCP and understand it well - that gives you a solid foundation since ACP intentionally re-uses MCP's message types where possible.

**For future experimentation:**

**A2A** might be interesting for your enterprise mesh if you want to:
- Enable discovery of agents across different divisions/subsidiaries
- Create a marketplace-like environment for internal agent sharing
- Future-proof for potential cross-organization collaboration

**ACP** seems more immediately relevant for your current architecture since:
- It's designed for the enterprise environment you're building
- You can wrap existing agents (CrewAI, custom frameworks) inside ACP servers
- Perfect for your multi-persona expansion (Product Manager, Data Analyst, etc.)

I'd be happy to help you experiment with both when you're ready! Your experience with MCP will definitely make the learning curve easier, especially with ACP since they're designed to work together.

The fact that you're building this now, while these protocols are still crystallizing, puts you in a great position to influence the direction and be an early adopter with real production experience.



