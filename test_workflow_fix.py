# Test fixed workflow visualization
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Import necessary packages
import asyncio
from typing import Dict, List, Any, Optional, TypedDict, Annotated
from dataclasses import dataclass, field
import json
from datetime import datetime

# LangGraph imports
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledGraph
from langchain_core.runnables.graph import MermaidDrawMethod

# LangChain imports
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic


# Simplified state and tool definitions
class ResearchState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    current_phase: str
    research_data: Dict[str, Any]
    stakeholder_analysis: Dict[str, Any]
    transparency_metrics: Dict[str, Any]
    institutional_factors: List[str]
    literature_review: Dict[str, Any]
    research_questions: List[str]
    methodology: Dict[str, Any]
    findings: Dict[str, Any]
    next_action: Optional[str]


@tool
def analyze_cecl_transparency(bank_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze CECL estimation transparency levels"""
    return {"transparency_score": 70, "factors": ["test"]}


@tool
def assess_stakeholder_tensions(
    stakeholder_data: Dict[str, List[str]],
) -> Dict[str, Any]:
    """Assess tensions between issuers and stakeholders"""
    return {"tension_level": 60}


@tool
def institutional_theory_analysis(firm_changes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Apply institutional theory to analyze firm behavior changes"""
    return {"isomorphic_pressures": {"coercive": [], "mimetic": [], "normative": []}}


# Simplified workflow class
class CECLResearchWorkflow:
    def __init__(self):
        self.llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.1)
        self.tools = [
            analyze_cecl_transparency,
            assess_stakeholder_tensions,
            institutional_theory_analysis,
        ]
        self.tool_node = ToolNode(self.tools)
        self.workflow = self._build_workflow()

    def _build_workflow(self) -> StateGraph:
        # Simple step functions
        async def bank_step(state: ResearchState) -> ResearchState:
            state["current_phase"] = "bank_strategy_analysis"
            return state

        async def regulatory_step(state: ResearchState) -> ResearchState:
            state["current_phase"] = "regulatory_assessment"
            return state

        async def auditor_step(state: ResearchState) -> ResearchState:
            state["current_phase"] = "audit_evaluation"
            return state

        async def analyst_step(state: ResearchState) -> ResearchState:
            state["current_phase"] = "market_analysis"
            return state

        async def coordination_step(state: ResearchState) -> ResearchState:
            state["current_phase"] = "simulation_coordination"
            return state

        async def synthesize_findings(state: ResearchState) -> ResearchState:
            state["current_phase"] = "synthesis"
            state["findings"] = {"test": "results"}
            return state

        # Build workflow graph
        workflow = StateGraph(ResearchState)

        # Add nodes
        workflow.add_node("bank_step", bank_step)
        workflow.add_node("regulatory_step", regulatory_step)
        workflow.add_node("auditor_step", auditor_step)
        workflow.add_node("analyst_step", analyst_step)
        workflow.add_node("coordination_step", coordination_step)
        workflow.add_node("synthesis", synthesize_findings)
        workflow.add_node("tools", self.tool_node)

        # Add sequential edge connections (Fix: use add_edge instead of conditional_edges)
        workflow.add_edge(START, "bank_step")
        workflow.add_edge("bank_step", "regulatory_step")
        workflow.add_edge("regulatory_step", "auditor_step")
        workflow.add_edge("auditor_step", "analyst_step")
        workflow.add_edge("analyst_step", "coordination_step")
        workflow.add_edge("coordination_step", "synthesis")
        workflow.add_edge("synthesis", END)

        # Compile workflow
        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)


def save_graph_as_png(app: CompiledGraph, output_file_path) -> None:
    """Save LangGraph workflow as PNG image"""
    png_image = app.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)
    with open(output_file_path, "wb") as f:
        f.write(png_image)
    print(f"Fixed graph saved as: {output_file_path}")


def test_workflow_visualization():
    """Test fixed workflow visualization"""
    print("=== Testing Fixed CECL Workflow Visualization ===")

    # Create workflow instance
    cecl_workflow = CECLResearchWorkflow()

    # Save PNG image
    output_path = "cecl_workflow_fixed_test.png"
    save_graph_as_png(cecl_workflow.workflow, output_path)

    # Save Mermaid code
    try:
        mermaid_output = cecl_workflow.workflow.get_graph().draw_mermaid()
        with open("cecl_workflow_fixed_test.mmd", "w") as f:
            f.write(mermaid_output)
        print("Mermaid code saved as: cecl_workflow_fixed_test.mmd")

        print("\n🔧 Generated Mermaid Code Preview:")
        print("-" * 50)
        print(
            mermaid_output[:800] + "..."
            if len(mermaid_output) > 800
            else mermaid_output
        )

    except Exception as e:
        print(f"Error saving Mermaid file: {e}")

    # Check graph structure
    graph = cecl_workflow.workflow.get_graph()
    print(f"\n📊 Graph Structure Analysis:")
    print(f"Number of nodes: {len(graph.nodes)}")
    print(f"Number of edges: {len(graph.edges)}")

    print(f"\n🔗 Edge Connection Details:")
    for edge in graph.edges:
        print(f"  {edge.source} → {edge.target}")

    print(f"\n✅ Fix Results:")
    if len(graph.edges) > 0:
        print("✅ Success: Graph now contains edge connections!")
        print("✅ PNG file should now display arrow connections")
    else:
        print("❌ Failed: Graph still has no edge connections")

    return cecl_workflow


if __name__ == "__main__":
    workflow = test_workflow_visualization()
