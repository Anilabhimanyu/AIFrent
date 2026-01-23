# Cloud Services Comparison: AWS vs GCP vs Azure

## Table of Contents
1. [General Cloud Services](#general-cloud-services)
2. [AI/ML Services](#aiml-services)

---

## General Cloud Services

### Compute Services

| Category | AWS | GCP | Azure | Purpose |
|----------|-----|-----|-------|---------|
| **Virtual Machines** | EC2 (Elastic Compute Cloud) | Compute Engine | Virtual Machines | • Scalable virtual servers<br>• Run applications in the cloud<br>• Pay-as-you-go pricing<br>• Multiple instance types |
| **Containers** | ECS (Elastic Container Service) | GKE (Google Kubernetes Engine) | AKS (Azure Kubernetes Service) | • Orchestrate containerized apps<br>• Kubernetes management<br>• Auto-scaling<br>• Service discovery |
| **Serverless Functions** | Lambda | Cloud Functions | Azure Functions | • Run code without servers<br>• Event-driven execution<br>• Auto-scaling<br>• Pay per execution |
| **Batch Processing** | AWS Batch | Cloud Batch | Azure Batch | • Run large-scale parallel jobs<br>• Automatic resource provisioning<br>• Job scheduling<br>• Cost optimization |
| **App Hosting** | Elastic Beanstalk | App Engine | App Service | • Deploy web apps easily<br>• Managed platform<br>• Auto-scaling<br>• Built-in load balancing |

---

### Storage Services

| Category | AWS | GCP | Azure | Purpose |
|----------|-----|-----|-------|---------|
| **Object Storage** | S3 (Simple Storage Service) | Cloud Storage | Blob Storage | • Store unstructured data<br>• Highly durable (99.999999999%)<br>• Versioning support<br>• Lifecycle management |
| **Block Storage** | EBS (Elastic Block Store) | Persistent Disk | Managed Disks | • Persistent volumes for VMs<br>• High performance<br>• Snapshot support<br>• Multiple volume types |
| **File Storage** | EFS (Elastic File System) | Filestore | Azure Files | • Shared file system<br>• NFS/SMB protocols<br>• Scalable storage<br>• Multi-instance access |
| **Archive Storage** | S3 Glacier | Cloud Storage Archive | Archive Storage | • Long-term cold storage<br>• Low-cost archival<br>• Infrequent access<br>• Compliance retention |
| **Data Transfer** | DataSync, Snow Family | Transfer Service | Data Box, AzCopy | • Large data migration<br>• Physical device transfer<br>• Bandwidth optimization<br>• Hybrid cloud sync |

---

### Database Services

| Category | AWS | GCP | Azure | Purpose |
|----------|-----|-----|-------|---------|
| **Relational Database** | RDS (Relational Database Service) | Cloud SQL | Azure SQL Database | • Managed SQL databases<br>• Automated backups<br>• Multi-AZ deployment<br>• Read replicas |
| **NoSQL Database** | DynamoDB | Firestore, Bigtable | Cosmos DB | • Key-value/document store<br>• Millisecond latency<br>• Automatic scaling<br>• Global distribution |
| **Data Warehouse** | Redshift | BigQuery | Synapse Analytics | • Petabyte-scale analytics<br>• Columnar storage<br>• SQL queries<br>• Business intelligence |
| **In-Memory Cache** | ElastiCache | Memorystore | Azure Cache for Redis | • High-speed caching<br>• Sub-millisecond latency<br>• Session storage<br>• Database query caching |
| **Graph Database** | Neptune | - | Cosmos DB (Gremlin API) | • Graph relationships<br>• Social networks<br>• Fraud detection<br>• Knowledge graphs |

---

### Networking Services

| Category | AWS | GCP | Azure | Purpose |
|----------|-----|-----|-------|---------|
| **Virtual Network** | VPC (Virtual Private Cloud) | VPC | Virtual Network (VNet) | • Isolated network environment<br>• Subnet configuration<br>• IP address management<br>• Network security |
| **Load Balancer** | ELB (Elastic Load Balancing) | Cloud Load Balancing | Load Balancer | • Distribute traffic<br>• High availability<br>• Health monitoring<br>• SSL termination |
| **CDN** | CloudFront | Cloud CDN | Azure CDN | • Content delivery network<br>• Edge caching<br>• Low latency<br>• Global distribution |
| **DNS** | Route 53 | Cloud DNS | Azure DNS | • Domain name resolution<br>• Traffic routing<br>• Health checks<br>• Failover support |
| **VPN** | VPN Gateway | Cloud VPN | VPN Gateway | • Secure connection to cloud<br>• Site-to-site VPN<br>• Encrypted tunnel<br>• Hybrid connectivity |

---

### Security & Identity

| Category | AWS | GCP | Azure | Purpose |
|----------|-----|-----|-------|---------|
| **Identity Management** | IAM (Identity & Access Management) | Cloud IAM | Azure Active Directory | • User authentication<br>• Role-based access control<br>• Policy management<br>• Multi-factor authentication |
| **Key Management** | KMS (Key Management Service) | Cloud KMS | Key Vault | • Encryption key management<br>• Secret storage<br>• Certificate management<br>• Hardware security modules |
| **Security Monitoring** | GuardDuty, Security Hub | Security Command Center | Microsoft Defender | • Threat detection<br>• Vulnerability scanning<br>• Compliance monitoring<br>• Security recommendations |
| **DDoS Protection** | AWS Shield | Cloud Armor | DDoS Protection | • DDoS attack mitigation<br>• Always-on detection<br>• Automatic response<br>• Network protection |
| **Web Application Firewall** | WAF | Cloud Armor | Web Application Firewall | • Protect web applications<br>• SQL injection prevention<br>• XSS protection<br>• Custom rules |

---

### Analytics & Big Data

| Category | AWS | GCP | Azure | Purpose |
|----------|-----|-----|-------|---------|
| **Data Lake** | S3 + Lake Formation | Cloud Storage + Dataproc | Data Lake Storage | • Centralized repository<br>• Store structured/unstructured data<br>• Analytics at scale<br>• Schema-on-read |
| **Stream Processing** | Kinesis | Dataflow | Stream Analytics | • Real-time data processing<br>• Event streaming<br>• Time-series analysis<br>• IoT data ingestion |
| **ETL Service** | Glue | Dataflow, Dataprep | Data Factory | • Extract, transform, load<br>• Data pipeline orchestration<br>• Serverless ETL<br>• Schema discovery |
| **Data Catalog** | Glue Data Catalog | Data Catalog | Purview | • Metadata management<br>• Data discovery<br>• Data lineage<br>• Governance |
| **Business Intelligence** | QuickSight | Looker, Data Studio | Power BI | • Data visualization<br>• Interactive dashboards<br>• Self-service analytics<br>• Report generation |

---

### Monitoring & Management

| Category | AWS | GCP | Azure | Purpose |
|----------|-----|-----|-------|---------|
| **Monitoring** | CloudWatch | Cloud Monitoring | Azure Monitor | • Performance metrics<br>• Log aggregation<br>• Custom metrics<br>• Alerting |
| **Logging** | CloudWatch Logs | Cloud Logging | Log Analytics | • Centralized logging<br>• Log query and analysis<br>• Log retention<br>• Troubleshooting |
| **Tracing** | X-Ray | Cloud Trace | Application Insights | • Distributed tracing<br>• Performance bottlenecks<br>• Request tracking<br>• Service dependencies |
| **Configuration Management** | Systems Manager | Cloud Deployment Manager | Automation | • Infrastructure automation<br>• Configuration management<br>• Patch management<br>• Change tracking |

---

### Developer Tools

| Category | AWS | GCP | Azure | Purpose |
|----------|-----|-----|-------|---------|
| **CI/CD** | CodePipeline | Cloud Build | Azure DevOps | • Continuous integration<br>• Continuous deployment<br>• Build automation<br>• Release management |
| **Source Control** | CodeCommit | Cloud Source Repositories | Azure Repos | • Git repository hosting<br>• Version control<br>• Code collaboration<br>• Branch management |
| **Container Registry** | ECR (Elastic Container Registry) | Container Registry | Container Registry | • Store Docker images<br>• Image scanning<br>• Access control<br>• Integration with K8s |
| **API Gateway** | API Gateway | API Gateway | API Management | • API creation and management<br>• Rate limiting<br>• Authentication<br>• API monitoring |

---

## AI/ML Services

### Foundation AI Services

| Category | AWS | GCP | Azure | Purpose |
|----------|-----|-----|-------|---------|
| **Large Language Models** | Bedrock | Vertex AI (PaLM 2, Gemini) | Azure OpenAI Service | • Access pre-trained LLMs<br>• GPT, Claude, Llama models<br>• Fine-tuning support<br>• Text generation |
| **Model Training Platform** | SageMaker | Vertex AI | Azure Machine Learning | • Train custom ML models<br>• Jupyter notebooks<br>• Distributed training<br>• Model versioning |
| **AutoML** | SageMaker Autopilot | Vertex AI AutoML | Azure AutoML | • Automated model training<br>• Feature engineering<br>• Hyperparameter tuning<br>• No-code ML |
| **Model Deployment** | SageMaker Endpoints | Vertex AI Endpoints | Azure ML Endpoints | • Deploy models to production<br>• Real-time inference<br>• Batch predictions<br>• Auto-scaling |
| **ML Pipeline** | SageMaker Pipelines | Vertex AI Pipelines | Azure ML Pipelines | • Orchestrate ML workflows<br>• Automated retraining<br>• Experiment tracking<br>• CI/CD for ML |

---

### Computer Vision

| Category | AWS | GCP | Azure | Purpose |
|----------|-----|-----|-------|---------|
| **Image Recognition** | Rekognition | Vision AI | Computer Vision | • Object detection<br>• Facial recognition<br>• Label detection<br>• Content moderation |
| **OCR (Text Extraction)** | Textract | Document AI | Form Recognizer | • Extract text from images<br>• Document understanding<br>• Form processing<br>• Handwriting recognition |
| **Video Analysis** | Rekognition Video | Video AI | Video Indexer | • Video content analysis<br>• Action recognition<br>• Celebrity detection<br>• Scene detection |
| **Custom Vision** | SageMaker + Custom Models | AutoML Vision | Custom Vision | • Train custom vision models<br>• Transfer learning<br>• Edge deployment<br>• Domain-specific recognition |

---

### Natural Language Processing

| Category | AWS | GCP | Azure | Purpose |
|----------|-----|-----|-------|---------|
| **Language Understanding** | Comprehend | Natural Language API | Language Service | • Sentiment analysis<br>• Entity extraction<br>• Key phrase detection<br>• Language detection |
| **Text Translation** | Translate | Cloud Translation API | Translator | • Multi-language translation<br>• 100+ languages<br>• Real-time translation<br>• Custom terminology |
| **Speech-to-Text** | Transcribe | Speech-to-Text API | Speech Service | • Convert speech to text<br>• Real-time transcription<br>• Multiple languages<br>• Custom vocabulary |
| **Text-to-Speech** | Polly | Text-to-Speech API | Speech Service (TTS) | • Convert text to speech<br>• Natural-sounding voices<br>• SSML support<br>• Custom voices |
| **Conversational AI** | Lex | Dialogflow | Bot Service | • Build chatbots<br>• Natural conversation<br>• Intent recognition<br>• Multi-channel deployment |

---

### Specialized AI Services

| Category | AWS | GCP | Azure | Purpose |
|----------|-----|-----|-------|---------|
| **Search Service** | Kendra | Vertex AI Search | Cognitive Search | • Enterprise search<br>• Semantic search<br>• Vector search<br>• Document indexing |
| **Recommendation Engine** | Personalize | Recommendations AI | Personalizer | • Personalized recommendations<br>• User behavior analysis<br>• Real-time suggestions<br>• A/B testing |
| **Forecasting** | Forecast | Vertex AI Forecasting | Time Series Insights | • Time-series predictions<br>• Demand forecasting<br>• Anomaly detection<br>• Capacity planning |
| **Fraud Detection** | Fraud Detector | - | Fraud Protection | • Real-time fraud detection<br>• Machine learning models<br>• Risk scoring<br>• Transaction monitoring |
| **Document Intelligence** | Textract | Document AI | Form Recognizer | • Intelligent document processing<br>• Form extraction<br>• Table detection<br>• Key-value pairs |

---

### AI Infrastructure

| Category | AWS | GCP | Azure | Purpose |
|----------|-----|-----|-------|---------|
| **GPU Instances** | EC2 P4/G5 instances | A2/A3 instances | NC/ND-series VMs | • Train deep learning models<br>• GPU acceleration<br>• High performance computing<br>• Parallel processing |
| **AI Chips** | Trainium, Inferentia | TPU (Tensor Processing Unit) | - | • Custom AI accelerators<br>• Cost-effective training<br>• Optimized inference<br>• High throughput |
| **Distributed Training** | SageMaker Distributed Training | Vertex AI Training | Azure ML Distributed Training | • Multi-GPU/multi-node training<br>• Data parallelism<br>• Model parallelism<br>• Large-scale models |
| **Feature Store** | SageMaker Feature Store | Vertex AI Feature Store | Azure ML Feature Store | • Centralized feature repository<br>• Feature sharing<br>• Online/offline serving<br>• Feature versioning |
| **Model Registry** | SageMaker Model Registry | Vertex AI Model Registry | Azure ML Model Registry | • Model versioning<br>• Model lineage<br>• Deployment tracking<br>• Governance |

---

### Vector Database & Embeddings

| Category | AWS | GCP | Azure | Purpose |
|----------|-----|-----|-------|---------|
| **Vector Database** | OpenSearch + Vector Engine | Vertex AI Vector Search | Cosmos DB Vector Search | • Store embeddings<br>• Similarity search<br>• Semantic search<br>• RAG applications |
| **Embedding Generation** | Bedrock Embeddings | Vertex AI Embeddings | Azure OpenAI Embeddings | • Generate text embeddings<br>• Semantic representation<br>• Multiple models<br>• Custom fine-tuning |

---

### MLOps & Governance

| Category | AWS | GCP | Azure | Purpose |
|----------|-----|-----|-------|---------|
| **Experiment Tracking** | SageMaker Experiments | Vertex AI Experiments | Azure ML Experiments | • Track training runs<br>• Compare metrics<br>• Parameter logging<br>• Visualization |
| **Model Monitoring** | SageMaker Model Monitor | Vertex AI Model Monitoring | Azure ML Model Monitoring | • Detect model drift<br>• Data quality monitoring<br>• Performance tracking<br>• Automated alerts |
| **Bias Detection** | SageMaker Clarify | - | Fairlearn Integration | • Detect model bias<br>• Fairness metrics<br>• Explainability<br>• Compliance reporting |
| **Model Explainability** | SageMaker Clarify | Vertex AI Explainable AI | Azure ML Interpretability | • Feature importance<br>• Model transparency<br>• SHAP values<br>• Trust & compliance |

---

### Generative AI Services

| Category | AWS | GCP | Azure | Purpose |
|----------|-----|-----|-------|---------|
| **Foundation Models** | Bedrock (Claude, Llama, Mistral) | Vertex AI (Gemini, PaLM, Llama) | Azure OpenAI (GPT-4, GPT-3.5) | • Access state-of-the-art LLMs<br>• Multiple model providers<br>• Fine-tuning capabilities<br>• Prompt engineering |
| **Code Generation** | CodeWhisperer | Gemini Code Assist | GitHub Copilot (Azure) | • AI-powered coding<br>• Code suggestions<br>• Code completion<br>• Security scanning |
| **Image Generation** | Bedrock (Stable Diffusion) | Vertex AI Imagen | Azure OpenAI DALL-E | • Text-to-image generation<br>• Image editing<br>• Style transfer<br>• Creative content |
| **Agent Framework** | Bedrock Agents | Vertex AI Agent Builder | Azure AI Agent Service | • Build autonomous agents<br>• Tool integration<br>• Multi-step reasoning<br>• Memory management |
| **RAG (Retrieval Augmented Generation)** | Bedrock Knowledge Bases | Vertex AI RAG | Azure AI Search + OpenAI | • Connect LLMs to data<br>• Document retrieval<br>• Grounded responses<br>• Citation support |

---

### AI Development Tools

| Category | AWS | GCP | Azure | Purpose |
|----------|-----|-----|-------|---------|
| **Notebooks** | SageMaker Studio | Vertex AI Workbench | Azure ML Notebooks | • Jupyter notebooks<br>• Collaborative environment<br>• Version control<br>• Git integration |
| **Data Labeling** | SageMaker Ground Truth | Vertex AI Data Labeling | Azure ML Data Labeling | • Annotate training data<br>• Human-in-the-loop<br>• Active learning<br>• Quality control |
| **Model Marketplace** | SageMaker Marketplace | Model Garden | Azure Marketplace | • Pre-trained models<br>• Third-party models<br>• Quick deployment<br>• Model discovery |

---

## Quick Reference: Service Equivalents

### Most Common AI/ML Mappings

| Purpose | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **LLM Access** | Bedrock | Vertex AI (Gemini) | Azure OpenAI Service |
| **ML Platform** | SageMaker | Vertex AI | Azure Machine Learning |
| **Image Recognition** | Rekognition | Vision AI | Computer Vision |
| **NLP/Text Analysis** | Comprehend | Natural Language API | Language Service |
| **Speech Services** | Transcribe/Polly | Speech-to-Text/TTS | Speech Service |
| **Chatbots** | Lex | Dialogflow | Bot Service |
| **Translation** | Translate | Cloud Translation | Translator |
| **Search + AI** | Kendra | Vertex AI Search | Cognitive Search |
| **Document Processing** | Textract | Document AI | Form Recognizer |
| **Custom Vision** | SageMaker | AutoML Vision | Custom Vision |
| **Vector Search** | OpenSearch Vector | Vertex AI Vector Search | Cosmos DB Vector |
| **RAG Platform** | Bedrock Knowledge Bases | Vertex AI RAG | Azure AI Search + OpenAI |

---

## Key Considerations When Choosing

### AWS (Amazon Web Services)
- ✓ Largest market share and ecosystem
- ✓ Most mature services and extensive features
- ✓ Bedrock for multi-model LLM access
- ✓ Strong enterprise adoption
- ✗ Steeper learning curve
- ✗ Complex pricing

### GCP (Google Cloud Platform)
- ✓ Best for data analytics and ML
- ✓ Gemini/PaLM native access
- ✓ TPU availability for training
- ✓ BigQuery integration
- ✓ Strong open-source support
- ✗ Smaller market share
- ✗ Fewer third-party integrations

### Azure (Microsoft Azure)
- ✓ Best for enterprise/Microsoft shops
- ✓ Azure OpenAI exclusive partnership
- ✓ Strong hybrid cloud support
- ✓ Active Directory integration
- ✓ Office 365 integration
- ✗ Service naming can be confusing
- ✗ Regional availability varies

---

## Cost Considerations

### General Pricing Patterns

| Service Type | Typical Pricing Model |
|-------------|----------------------|
| **Compute** | Per hour/second + instance type |
| **Storage** | Per GB stored + requests |
| **Database** | Instance size + storage + I/O |
| **AI/ML APIs** | Per API call / Per unit (images, minutes, tokens) |
| **Model Training** | Compute time + instance type |
| **LLM Usage** | Per token (input + output) |
| **Vector Search** | Storage + queries |

### Cost Optimization Tips
1. Use spot/preemptible instances for training
2. Reserved instances for production workloads
3. Auto-scaling to match demand
4. Archive infrequently accessed data
5. Use smaller models when possible
6. Batch processing for non-real-time tasks
7. Monitor and optimize token usage for LLMs
8. Use caching for repeated queries

---

**Last Updated:** January 2026

**Note:** Cloud services evolve rapidly. Always check official documentation for the latest offerings and pricing.
