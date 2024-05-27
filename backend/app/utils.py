def queryMammal(session, text, queryWord, offset):
    if queryWord is None or queryWord == '':
        curResult = session.execute(text("SELECT * FROM mammal LIMIT 10 OFFSET :offset"), {"offset": offset})
        columns = curResult.keys()
        results = curResult.fetchall()
        count = session.execute(text("SELECT COUNT(*) FROM mammal")).fetchone()
    else:
        sql_query_text = f"SELECT * FROM mammal WHERE lower(SciName) LIKE '%{queryWord}%' LIMIT 10 OFFSET {offset}"
        # curResult = session.execute(text("SELECT * FROM mammal WHERE lower(SciName) LIKE :name LIMIT 10 OFFSET :offset"), {"name": f"{queryWord}", "offset": offset})
        curResult = session.execute(text(sql_query_text))
        columns = curResult.keys()
        results = curResult.fetchall()
        sql_count_text = f"SELECT count(*) FROM mammal WHERE lower(SciName) LIKE '%{queryWord}%'"
        count = session.execute(text(sql_count_text)).fetchone()
        # count = session.execute(text("SELECT count(*) FROM mammal WHERE lower(SciName) LIKE :name LIMIT 10 OFFSET :offset"), {"name": f"'%{queryWord}%'", "offset": offset}).fetchone()
        # print(count, results, columns)
    return count, columns, results

def queryCountry(session, text, queryWord, offset):
    if queryWord is None or queryWord == '':
        curResult = session.execute(text("SELECT * FROM habitat LIMIT 10 OFFSET :offset"), {"offset": offset})
        columns = curResult.keys()
        results = curResult.fetchall()
        count = session.execute(text("SELECT COUNT(*) FROM habitat")).fetchone()
    else:
        raw_sql = """
            SELECT M.MammalId, SciName, GenusName, FamilyName, OrderName, Extinct, H.HabitatId, CountryName, ContinentName
            FROM 
                habitat H JOIN locate L JOIN mammal M
            ON H.HabitatId = L.HabitatId AND L.MammalId = M.MammalId
            WHERE lower(CountryName) LIKE '%{}%'
            ORDER BY L.MammalId
        """.format(queryWord)

        count_sql = f"SELECT COUNT(*) FROM ({raw_sql}) AS MAMMAL_HABITAT;"
        mammal_habitat_sql = f"{raw_sql} LIMIT 10 OFFSET {offset};"

        curResult = session.execute(text(mammal_habitat_sql))
        columns = curResult.keys()
        results = curResult.fetchall()
        count = session.execute(text(count_sql)).fetchone()
        # sql_query_text = f"SELECT * FROM habitat WHERE lower(CountryName) LIKE '%{queryWord}%'"
        # curResult = session.execute(text(sql_query_text))
        # columns = curResult.keys()
        # results = curResult.fetchall()
        # sql_count_text = f"SELECT count(*) FROM habitat WHERE lower(CountryName) LIKE '%{queryWord}%'"
        # count = session.execute(text(sql_count_text)).fetchone()
    return count, columns, results

def queryContinent(session, text, queryWord, offset):
    if queryWord is None or queryWord == '':
        curResult = session.execute(text("SELECT * FROM habitat LIMIT 10 OFFSET :offset"), {"offset": offset})
        columns = curResult.keys()
        results = curResult.fetchall()
        count = session.execute(text("SELECT COUNT(*) FROM habitat")).fetchone()
    else:
        sql_query_text = f"SELECT * FROM habitat WHERE lower(ContinentName) LIKE '%{queryWord}%' LIMIT 10 OFFSET {offset}"
        curResult = session.execute(text(sql_query_text))
        columns = curResult.keys()
        results = curResult.fetchall()
        sql_count_text = f"SELECT count(*) FROM habitat WHERE lower(ContinentName) LIKE '%{queryWord}%'"
        count = session.execute(text(sql_count_text)).fetchone()
    return count, columns, results

