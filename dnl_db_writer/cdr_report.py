#!/usr/bin/env python3
import os
import csv
from collections import defaultdict
from io import StringIO
import argparse
import datetime
import logging
import fcntl
import sys
import time
import codecs

import psycopg2

from lib.helper import Helper


CDR_FIELDS = ('connection_type', 'session_id', 'release_cause', 'start_time_of_date', 'answer_time_of_date', 'release_tod', 'minutes_west_of_greenwich_mean_time', 'release_cause_from_protocol_stack', 'binary_value_of_release_cause_from_protocol_stack', 'first_release_dialogue', 'trunk_id_origination', 'voip_protocol_origination', 'origination_source_number', 'origination_source_host_name', 'origination_destination_number', 'origination_destination_host_name', 'origination_call_id', 'origination_remote_payload_ip_address', 'origination_remote_payload_udp_address', 'origination_local_payload_ip_address', 'origination_local_payload_udp_address', 'origination_codec_list', 'origination_ingress_packets', 'origination_egress_packets', 'origination_ingress_octets', 'origination_egress_octets', 'origination_ingress_packet_loss', 'origination_ingress_delay', 'origination_ingress_packet_jitter', 'trunk_id_termination', 'voip_protocol_termination', 'termination_source_number', 'termination_source_host_name', 'termination_destination_number', 'termination_destination_host_name', 'termination_call_id', 'termination_remote_payload_ip_address', 'termination_remote_payload_udp_address', 'termination_local_payload_ip_address', 'termination_local_payload_udp_address', 'termination_codec_list', 'termination_ingress_packets', 'termination_egress_packets', 'termination_ingress_octets', 'termination_egress_octets', 'termination_ingress_packet_loss', 'termination_ingress_delay', 'termination_ingress_packet_jitter', 'final_route_indication', 'routing_digits', 'call_duration', 'pdd', 'ring_time', 'callduration_in_ms', 'conf_id', 'call_type', 'ingress_id', 'ingress_client_id', 'ingress_client_rate_table_id', 'ingress_client_currency_id', 'ingress_client_rate', 'ingress_client_currency', 'ingress_client_bill_time', 'ingress_client_bill_result', 'ingress_client_cost', 'egress_id', 'egress_rate_table_id', 'egress_rate', 'egress_cost', 'egress_bill_time', 'egress_client_id', 'egress_client_currency_id', 'egress_client_currency', 'egress_six_seconds', 'egress_bill_minutes', 'egress_bill_result', 'ingress_bill_minutes', 'ingress_dnis_type', 'ingress_rate_type', 'lrn_number_vendor', 'lrn_dnis', 'egress_dnis_type', 'egress_rate_type', 'item_id', 'translation_ani', 'ingress_rate_id', 'egress_rate_id', 'orig_code', 'orig_code_name', 'orig_country', 'term_code', 'term_code_name', 'term_country', 'ingress_rate_effective_date', 'egress_rate_effective_date', 'egress_erro_string', 'order_id', 'order_type', 'lnp_dipping_cost', 'is_final_call', 'egress_code_asr', 'egress_code_acd', 'static_route', 'dynamic_route', 'route_plan', 'route_prefix', 'orig_delay_second', 'term_delay_second', 'orig_call_duration', 'trunk_type', 'origination_profile_port', 'termination_profile_port', 'o_trunk_type2', 'o_billing_method', 't_trunk_type2', 't_billing_method', 'campaign_id', 'tax', 'agent_id', 'agent_rate', 'agent_cost', 'orig_jur_type', 'term_jur_type', 'ring_epoch', 'end_epoch', 'paid_user', 'rpid_user', 'timeout_type','q850_cause','q850_cause_string')
CDR_REPORT_GROUPS = ('ingress_client_id', 'ingress_id', 'egress_client_id', 'egress_id', 'ingress_prefix', 'release_cause', 'binary_value_of_release_cause_from_protocol_stack', 'release_cause_from_protocol_stack', 'report_time')
CDR_REPORT_ORIG_GROUPS = ('ingress_client_id', 'ingress_id', 'egress_client_id', 'egress_id', 'route_prefix', 'release_cause', 'binary_value_of_release_cause_from_protocol_stack', 'release_cause_from_protocol_stack', 'start_time_of_date')
#CDR_REPORT_DETAIL_GROUPS = ('ingress_client_id', 'ingress_id', 'ingress_country', 'ingress_code_name', 'ingress_code', 'egress_client_id', 'egress_id', 'egress_country', 'egress_code_name', 'egress_code', 'ingress_prefix', 'ingress_rate', 'egress_rate', 'ingress_rate_date', 'egress_rate_date',  'ingress_rate_table_id', 'route_plan_id', 'orig_jur_type', 'term_jur_type', 'origination_destination_host_name', 'termination_source_host_name', 'binary_value_of_release_cause_from_protocol_stack', 'release_cause', 'release_cause_from_protocol_stack', 'report_time')
#CDR_REPORT_DETAIL_ORIG_GROUPS = ('ingress_client_id', 'ingress_id', 'orig_country', 'orig_code_name', 'orig_code', 'egress_client_id', 'egress_id', 'term_country', 'term_code_name', 'term_code', 'route_prefix', 'ingress_client_rate', 'egress_rate', 'ingress_rate_effective_date', 'egress_rate_effective_date', 'ingress_client_rate_table_id', 'route_plan', 'orig_jur_type', 'term_jur_type', 'origination_destination_host_name', 'termination_source_host_name', 'binary_value_of_release_cause_from_protocol_stack', 'release_cause', 'release_cause_from_protocol_stack', 'start_time_of_date')
CDR_REPORT_DETAIL_GROUPS = ('ingress_client_id', 'ingress_id', 'ingress_country', 'ingress_code_name', 'egress_client_id', 'egress_id', 'egress_country', 'egress_code_name', 'ingress_prefix','ingress_rate_date', 'egress_rate_date',  'ingress_rate_table_id', 'route_plan_id', 'orig_jur_type', 'term_jur_type', 'origination_destination_host_name', 'termination_source_host_name', 'binary_value_of_release_cause_from_protocol_stack', 'release_cause', 'release_cause_from_protocol_stack', 'report_time')
CDR_REPORT_DETAIL_ORIG_GROUPS = ('ingress_client_id', 'ingress_id', 'orig_country', 'orig_code_name', 'egress_client_id', 'egress_id', 'term_country', 'term_code_name', 'route_prefix', 'ingress_rate_effective_date', 'egress_rate_effective_date', 'ingress_client_rate_table_id', 'route_plan', 'orig_jur_type', 'term_jur_type', 'origination_destination_host_name', 'termination_source_host_name', 'binary_value_of_release_cause_from_protocol_stack', 'release_cause', 'release_cause_from_protocol_stack', 'start_time_of_date')
CDR_REPORT_FIELDS = ("agent_cost","ingress_total_calls","egress_total_calls","not_zero_calls","ingress_success_calls","ingress_busy_calls","lrn_calls","ingress_cancel_calls","egress_success_calls","egress_busy_calls","egress_cancel_calls","duration","ingress_bill_time","ingress_bill_time_intra","ingress_bill_time_inter","ingress_call_cost","ingress_call_cost_intra","ingress_call_cost_inter","lnp_cost","pdd","egress_bill_time","egress_bill_time_intra","egress_bill_time_inter","egress_call_cost","egress_call_cost_intra","egress_call_cost_inter", 'incoming_bandwidth','outgoing_bandwidth','q850_cause_count','npr_count')
CDR_REPORT_DETAIL_FIELDS = ("agent_cost","ingress_total_calls","egress_total_calls","not_zero_calls","ingress_success_calls","ingress_busy_calls","lrn_calls","ingress_cancel_calls","egress_success_calls","egress_busy_calls","egress_cancel_calls","duration","ingress_bill_time","ingress_bill_time_intra","ingress_bill_time_inter","ingress_call_cost","ingress_call_cost_intra","ingress_call_cost_inter","lnp_cost","pdd","egress_bill_time","egress_bill_time_intra","egress_bill_time_inter","egress_call_cost","egress_call_cost_intra","egress_call_cost_inter","duration_6","not_zero_calls_6","duration_30","not_zero_calls_30","call_12s","call_18s","call_24s","call_2h","call_3h","call_4h",'incoming_bandwidth','outgoing_bandwidth','inter_ingress_total_calls','intra_ingress_total_calls','inter_duration','intra_duration','inter_not_zero_calls','intra_not_zero_calls','q850_cause_count','npr_count')
TYPE_CAST_TO_FLOAT = ('agent_cost', 'ingress_client_cost', 'lnp_dipping_cost', 'egress_cost','egress_rate')
TYPE_CAST_TO_INT = ("ingress_client_bill_time", 'lrn_number_vendor', 'egress_bill_time', 'call_duration', 'origination_ingress_packets', 'termination_ingress_packets', 'origination_egress_packets', 'termination_egress_packets', 'pdd', 'ingress_client_id', 'ingress_id', 'egress_client_id', 'egress_id', 'is_final_call','ingress_rate_type','egress_rate_type','ingress_dnis_type','orig_jur_type')


