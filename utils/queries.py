queries = {
    "fetch_series": '''
        SELECT 
            seriestype AS `SERIES TYPE`,
            series_id AS `SERIES ID`,
            series_name AS `SERIES NAME`,
            start_date AS `START DATE`,
            end_date AS `END DATE`
        FROM series;
    '''
}
