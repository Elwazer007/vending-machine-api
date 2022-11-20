from rest_access_policy import AccessPolicy

class ProductAccessPolicy(AccessPolicy):

    statements = [
        {
           "action":  ["<method:put>" , "<method:patch>" , "<method:delete>"], 
            "principal": "*",
            "effect": "allow",
            "condition": ["is_request_from_product_seller"],
        },
        {
           "action":  ["<method:get>"], 
            "principal": "*",
            "effect": "allow",
        }

    ]

    def is_request_from_product_seller(self, request, view , action):
        product = view.get_object()
        product_seller_id = product.seller.id
        request_user_id = request.user.id
        return product_seller_id == request_user_id
