"""
Prefect flow for legal research workflow.

This module implements the legal_research_flow orchestrating 6 specialized agent tasks.
"""

import logging
from prefect import flow, task
from app.services.openai_client import get_openai_service

logger = logging.getLogger(__name__)


@task(name="prepare_query_agent")
def prepare_query_agent(topic: str) -> str:
    """
    Prepare and structure the legal research query.
    
    This agent normalizes and clarifies the research topic into a focused legal question.
    
    Args:
        topic: The raw legal research topic from the user
        
    Returns:
        A structured and clarified research query
    """
    logger.info(f"[Prepare Query Agent] Structuring legal research topic: {topic}")
    
    openai_service = get_openai_service()
    
    prompt = f"""You are a legal research coordinator. The user has requested legal research on the following topic:

"{topic}"

Your task: Restructure this topic into a clear, focused legal research question. Make it specific and actionable for legal research.

Return only the restructured question, nothing else."""
    
    prepared_query = openai_service.generate_text(prompt, temperature=0.5, max_tokens=300)
    logger.info("[Prepare Query Agent] Query preparation complete")
    
    return prepared_query


@task(name="research_agent")
def research_agent(prepared_query: str) -> str:
    """
    Conduct legal research on the prepared query.
    
    This agent generates high-level legal context and identifies major themes.
    
    Args:
        prepared_query: The structured legal research question from prepare_query_agent
        
    Returns:
        Legal research notes and context
    """
    logger.info("[Research Agent] Gathering legal context and frameworks for research")
    
    openai_service = get_openai_service()
    
    prompt = f"""You are a legal research specialist. Based on the following legal research question:

"{prepared_query}"

Provide a concise summary of the major legal themes, frameworks, and areas of law that are relevant. Focus on:
- Key legal areas involved
- Regulatory contexts
- Common legal principles that apply

Keep your response to 3-4 key points, each 1-2 sentences."""
    
    research_notes = openai_service.generate_text(prompt, temperature=0.7, max_tokens=400)
    logger.info("[Research Agent] Legal research context gathering complete")
    
    return research_notes


@task(name="risk_assessment_agent")
def risk_assessment_agent(prepared_query: str, research_notes: str) -> str:
    """
    Assess potential risks and liabilities.
    
    This agent identifies practical business risks and exposure areas relevant to the topic.
    
    Args:
        prepared_query: The structured legal research question
        research_notes: Context from the research agent
        
    Returns:
        Risk assessment analysis
    """
    logger.info("[Risk Assessment Agent] Evaluating contractual liabilities and business exposure")
    
    openai_service = get_openai_service()
    
    prompt = f"""You are a legal risk analyst specializing in business risk. Based on this legal research question:

"{prepared_query}"

And considering these legal frameworks and themes:
{research_notes}

Identify the top 3-4 business risks and liability exposure areas. For each risk:
- Name the risk clearly
- Explain the potential impact (1-2 sentences)

Focus on practical, material risks that a business should care about."""
    
    risk_assessment = openai_service.generate_text(prompt, temperature=0.7, max_tokens=400)
    logger.info("[Risk Assessment Agent] Risk assessment complete")
    
    return risk_assessment


@task(name="precedent_search_agent")
def precedent_search_agent(prepared_query: str, research_notes: str) -> str:
    """
    Search for analogous cases and precedents.
    
    This agent generates plausible precedent-style guidance and examples.
    
    Args:
        prepared_query: The structured legal research question
        research_notes: Context from the research agent
        
    Returns:
        Precedent and case guidance
    """
    logger.info("[Precedent Search Agent] Searching analogous business scenarios and case patterns")
    
    openai_service = get_openai_service()
    
    prompt = f"""You are a legal case analyst. Based on this legal research question:

"{prepared_query}"

Considering these legal themes:
{research_notes}

Generate 2-3 analogous business scenarios or pattern-based guidance (similar to precedent):
- Describe each scenario or pattern (1-2 sentences)
- Explain how it applies or what it illustrates

These should be realistic scenarios that illustrate legal principles, not necessarily real cases."""
    
    precedent_notes = openai_service.generate_text(prompt, temperature=0.7, max_tokens=400)
    logger.info("[Precedent Search Agent] Precedent search and scenario analysis complete")
    
    return precedent_notes


