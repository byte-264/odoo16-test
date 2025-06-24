from odoo.tests import tagged, Form

from .common import HrTestEmployeeCommon


@tagged('post_install', '-at_install')
class TestHremployee(HrTestEmployeeCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Employee = cls.env['hr.employee'].with_context(tracking_disable=True)
        cls.ceo = Employee.create({
            'name': 'CEO',
            })
        cls.coo = Employee.create({
            'name': 'COO',
            })
        cls.department_bod = cls.env['hr.department'].create({'name': 'Board of Directors 1', 'manager_id': cls.ceo.id})
        cls.department_backoffice = cls.env['hr.department'].create({'name': 'Back Office', 'manager_id': cls.coo.id})
        cls.department_sale = cls.env['hr.department'].create({'name': 'Sales 1', 'parent_id': cls.department_bod.id})
        cls.department_qaqc = cls.env['hr.department'].create({'name': 'QA/QC', 'parent_id': cls.department_backoffice.id})
        cls.manager_l1 = Employee.create({
            'name': 'Manager Level 1',
            })
        cls.manager_l2 = Employee.create({
            'name': 'Manager Level 2',
            })
        cls.manager_l3 = Employee.create({
            'name': 'Manager Level 3',
            })

    def test_01_department_manager(self):
        """
        Sales Department Manager should take CEO as its manager
        """
        self.department_sale.manager_id = self.manager_l2
        self.manager_l2.department_id = self.department_sale
        self.assertTrue(self.manager_l2.parent_id == self.ceo)

    def test_01_employee_form_parent_id(self):
        """A department manager should not be a manager of himself"""
        self.department_sale.manager_id = self.manager_l2
        with Form(self.manager_l2):
            self.assertFalse(self.manager_l2.parent_id)
            # onchange employee's department
            self.manager_l2.department_id = self.department_sale
            self.assertTrue(self.manager_l2.parent_id != self.manager_l2)

    def test_02_employee_form_parent_id(self):
        """A department manager should not be a manager of himself"""
        self.department_sale.manager_id = self.manager_l2
        with Form(self.env['hr.employee']) as f:
            f.name = 'new employee'
            self.assertFalse(f.parent_id)
            # onchange employee's department
            f.department_id = self.department_sale
            self.assertTrue(f.parent_id == self.manager_l2)

    def test_01_recursive_managers(self):
        """
        Simple manager tree: manager_l1 => manager_l2 => manager_l3
        """
        self.manager_l1.parent_id = self.manager_l2
        self.manager_l2.parent_id = self.manager_l3
        self.assertRecordValues(
            self.manager_l1.parent_ids,
            [
                {
                    'id': self.manager_l2.id,
                    'parent_id': self.manager_l3.id
                    },
                {
                    'id': self.manager_l3.id,
                    'parent_id': False
                    }
                ]
            )
        self.assertEqual(self.manager_l1.parent_all_count, 2)
        self.assertEqual(self.manager_l2.parent_all_count, 1)
        self.assertEqual(self.manager_l3.parent_all_count, 0)

    def test_02_recursive_managers(self):
        """
        recursive mamager tree
        manager_l1 => manager_l2 => manager_l3 => manager_l1 -----
        ^                                                        |
        |---------------------------------------------------------

        1. Each will have 2 manager
        2. manager_l1 should not be a manager of itself
        """
        self.manager_l1.parent_id = self.manager_l2
        self.manager_l2.parent_id = self.manager_l3
        self.manager_l3.parent_id = self.manager_l1
        self.assertRecordValues(
            self.manager_l1.parent_ids,
            [
                {
                    'id': self.manager_l2.id,
                    'parent_id': self.manager_l3.id
                    },
                {
                    'id': self.manager_l3.id,
                    'parent_id': self.manager_l1.id
                    }
                ]
            )
        self.assertEqual(self.manager_l1.parent_all_count, 2)
        self.assertEqual(self.manager_l2.parent_all_count, 2)
        self.assertEqual(self.manager_l3.parent_all_count, 2)

    def test_03_recursive_managers(self):
        """
        Parent Tree: manager_l1 => manager_l2 => manager_l3
        Department Manager:
            BoD:
                manager: ceo
                member: manager_l3
            Sales:
                manager: manager_l2
                members: manager_l1, employee
        Expected: employee has 2 managers: manager_l2 and ceo
        """
        self.manager_l3.department_id = self.department_bod
        self.department_sale.manager_id = self.manager_l2
        self.manager_l1.department_id = self.department_sale
        self.employee.department_id = self.department_sale
        self.assertRecordValues(
                self.employee.parent_ids,
                [
                    {
                        'id': self.manager_l2.id
                        },
                    {
                        'id': self.ceo.id
                        }
                    ]
                )
        self.assertEqual(self.employee.parent_all_count, 2, "The Employee should have 2 managers")
        # in case we force the employee's manager on his profile as False,
        # he should still have 2 managers (his department manager - Sale, and the superior department manager - CEO)
        with self.env.cr.savepoint():
            self.employee.parent_id = False
            self.assertRecordValues(
                self.employee.parent_ids,
                [
                    {
                        'id': self.manager_l2.id
                        },
                    {
                        'id': self.ceo.id
                        }
                    ]
                )
            self.assertEqual(self.employee.parent_all_count, 2, "The Employee should have 2 managers")

    def test_01_recursive_managers_index_order(self):
        """
        managers are sorted from lower level to higher level in employee.parent_ids
        """
        self.manager_l1.parent_id = self.manager_l2
        self.manager_l2.parent_id = self.manager_l3
        self.employee.parent_id = self.manager_l1
        self.assertRecordValues(
            self.employee.parent_ids,
            [
                {
                    'id': self.manager_l1.id,
                    'parent_id': self.manager_l2.id
                    },
                {
                    'id': self.manager_l2.id,
                    'parent_id': self.manager_l3.id
                    },
                {
                    'id': self.manager_l3.id,
                    'parent_id': False
                    }
                ]
            )
        self.assertEqual(self.employee.parent_all_count, 3)
        self.assertEqual(self.manager_l1.parent_all_count, 2)
        self.assertEqual(self.manager_l2.parent_all_count, 1)
        self.assertEqual(self.manager_l3.parent_all_count, 0)

    def test_02_recursive_managers_index_order(self):
        """
        Input:
        BOD department
            department manager: ceo
            member: manager_l3

        ----Sale department
            department manager: manager_l2
            members: employee + manager_l1

        Expect:
        parent_ids of employee: manager_l2, ceo
        """
        self.department_sale.manager_id = self.manager_l2
        (self.employee + self.manager_l1).write({
            'department_id': self.department_sale.id
            })
        self.manager_l3.department_id = self.department_bod
        self.assertRecordValues(
            self.employee.parent_ids,
            [
                {
                    'id': self.manager_l2.id,
                    'parent_id': False,  # manager_l2 has no parent as he belongs to no department
                    'parent_ids': self.ceo.ids
                    },
                {
                    'id': self.ceo.id,
                    'parent_id': False,
                    'parent_ids': []
                    }
                ]
            )
        # Department of manager_l2: Sale department
        # Expect: parent_ids of manager_l1: manager_l2, ceo
        self.manager_l2.department_id = self.department_sale
        self.assertRecordValues(
            self.manager_l1.parent_ids,
            [
                {
                    'id': self.manager_l2.id,
                    'parent_id': self.ceo.id,
                    'parent_ids': self.ceo.ids
                    },
                {
                    'id': self.ceo.id,
                    'parent_id': False,
                    'parent_ids': []
                    }
                ]
            )

    def test_03_recursive_managers_index_order(self):
        """
        Input:
        BDO department:
            department manager: ceo
            members: manager_l3

        ----Sale department
            parent department: BOD
            department manager: manager_l2
            members: 1. manager_l2
                    2. manager_l1
                    3. employee
            manager of employee: manager_l1

        Expects:
        parent_ids of employee: manager_l1, manager_l2, ceo
        """
        self.department_sale.manager_id = self.manager_l2
        (self.employee + self.manager_l1 + self.manager_l2).write({
            'department_id': self.department_sale.id
            })
        self.employee.parent_id = self.manager_l1
        self.manager_l3.department_id = self.department_bod

        self.assertRecordValues(
            self.employee.parent_ids,
            [
                {
                    'id': self.manager_l1.id,
                    'parent_id': self.manager_l2.id,
                    'parent_ids': (self.manager_l2 + self.ceo).ids
                    },
                {
                    'id': self.manager_l2.id,
                    'parent_id': self.ceo.id,
                    'parent_ids': self.ceo.ids
                    },
                {
                    'id': self.ceo.id,
                    'parent_id': False,
                    'parent_ids': []
                    }
                ]
            )

    def test_04_recursive_managers_index_order(self):
        """
        Input:
        BOD department
            department manager: ceo
            member: manager_l3

        Back Office
            department manager: coo

        ----QA/QC department
                 parent department: Back Office
                 department manager: manager_l2

        ----Sale department
            parent department: BOD
            department manager: manager_l2
            members: employee + manager_l1

        Expect:
        parent_ids of employee: manager_l2, ceo, coo
        """

        self.department_sale.manager_id = self.manager_l2
        self.department_qaqc.manager_id = self.manager_l2
        (self.employee + self.manager_l1).write({
            'department_id': self.department_sale.id
            })
        self.manager_l3.department_id = self.department_bod
        self.assertRecordValues(
            self.employee.parent_ids,
            [
                {
                    'id': self.manager_l2.id,
                    'parent_id': False,  # manager_l2 has no parent as he belongs to no department
                    'parent_ids': (self.ceo + self.coo).ids
                    },
                 {
                    'id': self.coo.id,
                    'parent_id': False,
                    'parent_ids': []
                    },
                {
                    'id': self.ceo.id,
                    'parent_id': False,
                    'parent_ids': []
                    }
                ]
            )
        # Department of manager_l2= Sale department
        # Expect: parent_ids of manager_l1: manager_l2, ceo, coo
        self.manager_l2.department_id = self.department_sale
        self.assertRecordValues(
            self.manager_l1.parent_ids,
            [
                {
                    'id': self.manager_l2.id,
                    'parent_id': self.ceo.id,
                    'parent_ids': (self.ceo + self.coo).ids
                    },
                {
                    'id': self.ceo.id,
                    'parent_id': False,
                    'parent_ids': []
                    },
                {
                    'id': self.coo.id,
                    'parent_id': False,
                    'parent_ids': []
                    }
                ]
            )

    def test_05_recursive_managers_index_order(self):
        """
        Input:
        BDO department:
            department manager: ceo
            members: manager_l3

        Back Office:
            department manager: coo

        ----QA/QC department
            parent department: Back Office
            department manager: manager_l2

        ----Sale department
            parent department: BOD
            department manager: manager_l2
            members: 1. manager_l2
                    2. manager_l1
                    3. employee
            manager of employee: manager_l1

        Expects:
        parent_ids of employee: manager_l1, manager_l2, ceo, coo
        """
        self.department_sale.manager_id = self.manager_l2
        self.department_qaqc.manager_id = self.manager_l2
        (self.employee + self.manager_l1 + self.manager_l2).write({
            'department_id': self.department_sale.id
            })
        self.employee.parent_id = self.manager_l1
        self.manager_l3.department_id = self.department_bod

        self.assertRecordValues(
            self.employee.parent_ids,
            [
                {
                    'id': self.manager_l1.id,
                    'parent_id': self.manager_l2.id,
                    'parent_ids': (self.manager_l2 + self.ceo + self.coo).ids
                    },
                {
                    'id': self.manager_l2.id,
                    'parent_id': self.ceo.id,
                    'parent_ids': (self.ceo + self.coo).ids
                    },
                {
                    'id': self.ceo.id,
                    'parent_id': False,
                    'parent_ids': []
                    },
                {
                    'id': self.coo.id,
                    'parent_id': False,
                    'parent_ids': []
                    }
                ]
            )

    def test_01_department_managers(self):
        """
        Case 1.1:
            Input: department_sale_2 has parent_id is department_sale, department_sale has parent_id as department_bod,
                department_sale has manager_id unlike manager_id of department_bod
            Output: manager_ids of department_sale_2  as manager_id of department_sale and department_bod
        """
        self.department_sale.write({'manager_id': self.manager_l2.id})
        department_sale_2 = self.env['hr.department'].with_context(tracking_disable=True).create({
            'name': 'Sales 2', 'parent_id': self.department_sale.id
            })
        self.assertEqual(department_sale_2.manager_ids.ids, [self.department_sale.manager_id.id, self.department_bod.manager_id.id])

        # Case 1.2:
        # Input: department_sale_2 has parent_id is department_sale, department_sale has parent_id as department_bod,
        # department_sale has manager_id like manager_id of department_bod
        # Output: manager_ids of department_sale =  manager_id of department_bod
        self.department_sale.write({'manager_id': self.ceo.id})
        self.assertEqual(department_sale_2.manager_ids.ids, [self.department_bod.manager_id.id])

        # Case 1.3:
        # Input: departmet_sale_2 has manager_id = manage_l3 and parent_id of department_sale_2 = department_sale
        # Output: department_sale_2 has manager_id = manager_id of department_sale and department_sale_2
        department_sale_2.write({'manager_id': self.manager_l3.id})
        self.assertEqual(department_sale_2.manager_ids.ids, [department_sale_2.manager_id.id, self.department_sale.manager_id.id])

    def test_02_department_managers(self):
        """
        Case 2:
            Input: department_sale_2 has manager_id as manager_id of department_sale and parent_id of department_sale_2 = False
            Output: manager_ids of department_sale_2 = manager_id of department_sale
        """
        self.department_sale.write({'manager_id': self.manager_l2.id})
        department_sale_2 = self.env['hr.department'].with_context(tracking_disable=True).create({
            'name': 'Sales 2',
            'manager_id': self.manager_l2.id
            })
        self.assertEqual(department_sale_2.manager_ids.ids, [self.department_sale.manager_id.id])

    def test_01_department_recursive_childs(self):
        """
        Case 1.1:
            Input:  department_bod has child_ids = department_sale_2 and department_sale,
            Output: recursive_childs of department_bod = department_sale and department_sale_2
        """
        department_sale_2 = self.env['hr.department'].with_context(tracking_disable=True).create({'name': 'Sales 2', 'parent_id': self.department_bod.id})
        self.assertEqual(self.department_bod.recursive_child_ids.ids, [self.department_sale.id, department_sale_2.id])

        # Case 1.2:
        # Input:  department_bod has child_ids = department_sale and department_sale has child_ids = departmet_sale_2,
        # Output: recursive_childs of department_bod = department_sale and department_sale_2
        department_sale_2.write({'parent_id': self.department_sale.id})
        self.assertEqual(self.department_bod.recursive_child_ids.ids, [self.department_sale.id, department_sale_2.id])

    def test_01_employee_superiors(self):
        """
        Simple manager tree: manager_l1 => manager_l2 => manager_l3
        """
        self.manager_l3.write({'parent_id': self.manager_l2.id})
        self.manager_l2.write({'parent_id': self.manager_l1.id})
        self.assertTrue(self.manager_l3.parent_ids.ids == [self.manager_l2.id, self.manager_l1.id])
