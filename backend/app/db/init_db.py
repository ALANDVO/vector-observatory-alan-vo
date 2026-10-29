"""Database initialization and seed data."""

from sqlalchemy.orm import Session

from app.db.session import Base, engine, SessionLocal
from app.models.plugin import Plugin, Skill


def init_db() -> None:
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


def seed_data() -> None:
    """Seed initial plugin and skill data."""
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Plugin).first():
            return

        plugins_data = [
            {
                "name": "Claude Code",
                "slug": "claude-code",
                "description": "Anthropic's official CLI for Claude - code with AI in your terminal",
                "version": "1.0.0",
                "author": "Anthropic",
                "repository_url": "https://github.com/anthropics/claude-code",
                "homepage_url": "https://claude.ai/code",
                "license": "MIT",
                "tags": "cli,ai,coding,anthropic",
                "skills": [
                    {
                        "name": "Code Generation",
                        "slug": "code-generation",
                        "description": "Generate code from natural language descriptions",
                        "input_schema": '{"type": "object", "properties": {"prompt": {"type": "string"}, "language": {"type": "string"}}, "required": ["prompt"]}',
                        "output_schema": '{"type": "object", "properties": {"code": {"type": "string"}, "explanation": {"type": "string"}}}',
                    },
                    {
                        "name": "Code Review",
                        "slug": "code-review",
                        "description": "Review code for bugs, style, and best practices",
                        "input_schema": '{"type": "object", "properties": {"code": {"type": "string"}, "context": {"type": "string"}}, "required": ["code"]}',
                        "output_schema": '{"type": "object", "properties": {"issues": {"type": "array", "items": {"type": "object"}}, "suggestions": {"type": "array", "items": {"type": "string"}}}}',
                    },
                    {
                        "name": "Refactoring",
                        "slug": "refactoring",
                        "description": "Refactor code for readability, performance, or structure",
                        "input_schema": '{"type": "object", "properties": {"code": {"type": "string"}, "goal": {"type": "string"}}, "required": ["code"]}',
                        "output_schema": '{"type": "object", "properties": {"refactored_code": {"type": "string"}, "changes": {"type": "array", "items": {"type": "string"}}}}',
                    },
                ],
            },
            {
                "name": "LangChain",
                "slug": "langchain",
                "description": "Framework for developing applications powered by language models",
                "version": "0.3.0",
                "author": "LangChain Team",
                "repository_url": "https://github.com/langchain-ai/langchain",
                "homepage_url": "https://python.langchain.com",
                "license": "MIT",
                "tags": "framework,llm,agents,chains",
                "skills": [
                    {
                        "name": "Chain Construction",
                        "slug": "chain-construction",
                        "description": "Build composable chains of LLM calls",
                        "input_schema": '{"type": "object", "properties": {"steps": {"type": "array", "items": {"type": "object"}}, "input": {"type": "object"}}, "required": ["steps"]}',
                        "output_schema": '{"type": "object", "properties": {"output": {"type": "object"}, "intermediate_steps": {"type": "array"}}}',
                    },
                    {
                        "name": "Agent Execution",
                        "slug": "agent-execution",
                        "description": "Run autonomous agents with tools",
                        "input_schema": '{"type": "object", "properties": {"tools": {"type": "array", "items": {"type": "object"}}, "prompt": {"type": "string"}}, "required": ["prompt"]}',
                        "output_schema": '{"type": "object", "properties": {"result": {"type": "string"}, "tool_calls": {"type": "array"}}}',
                    },
                ],
            },
            {
                "name": "LlamaIndex",
                "slug": "llamaindex",
                "description": "Data framework for LLM applications - connect data to LLMs",
                "version": "0.11.0",
                "author": "LlamaIndex Team",
                "repository_url": "https://github.com/run-llama/llama_index",
                "homepage_url": "https://www.llamaindex.ai",
                "license": "MIT",
                "tags": "rag,data,embeddings,vector-store",
                "skills": [
                    {
                        "name": "Document Ingestion",
                        "slug": "document-ingestion",
                        "description": "Ingest and index documents for retrieval",
                        "input_schema": '{"type": "object", "properties": {"documents": {"type": "array", "items": {"type": "string"}}, "chunk_size": {"type": "integer"}}, "required": ["documents"]}',
                        "output_schema": '{"type": "object", "properties": {"nodes_created": {"type": "integer"}, "index_size": {"type": "string"}}}',
                    },
                    {
                        "name": "Query Engine",
                        "slug": "query-engine",
                        "description": "Query indexed data with natural language",
                        "input_schema": '{"type": "object", "properties": {"query": {"type": "string"}, "top_k": {"type": "integer"}}, "required": ["query"]}',
                        "output_schema": '{"type": "object", "properties": {"response": {"type": "string"}, "sources": {"type": "array", "items": {"type": "object"}}}}',
                    },
                ],
            },
            {
                "name": "AutoGPT",
                "slug": "autogpt",
                "description": "Autonomous AI agent that can plan and execute complex tasks",
                "version": "0.5.0",
                "author": "AutoGPT Team",
                "repository_url": "https://github.com/Significant-Gravitas/AutoGPT",
                "homepage_url": "https://agpt.co",
                "license": "MIT",
                "tags": "agent,autonomous,planning,task-execution",
                "skills": [
                    {
                        "name": "Task Planning",
                        "slug": "task-planning",
                        "description": "Decompose high-level goals into executable steps",
                        "input_schema": '{"type": "object", "properties": {"goal": {"type": "string"}, "constraints": {"type": "array", "items": {"type": "string"}}}, "required": ["goal"]}',
                        "output_schema": '{"type": "object", "properties": {"plan": {"type": "array", "items": {"type": "object"}}, "estimated_steps": {"type": "integer"}}}',
                    },
                ],
            },
        ]

        for plugin_data in plugins_data:
            skills_data = plugin_data.pop("skills")
            plugin = Plugin(**plugin_data)
            db.add(plugin)
            db.flush()

            for skill_data in skills_data:
                skill = Skill(plugin_id=plugin.id, **skill_data)
                db.add(skill)

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    seed_data()
    print("Database initialized and seeded successfully!")

