# Complete Syllabus — AI Engineering (Revised & Expanded)

> A production-focused syllabus for becoming a bulletproof AI engineer.
> Covers foundations → agents → systems → FDE craft → infra → internals → capstones.

---

## Phase 1 — AI & LLM Engineering (Foundations)

### 1.1 LLM Fundamentals
- What an LLM is: stateless next-token predictor
- The generation pipeline: text → tokens → IDs → transformer → logits → sample → detokenize
- Prefill vs Decode (two phases of inference)
- KV cache (high-level)
- Context window and its limits
- Training stages: pretraining → SFT → RLHF/DPO
- Inference parameters: temperature, top_p, top_k, max_tokens, stop sequences
- Base vs instruct models
- Streaming vs non-streaming responses

### 1.2 Tokenization
- Subword tokenization: BPE, WordPiece, SentencePiece
- Byte-level tokenization
- Vocabulary size and its implications
- Tokenization tax: English vs code vs JSON vs non-English
- Tokenizer differences across providers (OpenAI, Anthropic, Google, Llama)
- Rule of thumb: 1 token ≈ 4 chars ≈ ¾ English word
- Hands-on: implement BPE from scratch

### 1.3 Cost & Latency Math
- Price in vs price out (per-token billing)
- The cost formula: `cost = in_tokens × price_in + out_tokens × price_out`
- Why output is 2–4× more expensive than input
- TTFT (time to first token) vs total latency
- Latency formula: `total = TTFT + (output_tokens × time_per_token)`
- Percentiles: p50 / p95 / p99 (and why averages lie)
- Cost modeling before building
- Latency budgeting and SLOs
- Hands-on: build a cost + latency calculator

### 1.4 Prompt Engineering
- Message structure: system / user / assistant
- Zero-shot vs few-shot
- Chain-of-Thought (CoT)
- Structured output and schema constraints
- Delimiters and untrusted input tagging
- Defensive prompt engineering (injection defense)
- Instruction hierarchy (system > user > tool)
- Context placement (beginning/end vs middle)
- Prompt caching (static-first ordering)
- Prompt versioning and rollback
- Meta-prompting and DSPy (high-level)
- Decision tree: prompt vs RAG vs fine-tune
- Hands-on: build a production-grade prompt with schema validation + retry

### 1.5 Embeddings
- What an embedding is: text → fixed-size vector
- Semantic similarity: cosine, dot product
- Same model for docs and queries (critical rule)
- Dimensionality trade-offs
- Domain-specific embeddings (code, legal, medical)
- Embedding cost and caching
- Hands-on: embed a corpus, build semantic search

### 1.6 Vector Databases
- What a vector DB stores: (vector, text, metadata)
- Index types: Flat, HNSW, IVF, PQ
- ANN (Approximate Nearest Neighbor) search
- HNSW: how it works, recall/latency trade-offs
- Metadata filtering (pre-filter vs post-filter)
- Multi-tenancy patterns
- DB options: Chroma, Pinecone, Weaviate, FAISS, Qdrant, LanceDB, Supabase, MongoDB Atlas, pgvector
- When to use which
- Hands-on: load a corpus into Chroma, then Qdrant, compare

### 1.7 RAG (Retrieval-Augmented Generation)
- The full pipeline: ingest → chunk → embed → store → retrieve → rerank → generate
- Why RAG vs fine-tune (knowledge vs behavior)
- Chunking strategies:
  - Fixed-size
  - Recursive
  - Semantic
  - Document-aware (markdown, code, tables)
  - Parent-child
- Chunk size trade-offs
- Overlap strategies
- Hybrid search: dense + sparse (BM25) + RRF
- Reranking: cross-encoders, two-stage retrieval
- Query transformation:
  - Query rewriting
  - Multi-query
  - HyDE
  - Query decomposition
  - Step-back prompting
- Metadata filtering for access control
- Contextual retrieval (Anthropic pattern)
- Agentic RAG
- Self-RAG / corrective RAG
- GraphRAG (high-level)
- Generation prompt: constrain to context, citations, fallback
- RAG evals: recall@k, precision@k, MRR, faithfulness, relevance
- Common pitfalls (80% of bugs are retrieval bugs)
- Hands-on: build RAG from scratch (no framework), then with LangChain, then LlamaIndex

