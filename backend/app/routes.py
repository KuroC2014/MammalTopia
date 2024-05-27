from app import app, db
from app.models import Cite, Favor, Habitat, Institution, Locate, Mammal, Publication, User
from flask import request, jsonify

from flask import render_template
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from datetime import datetime

from app.utils import queryMammal, queryCountry, queryContinent, queryInstitution, queryPublication, \
    queryFavor, sortTopMammal, sortTopInstitutions, sortTopFavorited, sortTopCited

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/logout')
def logout():
    Session.pop('username', None) 
    return jsonify({'message': 'You are now logged out'}), 200

@app.route('/search_results')
def search_results():
    return "Search Results Page"

# @app.route('/test_db')
# def test_db():
#     try:
#         with Session(db.engine) as session:
#             result = session.execute(text('SELECT 1'))
#             return jsonify({'message': 'Database connected successfully.'})
#     except Exception as e:
#         return jsonify({'error': str(e)})


# POST API
# request body: {username: xxx, password: xxx, email: xxx}
# respons: error if fails
#
# example: POST 127.0.0.1:5000/register 
#          body: {"username":"xxx", "password":"123456", "email":"xxx@abc.com"}
@app.route('/register', methods=['POST'])
def register():
    data = request.json

    if 'username' not in data or 'password' not in data or 'email' not in data:
        return jsonify({'error': 'Missing username and password, or email field'}), 400
    
    username = data['username']
    password = data['password']
    email = data['email']

    result = db.session.execute(text("SELECT * FROM user WHERE UserName=:username"), {"username":username})
    if result.rowcount:
        return jsonify({'error': 'Username already exists'}), 409

    result = db.session.execute(text("SELECT * FROM user WHERE Email = :email"), {"email": email}) 
    if result.rowcount:
        return jsonify({'error': 'Email already registered'}), 409

    db.session.execute(text("INSERT INTO user (UserName, Password, Email) VALUES ( :username, :password, :email)"), {"username": username, "password": password, "email": email})
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


# GET API
# request parameter: username and password
# respons: error if fails
#
# example: GET 127.0.0.1:5000/login?username=xxx&password=123456
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username or password missing in the query parameters'}), 400
    
    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({'error': 'Username or password missing in the query parameters'}), 400

    result = db.session.execute(text("SELECT * FROM user WHERE UserName= :username AND Password= :password"), {"username": username, "password": password})

    if not result.rowcount:
        return jsonify({'error': 'Wrong username or password'}), 400

    users = []
    for user in result:
        users.append(user)
    if result:
        return jsonify({
            'message': 'Login successful', 
            'userId': users[0].UserId, 
            'username': users[0].UserName,
            'email': users[0].Email,
        }), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401
    

# POST API
# request body: {username: xxx, current_password: xxx, new_password: xxx}
# response: 
#
# example: POST 127.0.0.1:5000/change_password
#          body: {"username": "example", "current_password": "oldpassword", "new_password": "newpassword"}
# @app.route('/change_password', methods=['POST'])
# def change_password():
#     data = request.json
#     if 'username' not in data or 'current_password' not in data or 'new_password' not in data:
#         return jsonify({'error': 'Missing required fields'}), 400
    
#     username = data['username']
#     current_password = data['current_password']
#     new_password = data['new_password']

#     result = db.session.execute(text("SELECT * FROM user WHERE UserName= :username AND Password= :password"), {"username": username, "password": current_password})
#     if not result.rowcount:
#         return jsonify({'error': 'Wrong username or password'}), 400
    
#     if current_password == new_password:
#         return jsonify({'error': 'new password and current password can not be the same'}), 400
    
#     # Update the password
#     db.session.execute(text("UPDATE user SET Password=:password WHERE UserName=:username"),
#                        {"username": username, "password": new_password})
#     db.session.commit()

