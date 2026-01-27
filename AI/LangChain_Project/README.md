# LangChain with Open-Source Models

A comprehensive guide demonstrating LangChain capabilities using open-source models via Ollama.

## 📚 Features Covered

1. **Basic LLM Usage** - Simple text generation with open-source models
2. **Prompt Templates** - Dynamic, reusable prompt structures
3. **Chains** - Connect components for complex workflows
4. **Sequential Chains** - Multi-step processing pipelines
5. **Memory** - Maintain conversation context
6. **RAG (Retrieval-Augmented Generation)** - Question answering with custom documents
7. **Agents** - Autonomous reasoning with tools
8. **Output Parsers** - Extract structured data from responses
9. **Text Splitting** - Process large documents efficiently
10. **Chat Models** - Role-based conversational AI

## 🚀 Setup Instructions

### Step 1: Install Ollama

Download and install Ollama from [https://ollama.ai/](https://ollama.ai/)

### Step 2: Pull a Model

```bash
# Pull Llama 2 (7B parameters - good balance of speed and quality)
ollama pull llama2

# Alternative models:
# ollama pull mistral    # Faster, good for general tasks
# ollama pull codellama  # Optimized for coding
# ollama pull llama2:13b # Larger, more capable
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Examples

```bash
python main.py
```

## 📖 Code Structure

Each function in `main.py` demonstrates a specific LangChain feature:

- **Comprehensive docstrings** explain what each function does
- **Inline comments** clarify implementation details
- **Practical examples** show real-world usage patterns

## 🔧 Customization

### Change the Model

Replace `"llama2"` with any Ollama model:

```python
llm = Ollama(model="mistral")  # or "codellama", "llama2:13b", etc.
```

### Adjust Temperature

Control randomness (0.0 = deterministic, 1.0 = creative):

```python
llm = Ollama(model="llama2", temperature=0.7)
```

### Use Different Embeddings

Change the embeddings model for RAG:

```python
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"  # More accurate, slower
)
```

## 📝 Example Use Cases

### 1. Document Q&A System
Use the RAG example to build a system that answers questions based on your documents.

### 2. Conversational Chatbot
Combine memory and chat models for context-aware conversations.

### 3. Data Extraction
Use output parsers to extract structured information from unstructured text.

### 4. Content Generation Pipeline
Use sequential chains for multi-step content creation workflows.

## 🐛 Troubleshooting

### "Connection Error"
- Make sure Ollama is running: Check if you can access http://localhost:11434
- Restart Ollama if needed

### "Model not found"
- Pull the model: `ollama pull llama2`
- Check available models: `ollama list`

### Slow Performance
- Use a smaller model: `ollama pull mistral`
- Reduce temperature for faster responses
- Use GPU if available (Ollama auto-detects)

## 📚 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Open-Source LLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)

## 🤝 Contributing

Feel free to add more examples or improve existing ones!

## 📄 License

See LICENSE file in the root directory.
