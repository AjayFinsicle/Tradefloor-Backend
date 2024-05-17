# from firebase_functions import https_fn, firestore_fn, options
# from firebase_admin import initialize_app, auth, firestore, credentials
# import random

# # Initialize Firebase app
# cred = credentials.Certificate("sa.json")
# initialize_app(cred)

# db = firestore.client()

# # CORS configuration
# cors_options = options.CorsOptions(
#     cors_origins=["*"],  # Allow all origins, you can change it to a specific domain if needed
#     cors_methods=["GET", "POST", "DELETE", "PUT"],
# )

# # Create the Cloud Function
# @https_fn.on_request(cors=cors_options)
# def create_user(req: https_fn.Request) -> https_fn.Response:
#     data = req.json
#     email = data.get('email')
#     password = data.get('password')
#     display_name = data.get('displayName')

#     try:
#         # Create user in Firebase Authentication
#         user = auth.create_user(email=email, password=password, display_name=display_name)
#         print(f"User created in Firebase Authentication with UID: {user.uid}")

#         # Create a collection for the user using the UID as the document ID
#         user_collection_ref = db.collection('users').document(user.uid)

#         # Set initial data for the user (you can customize this based on your needs)
#         username = display_name or ''

#         # If display name exists, use the first part of the display name plus a random number
#         if display_name:
#             display_name_parts = display_name.split(' ')
#             username = f"{display_name_parts[0]}_{random.randint(0, 9999)}"

#         # Set initial data for the user (you can customize this based on your needs)
#         user_collection_ref.set({
#             'displayName': display_name or '',
#             'username': username,
#             'email': email,
#             # Add more fields as needed
#         })

#         print(f"Firestore user collection created for UID: {user.uid}")

#         return https_fn.Response(status=200, body={"message": "User created successfully"})
#     except Exception as e:
#         print(f"Error creating user: {e}")
#         return https_fn.Response(status=500, body={"message": "Error creating user"})