### 1.8 Tool Use / Function Calling
- The tool-calling protocol: declare → model emits call → you execute → send result
- Tool schemas: name, description, parameters
- Arguments as JSON strings (not objects)
- tool_call_id linking
- Parallel tool calls
- Tool design principles:
  - Verb names
  - Specific descriptions
  - Narrow scope
  - Structured, compact returns
  - additionalProperties: False
- Structured output vs tool calling
- Validation before execution
- Error handling and retries
- Cost multiplier (each round trip = extra LLM call)
- Security: never trust arguments, least privilege, sandboxing
- Hands-on: build a 3-tool agent with schema validation

### 1.9 Structured Output / JSON Mode
- Schema-constrained generation
- Pydantic / JSON Schema validation
- Retry loops on parse failure
- Provider-native structured output (OpenAI, Anthropic, Gemini)
- When to use structured output vs tool calling
- Hands-on: build a classifier with strict schema + retry

---

## Phase 2 — Agent Engineering

### 2.1 Agent Architecture
- The agent loop: observe → think → act → observe → repeat
- The four components: Brain (LLM), Tools, Memory, Loop
- Termination conditions:
  - Max steps
  - Max wall-clock time
  - Max cost
  - Loop detection (same tool + args twice)
  - Progress detection (no new info in N steps)
  - Explicit finish signal
- Agent patterns:
  - ReAct (Reason + Act)
  - Plan-and-Execute
  - Reflection / Self-Critique
  - Multi-agent (orchestrator/workers, debate, pipeline)
  - Agentic RAG
- Agent vs workflow decision framework
- Error handling: retryable vs fatal vs ambiguous
- Feeding errors back to the model
- State checkpointing (persistence for recovery)
- Human-in-the-loop for destructive actions
- Cost and latency scaling with steps
- Security: injection, confused deputy, exfiltration
- Hands-on: build the minimal agent loop (no framework)

### 2.2 Context & Memory Management
- The distinction: Context (RAM) vs Memory (disk)
- The attention problem:
  - Attention dilution
  - Lost in the middle
  - Compliance decay (73% at turn 5 → 33% at turn 16)
- Layered memory architecture:
  - Working memory (current task)
  - Structured memory (facts, preferences)
  - Episodic memory (events, timestamps)
  - Archival memory (documents)
- The retrieve-reason-writeback loop
- Compression strategies:
  - Full replay
  - Summarization
  - Extraction
  - Pinning
  - Purge
- Constraint pinning (hard constraints to top of system prompt)
- Token budgeting
- Memory scoping by user_id
- TTL and deletion policies
- Framework primitives:
  - LangGraph checkpointer (thread) vs store (cross-thread)
  - Letta tiers
  - Mem0 API
- Hands-on: build a memory manager with retrieval + writeback

### 2.3 Harness Engineering
- Definition: model = brain, harness = everything else
- The three layers:
  - Context Engineering (feedforward)
  - Architectural Constraints (guardrails)
  - Feedback & Verification (sensors)
- The five principles:
  - Repository as Source of Truth
  - Constraints via Linters, Not Prompts
  - The Ratchet (failures → structural rules)
  - Incremental Autonomy
  - Harness Failures, Not Model Failures
- Real examples: OpenAI's million-line codebase, LangChain's 14-point jump
- Enterprise/org-level harness:
  - Context lake
  - Integrations
  - Access controls
  - Agent registry
  - Workflow orchestrator
  - Scorecards
  - Human-in-the-loop
- Hands-on: build a minimal harness around a coding agent

### 2.4 Sandboxing
- Why: isolated, disposable execution environment
- Isolation levels:
  - Container (Docker)
  - Micro-VM (Firecracker, gVisor, Kata)
  - OS-level (filesystem, network)
- Lifecycle: provision → configure → experiment → inspect → reset
- State management:
  - RunState (harness-side)
  - Session state (serializable)
  - Snapshot (workspace files)
