"""
LangChain Complete Guide with Open-Source Models
================================================

This module demonstrates comprehensive LangChain usage with open-source models,
including chains, agents, memory, RAG, and more.

Author: AI Assistant
Date: January 26, 2026
"""

# ============================================================================
# IMPORTS
# ============================================================================

from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain_core.documents import Document
from typing import List, Dict, Any
import os


# ============================================================================
# 1. BASIC LLM USAGE WITH OPEN-SOURCE MODEL
# ============================================================================

def basic_llm_example():
    """
    Demonstrates basic LLM usage with Ollama (open-source model runtime).
    
    This example shows:
    - How to initialize an open-source LLM
    - Simple prompt execution
    - Basic text generation
    
    Requirements:
    - Ollama must be installed and running
    - A model like 'llama2' or 'mistral' must be pulled
    
    Returns:
        str: Generated response from the model
    """
    # Initialize Ollama with a specific model
    # Ollama supports models like llama2, mistral, codellama, etc.
    llm = Ollama(
        model="llama2",  # You can change this to "mistral", "codellama", etc.
        temperature=0.7,  # Controls randomness (0.0 = deterministic, 1.0 = creative)
    )
    
    # Simple prompt
    prompt = "Explain what LangChain is in 2 sentences."
    
    # Generate response
    response = llm.invoke(prompt)
    
    print("=== Basic LLM Example ===")
    print(f"Prompt: {prompt}")
    print(f"Response: {response}")
    print()
    
    return response


# ============================================================================
# 2. PROMPT TEMPLATES
# ============================================================================

def prompt_template_example():
    """
    Demonstrates the use of prompt templates for dynamic prompt generation.
    
    Prompt templates allow you to:
    - Create reusable prompt structures
    - Insert variables dynamically
    - Maintain consistency across prompts
    
    Returns:
        str: Generated response based on template
    """
    # Initialize the LLM
    llm = Ollama(model="llama2", temperature=0.5)
    
    # Create a prompt template with variables
    # Variables are defined using curly braces {}
    template = """
    You are a helpful AI assistant specialized in {domain}.
    
    User Question: {question}
    
    Please provide a detailed and accurate answer.
    """
    
    # Create PromptTemplate object
    prompt = PromptTemplate(
        input_variables=["domain", "question"],  # Define variables
        template=template
    )
    
    # Format the prompt with actual values
    formatted_prompt = prompt.format(
        domain="Python programming",
        question="What are decorators and how do they work?"
    )
    
    # Generate response
    response = llm.invoke(formatted_prompt)
    
    print("=== Prompt Template Example ===")
    print(f"Formatted Prompt:\n{formatted_prompt}")
    print(f"Response: {response}")
    print()
    
    return response


# ============================================================================
# 3. CHAINS - CONNECTING COMPONENTS
# ============================================================================

def simple_chain_example():
    """
    Demonstrates LangChain's chain functionality using LCEL (LangChain Expression Language).
    
    Chains allow you to:
    - Connect multiple components (prompts, models, parsers)
    - Create pipelines for processing
    - Build complex workflows from simple components
    
    Returns:
        str: Parsed output from the chain
    """
    # Initialize components
    llm = Ollama(model="llama2", temperature=0.7)
    
    # Create a prompt template
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="Write a short poem about {topic}."
    )
    
    # Create an output parser
    output_parser = StrOutputParser()
    
    # Create a chain using LCEL (LangChain Expression Language)
    # The pipe operator (|) connects components in sequence
    chain = prompt | llm | output_parser
    
    # Execute the chain
    result = chain.invoke({"topic": "artificial intelligence"})
    
    print("=== Simple Chain Example ===")
    print(f"Result:\n{result}")
    print()
    
    return result


# ============================================================================
# 4. SEQUENTIAL CHAINS - MULTIPLE STEPS
# ============================================================================

