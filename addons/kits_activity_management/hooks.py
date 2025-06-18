from odoo import api, SUPERUSER_ID

STORE_PROCEDURE = """
DROP PROCEDURE IF EXISTS public.kits_get_activity_data;
CREATE OR REPLACE PROCEDURE public.kits_get_activity_data(INOUT result JSON default null )
LANGUAGE 'plpgsql' 
AS $BODY$
DECLARE
	local_result JSON := result;
	ModelName TEXT = (local_result->>'model_name')::TEXT;
	UserId NUMERIC = (local_result->>'user_id')::NUMERIC;
	LoginUserId NUMERIC = (local_result->>'login_user_id')::NUMERIC;
	ActivityTypeId NUMERIC = (local_result->>'activity_type_id')::NUMERIC;
	RecordId NUMERIC = (local_result->>'record_id')::NUMERIC;
	ActivityState TEXT = (local_result->>'activity_state')::TEXT;
	SideFilter TEXT = (local_result->>'side_filter')::TEXT;
	UserRole TEXT = (local_result->>'user_role')::TEXT;
	Cids INT[];
	activity_data JSON;
	all_models JSON;
	all_activity_type JSON;
	done_count INT;
	today_count INT;
	planned_count INT;
	overdue_count INT;
	current_date DATE := CURRENT_DATE;
	after_date DATE := current_date + INTERVAL '7 days';

BEGIN
	Cids := ARRAY(SELECT jsonb_array_elements_text(local_result::jsonb->'cids')::INT);

	--collect all models for filter--
	select JSON_AGG(res)from(
	select 
		im.name->>'en_US' as name,
		im.model
	from ir_model im
	where is_mail_activity = true and is_mail_thread = true
	)res into all_models;

	--collect all activity types for filter--
	select JSON_AGG(res)from(
	select 
		mat.id,
		mat.name->>'en_US' as name
	from mail_activity_type mat
	)res into all_activity_type;

	--collect all activities data--
	select JSON_AGG(res)from(
	select 
		ma.id,
		mat.name->>'en_US' AS activity_type_name,
		rp.name AS user_name,
		ma.summary,
		ma.date_deadline::DATE,
		ma.kits_state as state,
		ma.res_name 
	from mail_activity ma
	left join mail_activity_type mat on mat.id = ma.activity_type_id
	left join res_users ru on ru.id = ma.user_id
	left join res_partner rp on rp.id = ru.partner_id
	WHERE (CASE WHEN SideFilter = 'my_activities' then ma.user_id = LoginUserId ELSE true END)
	AND (CASE WHEN SideFilter = 'my_activities_due_today' then ma.user_id = LoginUserId AND ma.kits_state = 'today' ELSE true END)
	AND (CASE WHEN SideFilter = 'overdue_activities' then ma.kits_state = 'overdue' ELSE true END)
	AND (CASE WHEN SideFilter = 'reschedule_activities' then ma.is_reschedule = true ELSE true END)
	AND (CASE WHEN SideFilter = 'due_seven_days' then ma.date_deadline <= after_date AND ma.date_deadline > current_date ELSE true END)
	AND (CASE WHEN UserId is not null then ma.user_id = UserId ELSE true END)
	AND (CASE WHEN ActivityTypeId is not null then ma.activity_type_id = ActivityTypeId ELSE true END)
	AND (CASE WHEN ModelName is not null then ma.res_model = ModelName ELSE true END)
	AND (CASE WHEN RecordId is not null then ma.res_id = RecordId ELSE true END)
	AND (CASE WHEN ActivityState is not null then ma.kits_state = ActivityState ELSE true END)
	AND (CASE WHEN UserRole = 'user' then ma.user_id = LoginUserId ELSE true END)
	AND (CASE WHEN UserRole = 'manager' then ma.user_id = LoginUserId or ma.manager_id = LoginUserId ELSE true END)
	AND (ma.company_id = ANY(Cids) or ma.company_id is null)
	)res into activity_data;

	--collect all activities counts--
	select COALESCE(count(id),0) from mail_activity ma
	where ma.kits_state = 'done' 
	AND (CASE WHEN SideFilter = 'my_activities' then ma.user_id = LoginUserId ELSE true END)
	AND (CASE WHEN SideFilter = 'my_activities_due_today' then ma.user_id = LoginUserId AND ma.kits_state = 'today' ELSE true END)
	AND (CASE WHEN SideFilter = 'overdue_activities' then ma.kits_state = 'overdue' ELSE true END)
	AND (CASE WHEN SideFilter = 'reschedule_activities' then ma.is_reschedule = true ELSE true END)
	AND (CASE WHEN SideFilter = 'due_seven_days' then ma.date_deadline <= after_date AND ma.date_deadline > current_date ELSE true END)
	AND (CASE WHEN UserId is not null then ma.user_id = UserId ELSE true END)
	AND (CASE WHEN ActivityTypeId is not null then ma.activity_type_id = ActivityTypeId ELSE true END)
	AND (CASE WHEN ModelName is not null then ma.res_model = ModelName ELSE true END)
	AND (CASE WHEN RecordId is not null then ma.res_id = RecordId ELSE true END)
	AND (CASE WHEN ActivityState is not null then ma.kits_state = ActivityState ELSE true END)
	AND (CASE WHEN UserRole = 'user' then ma.user_id = LoginUserId ELSE true END)
	AND (CASE WHEN UserRole = 'manager' then ma.user_id = LoginUserId or ma.manager_id = LoginUserId ELSE true END)
		AND (ma.company_id = ANY(Cids) or ma.company_id is null)
	into done_count;
	
	select COALESCE(count(id),0) from mail_activity ma
	where ma.kits_state = 'today' 
	AND (CASE WHEN SideFilter = 'my_activities' then ma.user_id = LoginUserId ELSE true END)
	AND (CASE WHEN SideFilter = 'my_activities_due_today' then ma.user_id = LoginUserId AND ma.kits_state = 'today' ELSE true END)
	AND (CASE WHEN SideFilter = 'overdue_activities' then ma.kits_state = 'overdue' ELSE true END)
	AND (CASE WHEN SideFilter = 'reschedule_activities' then ma.is_reschedule = true ELSE true END)
	AND (CASE WHEN SideFilter = 'due_seven_days' then ma.date_deadline <= after_date AND ma.date_deadline > current_date ELSE true END)
	AND (CASE WHEN UserId is not null then ma.user_id = UserId ELSE true END)
	AND (CASE WHEN ActivityTypeId is not null then ma.activity_type_id = ActivityTypeId ELSE true END)
	AND (CASE WHEN ModelName is not null then ma.res_model = ModelName ELSE true END)
	AND (CASE WHEN RecordId is not null then ma.res_id = RecordId ELSE true END)
	AND (CASE WHEN ActivityState is not null then ma.kits_state = ActivityState ELSE true END)
	AND (CASE WHEN UserRole = 'user' then ma.user_id = LoginUserId ELSE true END)
	AND (CASE WHEN UserRole = 'manager' then ma.user_id = LoginUserId or ma.manager_id = LoginUserId ELSE true END)
	AND (ma.company_id = ANY(Cids) or ma.company_id is null)
	into today_count;
	
	select COALESCE(count(id),0) from mail_activity ma
	where ma.kits_state = 'planned' 
	AND (CASE WHEN SideFilter = 'my_activities' then ma.user_id = LoginUserId ELSE true END)
	AND (CASE WHEN SideFilter = 'my_activities_due_today' then ma.user_id = LoginUserId AND ma.kits_state = 'today' ELSE true END)
	AND (CASE WHEN SideFilter = 'overdue_activities' then ma.kits_state = 'overdue' ELSE true END)
	AND (CASE WHEN SideFilter = 'reschedule_activities' then ma.is_reschedule = true ELSE true END)
	AND (CASE WHEN SideFilter = 'due_seven_days' then ma.date_deadline <= after_date AND ma.date_deadline > current_date ELSE true END)
	AND (CASE WHEN UserId is not null then ma.user_id = UserId ELSE true END)
	AND (CASE WHEN ActivityTypeId is not null then ma.activity_type_id = ActivityTypeId ELSE true END)
	AND (CASE WHEN ModelName is not null then ma.res_model = ModelName ELSE true END)
	AND (CASE WHEN RecordId is not null then ma.res_id = RecordId ELSE true END)
	AND (CASE WHEN ActivityState is not null then ma.kits_state = ActivityState ELSE true END)
	AND (CASE WHEN UserRole = 'user' then ma.user_id = LoginUserId ELSE true END)
	AND (CASE WHEN UserRole = 'manager' then ma.user_id = LoginUserId or ma.manager_id = LoginUserId ELSE true END)
	AND (ma.company_id = ANY(Cids) or ma.company_id is null)
	into planned_count;
	
	select COALESCE(count(id),0) from mail_activity ma
	where ma.kits_state = 'overdue' 
	AND (CASE WHEN SideFilter = 'my_activities' then ma.user_id = LoginUserId ELSE true END)
	AND (CASE WHEN SideFilter = 'my_activities_due_today' then ma.user_id = LoginUserId AND ma.kits_state = 'today' ELSE true END)
	AND (CASE WHEN SideFilter = 'overdue_activities' then ma.kits_state = 'overdue' ELSE true END)
	AND (CASE WHEN SideFilter = 'reschedule_activities' then ma.is_reschedule = true ELSE true END)
	AND (CASE WHEN SideFilter = 'due_seven_days' then ma.date_deadline <= after_date AND ma.date_deadline > current_date ELSE true END)
	AND (CASE WHEN UserId is not null then ma.user_id = UserId ELSE true END)
	AND (CASE WHEN ActivityTypeId is not null then ma.activity_type_id = ActivityTypeId ELSE true END)
	AND (CASE WHEN ModelName is not null then ma.res_model = ModelName ELSE true END)
	AND (CASE WHEN RecordId is not null then ma.res_id = RecordId ELSE true END)
	AND (CASE WHEN ActivityState is not null then ma.kits_state = ActivityState ELSE true END)
	AND (CASE WHEN UserRole = 'user' then ma.user_id = LoginUserId ELSE true END)
	AND (CASE WHEN UserRole = 'manager' then ma.user_id = LoginUserId or ma.manager_id = LoginUserId ELSE true END)
	AND (ma.company_id = ANY(Cids) or ma.company_id is null)
	into overdue_count;
	
	SELECT json_build_object(
		'activity_data', activity_data,
		'done_count', done_count,
		'today_count', today_count,
		'planned_count', planned_count,
		'overdue_count', overdue_count,
		'all_models', all_models,
		'all_activity_type', all_activity_type
	) INTO result;

END;
$BODY$;

DROP PROCEDURE IF EXISTS public.kits_get_company_id;
CREATE OR REPLACE PROCEDURE public.kits_get_company_id (INOUT result JSON DEFAULT NULL)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    local_result JSON := result;
    model_name TEXT := (local_result->>'model_name');
    rec_id NUMERIC := (local_result->>'rec_id')::NUMERIC;
    query_string TEXT;
    company_id NUMERIC;
BEGIN
    model_name := REPLACE(model_name, '.', '_');
    query_string := FORMAT('SELECT company_id FROM %I WHERE id = %L', model_name, rec_id);
    BEGIN
        EXECUTE query_string INTO company_id;
        result := json_build_object(
            'company_id', company_id
        );
    EXCEPTION
        WHEN OTHERS THEN
            result := json_build_object(
                'company_id', null
            );
    END;
END;
$BODY$;
"""
def kits_pre_init_hook(cr):
    cr.execute(STORE_PROCEDURE)
    
def kits_assign_current_activity_date(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    activities = env['mail.activity'].search([])
    for activity in activities:
        activity.due_datetime = activity.date_deadline
        activity.kits_state = activity.state

def kits_uninstall_hook(cr,registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    activity_reminders = env['kits.activity.reminder'].search([('automation_id','!=',False)])
    for activity_reminder in activity_reminders:
        activity_reminder.automation_id.child_ids.sudo().unlink()
        activity_reminder.automation_id.sudo().unlink()