HOST_BASED_REPORT_GROUPS = ('ingress_client_id','egress_client_id','ingress_ip','egress_ip','report_time')
HOST_BASED_REPORT_ORIG_GROUPS = ('ingress_client_id','egress_client_id','origination_source_host_name','termination_destination_host_name','start_time_of_date')
HOST_BASED_REPORT_FIELDS = ('duration','ingress_bill_time','ingress_call_cost','ingress_total_calls','not_zero_calls','ingress_success_calls','ingress_busy_calls','pdd','ingress_cancel_calls','egress_bill_time','egress_call_cost','egress_total_calls','egress_success_calls','egress_busy_calls','egress_cancel_calls','ingress_avg_rate','egress_avg_rate')

class CDRHandler():
    def __init__(self, start_time, end_time, is_dup_data):
        self.config_options = Helper.get_configurations(os.path.join(os.path.dirname(__file__), os.path.pardir, 'dnl_softswitch', 'conf', 'dnl_softswitch.conf'))
        self.connect_database()
        self.start_time = start_time if start_time is not None else self.get_start_time(end_time)
        self.end_time = end_time
        self.is_dup_data = is_dup_data
        self.total_start_time = start_time
        options = self.get_options()
        try:
            self.billing_path = options.get('switch_cdr', 'cdr_directory')
        except Exception:
            self.billing_path = None

        if not self.billing_path:
            self.billing_path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'dnl_softswitch', 'cdr')

        if not os.path.exists(self.billing_path):
            os.makedirs(self.billing_path)

    def connect_database(self):
        self.conn = psycopg2.connect(host=self.config_options.get('db', 'db_host'),
                                     port=self.config_options.get('db', 'db_listen_port'),
                                     database=self.config_options.get('db', 'db_name'),
                                     password=self.config_options.get('db', 'db_user_password'),
                                     user=self.config_options.get('db', 'db_user'))
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def close_database(self):
        self.cursor.close()
        self.conn.close()

    def get_start_time(self, end_time):
        self.cursor.execute("SELECT (max(report_time)+interval '1 hour')::timestamp without time zone as last_report_time from cdr_report")
        max_report_time = self.cursor.fetchone()[0]
        if max_report_time:
            return max_report_time
        else:
            return end_time

    #
    # def get_billing_path(self):
    #     billing_cdr_options = Helper.get_configurations(os.path.join(os.path.dirname(__file__), 'conf', 'billing_cdr.conf'))
    #     billing_api_options = Helper.get_configurations(os.path.join(os.path.dirname(__file__), 'conf', 'billing_switch_api.conf'))
    #
    #
    #     biling_path = "{}/{}/{}".format(billing_cdr_options['root']['hd_cdr_dir'],
    #                                          billing_api_options['root']['listen_ip'], billing_api_options['root']['listen_port'])
    #     return biling_path

    def get_options(self):
        ini_path= os.path.join(os.path.dirname(__file__), os.path.pardir, 'dnl_softswitch', 'conf', 'dnl_softswitch.conf')
        options = Helper.get_configurations(ini_path)
        return options


    def run(self):
        logger.info("Start Time: {}, End Time: {}".format(self.start_time, self.end_time))
        while self.start_time <= self.end_time:
            self.process(self.start_time)
            self.start_time = self.start_time + datetime.timedelta(hours=1)

        self.close_database()

    def process(self, start_time):
        walk_path = "{}/{}".format(self.billing_path, start_time.strftime("%Y/%m/%d/%H"))
        logger.info("Begin to walk path: [{}]".format(walk_path))
        if not os.path.exists(walk_path):
            logger.warning("The path [{}] does not exist!".format(walk_path))
            return
        # print(walk_path)

        cdr_report = defaultdict(lambda : dict.fromkeys(CDR_REPORT_FIELDS, 0))
        cdr_report_detail = defaultdict(lambda : dict.fromkeys(CDR_REPORT_DETAIL_FIELDS, 0))
        host_based_report = defaultdict(lambda : dict.fromkeys(HOST_BASED_REPORT_FIELDS, 0))

        for root, dirs, files in os.walk(walk_path):
            for name in files:
                cdr_pathname = os.path.join(root, name)


                with codecs.open(cdr_pathname, "r",encoding='latin1') as handle:
                    reader = csv.DictReader(handle, delimiter='?', fieldnames=CDR_FIELDS)
                    i = 0
                    for line in reader:
                        i += 1
                        # if len(line) != 129:
                        #     logger.error("Invalid number of columns at line {0:d} in file [{1}, actual length: {2}]".format(i, cdr_pathname, len(line)))
                        #     continue

                        for convert_to_int_key in TYPE_CAST_TO_INT:
                            try:
                                line[convert_to_int_key] = int(line[convert_to_int_key])
                            except (TypeError,ValueError):
                                line[convert_to_int_key] = 'NULL'

                        for convert_to_float_key in TYPE_CAST_TO_FLOAT:
                            try:
                                line[convert_to_float_key] = float(line[convert_to_float_key])
                            except (TypeError,ValueError):
                                line[convert_to_int_key] = 'NULL'

                        try:
                            line['start_time_of_date'] = datetime.datetime.fromtimestamp(int(line['start_time_of_date'][:-6])).strftime("%Y-%m-%d %H:00:00+00")
                        except (TypeError, ValueError):
                            logger.error("Parse start time error at line {0:d} in file [{1}]".format(i, cdr_pathname))
                            continue

                        if self.is_dup_data and datetime.datetime.strptime(line['start_time_of_date'],"%Y-%m-%d %H:00:00+00") >= start_time:
                            # logger.info("Parse start time {}".format(line['start_time_of_date']))
                            continue


                        # 排除长话单的cdr
                        # if line['first_release_dialogue'] == 'M' or line['first_release_dialogue'] == 'N':
                        #     if line['call_duration'] > 1800:
                        #         continue



                        cdr_report_key = ';'.join(str(line[k]) if line[k] is not None else 'NULL' for k in CDR_REPORT_ORIG_GROUPS)
                        cdr_report_detail_key = ';'.join(str(line[k]) if line[k] is not None else 'NULL' for k in CDR_REPORT_DETAIL_ORIG_GROUPS)
                        
                        host_based_report_key = ';'.join(str(line[k]) if line[k] is not None else 'NULL' for k in HOST_BASED_REPORT_ORIG_GROUPS)

                        if line['is_final_call'] == 1:
                            cdr_report[cdr_report_key]['agent_cost'] += line['agent_cost']
                            cdr_report[cdr_report_key]['ingress_bill_time'] += line['ingress_client_bill_time']
                            cdr_report[cdr_report_key]['ingress_call_cost'] += line['ingress_client_cost']
                            cdr_report[cdr_report_key]['lnp_cost'] += line['lnp_dipping_cost']
                            cdr_report[cdr_report_key]['ingress_total_calls'] += 1



                            cdr_report_detail[cdr_report_detail_key]['agent_cost'] += line['agent_cost']
                            cdr_report_detail[cdr_report_detail_key]['ingress_bill_time'] += line['ingress_client_bill_time']
                            cdr_report_detail[cdr_report_detail_key]['ingress_call_cost'] += line['ingress_client_cost']
                            cdr_report_detail[cdr_report_detail_key]['lnp_cost'] += line['lnp_dipping_cost']
                            cdr_report_detail[cdr_report_detail_key]['ingress_total_calls'] += 1
                            
                            host_based_report[host_based_report_key]['ingress_bill_time'] += line['ingress_client_bill_time']
                            host_based_report[host_based_report_key]['ingress_call_cost'] += line['ingress_client_cost']
                            host_based_report[host_based_report_key]['ingress_total_calls'] += 1
                            
                            line['ingress_client_rate'] = float(line['ingress_client_rate'])
                            
                            host_based_report[host_based_report_key]['ingress_avg_rate'] = round((host_based_report[host_based_report_key]['ingress_avg_rate']+line['ingress_client_rate'])/2,6)
                            

                            if line['ingress_rate_type'] == 2:
                                cdr_report[cdr_report_key]['ingress_call_cost_intra'] += line['ingress_client_cost']
                                cdr_report[cdr_report_key]['ingress_bill_time_intra'] += line['ingress_client_bill_time']
                                cdr_report_detail[cdr_report_detail_key]['ingress_call_cost_intra'] += line['ingress_client_cost']
                                cdr_report_detail[cdr_report_detail_key]['ingress_bill_time_intra'] += line['ingress_client_bill_time']
                                cdr_report_detail[cdr_report_detail_key]['intra_ingress_total_calls'] += 1
                            elif line['ingress_rate_type'] == 1:
                                cdr_report[cdr_report_key]['ingress_call_cost_inter'] += line['ingress_client_cost']
                                cdr_report[cdr_report_key]['ingress_bill_time_inter'] += line['ingress_client_bill_time']
                                cdr_report_detail[cdr_report_detail_key]['ingress_call_cost_inter'] += line['ingress_client_cost']
                                cdr_report_detail[cdr_report_detail_key]['ingress_bill_time_inter'] += line['ingress_client_bill_time']
                                cdr_report_detail[cdr_report_detail_key]['inter_ingress_total_calls'] += 1

                            if line['egress_id']:
                                cdr_report[cdr_report_key]['ingress_success_calls'] += 1
                                cdr_report_detail[cdr_report_detail_key]['ingress_success_calls'] += 1
                                host_based_report[host_based_report_key]['ingress_success_calls'] += 1

                            if '486' in line['binary_value_of_release_cause_from_protocol_stack']:
                                cdr_report[cdr_report_key]['ingress_busy_calls'] += 1
                                cdr_report_detail[cdr_report_detail_key]['ingress_busy_calls'] += 1
                                host_based_report[host_based_report_key]['ingress_busy_calls'] += 1


                            if '487' in line['binary_value_of_release_cause_from_protocol_stack']:
                                cdr_report[cdr_report_key]['ingress_cancel_calls'] += 1
                                cdr_report_detail[cdr_report_detail_key]['ingress_cancel_calls'] += 1
                                host_based_report[host_based_report_key]['ingress_cancel_calls'] += 1


                            if line['lrn_number_vendor'] != 0:
                                cdr_report[cdr_report_key]['lrn_calls'] += 1
                                cdr_report_detail[cdr_report_detail_key]['lrn_calls'] += 1

                            if line['egress_erro_string'].strip() != '':
                                egress_trunk_trace_list = line['egress_erro_string'].split('|')
                                egress_trunk_trace = egress_trunk_trace_list[0]
                                egress_trunk_trace_info = egress_trunk_trace.split(';')
                                del egress_trunk_trace_info[0]
                                over_flow_flg = 1
                                for index,egress_trunk_trace_item in enumerate(egress_trunk_trace_info):
                                    egress_trunk_trace_item_list = egress_trunk_trace_item.split(':')
                                    if len(egress_trunk_trace_item_list) != 2:
                                        continue
                                    egress_id = egress_trunk_trace_item_list[0]
                                    if egress_trunk_trace_item_list[1].strip() == '':
                                        continue
                                    egress_trunk_trace_item_result = int(egress_trunk_trace_item_list[1])
                                    if egress_trunk_trace_item_result != 21:
                                        over_flow_flg = 0

                                if over_flow_flg == 1:
                                    cdr_report[cdr_report_key]['npr_count'] += 1
                                    cdr_report_detail[cdr_report_detail_key]['npr_count'] += 1





                        cdr_report[cdr_report_key]['egress_bill_time'] += line['egress_bill_time']
                        cdr_report[cdr_report_key]['egress_call_cost'] += line['egress_cost']
                        cdr_report[cdr_report_key]['egress_total_calls'] += 1


                        cdr_report_detail[cdr_report_detail_key]['egress_bill_time'] += line['egress_bill_time']
                        cdr_report_detail[cdr_report_detail_key]['egress_call_cost'] += line['egress_cost']
                        cdr_report_detail[cdr_report_detail_key]['egress_total_calls'] += 1
                        
                        
                        host_based_report[host_based_report_key]['egress_bill_time'] += line['egress_bill_time']
                        host_based_report[host_based_report_key]['egress_call_cost'] += line['egress_cost']
                        host_based_report[host_based_report_key]['egress_total_calls'] += 1
                        line['egress_rate'] = float(line['egress_rate'])
                        host_based_report[host_based_report_key]['egress_avg_rate'] = round((host_based_report[host_based_report_key]['egress_avg_rate']+line['egress_rate'])/2,6)
                        

                        if line['egress_rate_type'] == 2:
                            cdr_report[cdr_report_key]['egress_call_cost_intra'] += line['egress_cost']
                            cdr_report[cdr_report_key]['egress_bill_time_intra'] += line['egress_bill_time']
                            cdr_report_detail[cdr_report_detail_key]['egress_call_cost_intra'] += line['egress_cost']
                            cdr_report_detail[cdr_report_detail_key]['egress_bill_time_intra'] += line['egress_bill_time']
                        elif line['egress_rate_type'] == 1:
                            cdr_report[cdr_report_key]['egress_call_cost_inter'] += line['egress_cost']
                            cdr_report[cdr_report_key]['egress_bill_time_inter'] += line['egress_bill_time']
                            cdr_report_detail[cdr_report_detail_key]['egress_call_cost_inter'] += line['egress_cost']
                            cdr_report_detail[cdr_report_detail_key]['egress_bill_time_inter'] += line['egress_bill_time']

                        if line['egress_id']:
                            cdr_report[cdr_report_key]['egress_success_calls'] += 1
                            cdr_report_detail[cdr_report_detail_key]['egress_success_calls'] += 1
                            host_based_report[host_based_report_key]['egress_success_calls'] += 1

                        if '486' in line['release_cause_from_protocol_stack']:
                            cdr_report[cdr_report_key]['egress_busy_calls'] += 1
                            cdr_report_detail[cdr_report_detail_key]['egress_busy_calls'] += 1
                            host_based_report[host_based_report_key]['egress_busy_calls'] += 1

                        if '487' in line['release_cause_from_protocol_stack']:
                            cdr_report[cdr_report_key]['egress_cancel_calls'] += 1
                            cdr_report_detail[cdr_report_detail_key]['egress_cancel_calls'] += 1
                            host_based_report[host_based_report_key]['egress_cancel_calls'] += 1

                        cdr_report[cdr_report_key]['duration'] += line['call_duration']
                        cdr_report_detail[cdr_report_detail_key]['duration'] += line['call_duration']
                        host_based_report[host_based_report_key]['duration'] += line['call_duration']
                        
                        if line['ingress_rate_type'] == 2:
                        	cdr_report_detail[cdr_report_detail_key]['intra_duration'] += line['call_duration']
                        elif line['ingress_rate_type'] == 1:
                        	cdr_report_detail[cdr_report_detail_key]['inter_duration'] += line['call_duration']
                        	                        	
                        if line['call_duration'] > 0:
                            cdr_report[cdr_report_key]['not_zero_calls'] += 1
                            cdr_report[cdr_report_key]['pdd'] += line['pdd']
                            cdr_report[cdr_report_key]['incoming_bandwidth'] += line['origination_ingress_packets']
                            cdr_report[cdr_report_key]['incoming_bandwidth'] += line['termination_ingress_packets']
                            cdr_report[cdr_report_key]['outgoing_bandwidth'] += line['origination_egress_packets']
                            cdr_report[cdr_report_key]['outgoing_bandwidth'] += line['termination_egress_packets']

                            cdr_report_detail[cdr_report_detail_key]['not_zero_calls'] += 1
                            cdr_report_detail[cdr_report_detail_key]['pdd'] += line['pdd']
                            cdr_report_detail[cdr_report_detail_key]['incoming_bandwidth'] += line['origination_ingress_packets']
                            cdr_report_detail[cdr_report_detail_key]['incoming_bandwidth'] += line['termination_ingress_packets']
                            cdr_report_detail[cdr_report_detail_key]['outgoing_bandwidth'] += line['origination_egress_packets']
                            cdr_report_detail[cdr_report_detail_key]['outgoing_bandwidth'] += line['termination_egress_packets']
                            
                            host_based_report[host_based_report_key]['not_zero_calls'] += 1
                            host_based_report[host_based_report_key]['pdd'] += line['pdd']
                            
                            if line['ingress_rate_type'] == 2:
                            	cdr_report_detail[cdr_report_detail_key]['intra_not_zero_calls'] += 1
                            elif line['ingress_rate_type'] == 1:
                            	cdr_report_detail[cdr_report_detail_key]['inter_not_zero_calls'] += 1

                            if line['call_duration'] < 6:
                                cdr_report_detail[cdr_report_detail_key]['duration_6'] += line['call_duration']
                                cdr_report_detail[cdr_report_detail_key]['not_zero_calls_6'] += 1
                            elif line['call_duration'] < 12:
                                cdr_report_detail[cdr_report_detail_key]['call_12s'] += 1
                            elif line['call_duration'] < 18:
                                cdr_report_detail[cdr_report_detail_key]['call_18s'] += 1
                            elif line['call_duration'] < 24:
                                cdr_report_detail[cdr_report_detail_key]['call_24s'] += 1
                            elif line['call_duration'] < 30:
                                cdr_report_detail[cdr_report_detail_key]['duration_30'] += line['call_duration']
                                cdr_report_detail[cdr_report_detail_key]['not_zero_calls_30'] += 1
                            elif line['call_duration'] < 7200:
                                cdr_report_detail[cdr_report_detail_key]['call_2h'] += 1
                            elif line['call_duration'] < 10800:
                                cdr_report_detail[cdr_report_detail_key]['call_3h'] += 1
                            elif line['call_duration'] < 14400:
                                cdr_report_detail[cdr_report_detail_key]['call_4h'] += 1

                        if line['q850_cause'] == '16' or line['q850_cause'] == '17' or line['q850_cause'] == '18' or line['q850_cause'] == '19' or line['q850_cause'] == '21':
                            cdr_report[cdr_report_key]['q850_cause_count'] += 1
                            cdr_report_detail[cdr_report_detail_key]['q850_cause_count'] += 1
                #
                #     logger.info('this file line is %s  t is %s is_final_call is %s' % (i,t,is_final_call))
                # total_is_final_call += is_final_call
                # total_i += i
                # total_t += t
            # logger.warning('this file line is %s  t is %s total_is_final_call is %s' % (total_i,total_t,total_is_final_call))


        f = StringIO()
        cdr_report_keys = None
        for cdr_report_key, cdr_report_item in cdr_report.items():
            if cdr_report_keys is None:
                cdr_report_keys = list(cdr_report_item.keys())
            row = list(cdr_report_item.values())
            row.append(cdr_report_key)
            #row.append(str_time)
            line = ';'.join(( str(item) for item in row))
            #print(line)
            f.write("{}\n".format(line))
        if cdr_report_keys is None:
            logger.warning("Cdr Report It seems the file is empty!")
        else:
            cdr_report_keys.extend(CDR_REPORT_GROUPS)
            #cdr_report_keys.append("report_time")
            f.seek(0)
            # print("column:", cdr_report_keys)
            self.cursor.copy_from(f, 'cdr_report', columns=cdr_report_keys, sep=';', null="NULL")

            logger.info("The cdr report file [{}] is imported successfully!".format(walk_path))


        cdr_report_detail_keys = None

        cdr_report_detail_len = len(list(cdr_report_detail.items()))
        line_count = 1
        finish_line = 0
        extend_flg = 0
        for cdr_report_detail_key, cdr_report_detail_item in cdr_report_detail.items():
            if line_count == 1:
                f = StringIO()
            # print ('cdr_report_detail_item is %s ' % cdr_report_detail_item)
            if cdr_report_detail_keys is None:
                cdr_report_detail_keys = list(cdr_report_detail_item.keys())
            row = list(cdr_report_detail_item.values())
            row.append(cdr_report_detail_key)
            #row.append(str_time)
            line = ';'.join((str(item) for item in row))
            f.write("{}\n".format(line))
            if line_count == 5000:
                finish_line += 5000
                if extend_flg == 0:
                    cdr_report_detail_keys.extend(CDR_REPORT_DETAIL_GROUPS)
                    extend_flg = 1
                f.seek(0)
                self.cursor.copy_from(f, 'cdr_report_detail', columns=cdr_report_detail_keys, sep=';', null='NULL')
                # logger.info("The cdr report detail file [{}] is imported {}/{}".format(walk_path,finish_line,cdr_report_detail_len))
                line_count = 1
            else:
                line_count += 1

        if cdr_report_detail_keys is None:
            logger.warning("Cdr Report Detail It seems the file is empty!")
        else:
            if extend_flg == 0:
                cdr_report_detail_keys.extend(CDR_REPORT_DETAIL_GROUPS)
            #cdr_report_detail_keys.append("report_time")
            f.seek(0)
            self.cursor.copy_from(f, 'cdr_report_detail', columns=cdr_report_detail_keys, sep=';', null='NULL')
            logger.info("The cdr report detail file [{}] is imported(count ({})) successfully!".format(walk_path,cdr_report_detail_len))



        f = StringIO()
        host_based_report_keys = None
        for host_based_report_key, host_based_report_item in host_based_report.items():
            #print ('host_based_report_item is %s ' % host_based_report_item)
            if host_based_report_keys is None:
                host_based_report_keys = list(host_based_report_item.keys())
            row = list(host_based_report_item.values())
            row.append(host_based_report_key)
            #row.append(str_time)
            line = ';'.join((str(item) for item in row))
            f.write("{}\n".format(line))
        if host_based_report_keys is None:
            logger.warning("Host Based Report It seems the file is empty!")
        else:
            host_based_report_keys.extend(HOST_BASED_REPORT_GROUPS)
            #cdr_report_detail_keys.append("report_time")
            f.seek(0)
            #print (host_based_report_keys)
            #self.cursor.copy_from(f, 'host_based_report', columns=host_based_report_keys, sep=';', null='NULL')
            #logger.info("The host based report file [{}] is imported successfully!".format(walk_path))


