import time
import uuid
import os
from dotenv import load_dotenv
from boto3.session import Session
from strands.agent import Agent
from strands.models.bedrock import BedrockModel
from strands.tools import tool

from bedrock_agentcore_starter_toolkit.operations.memory.manager import MemoryManager
from bedrock_agentcore.memory import MemoryClient
from bedrock_agentcore.memory.constants import StrategyType
from bedrock_agentcore.memory.integrations.strands.config import (
    AgentCoreMemoryConfig,
    RetrievalConfig,
)
from bedrock_agentcore.memory.integrations.strands.session_manager import (
    AgentCoreMemorySessionManager,
)

MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "amazon.nova-lite-v1:0")
ACTOR_ID = "dong01"
MEMORY_NAME = "CustomerSupportMemory"


@tool
def get_product_info(product_type: str) -> str:
    """Get product details and technical highlights for supported categories."""
    products = {
        "laptops": {
            "warranty": "1-year manufacturer warranty + optional extension",
            "specs": "Intel/AMD CPU, 8-32GB RAM, SSD storage",
            "features": "Backlit keyboard, USB-C/Thunderbolt, Wi-Fi 6",
            "compatibility": "Windows/macOS and good Linux support on selected models",
        },
        "headphones": {
            "warranty": "1-year manufacturer warranty",
            "specs": "Wired/wireless options, ANC, 20Hz-20kHz frequency range",
            "features": "Low-latency mode on gaming models, touch controls",
            "compatibility": "Bluetooth 5.0+, 3.5mm jack, USB-C charging",
        },
        "smartphones": {
            "warranty": "1-year manufacturer warranty",
            "specs": "5G support, 128GB-1TB storage, multi-camera systems",
            "features": "Wireless charging, water resistance, biometric unlock",
            "compatibility": "Android/iOS ecosystem accessories",
        },
    }

    product = products.get(product_type.lower())
    if not product:
        return (
            f"No product details found for '{product_type}'. "
            "Please provide a category like laptops, headphones, or smartphones."
        )

    return (
        f"Product overview for {product_type.title()}:\n"
        f"- Warranty: {product['warranty']}\n"
        f"- Specs: {product['specs']}\n"
        f"- Features: {product['features']}\n"
        f"- Compatibility: {product['compatibility']}"
    )


@tool
def get_return_policy(product_category: str) -> str:
    """Get return policy details for customer support scenarios."""
    policies = {
        "headphones": "30 days, original packaging preferred, refund in 3-5 business days",
        "laptops": "30 days, include all accessories, refund in 7-10 business days",
        "smartphones": "30 days, factory reset required, refund in 5-7 business days",
    }
    default = "30 days, product must be in good condition, refund in 5-7 business days"
    return f"Return policy for {product_category}: {policies.get(product_category.lower(), default)}"


@tool
def get_technical_support(issue: str) -> str:
    """Provide simple technical troubleshooting guidance."""
    issue_lower = issue.lower()
    if "overheat" in issue_lower or "nóng" in issue_lower:
        return (
            "For overheating issues: close heavy background apps, check ventilation, "
            "update OS/drivers, and run hardware diagnostics."
        )
    return (
        "Please share device model, OS version, and exact error symptoms so we can guide "
        "you with precise troubleshooting steps."
    )


SYSTEM_PROMPT = """You are a helpful and professional customer support assistant.
Use available tools for product, return policy, and technical support questions.
When memory context is available, personalize responses based on customer history.
Keep answers concise and practical."""


def create_or_get_memory(region: str, memory_name: str) -> str:
    memory_manager = MemoryManager(region_name=region)
    memory = memory_manager.get_or_create_memory(
        name=memory_name,
        strategies=[
            {
                StrategyType.USER_PREFERENCE.value: {
                    "name": "CustomerPreferences",
                    "description": "Captures customer preferences and behavior",
                    "namespaces": ["support/customer/{actorId}/preferences/"],
                }
            },
            {
                StrategyType.SEMANTIC.value: {
                    "name": "CustomerSupportSemantic",
                    "description": "Stores facts from conversations",
                    "namespaces": ["support/customer/{actorId}/semantic/"],
                }
            },
        ],
    )
    return memory["id"]


