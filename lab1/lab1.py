from ddgs.exceptions import DDGSException, RatelimitException
from ddgs import DDGS
# from strands_tools import retrieve
import os
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models import BedrockModel
import boto3

# 1. NẠP BIẾN MÔI TRƯỜNG & KHỞI TẠO KẾT NỐI
load_dotenv()
boto_session = boto3.Session()
region = boto_session.region_name

print("✅ Đã kết nối AWS thành công tại Region:", region)
print("-" * 50)

model = BedrockModel(
    model_id="us.amazon.nova-2-lite-v1:0", 
    temperature=0.3, 
    region_name=region
)
# System prompt định nghĩa vai trò và khả năng của agent
SYSTEM_PROMPT = """Bạn là trợ lý hỗ trợ khách hàng thân thiện và chuyên nghiệp cho công ty thương mại điện tử về thiết bị điện tử.
Nhiệm vụ của bạn:
- Cung cấp thông tin chính xác sử dụng các công cụ có sẵn.
- Hỗ trợ khách hàng với thông tin kỹ thuật và thông số sản phẩm.
- Luôn thân thiện, kiên nhẫn và thấu hiểu với khách hàng.
- Sau khi trả lời câu hỏi, luôn đề nghị hỗ trợ thêm.
- Nếu không thể giúp đỡ điều gì, hãy hướng khách hàng đến bộ phận liên hệ phù hợp.

Bạn có thể sử dụng các công cụ sau:
1. get_return_policy() – Để giải đáp thắc mắc về chính sách bảo hành và đổi trả.
2. get_product_info() – Để lấy thông tin chi tiết về một sản phẩm cụ thể.
3. web_search() – Để truy cập tài liệu kỹ thuật hiện tại hoặc cập nhật thông tin.
Luôn sử dụng công cụ phù hợp để có thông tin chính xác, cập nhật thay vì tự suy luận về sản phẩm điện tử hay thông số."""


@tool
def web_search(keywords: str, region: str = "us-en", max_results: int = 5) -> str:
    """Tìm kiếm trên web để lấy thông tin cập nhật.

    Args:
        keywords (str): Từ khóa tìm kiếm.
        region (str): Khu vực tìm kiếm: wt-wt, us-en, uk-en, ru-ru, v.v.
        max_results (int | None): Số lượng kết quả tối đa trả về.

    Returns:
        Danh sách các dictionary chứa kết quả tìm kiếm.
    """
    try:
        results = DDGS().text(keywords, region=region, max_results=max_results)
        return results if results else "Không tìm thấy kết quả nào."
    except RatelimitException:
        return "Đã đạt giới hạn tốc độ. Vui lòng thử lại sau."
    except DDGSException as e:
        return f"Lỗi tìm kiếm: {e}"
    except Exception as e:
        return f"Lỗi tìm kiếm: {str(e)}"

@tool
def get_return_policy(product_category: str) -> str:
    """
    Lấy thông tin chính sách đổi trả cho một danh mục sản phẩm.

    Args:
        product_category: Danh mục điện tử (ví dụ: 'điện thoại thông minh', 'máy tính xách tay', 'phụ kiện')

    Returns:
        Chi tiết chính sách đổi trả đã được định dạng bao gồm thời gian và điều kiện.
    """
    # Cơ sở dữ liệu chính sách đổi trả giả lập – trong triển khai thực tế sẽ truy vấn cơ sở dữ liệu chính sách
    return_policies = {
        "smartphones": {
            "window": "30 ngày",
            "condition": "Bao bì nguyên bản, không hư hỏng vật lý, cần khôi phục cài đặt gốc",
            "process": "Cổng RMA trực tuyến hoặc hỗ trợ kỹ thuật",
            "refund_time": "5-7 ngày làm việc sau khi kiểm tra",
            "shipping": "Miễn phí vận chuyển trả hàng, được cung cấp nhãn trả hàng trả phí",
            "warranty": "Bảo hành nhà sản xuất 1 năm đi kèm",
        },
        "laptops": {
            "window": "30 ngày",
            "condition": "Bao bì nguyên bản, đầy đủ phụ kiện, không chỉnh sửa phần mềm",
            "process": "Yêu cầu xác minh hỗ trợ kỹ thuật trước khi đổi trả",
            "refund_time": "7-10 ngày làm việc sau khi kiểm tra",
            "shipping": "Miễn phí vận chuyển trả hàng với bao bì nguyên bản",
            "warranty": "Bảo hành nhà sản xuất 1 năm, có các tùy chọn gia hạn",
        },
        "accessories": {
            "window": "30 ngày",
            "condition": "Ưu tiên bao bì chưa mở, đầy đủ linh kiện",
            "process": "Cổng đổi trả trực tuyến",
            "refund_time": "3-5 ngày làm việc sau khi nhận hàng",
            "shipping": "Khách hàng thanh toán phí vận chuyển trả hàng dưới 50$",
            "warranty": "Bảo hành nhà sản xuất 90 ngày",
        },
    }

    # Chính sách mặc định cho các danh mục không có trong danh sách
    default_policy = {
        "window": "30 ngày",
        "condition": "Tình trạng nguyên bản với tất cả linh kiện đi kèm",
        "process": "Liên hệ hỗ trợ kỹ thuật",
        "refund_time": "5-7 ngày làm việc sau khi kiểm tra",
        "shipping": "Chính sách vận chuyển trả hàng thay đổi tùy theo sản phẩm",
        "warranty": "Áp dụng bảo hành nhà sản xuất tiêu chuẩn",
    }

    policy = return_policies.get(product_category.lower(), default_policy)
    return (
        f"Chính sách đổi trả - {product_category.title()}:\n\n"
        f"• Thời gian đổi trả: {policy['window']} kể từ khi nhận hàng\n"
        f"• Điều kiện: {policy['condition']}\n"
        f"• Quy trình: {policy['process']}\n"
        f"• Thời gian hoàn tiền: {policy['refund_time']}\n"
        f"• Vận chuyển: {policy['shipping']}\n"
        f"• Bảo hành: {policy['warranty']}"
    )


