from firebase_functions import https_fn, options
from firebase_admin import initialize_app, auth, firestore, credentials
from flask import request, jsonify, make_response
from datetime import datetime

# Initialize Firebase app
cred = credentials.Certificate("sa.json")
initialize_app(cred)

db = firestore.client()

# CORS configuration
cors_options = options.CorsOptions(
    cors_origins=["*"],  # Allow all origins, you can change it to a specific domain if needed
    cors_methods=["GET", "POST", "DELETE", "PUT"],
)

# Create the Cloud Function
@https_fn.on_request(cors=cors_options)
def create_user(req: https_fn.Request) -> https_fn.Response:
    data = request.json
    uid = data.get("uid")
    referral_code = data.get("referral_code")
    
    # Check with Firebase Authentication
    try:
        user = auth.get_user(uid)
        user_ref = db.collection("logged_users").document(user.uid)
        user_doc = user_ref.get()
        
        if user_doc.exists:
            return jsonify({"error": "User already exists"}), 400

        created_at_now = datetime.now()
        created_at_str = created_at_now.strftime("%Y-%m-%d %H:%M:%S")
        #get timestamp by using created_at_str
        created_at = datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S")

        user_data = {
            "uid": user.uid,
            "email": user.email,
            "PhoneNumber": user.phone_number,
            "user provider": user.provider_id,
            "created_at": created_at,
            "display_name": user.display_name,
            "photo_url": user.photo_url,
            "authorized_partner":"Rejected",
        }

        if referral_code:
            referred_by = validate_referral(referral_code)
            print(referred_by)
            if referred_by:
                if referred_by == user.uid:  # Check if referral is oneself
                    return jsonify({"error": "You cannot refer yourself"}), 400
                user_data["referred_by"] = True
                add_user_to_referral(referred_by, uid, user_data)  # Corrected argument passing
            else:
                print("Invalid referral code")

        if not referral_code or not referred_by:
            print("Creating user data without referral")
            created_at_now = datetime.now()
            created_at_str = created_at_now.strftime("%Y-%m-%d %H:%M:%S")
            created_at = datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S")
            user_data = {
                "uid": user.uid,
                "email": user.email,
                "PhoneNumber": user.phone_number,
                "user provider": user.provider_id,
                "created_at": created_at,
                "display_name": user.display_name,
                "photo_url": user.photo_url,
                "referred_by": False,
                "authorized_partner":"Rejected",
            }
        add_data(user_data)
        
        return make_response(jsonify(user_data), 200)
    except ValueError:
        return jsonify({"error": "User not found"}), 404

def add_data(user_data):
    doc_ref = db.collection("logged_users").document(user_data.get("uid"))
    doc_ref.set(user_data)
    print("Data added successfully")

def validate_referral(referral_code):
    referrals_ref = db.collection("authorized_partnership").where("referral_code", "==", referral_code).stream()
    #debug both are same
    print(referrals_ref)
    
    for referral_doc in referrals_ref:
        return referral_doc.id # Corrected return statement
    return None

def add_user_to_referral(referral_id, uid, user_data):
    referral_user_ref = db.collection("referrals").document(referral_id).collection("users").document(uid)
    referral_user_ref.set(user_data)
    print("User added to referral successfully")
    return True