- Kubernetes Agent Sandbox CRD
- Warm pools and cold-start mitigation
- Common pitfalls:
  - Legal requests denied → agent goes around
  - Cold start penalties
  - Confusing isolation with capability
- Hands-on: run code in a sandboxed container

### 2.5 Permission Systems
- Why RBAC is insufficient for agents
- Over-permissioned agents (Replit deleting production DB)
- Role explosion problem
- Machine-speed damage
- Action-based authorization (not role-based)
- Capability tokens / mandates:
  - Scoped
  - Time-bound
  - Signed
  - Attenuable (can narrow, never widen)
- Deterministic enforcement (gate before LLM)
- Context authority (classify by source)
- Dangerous path protection (bypass-immune ASK)
- Least privilege per user
- Human-in-the-loop for destructive actions
- Hands-on: implement a permission gate with capability tokens

### 2.6 Tool Design
- The description is a prompt
- Naming conventions (verb + noun)
- Parameter design:
  - Flat > nested
  - Scalars > objects
  - Avoid JSON-in-string
- additionalProperties: False
- Validation is the harness's job
- Compact, structured returns
- Truncation of large results
- Many narrow tools > one giant tool
- Versioning tool schemas
- Testing tool schemas
- Hands-on: design and test 5 tool schemas

### 2.7 Observability
- Why: agents are non-deterministic, need full traces
- The cardinality trap (high-cardinality IDs on metric labels)
- Trace spans and structured logging
- Tail-based sampling (keep errors, slow, expensive)
- Attaching evals to spans
- LLM-specific tools:
  - LangSmith
  - Langfuse
  - Arize Phoenix
  - W&B Weave
  - OpenTelemetry
- What to trace:
  - Input messages
  - LLM response (with tool calls)
  - Tool execution + result + latency
  - Token counts, cost, timestamps
  - Errors
- Hands-on: instrument an agent with traces

### 2.8 Guardrails
- Input vs output guardrails
- Tripwire pattern (halt on violation)
- Layered defense:
  - Prompt injection detectors
  - Content filters
  - Blocklists
  - PII detection
  - Hallucination detection
- OpenAI Moderation API
- End-user ID tracing
- Abuse detection
- Hands-on: add input + output guardrails to an agent

### 2.9 The Eval Loop
- The loop: observe → cluster failures → promote → validate → deploy → repeat
- Offline vs online evaluation
- Staged promotion (offline → human → shadow → A/B → gradual rollout)
- Three grader families:
  - Code-based (fast, free)
  - Model-based / LLM-as-judge (slow, per-call)
  - Human (slowest, highest cost)
- LLM-as-judge calibration:
  - Length, position, verbosity biases
  - Cohen's kappa > 0.7
  - Multi-judge consensus
- Golden dataset maintenance
- CI/CD integration (evals as gates)
- Hands-on: build an eval harness with golden dataset + LLM-as-judge

### 2.10 Evaluation of Agents
- Unit of evaluation = the trajectory (not just final answer)
- Why output-only scoring fails
- Four core dimensions:
  - Task Success Rate (TSR)
  - Trajectory (tool selection, args, grounding, efficiency)
  - Efficiency (steps, tool calls, tokens, wall-clock)
  - Robustness (degradation under perturbation)
- Hard-fail conditions:
  - must_call tool skipped
  - must_not_call tool touched
  - grounding below threshold
- Eval frameworks: RAGAS, TruLens, DeepEval, Phoenix
- Common mistakes:
  - Output-only scoring
  - Aggregate TSR hiding regressions
  - Mocked tools with no error coverage
  - Frozen test sets
  - Eval and trace in different tools
  - Judge drift without calibration
- Hands-on: build a trajectory evaluator

### 2.11 Orchestration Frameworks
- Landscape:
  - LangChain (broad framework)
  - LangGraph (graph-based state machine)
  - LlamaIndex (retrieval-first)
  - CrewAI (role-based multi-agent)
  - AutoGen (conversational multi-agent)
  - Haystack (component pipelines)
  - OpenAI Agents SDK
  - DSPy (compile/optimize)
- Decision questions:
  - What's your failure mode?
  - Do you need state persistence?
  - Who owns the loop?
  - What's your team's orientation?
