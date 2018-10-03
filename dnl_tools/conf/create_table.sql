#Define create table or create index SQL template
#
#Create table without tablespace example
#CREATE TABLE client_cdr$date( CONSTRAINT timecheck CHECK ( time >= '$start_time'::timestamp with time zone AND time < '$end_time'::timestamp with time zone) ) INHERITS (client_cdr)
#Create table with tablespace example
#CREATE TABLE client_cdr$date( CONSTRAINT timecheck CHECK ( time >= '$start_time'::timestamp with time zone AND time < '$end_time'::timestamp with time zone) ) INHERITS (client_cdr) TABLESPACE your_cdr_tablespace


#--------------------------------------------
#---generic variable define
# $date, current date, example: 20160704
# $start_time, today start time, example: 2016-07-04 00:00:00+00
# $end_time, tomorrow start time, example: 2016-07-05 00:00:00+00

#--------------------------------------------
#--- Define create a new table SQL
#table: client_cdr
create_tbl_sql = CREATE TABLE client_cdr$date( CONSTRAINT timecheck CHECK ( time >= '$start_time'::timestamp with time zone AND time < '$end_time'::timestamp with time zone) ) INHERITS (client_cdr)

#table: cdr_report
#create_tbl_sql = CREATE TABLE cdr_report$date( CONSTRAINT timecheck CHECK ( report_time >= '$start_time'::timestamp with time zone AND report_time < '$end_time'::timestamp with time zone) ) INHERITS (cdr_report)

#table: cdr_report_detail
create_tbl_sql = CREATE TABLE cdr_report_detail$date( CONSTRAINT timecheck CHECK ( report_time >= '$start_time'::timestamp with time zone AND report_time < '$end_time'::timestamp with time zone) ) INHERITS (cdr_report_detail)

#table: did_report
create_tbl_sql = CREATE TABLE did_report$date( CONSTRAINT timecheck CHECK ( report_time >= '$start_time'::timestamp with time zone AND report_time < '$end_time'::timestamp with time zone) ) INHERITS (did_report)

#table: us_return_code_report
#create_tbl_sql = CREATE TABLE us_return_code_report$date( CONSTRAINT timecheck CHECK ( report_time >= '$start_time'::timestamp with time zone AND report_time < '$end_time'::timestamp with time zone) ) INHERITS (us_return_code_report)

#table: us_lcr_report
#create_tbl_sql = CREATE TABLE us_lcr_report$date( CONSTRAINT timecheck CHECK ( report_time >= '$start_time'::timestamp with time zone AND report_time < '$end_time'::timestamp with time zone) ) INHERITS (us_lcr_report)

#table: us_lcr_vendor_report_sql
#create_tbl_sql = CREATE TABLE us_lcr_vendor_report$date( CONSTRAINT timecheck CHECK ( report_time >= '$start_time'::timestamp with time zone AND report_time < '$end_time'::timestamp with time zone) ) INHERITS (us_lcr_vendor_report)

#table: us_termination_vendor_report
#create_tbl_sql = CREATE TABLE us_termination_vendor_report$date( CONSTRAINT timecheck CHECK ( report_time >= '$start_time'::timestamp with time zone AND report_time < '$end_time'::timestamp with time zone) ) INHERITS (us_termination_vendor_report)

#table: us_frequent_number_report
#create_tbl_sql = CREATE TABLE us_frequent_number_report$date( CONSTRAINT timecheck CHECK ( report_time >= '$start_time'::timestamp with time zone AND report_time < '$end_time'::timestamp with time zone) ) INHERITS (us_frequent_number_report)

#table: host_based_report
create_tbl_sql = CREATE TABLE host_based_report$date( CONSTRAINT timecheck CHECK ( report_time >= '$start_time'::timestamp with time zone AND report_time < '$end_time'::timestamp with time zone) ) INHERITS (host_based_report)