if __name__ == "__main__":
        logger = Helper.create_logger('cdr_report')
        parser = argparse.ArgumentParser(description="CDR Report")
        parser.add_argument("-r", '--run', action='store', dest='run_type', help='Run type', choices={'auto', 'manual','dup_data'}, default='auto')
        parser.add_argument("-s", "--start", action="store", dest='start_time', help="Start time")
        parser.add_argument("-e", "--end", action="store", dest='end_time', help="End time")
        args = parser.parse_args()

        if args.run_type == 'auto':
            logger.info("Begin to perform automatically")
            start_time = datetime.datetime.now() - datetime.timedelta(hours=1)
            end_time = datetime.datetime.now() - datetime.timedelta(hours=1)
            lock_file = os.path.join(os.path.dirname(__file__), 'cdr_report.lock')
            handle = open(lock_file, "wb")
            while(1):
                try:
                    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except IOError:
                    logger.error("Another instance is running...")
                    # sys.exit(-1)
                    time.sleep(30)
                    continue
                else:
                    break


            cdr_handler = CDRHandler(start_time, end_time,0)
            cdr_handler.run()

            handle.close()
        elif args.run_type == 'manual':
            logger.info("Begin to perform manually")
            start_time = datetime.datetime.strptime(args.start_time, "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(args.end_time, "%Y-%m-%d %H:%M:%S")
            cdr_handler = CDRHandler(start_time, end_time,0)
            cdr_handler.run()

        else:
            logger.info("Begin to perform duplicate data(when start time is last hour and end time is this hour)")
            start_time = datetime.datetime.strptime(args.start_time, "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(args.end_time, "%Y-%m-%d %H:%M:%S")
            cdr_handler = CDRHandler(start_time, end_time,1)
            cdr_handler.run()