- The 2026 production stack:
  - Orchestration: LangGraph + LangChain
  - Retrieval: LlamaIndex
  - Observability: LangSmith, Langfuse, Phoenix
  - Memory: Postgres + pgvector, Mem0, Zep
  - Tools: Composio, E2B
- When to use which
- Hands-on: rebuild an agent in LangGraph

---

## Phase 3 — Applied Systems Thinking

### 3.1 Data Pipelines for Agent Systems
- Ingestion pipelines (batch, streaming)
- Document loaders and connectors
- Chunking at scale
- Incremental ingestion (re-embed only what changed)
- Data versioning
- Schema drift detection
- Data quality for agents (27% of failures)
- Stale indexes and missing fields
- Hands-on: build an incremental ingestion pipeline

### 3.2 Enterprise Integration
- Connecting to internal systems (DBs, APIs, queues)
- Auth patterns (OAuth, service accounts, JIT)
- Rate limiting and backpressure
- Retries with exponential backoff
- Idempotency keys
- Webhook handling
- Multi-tenant data isolation
- Per-tenant configuration
- Per-tenant rate limits
- Hands-on: integrate an agent with an internal API

### 3.3 Production Deployment
- Serving options:
  - vLLM
  - TGI (Text Generation Inference)
  - SGLang
  - Ollama (local)
  - llama.cpp
- Batching strategies:
  - Static batching
  - Continuous batching
  - In-flight batching
- KV cache management (PagedAttention)
- Prefix caching
- Autoscaling
- Canary deployments
- Shadow deployments
- A/B testing
- Rollback plans
- Prompt versioning + rollback
- Cost guardrails:
  - Per-request caps
  - Per-user budgets
  - Kill switches
- Latency budgeting
- Incident response for AI
- Hands-on: deploy a model with vLLM and load test

### 3.4 Security & Safety
- Prompt injection:
  - Direct
  - Indirect (via tool output)
  - Multi-turn
- Defense:
  - Delimit untrusted input
  - Never put secrets in system prompts
  - Guard models
  - Validate output
  - Least privilege
- Jailbreaks and mitigation
- Data exfiltration (read-secrets + http-request = leak)
- Confused deputy problem
- Sandboxing code execution
- PII handling
- Compliance (GDPR, SOC2, HIPAA)
- Audit trails
- Retention policies
- Bias and fairness:
  - Sources of bias
  - Auditing models
  - Mitigation strategies
- Specific safety tooling:
  - OpenAI Moderation API
  - End-user ID tracing
  - Abuse detection
- Hands-on: red-team your own agent

### 3.5 Multi-Tenant Systems
- Data isolation patterns
- Per-tenant config
- Per-tenant rate limits
- Per-tenant cost tracking
- Shared vs dedicated infrastructure
- Tenant onboarding/offboarding
- Hands-on: add multi-tenancy to a RAG system

### 3.6 Cost Modeling & Budgeting
- Back-of-envelope estimation
- Cost per request, per user, per feature
- Cost attribution
- Cost dashboards
- Budget alerts
- Optimization levers:
  - Prompt caching
  - Response caching
  - Semantic caching
  - Model routing
  - Smaller models
  - Output caps
- Hands-on: build a cost dashboard

### 3.7 Latency Budgeting
- TTFT vs total latency
- p50/p95/p99 SLOs
- Latency budget allocation
- Optimization levers:
  - Streaming
  - Parallel tool calls
  - Model routing
  - Caching
  - Speculative decoding
- Hands-on: measure and optimize p95 latency

### 3.8 AI Product Thinking
- When NOT to use AI
- When a workflow beats an agent
- ROI framing
- Build vs buy
- Model selection trade-offs
- Feature scoping
- User experience for non-deterministic systems
- Hands-on: write a one-page product spec for an AI feature

---

## Phase 4 — The FDE Craft

### 4.1 Fact Extraction
- Separating facts from opinions from assumptions
- Identifying the actual problem vs the stated problem
- Practice on real case studies
- Hands-on: extract facts from 5 customer conversations