def sequential_chain_example():
    """
    Demonstrates sequential chains for multi-step processing.
    
    Sequential chains:
    - Execute multiple chains in order
    - Pass outputs from one chain as inputs to the next
    - Enable complex, multi-stage reasoning
    
    Returns:
        Dict: Final output from the sequential chain
    """
    # Initialize LLM
    llm = Ollama(model="llama2", temperature=0.7)
    
    # First chain: Generate a story idea
    idea_template = """Generate a creative story idea about {theme} in one sentence."""
    idea_prompt = PromptTemplate(
        input_variables=["theme"],
        template=idea_template
    )
    idea_chain = LLMChain(
        llm=llm,
        prompt=idea_prompt,
        output_key="story_idea"  # Name the output for next chain
    )
    
    # Second chain: Expand the idea into a plot
    plot_template = """Based on this story idea: {story_idea}
    
    Create a brief 3-sentence plot outline."""
    plot_prompt = PromptTemplate(
        input_variables=["story_idea"],
        template=plot_template
    )
    plot_chain = LLMChain(
        llm=llm,
        prompt=plot_prompt,
        output_key="plot_outline"
    )
    
    # Combine chains sequentially
    sequential_chain = SequentialChain(
        chains=[idea_chain, plot_chain],
        input_variables=["theme"],  # Initial input
        output_variables=["story_idea", "plot_outline"],  # Outputs to return
        verbose=True  # Print intermediate steps
    )
    
    # Execute the sequential chain
    result = sequential_chain.invoke({"theme": "time travel"})
    
    print("=== Sequential Chain Example ===")
    print(f"Story Idea: {result['story_idea']}")
    print(f"Plot Outline: {result['plot_outline']}")
    print()
    
    return result


# ============================================================================
# 5. MEMORY - CONVERSATION CONTEXT
# ============================================================================

def memory_example():
    """
    Demonstrates conversation memory for maintaining context across interactions.
    
    Memory allows:
    - Chatbots to remember previous messages
    - Context-aware conversations
    - Different storage strategies (buffer, summary, etc.)
    
    Returns:
        List[str]: Responses from the conversation
    """
    # Initialize LLM
    llm = Ollama(model="llama2", temperature=0.7)
    
    # Create conversation memory
    # ConversationBufferMemory stores all messages
    memory = ConversationBufferMemory(
        memory_key="chat_history",  # Key to store history
        return_messages=True  # Return as message objects
    )
    
    # Create a conversational prompt
    template = """The following is a conversation with an AI assistant.
    
    Chat History: {chat_history}
    
    Human: {input}
    AI Assistant:"""
    
    prompt = PromptTemplate(
        input_variables=["chat_history", "input"],
        template=template
    )
    
    # Create chain with memory
    conversation_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=True
    )
    
    # Simulate a conversation
    responses = []
    
    # First interaction
    response1 = conversation_chain.invoke({"input": "My name is Alex."})
    responses.append(response1['text'])
    print(f"User: My name is Alex.")
    print(f"AI: {response1['text']}\n")
    
    # Second interaction - AI should remember the name
    response2 = conversation_chain.invoke({"input": "What's my name?"})
    responses.append(response2['text'])
    print(f"User: What's my name?")
    print(f"AI: {response2['text']}\n")
    
    # Third interaction - Test context retention
    response3 = conversation_chain.invoke({"input": "What did I tell you about myself?"})
    responses.append(response3['text'])
    print(f"User: What did I tell you about myself?")
    print(f"AI: {response3['text']}\n")
    
    print("=== Memory Example Complete ===")
    print()
    
    return responses


# ============================================================================
# 6. RAG (RETRIEVAL-AUGMENTED GENERATION)
# ============================================================================

def rag_example():
    """
    Demonstrates Retrieval-Augmented Generation (RAG) with vector database.
    
    RAG combines:
    - Document storage in vector database
    - Semantic search for relevant context
    - LLM generation based on retrieved context
    
    This enables:
    - Question answering over custom documents
    - Grounded responses (reduces hallucination)
    - Scalable knowledge bases
    
    Returns:
        str: Answer generated using RAG
    """
    # Sample documents to index
    documents = [
        Document(
            page_content="LangChain is a framework for developing applications powered by language models. It enables applications that are context-aware and reason.",
            metadata={"source": "doc1"}
        ),
        Document(
            page_content="Vector databases store embeddings and enable semantic search. Popular options include Chroma, Pinecone, and Weaviate.",
            metadata={"source": "doc2"}
        ),
        Document(
            page_content="RAG (Retrieval-Augmented Generation) combines retrieval of relevant documents with LLM generation to provide accurate, grounded responses.",
            metadata={"source": "doc3"}
        ),
        Document(
            page_content="Open-source LLMs like Llama 2, Mistral, and Falcon can be run locally using tools like Ollama or GPT4All.",
            metadata={"source": "doc4"}
        ),
    ]
    
    # Initialize embeddings model (runs locally)
    # This converts text into numerical vectors
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"  # Lightweight, fast model
    )
    
    # Create vector database from documents
    # Chroma is an open-source vector database
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name="langchain_demo"
    )
    
    # Initialize LLM
    llm = Ollama(model="llama2", temperature=0.3)  # Lower temp for factual responses
    
    # Create retrieval QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # "stuff" puts all retrieved docs into prompt
        retriever=vectorstore.as_retriever(
            search_kwargs={"k": 2}  # Retrieve top 2 most relevant documents
        ),
        return_source_documents=True,  # Return source docs for transparency
        verbose=True
    )
    
    # Ask a question
    question = "What is RAG and why is it useful?"
    result = qa_chain.invoke({"query": question})
    
    print("=== RAG Example ===")
    print(f"Question: {question}")
    print(f"Answer: {result['result']}")
    print(f"\nSource Documents:")
    for i, doc in enumerate(result['source_documents'], 1):
        print(f"{i}. {doc.page_content[:100]}... (Source: {doc.metadata['source']})")
    print()
    
    # Cleanup
    vectorstore.delete_collection()
    
    return result['result']