#--------------------------------------------
#--- Define create a new index SQL
#table client_cdr index
create_idx_sql = CREATE INDEX class4_idx_client_cdr_egress_client_id_$date ON client_cdr$date USING btree (time,egress_client_id)
create_idx_sql = CREATE INDEX class4_idx_client_cdr_ingress_client_id_$date ON client_cdr$date USING btree (time,ingress_client_id)
create_idx_sql = CREATE INDEX class4_idx_client_cdr_egress_id_$date ON client_cdr$date USING btree (time,egress_id)
create_idx_sql = CREATE INDEX class4_idx_client_cdr_ingress_id_$date ON client_cdr$date USING btree (time,ingress_id)
create_idx_sql = CREATE INDEX class4_idx_client_cdr_time_$date ON client_cdr$date USING btree (time)
create_idx_sql = CREATE INDEX class4_idx_client_cdr_call_duration_$date ON client_cdr$date USING btree (call_duration) where call_duration>0
create_idx_sql = CREATE INDEX class4_idx_client_cdr_is_final_call_$date ON client_cdr$date USING btree (is_final_call) where is_final_call=1
create_idx_sql = CREATE INDEX client_cdr_origination_destination_number_idx_$date on client_cdr$date USING btree(origination_destination_number)
create_idx_sql = CREATE INDEX client_cdr_origination_source_number_idx_$date on client_cdr$date USING btree(origination_source_number)
create_idx_sql = CREATE INDEX client_cdr_routing_digits_idx_$date on client_cdr$date USING btree(routing_digits)

#table cdr_report index
#create_idx_sql = CREATE INDEX class4_idx_cdr_report_egress_client_id_$date ON cdr_report$date USING btree (report_time,egress_client_id)
#create_idx_sql = CREATE INDEX class4_idx_cdr_report_ingress_client_id_$date ON cdr_report$date USING btree (report_time,ingress_client_id)
#create_idx_sql = CREATE INDEX class4_idx_cdr_report_egress_id_$date ON cdr_report$date USING btree (report_time,egress_id)
#create_idx_sql = CREATE INDEX class4_idx_cdr_report_ingress_id_$date ON cdr_report$date USING btree (report_time,ingress_id)
#create_idx_sql = CREATE INDEX class4_idx_cdr_report_ingress_code_$date ON cdr_report$date USING btree (report_time,ingress_code)
#create_idx_sql = CREATE INDEX class4_idx_cdr_report_ingress_code_name_$date ON cdr_report$date USING btree (report_time,ingress_code_name)
#create_idx_sql = CREATE INDEX class4_idx_cdr_report_ingress_country_$date ON cdr_report$date USING btree (report_time,ingress_country)
#create_idx_sql = CREATE INDEX class4_idx_cdr_report_egress_code_$date ON cdr_report$date USING btree (report_time,egress_code)
#create_idx_sql = CREATE INDEX class4_idx_cdr_report_egress_code_name_$date ON cdr_report$date USING btree (report_time,egress_code_name)
#create_idx_sql = CREATE INDEX class4_idx_cdr_report_egress_country_$date ON cdr_report$date USING btree (report_time,egress_country)
#create_idx_sql = CREATE INDEX class4_idx_cdr_report_time_$date ON cdr_report$date USING btree (report_time)
#create_idx_sql = CREATE INDEX class4_idx_cdr_report_ingress_prefix_$date ON cdr_report$date USING btree (report_time,ingress_prefix)

#table cdr_report_detail index
create_idx_sql = CREATE INDEX class4_idx_cdr_report_detail_egress_client_id_$date ON cdr_report_detail$date USING btree (report_time,egress_client_id)
create_idx_sql = CREATE INDEX class4_idx_cdr_report_detail_ingress_client_id_$date ON cdr_report_detail$date USING btree (report_time,ingress_client_id)
create_idx_sql = CREATE INDEX class4_idx_cdr_report_detail_egress_id_$date ON cdr_report_detail$date USING btree (report_time,egress_id)
create_idx_sql = CREATE INDEX class4_idx_cdr_report_detail_ingress_id_$date ON cdr_report_detail$date USING btree (report_time,ingress_id)
create_idx_sql = CREATE INDEX class4_idx_cdr_report_detail_ingress_code_$date ON cdr_report_detail$date USING btree (report_time,ingress_code)
create_idx_sql = CREATE INDEX class4_idx_cdr_report_detail_ingress_code_name_$date ON cdr_report_detail$date USING btree (report_time,ingress_code_name)
create_idx_sql = CREATE INDEX class4_idx_cdr_report_detail_ingress_country_$date ON cdr_report_detail$date USING btree (report_time,ingress_country)
create_idx_sql = CREATE INDEX class4_idx_cdr_report_detail_egress_code_$date ON cdr_report_detail$date USING btree (report_time,egress_code)
create_idx_sql = CREATE INDEX class4_idx_cdr_report_detail_egress_code_name_$date ON cdr_report_detail$date USING btree (report_time,egress_code_name)
create_idx_sql = CREATE INDEX class4_idx_cdr_report_detail_egress_country_$date ON cdr_report_detail$date USING btree (report_time,egress_country)
create_idx_sql = CREATE INDEX class4_idx_cdr_report_detail_time_$date ON cdr_report_detail$date USING btree (report_time)
create_idx_sql = CREATE INDEX class4_idx_cdr_report_detail_ingress_prefix_$date ON cdr_report_detail$date USING btree (report_time,ingress_prefix)
create_idx_sql = CREATE INDEX class4_idx_cdr_report_detail_route_plan_id_$date ON cdr_report_detail$date USING btree (report_time,route_plan_id)
create_idx_sql = CREATE INDEX class4_idx_cdr_report_detail_agent_id_$date ON cdr_report_detail$date USING btree (report_time,agent_id)

#table us_return_code_report index
#create_idx_sql = CREATE INDEX class4_idx_us_return_code_report_rate_table_id_$date ON us_return_code_report$date USING btree (report_time,rate_table_id)
#create_idx_sql = CREATE INDEX class4_idx_us_return_code_report_route_plan_$date ON us_return_code_report$date USING btree (report_time,route_plan)
#create_idx_sql = CREATE INDEX class4_idx_us_return_code_report_orig_jur_type_$date ON us_return_code_report$date USING btree (report_time,orig_jur_type)
#create_idx_sql = CREATE INDEX class4_idx_us_return_code_report_ingress_rate_type_$date ON us_return_code_report$date USING btree (report_time,ingress_rate_type)
#create_idx_sql = CREATE INDEX class4_idx_us_return_code_report_npanxx_$date ON us_return_code_report$date USING btree (report_time,npanxx)
#create_idx_sql = CREATE INDEX class4_idx_us_return_code_report_ingress_dnis_type_$date ON us_return_code_report$date USING btree (report_time,ingress_dnis_type)

#table us_lcr_report index
#create_idx_sql = CREATE INDEX class4_idx_us_lcr_report_rate_table_id_$date ON us_lcr_report$date USING btree (report_time,rate_table_id)
#create_idx_sql = CREATE INDEX class4_idx_us_lcr_report_route_plan_$date ON us_lcr_report$date USING btree (report_time,route_plan)
#create_idx_sql = CREATE INDEX class4_idx_us_lcr_report_orig_jur_type_$date ON us_lcr_report$date USING btree (report_time,orig_jur_type)
#create_idx_sql = CREATE INDEX class4_idx_us_lcr_report_npanxx_$date ON us_lcr_report$date USING btree (report_time,npanxx)
#create_idx_sql = CREATE INDEX class4_idx_us_lcr_report_ingress_dnis_type_$date ON us_lcr_report$date USING btree (report_time,ingress_dnis_type)