@task(name="legal_reasoning_agent")
def legal_reasoning_agent(research_notes: str, risk_assessment: str, precedent_notes: str) -> str:
    """
    Synthesize findings into coherent legal reasoning.
    
    This agent integrates research, risk, and precedent findings into a unified legal interpretation.
    
    Args:
        research_notes: Legal context and frameworks
        risk_assessment: Identified risks and liabilities
        precedent_notes: Analogous scenarios and guidance
        
    Returns:
        Synthesized legal reasoning
    """
    logger.info("[Legal Reasoning Agent] Synthesizing findings into comprehensive legal interpretation")
    
    openai_service = get_openai_service()
    
    prompt = f"""You are a senior legal analyst tasked with synthesizing research findings.

You have gathered the following information:

LEGAL FRAMEWORKS AND CONTEXT:
{research_notes}

IDENTIFIED RISKS:
{risk_assessment}

ANALOGOUS SCENARIOS AND GUIDANCE:
{precedent_notes}

Your task: Synthesize all of this into a coherent legal interpretation that:
1. Connects the risks to the legal frameworks
2. Explains the implications
3. Draws conclusions about how the analogous scenarios inform the current situation

Provide 3-4 paragraphs of integrated legal reasoning."""
    
    legal_reasoning = openai_service.generate_text(prompt, temperature=0.7, max_tokens=600)
    logger.info("[Legal Reasoning Agent] Legal reasoning synthesis complete")
    
    return legal_reasoning


@task(name="briefing_agent")
def briefing_agent(legal_reasoning: str) -> str:
    """
    Generate executive legal briefing.
    
    This agent produces a final, business-facing legal briefing in a structured format.
    
    Args:
        legal_reasoning: Synthesized legal reasoning from previous agents
        
    Returns:
        Formatted executive legal briefing
    """
    logger.info("[Briefing Agent] Generating executive legal briefing for leadership")
    
    openai_service = get_openai_service()
    
    prompt = f"""You are a legal briefing specialist creating an executive summary for business leadership.

Based on this legal reasoning and analysis:
{legal_reasoning}

Create a concise executive briefing with exactly this structure:

Key Issue:
[A 1-2 sentence statement of the core legal issue or question]

Potential Risk:
[A 1-2 sentence description of the primary business risk or liability exposure]

Recommended Action:
[A 1-2 sentence recommendation for how to address or mitigate the risk]

Keep the entire briefing to under 200 words. Use clear, non-technical business language."""
    
    briefing = openai_service.generate_text(prompt, temperature=0.7, max_tokens=300)
    logger.info("[Briefing Agent] Executive briefing generation complete")
    
    return briefing


@flow(name="legal_research_flow")
def legal_research_flow(topic: str) -> str:
    """
    Orchestrate the legal research workflow.
    
    This flow coordinates 6 specialized agent tasks to conduct comprehensive legal research
    and produce an executive briefing.
    
    Workflow shape:
    - prepare_query_agent: Normalize and structure the topic
    - research_agent: Gather legal context and frameworks
    - risk_assessment_agent: Identify business risks
    - precedent_search_agent: Find analogous scenarios
    - legal_reasoning_agent: Synthesize findings
    - briefing_agent: Generate executive summary
    
    Args:
        topic: The legal research topic from the user
        
    Returns:
        Final legal briefing summary
    """
    logger.info(f"[LEGAL RESEARCH FLOW] Starting workflow for topic: {topic}")
    
    # Step 1: Prepare the query
    prepared_query = prepare_query_agent(topic)
    
    # Step 2: Research legal context
    research_notes = research_agent(prepared_query)
    
    # Step 3: Assess risks
    risk_assessment = risk_assessment_agent(prepared_query, research_notes)
    
    # Step 4: Search precedents
    precedent_notes = precedent_search_agent(prepared_query, research_notes)
    
    # Step 5: Synthesize reasoning
    legal_reasoning = legal_reasoning_agent(research_notes, risk_assessment, precedent_notes)
    
    # Step 6: Generate briefing
    briefing = briefing_agent(legal_reasoning)
    
    logger.info("[LEGAL RESEARCH FLOW] Workflow complete - briefing generated successfully")
    
    return briefing
