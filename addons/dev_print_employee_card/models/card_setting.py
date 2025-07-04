# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################
from odoo import models,fields, api

class card_setting(models.Model):
    _name ='card.setting'
    _description = 'Card Setting'


    name = fields.Char('Name', required="1")
    back_image = fields.Binary('Background Image')
    page_type =fields.Selection([('front','Front'),('back','Back')], string='Page', default='front')
    
    card_width =fields.Float('Width', default=300)
    card_height = fields.Float('Height', default=500)
    
    is_company_logo= fields.Boolean('Company Logo', default=True)
    logo_width = fields.Float(string='Width', default=180.00)
    logo_m_top = fields.Float(string='From Top', default=15)
    logo_m_left = fields.Float(string='From Left', default=10)
    
    
    
    is_emp_image= fields.Boolean(string='Employee Image', default=True)
    image_round = fields.Boolean('Round Image', default=True)
    emp_img_width = fields.Float(string='Width', default=100)
    emp_img_m_top = fields.Float(string='From Top', default=100)
    emp_img_m_left = fields.Float(string='From Left', default=100)
    
    # Employee Name
    is_employee = fields.Boolean(string='Employee Name',default=True)
    is_name_label = fields.Boolean(string='Print Label')
    name_label = fields.Char('Label', default='Name')
    name_lab_bold = fields.Boolean(string='Bold')
    name_lab_color= fields.Char(string='Font Color', default='#000')
    name_lab_font_size = fields.Float(string='Font Size',default=0)
    name_lab_m_top = fields.Float(string='From Top', default=0)
    name_lab_m_left = fields.Float(string='From Left', default=0)
    is_label_emp_name_center = fields.Boolean('Label Center')
    
    
    emp_bold = fields.Boolean(string='Bold', default=True)
    emp_color= fields.Char(string='Font Color', default='#26A3AE')
    emp_font_size = fields.Float(string='Font Size',default=25)
    emp_m_top = fields.Float(string='From Top', default=210)
    emp_m_left = fields.Float(string='From Left', default=35)
    is_emp_name_center = fields.Boolean('Name Center', default=True)
    
    
    # Employee Job Position
    is_jobposition = fields.Boolean(string='Employee Position',default=True)
    is_job_label = fields.Boolean(string='Print Label')
    job_label = fields.Char('Label', default='Name')
    job_lab_bold = fields.Boolean(string='Bold')
    job_lab_color= fields.Char(string='Font Color', default='#000')
    job_lab_font_size = fields.Float(string='Font Size',default=0)
    job_lab_m_top = fields.Float(string='From Top', default=0)
    job_lab_m_left = fields.Float(string='From Left', default=0)
    is_label_emp_job_center = fields.Boolean('Label Center')
    
    
    job_bold = fields.Boolean(string='Bold')
    job_color= fields.Char(string='Font Color', default='#000')
    job_font_size = fields.Float(string='Font Size',default=20)
    job_m_top = fields.Float(string='From Top', default=240)
    job_m_left = fields.Float(string='From Left', default=35)
    is_job_name_center = fields.Boolean('Name Center', default=True)
    
    #=================================================================
    
    
    # Employee Number      
    
    is_number = fields.Boolean(string='Employee No',default=True)
    is_number_label = fields.Boolean(string='Print Label', default=True)
    number_label = fields.Char('Label', default='Employee No')
    num_lab_bold = fields.Boolean(string='Bold')
    num_lab_color= fields.Char(string='Font Color', default='#000')
    num_lab_font_size = fields.Float(string='Font Size',default=15)
    num_lab_m_top = fields.Float(string='From Top', default=290)
    num_lab_m_left = fields.Float(string='From Left', default=30)
    is_num_lab_center = fields.Boolean('Label Center')
    
    is_number_center = fields.Boolean('Center')
    num_bold = fields.Boolean(string='Bold')
    num_color= fields.Char(string='Font Color', default='#000')
    num_font_size = fields.Float(string='Font Size',default=15)
    num_m_top = fields.Float(string='From Top', default=290)
    num_m_left = fields.Float(string='From Left', default=140)
    
    #=================================================================
    
    # Employee Birthday      
    
    is_birthday = fields.Boolean(string='Birthday',default=True)
    is_birthday_label = fields.Boolean(string='Print Label', default=True)
    birthday_label = fields.Char('Label', default='D.O.B.')
    birthday_lab_bold = fields.Boolean(string='Bold')
    birthday_lab_color= fields.Char(string='Font Color', default='#000')
    birthday_lab_font_size = fields.Float(string='Font Size',default=15)
    birthday_lab_m_top = fields.Float(string='From Top', default=315)
    birthday_lab_m_left = fields.Float(string='From Left', default=30)
    is_birthday_lab_center = fields.Boolean('Label Center')
    
    is_birthday_center = fields.Boolean('Center')
    birthday_bold = fields.Boolean(string='Bold')
    birthday_color= fields.Char(string='Font Color', default='#000')
    birthday_font_size = fields.Float(string='Font Size',default=15)
    birthday_m_top = fields.Float(string='From Top', default=315)
    birthday_m_left = fields.Float(string='From Left', default=140)
    
    
    #=================================================================
    
    # Employee Phone      
    
    is_phone = fields.Boolean(string='Phone',default=True)
    is_phone_label = fields.Boolean(string='Print Label', default=True)
    phone_label = fields.Char('Label', default='Phone')
    phone_lab_bold = fields.Boolean(string='Bold')
    phone_lab_color= fields.Char(string='Font Color', default='#000')
    phone_lab_font_size = fields.Float(string='Font Size',default=15)
    phone_lab_m_top = fields.Float(string='From Top', default=340)
    phone_lab_m_left = fields.Float(string='From Left', default=30)
    is_phone_lab_center = fields.Boolean('Label Center')
    
    is_phone_center = fields.Boolean('Center')
    phone_bold = fields.Boolean(string='Bold')
    phone_color= fields.Char(string='Font Color', default='#000')
    phone_font_size = fields.Float(string='Font Size',default=15)
    phone_m_top = fields.Float(string='From Top', default=340)
    phone_m_left = fields.Float(string='From Left', default=140)
    
    #=================================================================
    
    # Employee b_group      
    is_b_group = fields.Boolean(string='Blood Group')
    is_b_group_label = fields.Boolean(string='Print Label', default=True)
    b_group_label = fields.Char('Label', default='Blood Group')
    b_group_lab_bold = fields.Boolean(string='Bold')
    b_group_lab_color= fields.Char(string='Font Color', default='#000')
    b_group_lab_font_size = fields.Float(string='Font Size',default=15)
    b_group_lab_m_top = fields.Float(string='From Top', default=365)
    b_group_lab_m_left = fields.Float(string='From Left', default=30)
    is_b_group_lab_center = fields.Boolean('Label Center')
    
    is_b_group_center = fields.Boolean('Center')
    b_group_bold = fields.Boolean(string='Bold', default=True)
    b_group_color= fields.Char(string='Font Color', default='#000')
    b_group_font_size = fields.Float(string='Font Size',default=15)
    b_group_m_top = fields.Float(string='From Top', default=365)
    b_group_m_left = fields.Float(string='From Left', default=140)
    
    #=================================================================
    
    # Employee Email      
    is_email = fields.Boolean(string='Email',default=True)
    is_email_label = fields.Boolean(string='Print Label', default=True)
    email_label = fields.Char('Label', default='Email')
    email_lab_bold = fields.Boolean(string='Bold')
    email_lab_color= fields.Char(string='Font Color', default='#000')
    email_lab_font_size = fields.Float(string='Font Size',default=15)
    email_lab_m_top = fields.Float(string='From Top', default=370)
    email_lab_m_left = fields.Float(string='From Left', default=30)
    is_email_lab_center = fields.Boolean('Label Center', default=True)
    
    is_email_center = fields.Boolean('Center', default=True)
    email_bold = fields.Boolean(string='Bold')
    email_color= fields.Char(string='Font Color', default='#000')
    email_font_size = fields.Float(string='Font Size',default=15)
    email_m_top = fields.Float(string='From Top', default=390)
    email_m_left = fields.Float(string='From Left', default=100)
    #=================================================================    
    
    # BARCODE
    is_barcode = fields.Boolean(string='Print Barcode',default=True)
    is_barcode_center = fields.Boolean(string='Center', default=True)
    barcode_width = fields.Float(string='Width', default=270)
    barcode_type = fields.Selection([('Code128','Code128'),
                                     ('Code11','Code11'),
                                     ('Codabar','Codabar'),
                                     ('EAN13','EAN13'),
                                     ('EAN8','EAN8'),
                                     ('Extended39','Extended39'),
                                     ('Extended93','Extended93'),
                                     ('I2of5','I2of5'),
                                     ('QR','QR'),
                                     ('Standard39','Standard39'),
                                     ('Standard93','Standard93'),
                                     ('UPCA','UPCA')], string='Barcode Type', default='Code128', required="1")
    barcode_height = fields.Float(string='Height', default=40)
    barcode_m_top = fields.Float(string='From Top', default=425)
    barcode_m_left = fields.Float(string='From Left', default=15)
    
    
    
    is_company_name = fields.Boolean(string='Print Company Name')
    is_company_name_center = fields.Boolean('Center')
    company_name_bold = fields.Boolean(string='Bold', default=True)
    company_name_color= fields.Char(string='Font Color', default='#000')
    company_name_font_size = fields.Float(string='Font Size',default=15)
    company_name_m_top = fields.Float(string='From Top', default=355)
    company_name_m_left = fields.Float(string='From Left', default=5)
    
    
    # Company Website      
    
    is_c_website = fields.Boolean(string='Company Website',default=True)
    is_c_website_label = fields.Boolean(string='Print Label')
    c_website_label = fields.Char('Label', default='Website')
    c_website_lab_bold = fields.Boolean(string='Bold')
    c_website_lab_color= fields.Char(string='Font Color', default='#000')
    c_website_lab_font_size = fields.Float(string='Font Size',default=15)
    c_website_lab_m_top = fields.Float(string='From Top', default=325)
    c_website_lab_m_left = fields.Float(string='From Left', default=30)
    is_c_website_lab_center = fields.Boolean('Label Center')
    
    is_c_website_center = fields.Boolean('Center', default=True)
    c_website_bold = fields.Boolean(string='Bold')
    c_website_color= fields.Char(string='Font Color', default='#000')
    c_website_font_size = fields.Float(string='Font Size',default=15)
    c_website_m_top = fields.Float(string='From Top', default=470)
    c_website_m_left = fields.Float(string='From Left', default=5)
    
    
    is_home_address = fields.Boolean(string='Private Address')
    is_home_address_label = fields.Boolean(string='Private Address Label',default=True)
    home_address_label = fields.Char('Label', default='Home Address')
    home_address_lab_bold = fields.Boolean(string='Bold')
    home_address_lab_color= fields.Char(string='Font Color', default='#000')
    home_address_lab_font_size = fields.Float(string='Font Size',default=15)
    home_address_lab_m_top = fields.Float(string='From Top', default=325)
    home_address_lab_m_left = fields.Float(string='From Left', default=30)
    is_home_address_lab_center = fields.Boolean('Label Center')
    
    
    is_h_street = fields.Boolean(string='Print Street')
    is_h_street_center = fields.Boolean('Center')
    h_street_bold = fields.Boolean(string='Bold', default=True)
    h_street_color= fields.Char(string='Font Color', default='#000')
    h_street_font_size = fields.Float(string='Font Size',default=15)
    h_street_m_top = fields.Float(string='From Top', default=355)
    h_street_m_left = fields.Float(string='From Left', default=5)
    
    is_h_street2 = fields.Boolean(string='Print Street 2')
    is_h_street2_center = fields.Boolean('Center')
    h_street2_bold = fields.Boolean(string='Bold', default=True)
    h_street2_color= fields.Char(string='Font Color', default='#000')
    h_street2_font_size = fields.Float(string='Font Size',default=15)
    h_street2_m_top = fields.Float(string='From Top', default=355)
    h_street2_m_left = fields.Float(string='From Left', default=5)
    
    
    is_h_city = fields.Boolean(string='Print City / Zip',)
    is_h_city_center = fields.Boolean('Center')
    h_city_bold = fields.Boolean(string='Bold', default=True)
    h_city_color= fields.Char(string='Font Color', default='#000')
    h_city_font_size = fields.Float(string='Font Size',default=15)
    h_city_m_top = fields.Float(string='From Top', default=355)
    h_city_m_left = fields.Float(string='From Left', default=5)
    
    is_h_state = fields.Boolean(string='Print State')
    is_h_state_center = fields.Boolean('Center')
    h_state_bold = fields.Boolean(string='Bold', default=True)
    h_state_color= fields.Char(string='Font Color', default='#000')
    h_state_font_size = fields.Float(string='Font Size',default=15)
    h_state_m_top = fields.Float(string='From Top', default=355)
    h_state_m_left = fields.Float(string='From Left', default=5)
    
    is_h_country = fields.Boolean(string='Print Country')
    is_h_country_center = fields.Boolean('Center')
    h_country_bold = fields.Boolean(string='Bold', default=True)
    h_country_color= fields.Char(string='Font Color', default='#000')
    h_country_font_size = fields.Float(string='Font Size',default=15)
    h_country_m_top = fields.Float(string='From Top', default=355)
    h_country_m_left = fields.Float(string='From Left', default=5)
    
    #=================================================================
    
    
    
    
    
    
    
    
    
    is_work_address = fields.Boolean(string='Work Address')
    is_work_address_label = fields.Boolean(string='Work Address Label',default=True)
    work_address_label = fields.Char('Label', default='Work Address')
    work_address_lab_bold = fields.Boolean(string='Bold')
    work_address_lab_color= fields.Char(string='Font Color', default='#000')
    work_address_lab_font_size = fields.Float(string='Font Size',default=15)
    work_address_lab_m_top = fields.Float(string='From Top', default=325)
    work_address_lab_m_left = fields.Float(string='From Left', default=30)
    is_work_address_lab_center = fields.Boolean('Label Center')
    
    
    is_w_street = fields.Boolean(string='Print Street')
    is_w_street_center = fields.Boolean('Center')
    w_street_bold = fields.Boolean(string='Bold', default=True)
    w_street_color= fields.Char(string='Font Color', default='#000')
    w_street_font_size = fields.Float(string='Font Size',default=15)
    w_street_m_top = fields.Float(string='From Top', default=355)
    w_street_m_left = fields.Float(string='From Left', default=5)
    
    
    
    is_w_street2 = fields.Boolean(string='Print Street 2')
    is_w_street2_center = fields.Boolean('Center')
    w_street2_bold = fields.Boolean(string='Bold', default=True)
    w_street2_color= fields.Char(string='Font Color', default='#000')
    w_street2_font_size = fields.Float(string='Font Size',default=15)
    w_street2_m_top = fields.Float(string='From Top', default=355)
    w_street2_m_left = fields.Float(string='From Left', default=5)
    
    
    is_w_city = fields.Boolean(string='Print City / Zip')
    is_w_city_center = fields.Boolean('Center')
    w_city_bold = fields.Boolean(string='Bold', default=True)
    w_city_color= fields.Char(string='Font Color', default='#000')
    w_city_font_size = fields.Float(string='Font Size',default=15)
    w_city_m_top = fields.Float(string='From Top', default=355)
    w_city_m_left = fields.Float(string='From Left', default=5)
    
    is_w_state = fields.Boolean(string='Print State')
    is_w_state_center = fields.Boolean('Center')
    w_state_bold = fields.Boolean(string='Bold', default=True)
    w_state_color= fields.Char(string='Font Color', default='#000')
    w_state_font_size = fields.Float(string='Font Size',default=15)
    w_state_m_top = fields.Float(string='From Top', default=355)
    w_state_m_left = fields.Float(string='From Left', default=5)
    
    is_w_country = fields.Boolean(string='Print Country')
    is_w_country_center = fields.Boolean('Center')
    w_country_bold = fields.Boolean(string='Bold', default=True)
    w_country_color= fields.Char(string='Font Color', default='#000')
    w_country_font_size = fields.Float(string='Font Size',default=15)
    w_country_m_top = fields.Float(string='From Top', default=355)
    w_country_m_left = fields.Float(string='From Left', default=5)
    
    
    
    is_notes = fields.Boolean(string='Print Notes')
    is_notes_center = fields.Boolean('Center')
    notes_bold = fields.Boolean(string='Bold', default=True)
    notes_color= fields.Char(string='Font Color', default='#000')
    notes_font_size = fields.Float(string='Font Size',default=15)
    notes_m_top = fields.Float(string='From Top', default=355)
    notes_m_left = fields.Float(string='From Left', default=5)
    note = fields.Char('Notes')
    
    
    
    
    
# vim:expandtab:smartindent:tabstop=4:4softtabstop=4:shiftwidth=4:
