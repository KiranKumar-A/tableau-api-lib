"""
Helper functions for querying REST API data for workbooks and views
"""


import pandas as pd
from tableau_api_lib.utils import extract_pages
from tableau_api_lib.exceptions.tableau_server_exceptions import ContentNotFound


def get_all_workbook_fields(conn):
    all_workbooks = extract_pages(conn.query_workbooks_for_site, parameter_dict={'fields': 'fields=_all_'})
    return all_workbooks


def get_workbooks_dataframe(conn):
    workbooks_df = pd.DataFrame(get_all_workbook_fields(conn))
    return workbooks_df


def get_all_view_fields(conn):
    all_workbooks = extract_pages(conn.query_views_for_site, parameter_dict={'fields': 'fields=_all_'})
    return all_workbooks


def get_views_dataframe(conn):
    views_df = pd.DataFrame(get_all_view_fields(conn))
    return views_df


def extract_datasource_details(df, keys):
    for key in keys:
        df['datasource_' + key] = df['datasource'].apply(lambda project: project[key])
    df.drop(columns=['datasource'], inplace=True)
    return df


def get_workbook_connections_dataframe(conn, workbook_id):
    try:
        connections_json = conn.query_workbook_connections(workbook_id).json()['connections']['connection']
        connections_df = pd.DataFrame(connections_json)
        connections_df = extract_datasource_details(connections_df, ['name'])
        return connections_df
    except KeyError:
        raise ContentNotFound('workbook', workbook_id)
