from rest_access_policy import AccessPolicy
import logging

from users.models import ROLES

logger = logging.getLogger(__name__)


class ProductAccessPolicy(AccessPolicy):

    statements = [
        {
            "action": ["<method:put>", "<method:patch>", "<method:delete>"],
            "principal": "*",
            "effect": "allow",
            "condition": ["is_request_from_product_seller"],
        },
        {
            "action": ["<method:get>"],
            "principal": "*",
            "effect": "allow",
        },
        {
            "action": ["<method:post>"],
            "principal": "*",
            "effect": "allow",
            "condition": ["is_role_allowed"],
        },
    ]

    def is_request_from_product_seller(self, request, view, action):
        try:
            product = view.get_object()
        except AssertionError:
            logger.warning(f"Endpoint {action} called without provided pk")
            return True
        product_seller_id = product.seller.id
        request_user_id = request.user.id
        return product_seller_id == request_user_id

    def is_role_allowed(self, request, view, action):
        user_role = request.user.role
        if action == "buy":
            return user_role == ROLES.buyer
        return user_role == ROLES.seller