def queryInstitution(session, text, queryWord, offset):
    if queryWord is None or queryWord == '':
        curResult = session.execute(text("SELECT * FROM institution LIMIT 10 OFFSET :offset"), {"offset": offset})
        columns = curResult.keys()
        results = curResult.fetchall()
        count = session.execute(text("SELECT COUNT(*) FROM institution")).fetchone()
    else:
        sql_query_text = f"SELECT * FROM institution WHERE lower(InstitutionName) LIKE '%{queryWord}%' LIMIT 10 OFFSET {offset}"
        curResult = session.execute(text(sql_query_text))
        columns = curResult.keys()
        results = curResult.fetchall()
        sql_count_text = f"SELECT count(*) FROM institution WHERE lower(InstitutionName) LIKE '%{queryWord}%'"
        count = session.execute(text(sql_count_text)).fetchone()
    return count, columns, results

def queryPublication(session, text, queryWord, offset):
    if queryWord is None or queryWord == '':
        curResult = session.execute(text("SELECT * FROM publication LIMIT 10 OFFSET :offset"), {"offset": offset})
        columns = curResult.keys()
        results = curResult.fetchall()
        count = session.execute(text("SELECT COUNT(*) FROM publication")).fetchone()
    else:
        sql_query_text = f"SELECT * FROM publication WHERE lower(PublicationName) LIKE '%{queryWord}%' LIMIT 10 OFFSET {offset}"
        curResult = session.execute(text(sql_query_text))
        columns = curResult.keys()
        results = curResult.fetchall()
        sql_count_text = f"SELECT count(*) FROM publication WHERE lower(PublicationName) LIKE '%{queryWord}%'"
        count = session.execute(text(sql_count_text)).fetchone()
    return count, columns, results


def queryFavor(session, text, userId, offset):
    raw_sql = """
        SELECT M.MammalId, SciName, Extinct, GenusName, FamilyName, OrderName, FavorTime
        FROM 
            user U JOIN favor F JOIN mammal M
        ON 
            U.UserId = F.UserId AND F.MammalId = M.MammalId
        WHERE 
            U.UserId = {}
        ORDER BY F.FavorTime DESC
    """.format(userId)

    count_sql = f"SELECT COUNT(*) FROM ({raw_sql}) AS USER_FAVOR;"
    top_mammal_sql = f"{raw_sql} LIMIT 10 OFFSET {offset};"
    curResult = session.execute(text(top_mammal_sql))
    columns = curResult.keys()
    results = curResult.fetchall()
    count = session.execute(text(count_sql)).fetchone()
    return count, columns, results

def sortTopMammal(session, text, offset):
    raw_sql = """
        SELECT 
            M.OrderName,
            COUNT(M.MammalId) AS MammalCount,
            (SELECT H.ContinentName
            FROM mammal M2 
            JOIN locate L ON M2.MammalId = L.MammalId
            JOIN habitat H ON H.HabitatId = L.HabitatId 
            AND M2.OrderName = M.OrderName
                WHERE M2.OrderName IS NOT NULL AND M2.FamilyName IS NOT NULL AND M2.GenusName IS NOT NULL
            GROUP BY H.ContinentName
            ORDER BY COUNT(*) DESC
            LIMIT 1) AS MostCommonContinent
        FROM 
            mammal M
        GROUP BY 
            M.OrderName
        ORDER BY 
            MammalCount DESC
    """

    count_sql = f"SELECT COUNT(*) FROM ({raw_sql}) AS TOP_MAMMAL;"
    top_mammal_sql = f"{raw_sql} LIMIT 10 OFFSET {offset};"

    curResult = session.execute(text(top_mammal_sql))
    columns = curResult.keys()
    results = curResult.fetchall()
    count = session.execute(text(count_sql)).fetchone()
    return count, columns, results