@tool
def get_product_info(product_type: str) -> str:
    """
    Lấy thông tin chi tiết và thông số kỹ thuật cho sản phẩm điện tử.

    Args:
        product_type: Loại sản phẩm điện tử (ví dụ: 'máy tính xách tay', 'điện thoại thông minh', 'tai nghe', 'màn hình')

    Returns:
        Thông tin sản phẩm đã định dạng bao gồm bảo hành, tính năng và chính sách.
    """
    # Danh mục sản phẩm giả lập – trong triển khai thực tế sẽ truy vấn cơ sở dữ liệu sản phẩm
    products = {
        "laptops": {
            "warranty": "Bảo hành nhà sản xuất 1 năm + tùy chọn bảo hành mở rộng",
            "specs": "Bộ vi xử lý Intel/AMD, RAM 8-32GB, ổ SSD, kích thước màn hình đa dạng",
            "features": "Bàn phím có đèn nền, cổng USB-C/Thunderbolt, Wi-Fi 6, Bluetooth 5.0",
            "compatibility": "Windows 11, macOS, hỗ trợ Linux tùy từng model",
            "support": "Bao gồm hỗ trợ kỹ thuật và cập nhật trình điều khiển",
        },
        "smartphones": {
            "warranty": "Bảo hành nhà sản xuất 1 năm",
            "specs": "Kết nối 5G/4G, dung lượng lưu trữ 128GB-1TB, hệ thống nhiều camera",
            "features": "Sạc không dây, kháng nước, bảo mật vân tay/khuôn mặt",
            "compatibility": "iOS/Android, có tùy chọn mở khóa mạng",
            "support": "Bao gồm cập nhật phần mềm và hỗ trợ kỹ thuật",
        },
        "headphones": {
            "warranty": "Bảo hành nhà sản xuất 1 năm",
            "specs": "Có dây/không dây, chống ồn, dải tần 20Hz-20kHz",
            "features": "Chống ồn chủ động, điều khiển cảm ứng, trợ lý giọng nói",
            "compatibility": "Bluetooth 5.0+, jack 3.5mm, sạc USB-C",
            "support": "Cập nhật firmware qua ứng dụng đồng hành",
        },
        "monitors": {
            "warranty": "Bảo hành nhà sản xuất 3 năm",
            "specs": "Độ phân giải 4K/1440p/1080p, tấm nền IPS/OLED, kích thước đa dạng",
            "features": "Hỗ trợ HDR, tần số quét cao, chân đế điều chỉnh",
            "compatibility": "Cổng HDMI, DisplayPort, USB-C",
            "support": "Hiệu chỉnh màu và hỗ trợ kỹ thuật",
        },
    }
    product = products.get(product_type.lower())
    if not product:
        return f"Thông số kỹ thuật cho {product_type} hiện không có sẵn. Vui lòng liên hệ đội hỗ trợ kỹ thuật để biết thông tin chi tiết về sản phẩm và yêu cầu tương thích."

    return (
        f"Thông tin kỹ thuật - {product_type.title()}:\n\n"
        f"• Bảo hành: {product['warranty']}\n"
        f"• Thông số: {product['specs']}\n"
        f"• Tính năng nổi bật: {product['features']}\n"
        f"• Tương thích: {product['compatibility']}\n"
        f"• Hỗ trợ: {product['support']}"
    )



agent = Agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[web_search, get_return_policy, get_product_info]
)
if __name__ == "__main__":
    response = agent("túi sách") 