### 4.2 Gap-Spotting
- What's missing from the requirement?
- What hasn't been asked?
- Hidden dependencies
- Unstated constraints
- Hands-on: find gaps in 5 requirements docs

### 4.3 Asking Non-Redundant Questions
- The question that unlocks the most information
- Avoiding questions you can answer yourself
- Sequencing questions
- Hands-on: practice on 5 scenarios

### 4.4 Risk / Worst-Case Framing
- What happens if this fails?
- What's the worst case?
- Blast radius
- Recovery plans
- Hands-on: worst-case analysis on 5 systems

### 4.5 Picking One Narrow Slice
- Don't boil the ocean
- Ship one thing
- Then expand
- Hands-on: scope 5 vague problems into shippable slices

### 4.6 Naming the Explicit Cut
- "We're NOT doing X, Y, Z"
- "We ARE doing W"
- Why cuts matter
- Hands-on: write explicit cuts for 5 projects

### 4.7 The Pitch Sentence
- One sentence that explains the value
- Audience-aware framing
- Hands-on: write 10 pitch sentences

### 4.8 Rapid Prototyping Mindset
- 2-hour prototype
- Fake it before you build it
- Demo-driven development
- Hands-on: prototype 5 features in 2 hours each

### 4.9 Live Demoing
- Demo to non-technical audience
- Handle questions
- Recover from failures
- Hands-on: demo a prototype to a friend

### 4.10 Real FDE Case Studies
- Study successful FDE deployments
- Study failures
- Extract patterns
- Hands-on: write up 5 case studies

### 4.11 Capstone Simulation
- Full FDE engagement simulation
- Vague problem → scoped feature → shipped
- Hands-on: run a full simulation

### 4.12 Live Hypothesis Commitment
- State your hypothesis before building
- Commit to a metric
- Measure against it
- Hands-on: run 5 hypothesis-driven experiments

---

## Phase 5 — LLM Infrastructure & Model Internals

### 5.1 Self Attention
- The intuition: each token looks at every other token
- Q, K, V: Query, Key, Value
- The computation:
  - scores = Q · Kᵀ / √d_k
  - mask = -∞ for future positions
  - weights = softmax(scores)
  - output = weights · V
- Multi-head attention (covered in 5.2)
- Complexity: O(n²) compute and memory
- Positional encoding:
  - Sinusoidal
  - Learned
  - RoPE
  - ALiBi
- Attention variants:
  - MHA (standard)
  - MQA (multi-query)
  - GQA (grouped-query)
  - MLA (multi-head latent)
- Efficient implementations:
  - FlashAttention
  - PagedAttention
  - Sliding window
  - Sparse attention
  - Linear attention
- Why "lost in the middle" happens
- Hands-on: implement self-attention from scratch in PyTorch

### 5.2 Multi-Headed Attention
- Why multiple heads
- Different heads learn different relationships
- How it works:
  - Split dimension into h heads
  - Each head has its own W_q, W_k, W_v
  - Concat + project with W_o
- Same total compute, higher expressiveness
- Typical: 8–32 heads
- Hands-on: implement multi-head attention

### 5.3 Cross Attention
- Q from one sequence, K/V from another
- Self-attention vs cross-attention
- Used in:
  - Encoder-decoder models (T5, Whisper)
  - Multimodal models (Flamingo, Stable Diffusion)
  - Image captioning
  - Speech recognition
- Not used in decoder-only LLMs (GPT, Llama)
- Hands-on: build a toy encoder-decoder with cross-attention

### 5.4 Precisions (fp32 / fp16 / bf16 / int8)
- What precision means: bits per number
- The formats:
  - fp32: 4 bytes, ~7 digits
  - fp16: 2 bytes, ~3 digits, narrow range
  - bf16: 2 bytes, ~2 digits, same range as fp32
  - fp8: 1 byte (E4M3, E5M2)
  - int8: 1 byte, quantized
  - int4: 0.5 bytes, quantized
- Memory math: 7B model at bf16 = 14 GB
- Speed: bf16 is 16× faster than fp32 on H100
- Mixed precision training:
  - Forward: bf16
  - Master weights: fp32
  - Gradients: bf16 or fp8
  - Loss scaling (needed for fp16, optional for bf16)