def sortTopInstitutions(session, text, offset):
    raw_sql = """
        SELECT 
            I.InstitutionName, 
            COUNT(M.MammalId) AS ExtinctMammalsCount
        FROM 
            institution I
        JOIN 
            mammal M ON I.InstitutionId = M.InstitutionId
        JOIN 
            locate L ON M.MammalId = L.MammalId
        JOIN 
            habitat H ON L.HabitatId = H.HabitatId
        WHERE 
            M.Extinct = 1
        GROUP BY 
            I.InstitutionName, H.ContinentName
        ORDER BY 
            ExtinctMammalsCount DESC
    """

    count_sql = f"SELECT COUNT(*) FROM ({raw_sql}) AS TOP_INSTITUTION;"
    top_mammal_sql = f"{raw_sql} LIMIT 10 OFFSET {offset};"

    curResult = session.execute(text(top_mammal_sql))
    columns = curResult.keys()
    results = curResult.fetchall()
    count = session.execute(text(count_sql)).fetchone()
    return count, columns, results

def sortTopFavorited(session, text, offset):
    raw_sql = """
        SELECT 
            I.InstitutionName,
            FavMammal.SciName AS MostFavoritedMammal,
            FavMammal.FavoritesCount
        FROM 
            institution I
        JOIN (
            SELECT 
                M.InstitutionId, 
                M.SciName,
                COUNT(F.UserId) AS FavoritesCount
            FROM 
                mammal M
            JOIN 
                favor F ON M.MammalId = F.MammalId
            GROUP BY 
                M.InstitutionId, 
                M.SciName
            ) FavMammal ON I.InstitutionId = FavMammal.InstitutionId
        JOIN (
            SELECT 
                InstitutionId, 
                MAX(FavoritesCount) AS MaxFavorites
            FROM (
                SELECT 
                    M.InstitutionId, 
                    COUNT(F.UserId) AS FavoritesCount
                FROM 
                    mammal M
                JOIN 
                    favor F ON M.MammalId = F.MammalId
                GROUP BY 
                    M.InstitutionId, 
                    M.SciName
                ) AS GroupedFav
            GROUP BY 
                InstitutionId
            ) AS MaxFav ON FavMammal.InstitutionId = MaxFav.InstitutionId AND FavMammal.FavoritesCount = MaxFav.MaxFavorites
            ORDER BY FavMammal.FavoritesCount DESC, I.InstitutionName ASC
    """

    count_sql = f"SELECT COUNT(*) FROM ({raw_sql}) AS TOP_FAVORITE;"
    top_mammal_sql = f"{raw_sql} LIMIT 10 OFFSET {offset};"

    curResult = session.execute(text(top_mammal_sql))
    columns = curResult.keys()
    results = curResult.fetchall()
    count = session.execute(text(count_sql)).fetchone()
    return count, columns, results

def sortTopCited(session, text, offset):
    raw_sql = """
        SELECT 
            I.InstitutionName, 
            COUNT(DISTINCT M.MammalId) AS TotalMammals
        FROM 
            institution I
        JOIN 
            mammal M ON I.InstitutionId = M.InstitutionId
        JOIN 
            (SELECT 
                C.MammalId 
            FROM 
                publication P
            JOIN 
                cite C ON P.PublicationId = C.PublicationId
            ) AS RecentCites ON M.MammalId = RecentCites.MammalId
        GROUP BY 
            I.InstitutionName

        ORDER BY 
            TotalMammals DESC 
    """

    count_sql = f"SELECT COUNT(*) FROM ({raw_sql}) AS TOP_CITED;"
    top_mammal_sql = f"{raw_sql} LIMIT 10 OFFSET {offset};"

    curResult = session.execute(text(top_mammal_sql))
    columns = curResult.keys()
    results = curResult.fetchall()
    count = session.execute(text(count_sql)).fetchone()
    return count, columns, results