# ============================================================================
# 7. AGENTS - AUTONOMOUS REASONING
# ============================================================================

def agent_example():
    """
    Demonstrates LangChain agents with tools.
    
    Agents can:
    - Reason about which tools to use
    - Execute multi-step plans
    - Make decisions based on observations
    
    This example creates a simple agent with custom tools.
    
    Returns:
        str: Agent's final response
    """
    # Initialize LLM
    llm = Ollama(model="llama2", temperature=0)
    
    # Define custom tools
    def calculate_tool(expression: str) -> str:
        """Evaluates a mathematical expression."""
        try:
            # Safe evaluation for simple math
            result = eval(expression, {"__builtins__": {}}, {})
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def length_tool(text: str) -> str:
        """Returns the length of the given text."""
        return str(len(text))
    
    # Create tool objects
    tools = [
        Tool(
            name="Calculator",
            func=calculate_tool,
            description="Useful for mathematical calculations. Input should be a valid Python mathematical expression like '2+2' or '10*5'."
        ),
        Tool(
            name="TextLength",
            func=length_tool,
            description="Useful for finding the length of text. Input should be a string."
        ),
    ]
    
    # Create agent prompt
    agent_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant with access to tools."),
        ("human", "{input}"),
        ("assistant", "Let me think step by step using the available tools."),
        ("assistant", "{agent_scratchpad}"),
    ])
    
    # Note: Agent creation requires specific template format
    # For demonstration purposes, we'll show tool usage manually
    print("=== Agent Example ===")
    print("Available Tools:")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")
    
    # Manual tool demonstration
    calc_result = calculate_tool("25 * 4")
    print(f"\nCalculator Tool: 25 * 4 = {calc_result}")
    
    text_result = length_tool("LangChain is awesome")
    print(f"TextLength Tool: Length of 'LangChain is awesome' = {text_result}")
    print()
    
    return "Agent tools demonstrated successfully"


# ============================================================================
# 8. OUTPUT PARSERS - STRUCTURED DATA
# ============================================================================

