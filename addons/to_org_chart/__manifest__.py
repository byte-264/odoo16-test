{
    'name': "Org Chart",
    'name_vi_VN': "Biểu đồ tổ chức doanh nghiệp",

    'summary': """
Provide Organization Chart view to others to use
    """,

    'summary_vi_VN': """
Cung cấp giao diện Sơ đồ tổ chức cho các module khác tái sử dụng
    """,

    'description': """
Demo video: `Org Chart <https://youtu.be/tjdPnEQxe2Y>`_

Key Value
=========
The module adds an Organization Chart to the OKR App, providing Users an intuitive view of all Objectives and Key Results of Businesses.

The hierarchy structure of Objectives and Key Results helps Users:

* Track all the planned OKRs from the lowest level (personal objectives) to the highest ones (objective of the department/company).
* Clarify which objectives contribute to achieving higher objectives.

Supported Editions
==================
1. Community Edition
2. Enterprise Edition

    """,

    'description_vi_VN': """
Demo video: `Biểu đồ tổ chức doanh nghiệp <https://youtu.be/tjdPnEQxe2Y>`_

Tính năng
=========
Mô-đun bổ sung giao diện Sơ đồ tổ chức vào Ứng dụng OKR, mang đến một cái nhìn trực quan về tất cả các Mục tiêu và Kết quả then chốt của Doanh nghiệp.

Các mục tiêu được sắp xếp theo thứ tự phân cấp phả hệ, giúp người dùng:

* Dễ dàng theo dõi tất cả các OKR đã lên kế hoạch của Doanh nghiệp từ cấp thấp nhất (mục tiêu của cá nhân) đến cấp cao nhất (mục tiêu chung của phòng ban, doanh nghiệp).
* Thấy được từng mục tiêu nhỏ hỗ trợ, đóng góp thành tích cho các mục tiêu cao hơn.

Ấn bản được Hỗ trợ
==================
1. Ấn bản Community
2. Ấn bản Enterprise

    """,

    'author': "T.V.T Marine Automation (aka TVTMA),Viindoo",
    'website': "https://viindoo.com/apps/app/16.0/to_org_chart",
    'live_test_url': "https://v16demo-int.viindoo.com",
    'live_test_url_vi_VN': "https://v16demo-vn.viindoo.com",
    'demo_video_url': "https://youtu.be/tjdPnEQxe2Y",
    'support': "apps.support@viindoo.com",
    'category': 'Human Resources/OKR',
    'version': '0.1',
    'depends': ['web'],
    'data': [],
    'images': [
        'static/description/main_screenshot.png'
    ],
    'assets': {
        'web.assets_backend': [
            'to_org_chart/static/lib/orgchart/jquery.orgchart.css',
            'to_org_chart/static/src/scss/org_chart_view.scss',
            'to_org_chart/static/src/js/**/*'
            ],
        'web.qunit_suite_tests': [
            'to_org_chart/static/tests/**/*'
            ]
        },
    # TODO: Improved to allow customizing views similar to tree views, kanban views from version 17.0
    'installable': True,
    'application': False,
    'auto_install': True,
    'price': 9.9,
    'currency': 'EUR',
    'license': 'OPL-1',
}