- Why bf16 wins
- KV cache precision
- Hands-on: load a model in different precisions, benchmark

### 5.5 Quantization
- What quantization is
- Post-Training Quantization (PTQ):
  - GPTQ
  - AWQ
  - bitsandbytes (bnb)
  - GGUF (llama.cpp)
- Quantization-Aware Training (QAT)
- How int8 quantization works (scale factors, calibration)
- How int4 quantization works (group-wise scales)
- Quality spectrum: bf16 → int8 → int4 → int3 → int2
- KV cache quantization (KIVI, KVQuant)
- When to use which
- Hands-on: quantize a model with GPTQ and AWQ, benchmark

### 5.6 Model Distillation
- What distillation is: teacher → student
- Classical distillation:
  - Hard labels vs soft targets
  - Temperature scaling
  - Dark knowledge
- Modern LLM distillation:
  - Synthetic data distillation
  - Logit distillation
  - Feature distillation
  - Chain-of-Thought distillation
- Real examples: DeepSeek R1 Distill, Alpaca
- Distillation vs quantization
- Limitations: task breadth, domain transfer, shallow imitation
- Hands-on: distill a small model from a large one

### 5.7 KV Caching
- The problem: O(N²) generation without cache
- The insight: cache K and V, not Q
- How it works: append new K, V each step
- What gets cached:
  - Every token
  - Every layer
  - Every KV head
- Cache size math:
  - 2 × layers × batch × KV_heads × seq_len × head_dim × bytes
- Prefill vs decode (compute-bound vs memory-bandwidth-bound)
- KV cache variants:
  - MHA
  - MQA
  - GQA
  - MLA
- KV cache quantization
- PagedAttention (vLLM)
- Prefix caching
- Prompt caching
- Hands-on: implement KV cache, measure speedup

### 5.8 Deployment of LLMs at Scale
- Serving options:
  - vLLM
  - TGI
  - SGLang
  - Ollama
  - llama.cpp
  - TensorRT-LLM
- Batching strategies:
  - Static
  - Continuous
  - In-flight
- KV cache management
- Prefix caching
- Autoscaling
- Multi-GPU and multi-node
- Model parallelism (tensor, pipeline, expert)
- Latency vs throughput trade-offs
- Cost optimization
- Hands-on: serve a model with vLLM, load test, tune batching

### 5.9 vLLM
- What vLLM is
- PagedAttention:
  - Page-based KV cache
  - No fragmentation
  - 2–4× higher throughput
- Continuous batching
- Prefix caching
- Tensor parallelism
- Quantization support (GPTQ, AWQ, FP8)
- LoRA support
- OpenAI-compatible API
- Deployment patterns
- Hands-on: deploy vLLM with prefix caching + quantization

### 5.10 MCP (Model Context Protocol)
- What MCP is: standard for tool integration
- Why it exists: interoperability
- Architecture:
  - MCP servers (expose tools)
  - MCP clients (agents/LLMs)
  - Resources, prompts, tools
- Transports: stdio, HTTP, SSE
- Building an MCP server
- Connecting an agent to MCP servers
- Security considerations
- Hands-on: build an MCP server, connect it to an agent

### 5.11 Speculative Decoding
- What it is: small model drafts, large model verifies
- Why it works: small model is fast, large model is accurate
- Acceptance rate and speedup
- Variants:
  - Draft model
  - Medusa
  - Lookahead
  - Self-speculative
- When it helps, when it doesn't
- Hands-on: implement speculative decoding

### 5.12 Continuous Batching
- Static batching vs continuous batching
- How continuous batching works
- Why it improves throughput
- Interaction with KV cache
- vLLM and TGI support
- Hands-on: measure throughput with and without continuous batching

### 5.13 Model Routing
- Route easy tasks to cheap models
- Route hard tasks to expensive models
- Router design:
  - Classifier-based
  - LLM-based
  - Confidence-based
- Cost vs quality trade-offs
- Hands-on: build a model router

### 5.14 Fine-Tuning
- When to fine-tune (behavior, format, tone)
- When NOT to fine-tune (knowledge → use RAG)
- Full fine-tuning vs PEFT:
  - LoRA
  - QLoRA
  - Prefix tuning
  - Adapters