def output_parser_example():
    """
    Demonstrates output parsers for extracting structured data from LLM responses.
    
    Output parsers:
    - Convert unstructured LLM output to structured format
    - Validate output format
    - Enable downstream processing
    
    Returns:
        Dict: Parsed structured output
    """
    from langchain_core.pydantic_v1 import BaseModel, Field
    
    # Define output structure using Pydantic
    class Person(BaseModel):
        """Information about a person."""
        name: str = Field(description="The person's full name")
        age: int = Field(description="The person's age")
        occupation: str = Field(description="The person's job")
        hobbies: List[str] = Field(description="List of hobbies")
    
    # Initialize LLM and parser
    llm = Ollama(model="llama2", temperature=0.7)
    parser = JsonOutputParser(pydantic_object=Person)
    
    # Create prompt with format instructions
    prompt = PromptTemplate(
        template="""Generate information about a fictional person named {name}.
        
        {format_instructions}
        
        Return only the JSON, nothing else.""",
        input_variables=["name"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    # Create chain
    chain = prompt | llm | parser
    
    try:
        # Execute chain
        result = chain.invoke({"name": "Sarah"})
        
        print("=== Output Parser Example ===")
        print(f"Parsed Result: {result}")
        print(f"Type: {type(result)}")
        print()
        
        return result
    except Exception as e:
        print(f"Note: JSON parsing may vary with model responses. Error: {e}")
        return {}


# ============================================================================
# 9. TEXT SPLITTING - DOCUMENT PROCESSING
# ============================================================================

def text_splitting_example():
    """
    Demonstrates text splitting for processing large documents.
    
    Text splitting is essential for:
    - Breaking large documents into manageable chunks
    - Fitting content within token limits
    - Creating meaningful semantic units
    
    Returns:
        List[Document]: Split document chunks
    """
    # Sample long text
    long_text = """
    Artificial Intelligence (AI) has revolutionized numerous industries and aspects of daily life. 
    From healthcare to finance, AI systems are being deployed to solve complex problems and automate tasks.
    
    Machine Learning, a subset of AI, enables systems to learn from data without explicit programming.
    Deep Learning, using neural networks with multiple layers, has achieved breakthrough results in 
    image recognition, natural language processing, and game playing.
    
    Natural Language Processing (NLP) focuses on the interaction between computers and human language.
    Modern NLP systems can translate languages, summarize documents, answer questions, and even 
    generate human-like text.
    
    The ethical implications of AI are increasingly important. Issues like bias in algorithms, 
    privacy concerns, and the impact on employment require careful consideration and regulation.
    """
    
    # Create text splitter
    # RecursiveCharacterTextSplitter tries to split on natural boundaries
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,  # Maximum characters per chunk
        chunk_overlap=50,  # Overlap to maintain context between chunks
        length_function=len,  # Function to measure chunk size
        separators=["\n\n", "\n", " ", ""]  # Split on these in order of preference
    )
    
    # Split the text
    chunks = text_splitter.create_documents([long_text])
    
    print("=== Text Splitting Example ===")
    print(f"Original text length: {len(long_text)} characters")
    print(f"Number of chunks: {len(chunks)}")
    print()
    
    # Display chunks
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i} ({len(chunk.page_content)} chars):")
        print(f"{chunk.page_content[:100]}...")
        print()
    
    return chunks


# ============================================================================
# 10. CHAT MODELS - CONVERSATIONAL AI
# ============================================================================

def chat_model_example():
    """
    Demonstrates chat models with message history and role-based interactions.
    
    Chat models:
    - Support system, user, and assistant roles
    - Enable more structured conversations
    - Better for chatbot applications
    
    Returns:
        str: Chat model response
    """
    from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
    
    # Initialize chat model
    chat = ChatOllama(
        model="llama2",
        temperature=0.7
    )
    
    # Create messages with different roles
    messages = [
        SystemMessage(content="You are a helpful AI coding assistant specialized in Python."),
        HumanMessage(content="How do I read a CSV file in Python?"),
    ]
    
    # Get response
    response = chat.invoke(messages)
    
    print("=== Chat Model Example ===")
    print(f"System: {messages[0].content}")
    print(f"User: {messages[1].content}")
    print(f"Assistant: {response.content}")
    print()
    
    # Continue conversation
    messages.append(AIMessage(content=response.content))
    messages.append(HumanMessage(content="Can you show me a code example?"))
    
    response2 = chat.invoke(messages)
    print(f"User: {messages[3].content}")
    print(f"Assistant: {response2.content}")
    print()
    
    return response2.content


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main function to demonstrate all LangChain features.
    
    Executes all example functions in sequence to showcase
    the complete capabilities of LangChain with open-source models.
    """
    print("=" * 80)
    print("LANGCHAIN WITH OPEN-SOURCE MODELS - COMPLETE GUIDE")
    print("=" * 80)
    print()
    
    print("📋 Prerequisites:")
    print("1. Install Ollama: https://ollama.ai/")
    print("2. Pull a model: ollama pull llama2")
    print("3. Install requirements: pip install -r requirements.txt")
    print()
    print("=" * 80)
    print()
    
    try:
        # Run all examples
        basic_llm_example()
        prompt_template_example()
        simple_chain_example()
        sequential_chain_example()
        memory_example()
        rag_example()
        agent_example()
        output_parser_example()
        text_splitting_example()
        chat_model_example()
        
        print("=" * 80)
        print("✅ All examples completed successfully!")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure Ollama is installed and running with a model pulled.")
        print("Run: ollama pull llama2")


if __name__ == "__main__":
    main()
