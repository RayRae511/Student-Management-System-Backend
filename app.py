from flask import Flask, request, jsonify, make_response, json
from flask_jwt_extended import create_access_token, JWTManager, get_jwt, get_jwt_identity, unset_jwt_cookies, jwt_required
from datetime import datetime, timedelta, timezone
from flask_cors import CORS
from models import db, User
from flask_bcrypt import Bcrypt
from werkzeug.security import check_password_hash
# import os

app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config['SECRET_KEY'] = 'THISISOURSECRETKEYLOLXD'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user_data.db"
#postgres://user_data_iair_user:EEtXVJngNJrjFdWcGUNfwAjLiqtnkWOo@dpg-ckhpfkeafg7c73fvjerg-a.oregon-postgres.render.com/user_data_iair
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
bcrypt = Bcrypt(app)
db.init_app(app)
CORS(app, supports_credentials=True)

with app.app_context():
    db.create_all()

# Login route
@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()

    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    user = User.query \
        .filter_by(email=auth.get('email')) \
        .first()

    if not user:
        # returns 401 if the user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    if bcrypt.check_password_hash(user.password.decode('utf-8'), auth.get('password')):
        # Generate the JWT Token
        token = create_access_token({
            'public_id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        # Print the generated token for debugging
        #print(f"Token generated: {token.decode('utf-8')}")

        return make_response(jsonify({'token': token}), 201)
    # returns 403 if the password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )

@app.route('/adminlogin', methods=['POST'])
def admin_login():
    email = request.json['email']
    password = request.json['password']

    if email == 'admin@scholar.com' and password == 'admin@123':
        access_token = create_access_token(identity=email)
        return jsonify({
            "Success": "Admin logged in successfully",
            "Access token": access_token
        })
    else:
        return jsonify({"message":'Invalid email or password'}), 401
    
@app.route('/admin/data', methods=['GET'])
@jwt_required
def get_admin_data():
    current_user = get_jwt_identity()
    data = {'admin@scholar.com': 'Admin data'}
    if current_user in data:
        return {'data': data[current_user]}
    
    return {'Error 404! Data not found'}, 404


@app.route("/Signup", methods=["POST"])
def signup():
    email = request.json['email']
    password = request.json['password']

    user_exists = User.query.filter_by(email=email).first() is not None
    

    if user_exists:
        return jsonify({"message":"There's a user that already exist!"}), 409
    
    
    hashed_passowrd = bcrypt.generate_password_hash(password)
    new_user = User(email=email, password=hashed_passowrd)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message":"Signed up successfully"}), 201

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        return response
    
@app.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"message":'Successfully logged out'})
    unset_jwt_cookies(response)
    return response

# For profile page but scrapped it
#@app.route('/profile/<getemail>', methods=['GET'])
#@jwt_required()
#def profile(getemail):
#    print(getemail)
#    if not getemail:
#        return jsonify({'No email found'}), 404
#    
#    user = User.query.filter_by(email=getemail).first()
#
#    response_body = {
#        'email': user.email,
#        'id': user.id,
#    }
#
#    return response_body



port_number = 6942
if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=port_number)