- Dataset engineering:
  - Curation
  - Cleaning
  - Synthetic data
  - Deduplication
  - Format consistency
- Training loops
- Evaluation of fine-tuned models
- Serving fine-tuned models
- Hands-on: fine-tune a model with LoRA

### 5.15 Local / Open-Source Inference Tooling
- Ollama (easy local inference)
- llama.cpp (CPU + GPU, GGUF)
- HuggingFace Transformers (Python)
- Transformers.js (JS)
- vLLM (production serving)
- When to use local vs API
- Cost comparison
- Hands-on: run Llama 3 locally with Ollama

### 5.16 Multimodal AI
- Vision + text:
  - GPT-4V, Claude with images
  - LLaVA, Qwen-VL
  - Image captioning
  - Visual QA
- Audio:
  - Whisper (STT)
  - TTS models
  - Voice agents
- Video:
  - Frame extraction
  - Video QA
- Multimodal RAG
- Hands-on: build a multimodal RAG system

### 5.17 Bias and Fairness
- Sources of bias:
  - Training data
  - Model architecture
  - Deployment context
- Types of bias:
  - Representation
  - Stereotyping
  - Performance disparity
- Auditing models
- Mitigation strategies
- Regulatory landscape
- Hands-on: audit a model for bias

### 5.18 Safety Tooling
- OpenAI Moderation API
- End-user ID tracing
- Abuse detection
- Rate limiting per user
- Content filtering
- PII detection
- Hands-on: add safety tooling to an agent

---

## Phase 6 — Deep Revision Pass (Chip Huyen, AI Engineering)

### 6.1 The AI Stack
- Application layer
- Model development layer
- Infrastructure layer

### 6.2 Pre-training vs Post-training
- Pre-training
- SFT (Supervised Fine-Tuning)
- RLHF (Reinforcement Learning from Human Feedback)
- DPO (Direct Preference Optimization)

### 6.3 Sampling Strategies
- Top-k sampling
- Top-p (nucleus) sampling
- Temperature
- Beam search
- When to use each

### 6.4 Evaluation Methodology
- Exact evaluation
- Language modeling metrics (perplexity, BLEU, ROUGE)
- AI-as-judge
- Comparative evaluation
- Criteria design
- Model selection for evaluation

### 6.5 Defensive Prompt Engineering
- Tagging untrusted content
- Delimiters
- Instruction hierarchy
- Injection defense

### 6.6 Retrieval Strategies
- Dense retrieval
- Sparse retrieval (BM25)
- Hybrid retrieval
- Re-ranking
- When to use which

### 6.7 Agent Planning Strategies
- ReAct
- Plan-and-Execute
- Reflexion
- Tree of Thoughts
- When to use which

### 6.8 Finetuning
- Form vs facts
- When to fine-tune
- Dataset requirements
- Evaluation

### 6.9 Dataset Engineering
- Curation
- Cleaning
- Synthetic data generation
- Deduplication
- Format consistency
- Train/val/test splits

### 6.10 Inference Optimization Tradeoffs
- Latency
- Throughput
- Cost
- Quality
- The four-way trade-off

### 6.11 Architecture & the Data Flywheel
- Feedback loops
- Continuous improvement
- Data collection
- Model updates

---

## Phase 7 — Capstone Projects

### 7.1 Order Support Agent
- Python
- LangGraph
- Tools: order lookup, refund, escalation
- Memory: customer context
- Evals: task success rate
- Deployment: production-ready

### 7.2 IncidentIQ
- Rust
- Multi-agent
- No framework
- Tools: log search, metric query, alert management
- Evals: trajectory evaluation
- Deployment: production-ready

### 7.3 Refactor
- Multi-agent legacy code migration
- Tools: read, edit, test, deploy
- Harness: constraints, sandboxing, permissions
- Evals: code correctness
- Deployment: CI/CD integration

### 7.4 Conduit
- MCP-native multi-agent ops automation
- Tools: MCP servers, internal APIs
- Orchestration: LangGraph or custom
- Observability: full tracing
- Evals: task success + trajectory
- Deployment: production-ready

