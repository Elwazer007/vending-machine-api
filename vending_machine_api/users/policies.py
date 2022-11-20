from rest_access_policy import AccessPolicy
from .models import ROLES

class UserAccessPolicy(AccessPolicy):

    statements = [
        {
            "action" : ["<safe_methods>"], 
            "principal": "*",
            "effect": "allow",
        },
        {
           "action":  ["<method:put>" , "<method:patch>" , "<method:delete>"], 
            "principal": "*",
            "effect": "allow",
            "condition": ["is_request_from_same_user"],
        },
        {
           "action":  ["deposit"], 
            "principal": "*",
            "effect": "deny",
            "condition": ["is_seller"],
        },
       
        
    ]

    def is_request_from_same_user(self, request, view , action):
        user_id = view.get_object().id
        user_request_id = request.user.id
        return user_id == user_request_id

    def is_seller(self , request , view , action):
        user_role = request.user.role
        return user_role == ROLES.seller