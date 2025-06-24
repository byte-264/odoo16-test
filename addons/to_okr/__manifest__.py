{
    'name': "Objectives & Key Results - OKR",
    'name_vi_VN': "Mục tiêu & Kết quả then chốt - OKR",
    'summary': """Help you implement and execute OKR (Objectives & Key Results) in your organizations""",
    'summary_vi_VN': """Giúp bạn triển khai hiệu quả hệ thống quản trị doanh nghiệp với Mục tiêu & Kết quả then chốt - OKR""",
    'description': """
**Demo video**: `Objectives & Key Results - OKR <https://youtu.be/spJkKU6U2tg>`_

What it does
============
OKR (Objectives & Key Results) is a goal-setting framework designed to define and link the objectives of enterprises, departments, and employees to specific, measurable outcomes.

* OKRs help enterprises focus on the most critical goals and allocate resources effectively to achieve them;
* It helps individuals to understand their contribution to the organization's objectives and measure the progress of activities;
* This application helps you focus on your objectives and measure success through key results;

Key Features
============
1. **OKR Definitions**: Create, edit, and track OKRs at individual, department, and organizational levels. Align personal objectives with organizational goals for strategic coherence;
2. **Automated Progress Measurement**: Track objective achievements automatically through key result metrics;
3. **OKR Visualization**: View objectives & key result hierarchies through an intuitive OKR chart;
4. **Extensibility**: Seamlessly integrates with other applications such as Projects, Timesheet, and Gamification.

Benefits
========
1. **Clear Objective Alignment**: Link personal, departmental, and organizational objectives to foster unified efforts toward common goals;
2. **Empowered Contribution**: Boost employee motivation and productivity by clarifying individual roles and contributions;
3. **Strategic Vision**: Build and track long-term strategies for sustainable growth;
4. **Efficient Progress Tracking**: Automatically update and measure progress, improving management efficiency;
5. **Actionable Insights**: Transparent OKR diagrams provide clarity for faster and more accurate decision-making.

Who should use this module
==========================
The OKR software is designed for organizations of all sizes and industries:

* Executives seeking to define and align strategic goals;
* Managers aiming to monitor and guide their teams effectively;
* Employees who want to contribute to and track progress toward shared objectives.

Supported Editions
==================
1. Community Edition
2. Enterprise Edition

    """,

    'description_vi_VN': """
**Video demo**: `Mục tiêu & Kết quả then chốt - OKR <https://youtu.be/kl-CAPhplD4>`_

Mô-đun này làm gì
=================
OKR (Mục tiêu & Kết quả then chốt) là một khung thiết lập mục tiêu được thiết kế để xác định và liên kết các mục tiêu của doanh nghiệp, phòng ban và nhân viên với các kết quả cụ thể, có thể đo lường được.

* OKR giúp doanh nghiệp tập trung vào các mục tiêu quan trọng nhất và phân bổ tài nguyên hiệu quả để đạt được chúng;
* Nó giúp cá nhân hiểu rõ đóng góp của mình vào các mục tiêu của tổ chức và đo lường tiến độ của các hoạt động;
* Ứng dụng này giúp bạn tập trung vào mục tiêu của mình và đo lường thành công thông qua các kết quả then chốt;

Các tính năng chính
===================
1. **Định nghĩa OKR**: Tạo, chỉnh sửa và theo dõi OKR ở cấp độ cá nhân, phòng ban và tổ chức. Liên kết mục tiêu cá nhân với mục tiêu tổ chức để đạt được sự nhất quán chiến lược;
2. **Đo lường tiến độ tự động**: Theo dõi thành tựu mục tiêu tự động thông qua các chỉ số kết quả then chốt;
3. **Trực quan hóa OKR**: Xem các mục tiêu và hệ thống kết quả then chốt thông qua biểu đồ OKR trực quan;
4. **Khả năng mở rộng**: Tích hợp liền mạch với các ứng dụng khác như Dự án, Bảng chấm công và Gamification.

Lợi ích
=======
1. **Liên kết mục tiêu rõ ràng**: Liên kết các mục tiêu cá nhân, phòng ban và tổ chức để thúc đẩy nỗ lực thống nhất hướng tới các mục tiêu chung;
2. **Đóng góp được tăng cường**: Tăng cường động lực và năng suất của nhân viên bằng cách làm rõ vai trò và đóng góp cá nhân;
3. **Tầm nhìn chiến lược**: Xây dựng và theo dõi các chiến lược dài hạn để phát triển bền vững;
4. **Theo dõi tiến độ hiệu quả**: Tự động cập nhật và đo lường tiến độ, cải thiện hiệu quả quản lý;
5. **Thông tin có thể hành động**: Biểu đồ OKR minh bạch cung cấp sự rõ ràng để đưa ra quyết định nhanh chóng và chính xác hơn.

Ai nên sử dụng mô-đun này
=========================
Phần mềm OKR được thiết kế cho các tổ chức thuộc mọi quy mô và ngành nghề:

* Các nhà lãnh đạo tìm cách xác định và liên kết các mục tiêu chiến lược;
* Các nhà quản lý muốn giám sát và hướng dẫn đội ngũ của họ một cách hiệu quả;
* Nhân viên muốn đóng góp và theo dõi tiến độ hướng tới các mục tiêu chung.

Ấn bản được hỗ trợ
==================
1. Ấn bản Community
2. Ấn bản Enterprise

    """,

    'author': "T.V.T Marine Automation (aka TVTMA),Viindoo",
    'website': "https://viindoo.com/intro/okr",
    'live_test_url': "https://v16demo-int.viindoo.com",
    'live_test_url_vi_VN': "https://v16demo-vn.viindoo.com",
    'demo_video_url': "https://youtu.be/spJkKU6U2tg",
    'demo_video_url_vi_VN': "https://youtu.be/kl-CAPhplD4",
    'support': "apps.support@viindoo.com",
    'category': 'Human Resources/OKR',
    'version': '0.1.3',
    'depends': ['to_org_chart', 'viin_hr'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/okr_node_views.xml',
        'views/root_menu.xml',
        'views/hr_employee_public_views.xml',
        'views/hr_employee_views.xml',
        'views/res_config_setting.xml',
    ],
    'images': [
        'static/description/main_screenshot.png'
        ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 144.9,
    'subscription_price': 4.97,
    'currency': 'EUR',
    'license': 'OPL-1',
}