---

## Additional Applied Concepts

### Multi-Tenant Systems
- Data isolation
- Per-tenant config
- Per-tenant rate limits
- Per-tenant cost tracking
- Shared vs dedicated infra

### Gap-Closing Pass (roadmap.sh AI Engineer)
- Embeddings (deep dive)
- Vector databases (deep dive)
- ANN / HNSW indexing

### Remaining Gaps
- Real end-to-end RAG implementation (hands-on)
- Local/open-source inference tooling (Ollama, HF Hub, Transformers.js)
- Multimodal AI implementation (image/video/audio, TTS/STT)
- Bias and fairness in AI systems
- Specific safety tooling (OpenAI Moderation API, end-user ID tracing)

---

## Phase 8 — Bulletproof Standards (Self-Assessment)

### Core 20 (Must Be Bulletproof)
1. LLM Fundamentals
2. Tokenization + Cost/Latency Math
3. Prompt Engineering
4. Tool Use / Function Calling
5. Agent Architecture
6. Context & Memory Management
7. RAG
8. Embeddings + Vector DBs
9. Evals
10. Observability
11. Guardrails + Permission Systems
12. Sandboxing
13. Harness Engineering
14. KV Caching + Inference Optimization
15. Quantization + Precision
16. Fine-tuning vs RAG vs Prompting
17. Deployment (vLLM, batching, serving)
18. Security (injection, exfiltration, least privilege)
19. Cost Modeling + Latency Budgeting
20. FDE Craft

### The Rest (Proficient)
- Multi-agent patterns
- GraphRAG
- Model distillation
- Speculative decoding
- Continuous batching
- MCP
- Multimodal
- Bias/fairness
- Compliance

### The Bulletproof Test
You're bulletproof when you can:
1. Whiteboard any AI system architecture in 10 minutes
2. Estimate cost and latency before building
3. Build a working prototype in a day
4. Break your own system and find failures
5. Fix failures with proper engineering
6. Measure quality with evals
7. Debug production incidents by reading traces
8. Explain any topic to a non-technical stakeholder
9. Defend trade-offs in an interview
10. Ship to production with confidence

---

## Phase 9 — Execution Plan (16 Weeks)

### Weeks 1–2: Foundations
- LLM Fundamentals
- Tokenization
- Cost/Latency Math
- Prompt Engineering
- Tool Calling
- Agent Loop
- Review + blog post

### Weeks 3–4: RAG Deep Dive
- Chunking
- Embeddings
- Vector DB
- Hybrid Search
- Reranking
- RAG Evals
- Review + break your RAG system

### Weeks 5–6: Agent Engineering
- Agent loop with tools + memory
- Context management
- Memory
- Observability
- Guardrails
- Evals
- Review + rebuild in LangGraph

### Weeks 7–8: Systems Thinking
- Multi-tenancy
- Cost tracking
- Rate limiting
- Shadow deployment
- A/B testing
- Incident response
- Review + document architecture

### Weeks 9–10: FDE Craft
- Fact extraction
- Gap-spotting
- Question asking
- Risk framing
- Scoping
- Pitching
- Demo

### Weeks 11–12: Infrastructure & Internals
- Self-attention
- Multi-head attention
- Cross-attention
- Precisions
- Quantization
- KV caching
- vLLM

### Weeks 13–14: Advanced Topics
- Distillation
- Speculative decoding
- Continuous batching
- MCP
- Multimodal
- Bias/fairness
- Safety tooling

### Weeks 15–16: Capstone
- Build one capstone end-to-end
- Full eval suite
- Full observability
- Cost tracking
- Security review
- Deployment
- Documentation
- Demo

---

## Resources

### Books
- AI Engineering — Chip Huyen
- Designing Machine Learning Systems — Chip Huyen
- Building LLM Apps — Valentino Gagliardi

### Blogs
- Anthropic Engineering Blog
- OpenAI Cookbook
- LangChain Blog
- vLLM Blog
- HuggingFace Blog

### Docs
- LangGraph Docs
- LlamaIndex Docs
- vLLM Docs