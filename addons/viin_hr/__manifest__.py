{
    'name': "Employees Customization",
    'name_vi_VN': "Tùy biến Nhân viên",
    'summary': "This is a technical module that improves and customizes the technical aspects of the HR application",
    'summary_vi_VN': "Đây là mô-đun kỹ thuật cải thiện và tùy chỉnh các khía cạnh kỹ thuật của ứng dụng Nhân viên (HR)",
    'description': """
**Demo video:** `Employees Customization <https://youtu.be/68q726yNq-s>`_

What it does
============
Enhance employee profiles, expand role-based permissions, establish a structured hierarchy for management and departments, and prepare for future scalability.

Key Features
============

1. **Enhanced Employee Profiles**: Add critical fields to employee profiles, including *VAT*, *Place Of Origin*, and a designation to mark employees as *Department Heads*. VAT is linked directly from private contact records for accuracy and time-saving.
2. **Expanded Role-Based Permissions**: Users with roles like *HR Officer: Manage All Employees* and *Contact Creator* can securely update private employee records, including:
    - *Email (email)*
    - *Phone (phone)*
    - *Mobile (mobile)*
    - *Date of Birth (dob)*
    - *Bank Accounts (bank_ids)*
    - *Contact Name (name)*
    - *Company (company_id)*
    - *Contact Type (type)*

3. **Employee Management Hierarchy**: Add technical fields to define relationships, including direct and indirect supervisors (``parent_ids``) and coaches (``coach_ids``), creating a clear structure.
4. **Departmental Hierarchy Structure**: Introduce fields for direct and indirect parent departments (``parent_ids``) and subordinate departments (``recursive_child_ids``) for systematic department management.
5. **Multilingual Department Names**: Allow department names to be entered and displayed in multiple languages, enhancing usability in international environments.
6. **Scalability**: Designed to integrate easily with other modules like `Employee Ranks </apps/modules/16.0/viin_hr_rank>`_, `Payroll </apps/modules/16.0/to_hr_payroll>`_, and `HR Accounting </apps/modules/16.0/viin_hr_account>`_.

Who Should Use This Module?
===========================

1. **HR Departments**:
    - Manage detailed employee data, including VAT and hometowns.
    - Establish clear organizational structures for efficient employee management.

2. **Businesses Operating in Multilingual Environments**:
    - Ideal for international companies requiring multilingual department names.

3. **Senior Management**:
    - Understand and improve organizational hierarchy with structured data.

4. **Businesses Seeking Future Scalability**:
    - Build a foundation for advanced features like reporting, organizational analysis, and productivity management.

Supported Editions
==================

- Community Edition
- Enterprise Edition

    """,
    'description_vi_VN': """
**Demo video:** `Tùy biến Nhân viên <https://youtu.be/1bKYcUDhMPQ`_

Mô-đun này làm gì
=================
Cải thiện thông tin hồ sơ nhân viên, mở rộng phân quyền, hoàn thiện cấu trúc phân cấp quản lý & phòng ban, sẵn sàng cho sự mở rộng trong tương lai.

Tính năng chính
===============

#. **Cải thiện thông tin hồ sơ nhân viên**: Thêm các trường thông tin quan trọng vào hồ sơ nhân viên, bao gồm *Mã số thuế cá nhân (VAT)*, *Quê quán* và tùy chọn đánh dấu nhân viên *Là trưởng phòng*. Hệ thống tự động đồng bộ dữ liệu VAT từ thông tin liên hệ riêng tư, đảm bảo tính chính xác và tiết kiệm thời gian.
#. **Mở rộng phân quyền**: Người dùng có vai trò *Cán bộ: Quản lý toàn bộ nhân viên* và *Tạo liên hệ* được phép cập nhật một số trường trong *Liên hệ riêng tư* của nhân viên, bao gồm:
    + *Email (email)*
    + *Điện thoại (phone)*
    + *Di động (mobile)*
    + *Ngày sinh (dob)*
    + *Tài khoản ngân hàng (bank_ids)*
    + *Tên liên hệ (name)*
    + *Công ty (company_id)*
    + *Loại liên hệ (type)*

#. **Cấu trúc cấp quản lý nhân viên**: Thêm các trường kỹ thuật để xác định mối quan hệ nhân viên, bao gồm cấp trên trực tiếp và gián tiếp (``parent_ids``) cũng như huấn luyện viên (``coach_ids``), giúp quản lý cấu trúc nhân sự rõ ràng và có hệ thống.
#. **Cấu trúc phân cấp phòng ban**: Thêm các trường kỹ thuật để thể hiện quan hệ phân cấp, bao gồm phòng ban cấp trên trực tiếp và gián tiếp (``parent_ids``) và phòng ban cấp dưới (``recursive_child_ids``), giúp quản lý bộ phận rõ ràng và có hệ thống.
#. **Hỗ trợ đa ngôn ngữ cho tên phòng ban**: Cho phép nhập và hiển thị tên phòng ban bằng nhiều ngôn ngữ, nâng cao khả năng sử dụng trong môi trường quốc tế.
#. **Sẵn sàng cho sự mở rộng**: Mô-đun này được thiết kế để dễ dàng mở rộng và tương thích với các mô-đun khác (Chức danh Nhân viên </apps/modules/16.0/viin_hr_rank>`_, Bảng lương </apps/modules/16.0/to_hr_payroll>`_, Kế toán Nhân sự </apps/modules/16.0/viin_hr_account>`_, v.v.).

Ai nên sử dụng mô-đun này?
==========================

#. **Phòng Nhân sự (HR Department)**:
    - Quản lý thông tin nhân viên chi tiết hơn, bao gồm mã số thuế cá nhân và quê quán.
    - Thiết lập và quản lý cấu trúc tổ chức rõ ràng, giúp tối ưu hóa hiệu quả quản lý nhân viên.

#. **Doanh nghiệp hoạt động trong môi trường đa ngôn ngữ**:
    - Phù hợp với các công ty quốc tế cần hỗ trợ tên phòng ban bằng nhiều ngôn ngữ.

#. **Quản lý cấp cao**:
    - Hiểu rõ hơn về cấu trúc phân cấp của tổ chức, từ cấp quản lý trực tiếp đến cấp gián tiếp.
    - Dễ dàng đánh giá và cải thiện hệ thống tổ chức thông qua cấu trúc dữ liệu rõ ràng.

#. **Doanh nghiệp mong muốn mở rộng tính năng trong tương lai**:
    - Làm nền tảng cho việc phát triển các tính năng nâng cao như báo cáo, phân tích tổ chức, hoặc quản lý năng suất.

Ấn bản hỗ trợ
=============

#. Ấn bản Community
#. Ấn bản Enterprise

    """,
    'author': 'Viindoo',
    'website': 'https://viindoo.com/apps/app/16.0/viin_hr',
    'live_test_url': "https://v16demo-int.viindoo.com",
    'live_test_url_vi_VN': "https://v16demo-vn.viindoo.com",
    'demo_video_url': 'https://youtu.be/68q726yNq-s',
    'demo_video_url_vi_VN': 'https://youtu.be/1bKYcUDhMPQ',
    'support': 'apps.support@viindoo.com',
    'category': 'Hidden',
    'version': '0.1.1',
    # any module necessary for this one to work correctly
    'depends': ['hr', 'hr_org_chart'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'views/res_partner_views.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'auto_install': True,
    'price': 18.9,
    'currency': 'EUR',
    'license': 'OPL-1',
}