def seed_customer_history(memory_client: MemoryClient, memory_id: str, actor_id: str) -> None:
    previous_interactions = [
        ("I'm having issues with my MacBook Pro overheating during video editing.", "USER"),
        (
            "I can help with that thermal issue. For video editing workloads, let's check your "
            "Activity Monitor and adjust performance settings. Your MacBook Pro order #MB-78432 "
            "is still under warranty.",
            "ASSISTANT",
        ),
        (
            "What's the return policy on gaming headphones? I need low latency for competitive "
            "FPS games",
            "USER",
        ),
        (
            "For gaming headphones, you have 30 days to return. Since you're into competitive "
            "FPS, I'd recommend checking the audio latency specs - most gaming models have "
            "<40ms latency.",
            "ASSISTANT",
        ),
        (
            "I need a laptop under $1200 for programming. Prefer 16GB RAM minimum and good "
            "Linux compatibility. I like ThinkPad models.",
            "USER",
        ),
        (
            "Perfect! For development work, I'd suggest looking at our ThinkPad E series or "
            "Dell XPS models. Both have excellent Linux support and 16GB RAM options within "
            "your budget.",
            "ASSISTANT",
        ),
    ]

    memory_client.create_event(
        memory_id=memory_id,
        actor_id=actor_id,
        session_id="previous_session",
        messages=previous_interactions,
    )


def wait_and_fetch_memories(
    memory_client: MemoryClient,
    memory_id: str,
    actor_id: str,
    namespace: str,
    query: str,
    max_retries: int = 6,
) -> list:
    retries = 0
    while retries < max_retries:
        memories = memory_client.retrieve_memories(
            memory_id=memory_id,
            namespace=namespace.format(actorId=actor_id),
            query=query,
        )
        if memories:
            return memories

        retries += 1
        if retries < max_retries:
            print(f"⏳ Processing... wait 10s ({retries}/{max_retries})")
            time.sleep(10)
    return []


def print_memories(title: str, memories: list) -> None:
    print(title)
    print("=" * 80)
    if not memories:
        print("(No memories returned yet)")
        return

    for index, item in enumerate(memories, 1):
        if isinstance(item, dict):
            content = item.get("content", {})
            text = content.get("text", "") if isinstance(content, dict) else ""
            print(f"{index}. {text}")


def build_memory_agent(region: str, memory_id: str, actor_id: str) -> Agent:
    session_id = str(uuid.uuid4())
    memory_config = AgentCoreMemoryConfig(
        memory_id=memory_id,
        session_id=session_id,
        actor_id=actor_id,
        retrieval_config={
            "support/customer/{actorId}/semantic/": RetrievalConfig(
                top_k=3,
                relevance_score=0.2,
            ),
            "support/customer/{actorId}/preferences/": RetrievalConfig(
                top_k=3,
                relevance_score=0.2,
            ),
        },
    )

    model = BedrockModel(model_id=MODEL_ID, region_name=region)
    return Agent(
        model=model,
        session_manager=AgentCoreMemorySessionManager(memory_config, region),
        tools=[get_product_info, get_return_policy, get_technical_support],
        system_prompt=SYSTEM_PROMPT,
    )

# 1. NẠP BIẾN MÔI TRƯỜNG & KHỞI TẠO KẾT NỐI
load_dotenv()
boto_session = Session()
region = boto_session.region_name

print(f"✅ Đã kết nối AWS tại Region: {region}")
print("-" * 50)

if not region:
    raise RuntimeError(
        "AWS region is not configured. Set AWS_REGION/AWS_DEFAULT_REGION or configure AWS CLI."
    )

memory_id = create_or_get_memory(region=region, memory_name=MEMORY_NAME)
print("✅ Thành công! Kho lưu trữ đã sẵn sàng.")
print(f"🔑 Memory ID của bạn là: {memory_id}")
print("=" * 50)

memory_client = MemoryClient(region_name=region)

try:
    seed_customer_history(memory_client, memory_id, ACTOR_ID)
    print("✅ Seeded customer history successfully")
    print("📝 Interactions saved to Short-Term Memory")
except Exception as error:
    print(f"⚠️ Error seeding history: {error}")

print("🔍 Checking for processed Long-Term Memories...")
preference_memories = wait_and_fetch_memories(
    memory_client=memory_client,
    memory_id=memory_id,
    actor_id=ACTOR_ID,
    namespace="support/customer/{actorId}/preferences/",
    query="can you summarize the support issue",
)
print_memories(
    "🎯 Extracted customer preferences from seeded conversations:",
    preference_memories,
)

semantic_memories = wait_and_fetch_memories(
    memory_client=memory_client,
    memory_id=memory_id,
    actor_id=ACTOR_ID,
    namespace="support/customer/{actorId}/semantic/",
    query="information on the technical support issue",
)
print_memories(
    "🧠 Extracted factual semantic memories:",
    semantic_memories,
)

print("\n🚀 Building memory-enabled customer support agent...")
agent = build_memory_agent(region=region, memory_id=memory_id, actor_id=ACTOR_ID)

print("\n🎧 Test 1: Headphone recommendation with memory")
agent("Which headphones would you recommend?")

print("\n💻 Test 2: Recall laptop preferences")
agent("What is my preferred laptop brand and requirements?")