#table us_lcr_vendor_report index
#create_idx_sql = CREATE INDEX class4_idx_us_lcr_vendor_report_rate_table_id_$date ON us_lcr_vendor_report$date USING btree (report_time,rate_table_id)
#create_idx_sql = CREATE INDEX class4_idx_us_lcr_vendor_report_route_plan_$date ON us_lcr_vendor_report$date USING btree (report_time,route_plan)
#create_idx_sql = CREATE INDEX class4_idx_us_lcr_vendor_report_orig_jur_type_$date ON us_lcr_vendor_report$date USING btree (report_time,orig_jur_type)
#create_idx_sql = CREATE INDEX class4_idx_us_lcr_vendor_report_npanxx_$date ON us_lcr_vendor_report$date USING btree (report_time,npanxx)
#create_idx_sql = CREATE INDEX class4_idx_us_lcr_vendor_report_ingress_dnis_type_$date ON us_lcr_vendor_report$date USING btree (report_time,ingress_dnis_type)

#table us_termination_vendor_report index
#create_idx_sql = CREATE INDEX class4_idx_us_term_vendor_report_rate_table_id_$date ON us_termination_vendor_report$date USING btree (report_time,rate_table_id)
#create_idx_sql = CREATE INDEX class4_idx_us_term_vendor_report_route_plan_$date ON us_termination_vendor_report$date USING btree (report_time,route_plan)
#create_idx_sql = CREATE INDEX class4_idx_us_term_vendor_report_orig_jur_type_$date ON us_termination_vendor_report$date USING btree (report_time,orig_jur_type)
#create_idx_sql = CREATE INDEX class4_idx_us_term_vendor_report_egress_id_$date ON us_termination_vendor_report$date USING btree (report_time,egress_id)
#create_idx_sql = CREATE INDEX class4_idx_us_term_vendor_report_ingress_dnis_type_$date ON us_termination_vendor_report$date USING btree (report_time,ingress_dnis_type)

#table us_frequent_number_report index
#create_idx_sql = CREATE INDEX class4_idx_us_frequent_number_report_route_plan_$date ON us_frequent_number_report$date USING btree (report_time,route_plan)
#create_idx_sql = CREATE INDEX class4_idx_us_frequent_number_report_number_code_$date ON us_frequent_number_report$date USING btree (report_time,number_code)
#create_idx_sql = CREATE INDEX class4_idx_us_frequent_number_report_number_type_$date ON us_frequent_number_report$date USING btree (report_time,number_type)
#create_idx_sql = CREATE INDEX class4_idx_us_frequent_number_report_ingress_id_$date ON us_frequent_number_report$date USING btree (report_time,ingress_id)

#table host_based_report index
create_idx_sql = CREATE INDEX class4_idx_host_based_report_time_$date ON host_based_report$date USING btree (report_time)
create_idx_sql = CREATE INDEX class4_idx_host_based_report_egress_client_id_$date ON host_based_report$date USING btree (report_time,egress_client_id)
create_idx_sql = CREATE INDEX class4_idx_host_based_report_ingress_client_id_$date ON host_based_report$date USING btree (report_time,ingress_client_id)
create_idx_sql = CREATE INDEX class4_idx_host_based_report_egress_ip_$date ON host_based_report$date USING btree (report_time,egress_ip)
create_idx_sql = CREATE INDEX class4_idx_host_based_report_ingress_ip_$date ON host_based_report$date USING btree (report_time,ingress_ip)


#--------------------------------------------
#--- Define replace trigger function, format: table_name,trigger_function_name
replace_trigger_functon_name = client_cdr,class4_trigfun_cdr_insert
#replace_trigger_functon_name = cdr_report,class4_trigfun_report_insert
replace_trigger_functon_name = cdr_report_detail,class4_trigfun_report_detail_insert
replace_trigger_functon_name = did_report,class4_trigfun_did_report_insert
#replace_trigger_functon_name = us_return_code_report,class4_trigfun_us_return_code_report_insert
#replace_trigger_functon_name = us_lcr_report,class4_trigfun_us_lcr_report_insert
#replace_trigger_functon_name = us_lcr_vendor_report,class4_trigfun_us_lcr_vendor_report_insert
#replace_trigger_functon_name = us_termination_vendor_report,class4_trigfun_us_termination_vendor_report_insert
#replace_trigger_functon_name = us_frequent_number_report,class4_trigfun_us_frequent_number_report_insert
replace_trigger_functon_name = host_based_report,class4_trigfun_host_based_report_insert


