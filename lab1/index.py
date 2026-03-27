import os
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models import BedrockModel
from boto3.session import Session

# 1. NẠP BIẾN MÔI TRƯỜNG & KHỞI TẠO KẾT NỐI
load_dotenv()
boto_session = Session()
region = boto_session.region_name

print("✅ Đã kết nối AWS thành công tại Region:", region)
print("-" * 50)

# ==========================================
# BƯỚC 1: XÂY DỰNG CÔNG CỤ (TOOLS) - PHÉP TOÁN
# ==========================================
@tool
def add(a: float, b: float) -> float:
    """
    Cộng hai số.
    Args:
        a: số thứ nhất
        b: số thứ hai
    Returns:
        Kết quả của a + b
    """
    return a + b

@tool
def subtract(a: float, b: float) -> float:
    """
    Trừ hai số.
    Args:
        a: số bị trừ
        b: số trừ
    Returns:
        Kết quả của a - b
    """
    return a - b

@tool
def multiply(a: float, b: float) -> float:
    """
    Nhân hai số.
    Args:
        a: số thứ nhất
        b: số thứ hai
    Returns:
        Kết quả của a * b
    """
    return a * b

@tool
def divide(a: float, b: float) -> float:
    """
    Chia hai số.
    Args:
        a: số bị chia
        b: số chia
    Returns:
        Kết quả của a / b
    """
    if b == 0:
        return "Lỗi: không thể chia cho 0"
    return a / b

# ==========================================
# BƯỚC 2: CẤU HÌNH BỘ NÃO (FOUNDATION MODEL)
# ==========================================
model = BedrockModel(
    model_id="us.amazon.nova-2-lite-v1:0", 
    temperature=0.3, 
    region_name=region
)

# ==========================================
# BƯỚC 3: LẮP RÁP AGENT VỚI SYSTEM PROMPT
# ==========================================
system_prompt = """You are a helpful assistant that can perform basic arithmetic using the tools provided.
When the user asks for a calculation, use the appropriate tool (add, subtract, multiply, divide) to get the result.
Always answer in Vietnamese. Explain briefly what you did."""

agent = Agent(
    model=model,        
    tools=[add, subtract, multiply, divide],
    system_prompt=system_prompt,    
)

# ==========================================
# BƯỚC 4: CHẠY THỬ NGHIỆM (TESTING)
# ==========================================
test_queries = [
    "Tính 15 cộng 27 giúp tôi",
    "Lấy 100 trừ 45",
    "Nhân 8 với 9",
    "Chia 144 cho 12",
    "Tính 25 chia 0"  # test lỗi chia cho 0
]

for query in test_queries:
    print(f"👤 Khách hàng: {query}")
    response = agent(query) 
    # print(f"🤖 Agent: {response}")
    print("=" * 50 + "\n")