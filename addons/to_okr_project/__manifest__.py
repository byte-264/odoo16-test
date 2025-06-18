{
    'name': "OKR & Project Integrator",
    'name_vi_VN': "Tích hợp OKR với Dự án",
    'summary': "Link or create tasks from OKR Key Results to align goals with actionable activities",
    'summary_vi_VN': "Liên kết hoặc tạo nhiệm vụ từ Kết quả then chốt OKR, giúp kết nối mục tiêu với hành động cụ thể",
    'description': """
Demo video: `OKR & Project Integrator <https://youtu.be/CWkPgcH8aK4>`_

What It Does
============
**Transform objectives into actionable plans**: This module seamlessly integrates the OKR (Objectives & Key Results) framework with the Project application, enabling your organization to effortlessly connect strategic objectives with actionable tasks and measurable outcomes.

Key Features
============
1. Assign Objectives & Key Results to Projects/Tasks;
2. Create Projects/Tasks directly within OKR;
3. Track the number of Objectives & Key Results linked to each Project;
4. Manage the number of Projects/Tasks under one Objective or Key Result.

Benefits
========
1. **Turn OKR into actionable plans**: Don't let goals just stay on paper. Create projects and tasks directly from OKR and witness how objectives turn into real progress;
2. **Easy collaboration**: Assign objectives and key results to specific tasks and individual team members. Help your team understand their role in achieving common success;
3. **Real-time progress tracking**: Clearly visualize how objectives are linked to daily activities. Measure success as tasks are completed and key results are achieved — all in one place;
4. **Optimize workflow**: Break down large projects into smaller, easily assignable tasks and ensure everyone is working towards the same goal;
5. **Focus and transparency**: With automatic time tracking and detailed monitoring features, you can control resources and ensure all efforts are recognized.

Who Should Use This Module
==========================
1. **Leaders and managers**: Want to ensure strategic goals are integrated into daily activities;
2. **Teams**: Looking for clarity in work and simplified task management;
3. **Businesses**: Want to optimize the alignment between goals and actions to improve performance and transparency.

Supported Editions
==================
1. Community Edition
2. Enterprise Edition

    """,
    'description_vi_VN': """
Demo video: `Tích hợp OKR với Dự án <https://youtu.be/EFn4xBH6x9s>`_

Mô-đun này làm gì
=================
**Biến mục tiêu thành hành động cụ thể**: Module này liên kết liền mạch giữa khung OKR (Objectives & Key Results) và ứng dụng Dự án, giúp tổ chức của bạn dễ dàng kết nối các mục tiêu chiến lược với các nhiệm vụ thực tế và kết quả đo lường được.

Tính năng nổi bật
=================
1. Gán Mục tiêu & Kết quả then chốt vào Dự án/Nhiệm vụ;
2. Tạo Dự án/Nhiệm vụ trực tiếp trong OKR;
3. Theo dõi số lượng Mục tiêu & Kết quả then chốt được liên kết với từng Dự án;
4. Quản lý số lượng Dự án/Nhiệm vụ thuộc một Mục tiêu hoặc Kết quả then chốt.

Lợi ích
=======
1. **Biến OKR thành kế hoạch hành động**: Đừng để mục tiêu chỉ nằm trên giấy. Tạo các dự án và nhiệm vụ trực tiếp từ OKR và chứng kiến cách các mục tiêu biến thành tiến trình thực tế;
2. **Hợp tác dễ dàng**: Gán mục tiêu và kết quả then chốt vào các nhiệm vụ cụ thể và từng thành viên trong nhóm. Giúp đội ngũ của bạn hiểu rõ vai trò của mình trong việc đạt được thành công chung;
3. **Theo dõi tiến độ theo thời gian thực**: Hình dung rõ cách các mục tiêu liên kết với hoạt động hàng ngày. Đo lường thành công khi các nhiệm vụ được hoàn thành và kết quả then chốt được đạt được — tất cả chỉ trong một nơi;
4. **Tối ưu hóa quy trình làm việc**: Phân chia các dự án lớn thành các nhiệm vụ nhỏ hơn, dễ dàng phân công và đảm bảo mọi thành viên đều làm việc hướng đến cùng một mục tiêu;
5. **Tập trung và minh bạch**: Với tính năng tự động ghi chấm công và theo dõi chi tiết, bạn có thể kiểm soát nguồn lực và đảm bảo mọi nỗ lực đều được ghi nhận.

Ai nên sử dụng mô-đun này
=========================
1. **Lãnh đạo và quản lý**: Muốn đảm bảo các mục tiêu chiến lược được tích hợp vào các hoạt động hàng ngày;
2. **Đội nhóm**: Tìm kiếm sự rõ ràng trong công việc và đơn giản hóa quản lý nhiệm vụ;
3. **Doanh nghiệp**: Muốn tối ưu hóa sự liên kết giữa mục tiêu và hành động để cải thiện hiệu suất và minh bạch.

Ấn bản được Hỗ trợ
==================
1. Ấn bản Community
2. Ấn bản Enterprise

    """,

    'author': "T.V.T Marine Automation (aka TVTMA),Viindoo",
    'website': "https://viindoo.com/apps/app/16.0/to_okr_project",
    'live_test_url': "https://v16demo-int.viindoo.com",
    'live_test_url_vi_VN': "https://v16demo-vn.viindoo.com",
    'demo_video_url': "https://youtu.be/CWkPgcH8aK4",
    'demo_video_url_vi_VN': "https://youtu.be/EFn4xBH6x9s",
    'support': "apps.support@viindoo.com",
    'category': 'Human Resources/OKR',
    'version': '0.1',
    'depends': ['to_okr', 'project'],
    'data': [
        'security/security.xml',
        'views/okr_node_views.xml',
        'views/project_project_views.xml',
        'views/project_task_views.xml',
    ],
    'images': [
        'static/description/main_screenshot.png'
        ],
    'installable': True,
    'application': False,
    'auto_install': True,
    'price': 27,
    'currency': 'EUR',
    'license': 'OPL-1',
}