#     return jsonify({'message': 'password changed successfully'}), 200
@app.route('/change_password', methods=['POST'])
def change_password():
    data = request.json
    if 'userId' not in data or 'current_password' not in data or 'new_password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    userId = data['userId']
    old_password = data['current_password']
    new_password = data['new_password']

    if old_password == new_password:
        return jsonify({'error': 'New password and current password cannot be the same'}), 400

    try:
        user = db.session.execute(text("SELECT UserId FROM user WHERE userId = :userId"), {"userId": userId}).fetchone()
        if user is None:
            return jsonify({'error': 'User not found'}), 404

        db.session.execute(text("CALL UpdateUserPassword(:user_id, :old_pass, :new_pass)"), 
                                    {'user_id': user[0], 'old_pass': old_password, 'new_pass': new_password})
        db.session.commit()
        return jsonify({'message': 'Password updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# POST API
# request body: {username: xxx, password: xxx}
# response: {'message': 'Account removed successfully'} or {'error': 'User not found'}
#
# example: POST 127.0.0.1:5000/delete_account
#          body: {"username":"xxx", "password": "xxx"}
@app.route('/delete_account', methods=['POST'])
def delete_account():
    data = request.json
    if 'userId' not in data:
        return jsonify({'error': 'Missing userId'}), 400

    userId = data['userId']

    result = db.session.execute(text("SELECT * FROM user WHERE UserId= :userId"), {"userId": userId})

    if not result.rowcount:
        return jsonify({'error': 'No such userId'}), 400

    # Delete the user
    result = db.session.execute(text("DELETE FROM user WHERE UserId= :userId"), {"userId": userId})
    db.session.commit()

    if result.rowcount:
        return jsonify({'message': 'Account was deleted successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404
    

# GET API
# request parameter: type (string), query (string), page (int)
# Support types: mammal, country, continent
# response: JSON object with an array of entities based on type and query, or error message if query/type is missing or invalid
#
# example usage:
# To search for entities of a specific type with a name similar to the provided query:
# GET 127.0.0.1:5000/search?type=mammal&query=Ornithorhynchus_anatinus&page=0
#
# page starts from 0
@app.route('/search', methods=['POST'])
def search():
    data = request.json
    if 'type' not in data or 'query' not in data or 'page' not in data:
        return jsonify({'error': 'Missing query type or query text or query page!'}), 400
    # type = request.args.get('type')
    queryType = data['type']
    queryWord = data['query']
    print('queryWord: ' + queryWord)
    page = data['page'] - 1
    # page = int(request.args.get('page'))
    offset = page * 10

    if queryType == 'Mammal':
        count, columns, results = queryMammal(db.session, text, queryWord, offset)
    elif queryType == 'Country':
        count, columns, results = queryCountry(db.session, text, queryWord, offset)
    elif queryType == 'Continent':
        count, columns, results = queryContinent(db.session, text, queryWord, offset)
    elif queryType == 'Institution':
        count, columns, results = queryInstitution(db.session, text, queryWord, offset)
    elif queryType == 'Publication':
        count, columns, results = queryPublication(db.session, text, queryWord, offset)
    else:
        return jsonify({'message': f'No such query type {queryType}'}), 400
    
    if len(results) > 0 and len(columns) != len(results[0]):
        return jsonify({'error': 'key and value in table can not match!'}), 500
    
    dataList = []
    if len(results) == 0:
        row_dict = {k: None for k in columns}
        dataList.append(row_dict)
        return jsonify({'message': 'query data successfully', 'dataList': dataList, 'count': count[0] }), 200
    
    for row in results:
        row_dict = {k: v for k, v in zip(columns, row)}
        dataList.append(row_dict)
    # dataList = [{column: getattr(row, column) for column in columns} for row in results]
    # print(dataList)    
    return jsonify({'message': 'query data successfully', 'dataList': dataList, 'count': count[0] }), 200

    # serialized_results = []
    # if queryType == 'mammal':
    #     mammal_name = request.args.get('query')

    #     if not mammal_name:
    #         return jsonify({'error': 'mammal_name is missing in the query parameters'}), 400

    #     results = db.session.execute(text("SELECT * FROM mammal WHERE lower(SciName) LIKE lower(:name)"), {"name": f"%{mammal_name}%"}) 
        
    #     if not results:
    #         return jsonify({'message': 'No mammals found with the provided name'}), 404
        
    #     if offset > results.rowcount:
    #         offset = int(results.rowcount) // 10 * 10

    #     limit = min(10, results.rowcount-offset)

    #     results = db.session.execute(text("SELECT * FROM mammal WHERE lower(SciName) LIKE lower(:name) LIMIT :limit OFFSET :offset"), {"name": f"%{mammal_name}%", "limit": limit, "offset": offset}) 
    # elif queryType == 'country':
    #     country_name = request.args.get('query')

    #     if not country_name:
    #         return jsonify({'error': 'country_name is missing in the query parameters'}), 400

    #     result = db.session.execute(text("SELECT * FROM habitat WHERE lower(CountryName) LIKE lower(:name)"), {"name": f"%{country_name}%"})
    #     if not result.rowcount:
    #         return jsonify({'error': 'no country_name matched'}), 400


    #     habitat_id = result.fetchone().HabitatId
    #     habitats = db.session.execute(text("SELECT * FROM locate WHERE HabitatId = :id"), {"id": habitat_id})

    #     mammal_ids = [hab.MammalId for hab in habitats]
    #     mammal_id_str = ', '.join(map(str, mammal_ids))
    #     sql_query = f"SELECT * FROM mammal WHERE MammalId IN ({mammal_id_str})"
    #     results = db.session.execute(text(sql_query))

    #     if not results:
    #         return jsonify({'message': 'No mammals found with the provided country'}), 404

    #     if offset > results.rowcount:
    #         offset = results.rowcount // 10 * 10
    #     limit = min(10, results.rowcount-offset)

    #     sql_query = f"SELECT * FROM mammal WHERE MammalId IN ({mammal_id_str}) LIMIT {limit} OFFSET {offset}"
    #     results = db.session.execute(text(sql_query)).fetchall()
    # elif queryType == 'continent':
    #     continent_name = request.args.get('query')  

    #     if not continent_name:
    #         return jsonify({'error': 'continent_name is missing in the query parameters'}), 400

    #     result = db.session.execute(text("SELECT * FROM habitat WHERE lower(ContinentName) LIKE lower(:name)"), {"name": f"%{continent_name}%"})
    #     if not result.rowcount:
    #         return jsonify({'error': 'no country_name matched'}), 400

    #     habitat_id = result.fetchone().HabitatId
    #     habitats = db.session.execute(text("SELECT * FROM locate WHERE HabitatId = :id"), {"id": habitat_id}) 
        
    #     mammal_ids = [hab.MammalId for hab in habitats]
    #     mammal_id_str = ', '.join(map(str, mammal_ids))
    #     sql_query = f"SELECT * FROM mammal WHERE MammalId IN ({mammal_id_str})"
    #     results = db.session.execute(text(sql_query))

    #     if not results:
    #         return jsonify({'message': 'No mammals found with the provided continent'}), 404
        
    #     if offset > results.rowcount:
    #         offset = results.rowcount // 10 * 10
    #     limit = min(10, results.rowcount-offset)

    #     sql_query = f"SELECT * FROM mammal WHERE MammalId IN ({mammal_id_str}) LIMIT {limit} OFFSET {offset}"
    #     results = db.session.execute(text(sql_query)).fetchall()

    # for mammal in results:
    #     serialized_mammal = {
    #         'MammalId': mammal.MammalId,
    #         'SciName': mammal.SciName,
    #         'Extinct': bool(mammal.Extinct),
    #         'GenusName': mammal.GenusName,
    #         'FamilyName': mammal.FamilyName,
    #         'OrderName': mammal.OrderName,
    #         'InstitutionId': mammal.InstitutionId
    #     }
    #     serialized_results.append(serialized_mammal)

    # return jsonify({'results': serialized_results}), 200



# # GET APImerialized_results}), 200

# POST API
# request body: {action: xxx, UserId: xxx, MammalId: xxx}
# supported action: add and delete
# response: {'message': 'Favor added successfully'} or {'error': 'Missing required fields: UserId and MammalId' or 'User not found' or 'Mammal not found' or 'This favor already exists'}
#
# example: POST 127.0.0.1:5000/add_favor
#          body: {"action": "add", "UserId": 1, "MammalId": 1000001}

# @app.route('/favor', methods=['POST'])
# def add_favor():
#     data = request.json

#     action = data['action']
#     if not data or 'UserId' not in data or 'MammalId' not in data:
#         return jsonify({'error': 'Missing required fields: UserId and MammalId'}), 400
    
#     user_id = data['UserId']
#     mammal_id = data['MammalId']

#     user = db.session.execute(text("SELECT * FROM user WHERE UserId = :user_id"), {'user_id': user_id}).fetchone()
#     if not user:
#         return jsonify({'error': 'User not found'}), 404

#     mammal = db.session.execute(text("SELECT * FROM mammal WHERE MammalId = :mammal_id"), {'mammal_id': mammal_id}).fetchone()
#     if not mammal:
#         return jsonify({'error': 'Mammal not found'}), 404


#     if action == 'add':
#         # Check if the favor already exists
#         favor = db.session.execute(text("SELECT * FROM favor WHERE UserId = :user_id AND MammalId = :mammal_id"), 
#                                 {'user_id': user_id, 'mammal_id': mammal_id}).fetchone()
#         if favor:
#             return jsonify({'error': 'This favor already exists'}), 409

#         db.session.execute(text("INSERT INTO favor (UserId, MammalId, FavorTime) VALUES (:user_id, :mammal_id, :favor_time)"), 
#                             {'user_id': user_id, 'mammal_id': mammal_id, 'favor_time': datetime.utcnow()})
#         db.session.commit()
#         return jsonify({'message': 'Favor added sauccessfully'}), 201
#     elif action == 'delete':
#         # Check if the favor already exists
#         favor = db.session.execute(text("SELECT * FROM favor WHERE UserId = :user_id AND MammalId = :mammal_id"), 
#                                 {'user_id': user_id, 'mammal_id': mammal_id}).fetchone()
#         if not favor:
#             return jsonify({'error': 'This favor does not exist'}), 409
    


#         db.session.execute(text("DELETE FROM favor WHERE UserId=:user_id AND MammalId=:mammal_id"), 
#                             {'user_id': user_id, 'mammal_id': mammal_id})
#         db.session.commit()
        
#         return jsonify({'message': 'Favor deleted sauccessfully'}), 201

@app.route('/edit_favor', methods=['POST'])
def manage_favor():
    data = request.json
    if 'userId' not in data or 'mammalName' not in data or 'action' not in data:
        return jsonify({'error': 'Missing userId or mammalName or action!'}), 400
    # type = request.args.get('type')
    userId = data['userId']
    mammalName = data['mammalName']
    action = data['action']
    
    user = db.session.execute(text("SELECT * FROM user WHERE UserId = :userId"), {'userId': userId}).fetchone()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    mammal = db.session.execute(text("SELECT * FROM mammal WHERE SciName = :mammalName"), {'mammalName': mammalName}).fetchone()
    if not mammal:
        return jsonify({'error': 'Mammal not found'}), 404
    mammalId = mammal.MammalId

    try:
        if action == 'add':
            db.session.execute(text("CALL AddFavor(:userId, :mammalId)"), {'userId': userId, 'mammalId': mammalId})
        elif action == 'remove':
            db.session.execute(text("CALL RemoveFavor(:userId, :mammalId)"), {'userId': userId, 'mammalId': mammalId})
        else:
            return jsonify({'error': 'Invalid action specified'}), 400
        db.session.commit()
        return jsonify({'message': f'Favor {action}ed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
# GET API
# request parameter: UserId
# response: {'favors': [{'MammalId': xxx, 'FavorTime': 'yyyy-mm-ddThh:mm:ss'}]} or {'error': 'UserId is required' or 'User not found' or 'No favors found for this user'}
#
# example: GET 127.0.0.1:5000/get_favors?UserId=1
# @app.route('/get_favors', methods=['GET'])
# def get_favors():
#     user_id = request.args.get('UserId')
#     if not user_id:
#         return jsonify({'error': 'UserId is required'}), 400

#     # Check if the user exists
#     user = db.session.execute(text("SELECT * FROM user WHERE UserId = :user_id"), {'user_id': user_id}).fetchone()
#     if not user:
#         return jsonify({'error': 'User not found'}), 404

#     # Retrieve all favor records for this user
#     favor_query = text("SELECT MammalId, FavorTime FROM favor WHERE UserId = :user_id")
#     favor_records = db.session.execute(favor_query, {'user_id': user_id}).fetchall()

#     if not favor_records:
#         return jsonify({'error': 'No favors found for this user'}), 404

#     favors_list = []
#     for record in favor_records:
#             record_dict = {
#                 'MammalId': record[0],
#                 'FavorTime': record[1].isoformat()
#             }
#             favors_list.append(record_dict)

#     return jsonify({'results': favors_list}), 200
    

# @app.route('/get_favors', methods=['POST'])
# def get_favors():
#     data = request.json
#     if 'userId' not in data or 'page' not in data:
#         return jsonify({'error': 'Missing userId or query page!'}), 400
#     userId = data['userId']
#     page = data['page'] - 1
#     offset = page * 10

#     try:
#         count, columns, results = queryFavor(db.session, text, userId, offset)
#         if len(results) > 0 and len(columns) != len(results[0]):
#             return jsonify({'error': 'key and value in table can not match!'}), 500
    
#         dataList = []
#         if len(results) == 0:
#             row_dict = {k: None for k in columns}
#             dataList.append(row_dict)
#             return jsonify({'message': 'query data successfully', 'dataList': dataList, 'count': count[0] }), 200
        
#         for row in results:
#             row_dict = {k: v for k, v in zip(columns, row)}
#             dataList.append(row_dict)
#         return jsonify({'message': 'query data successfully', 'dataList': dataList, 'count': count[0] }), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    
    # try:
    #     results = db.session.execute(text("CALL GetUserFavorites(:userId)"), {'user_id': userId})
    #     favors_list = [{'MammalId': row['MammalId'], 'FavorTime': row['FavorTime'].isoformat()} for row in results]

    #     results.next()  
    #     count_result = results.fetchone()
    #     total_favors = count_result['TotalFavors']

    #     if not favors_list:
    #         return jsonify({'error': 'No favors found for this user'}), 404

    #     return jsonify({'results': favors_list, 'count': total_favors}), 200
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500


# ===========================
@app.route('/get_favors', methods=['POST'])
def get_favors():
    data = request.json
    user_id = data.get('userId')
    page = data.get('page', 1) - 1 
    items_per_page = 10  

    if not user_id:
        return jsonify({'error': 'Missing userId'}), 400

    try:

        result_proxy = db.session.execute(
            "CALL GetFavorDetails(:user_id, :offset, :limit)",
            {'user_id': user_id, 'offset': page * items_per_page, 'limit': items_per_page}
        )

        results = result_proxy.fetchall()

     
        if result_proxy.nextset():
            total_count = result_proxy.fetchone()[0]
        else:
            total_count = 0  

        favors_list = [
            {
                'MammalId': row['MammalId'],
                'ScientificName': row['ScientificName'],
                'GenusName': row['GenusName'],
                'FamilyName': row['FamilyName'],
                'OrderName': row['OrderName'],
                'CountryName': row['CountryName'],
                'ContinentName': row['ContinentName'],
                'InstitutionName': row['InstitutionName'],
                'FavorTime': row['FavorTime'].isoformat() if row['FavorTime'] else None
            }
            for row in results
        ]


        return jsonify({'results': favors_list, 'count': total_count}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/statistic', methods=['POST'])
def get_statistic():
    data = request.json
    if 'statisticKey' not in data or 'page' not in data:
        return jsonify({'error': 'Missing statistic key or query page!'}), 400
    statisticKey = data['statisticKey']
    page = data['page'] - 1
    offset = page * 10

    if statisticKey == 1:
        count, columns, results = sortTopMammal(db.session, text, offset)
    elif statisticKey == 2:
        count, columns, results = sortTopInstitutions(db.session, text, offset)
    elif statisticKey == 3:
        count, columns, results = sortTopFavorited(db.session, text, offset)
    elif statisticKey == 4:
        count, columns, results = sortTopCited(db.session, text, offset)
    else:
        return jsonify({'message': f'No such query statisticKey {statisticKey}'}), 400
    
    if len(results) > 0 and len(columns) != len(results[0]):
        return jsonify({'error': 'key and value in table can not match!'}), 500
    
    dataList = []
    if len(results) == 0:
        row_dict = {k: None for k in columns}
        dataList.append(row_dict)
        return jsonify({'message': 'query data successfully', 'dataList': dataList, 'count': count[0] }), 200
    
    for row in results:
        row_dict = {k: v for k, v in zip(columns, row)}
        dataList.append(row_dict)
    # dataList = [{column: getattr(row, column) for column in columns} for row in results]
    # print(dataList)    
    return jsonify({'message': 'query data successfully', 'dataList': dataList, 'count': count[0] }), 200