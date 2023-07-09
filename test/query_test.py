#! /usr/bin/env python3
# -*- coding: utf-8 -*-

def test_region_query(region: str,
                      sport: str = None,
                      season: str = None):
    region = region.capitalize()
    select = "SELECT region,"
    groupby = "GROUP BY region"
    where = f"WHERE region = '{region}'"
    query = f"""
    {select}
    COUNT(n_medals) as n_medals
    FROM region_view
    {where}
    {groupby}
    """
    if sport is not None:
        new_select = select + " sport,"
        new_groupby = groupby + ", sport"
        query_and = f"AND sport = '{sport}'"
        new_where = where + " " + query_and
        query = query.replace(select, new_select)
        query = query.replace(groupby, new_groupby)
        query = query.replace(where, new_where)
    return query

print(test_region_query("france"))
print(test_region_query("france", sport="Swimming"))
