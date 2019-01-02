import requests
from datetime import datetime
from flask_restplus import Resource
from app.extensions import jwt, api
from dateutil.relativedelta import relativedelta

from ....utils.resources_mixins import UserMixin, ErrorMixin
from app.api.nris_services import NRIS_service


class MineComplianceResource(Resource, UserMixin, ErrorMixin):
    @api.doc(params={'mine_no': 'Mine ID.'})
    @jwt.requires_roles(["mds-mine-view"])
    def get(self, mine_no=None):

        try:
            data = NRIS_service.get_EMPR_data_from_NRIS(mine_no)
        except requests.exceptions.Timeout:
            return self.raise_error(408, 'NRIS is down or unresponsive.')
        except requests.exceptions.HTTPError as errhttp:
            return self.raise_error(errhttp.response.status_code,
                                    'NRIS error occurred.' + str(errhttp))

        if len(data) == 0:
            return None
        else:
            data = sorted(
                data,
                key=lambda k: datetime.strptime(k.get('assessmentDate'), '%Y-%m-%d %H:%M'),
                reverse=True)

            most_recent = data[0]

            advisories = 0
            warnings = 0
            num_open_orders = 0
            num_overdue_orders = 0
            section_35_orders = 0
            open_orders_list = []

            for report in data:
                report_date = self.get_datetime_from_NRIS_data(report.get('assessmentDate'))
                one_year_ago = datetime.now() - relativedelta(years=1)

                inspection = report.get('inspection')
                stops = inspection.get('stops')
                order_count = 1

                for stop in stops:

                    stop_orders = stop.get('stopOrders')
                    stop_advisories = stop.get('stopAdvisories')
                    stop_warnings = stop.get('stopWarnings')

                    for order in stop_orders:
                        if order.get('orderStatus') == 'Open':

                            legislation = order.get('orderLegislations')
                            permit = order.get('orderPermits')
                            section = None

                            if legislation:
                                section = legislation[0].get('section')
                            elif permit:
                                section = permit[0].get('permitSectionNumber')

                            order_to_add = {
                                'order_no': f'{report.get("assessmentId")}-{order_count}',
                                'code_viloation': section,
                                'report_no': report.get('assessmentId'),
                                'inspector': report.get('assessor'),
                                'due_date': order.get('orderCompletionDate'),
                                'overdue': False,
                            }

                            num_open_orders += 1

                            if order.get('orderCompletionDate'
                                         ) is not None and self.get_datetime_from_NRIS_data(
                                             order.get('orderCompletionDate')) < datetime.now():
                                num_overdue_orders += 1
                                order_to_add['overdue'] = True

                            open_orders_list.append(order_to_add)
                            order_count += 1

                        if order.get('orderAuthoritySection') == 'Section 35':
                            section_35_orders += 1

                    if one_year_ago < report_date:
                        advisories += len(stop_advisories)
                        warnings += len(stop_warnings)

            overview = {
                'last_inspection': most_recent.get('assessmentDate'),
                'inspector': most_recent.get('assessor'),
                'num_open_orders': num_open_orders,
                'num_overdue_orders': num_overdue_orders,
                'advisories': advisories,
                'warnings': warnings,
                'section_35_orders': section_35_orders,
                'open_orders': open_orders_list,
            }

            return overview

    @classmethod
    def get_datetime_from_NRIS_data(self, date):
        return datetime.strptime(date, '%Y-%m-%d %H:%M')
