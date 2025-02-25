from models.user import User
from models.gift import Gift
from services.unit_of_work import UnitOfWork
from repositories.gift_repository import GiftRepository

class GiftService:
    def __init__(self, session):
        self.gift_repository = GiftRepository(session)

    @staticmethod
    def send_gift(user_id, email, amount, asset_id):
        """
        Create a new gift from sender to receiver
        
        Args:
            user_id (str): ID of the user sending the gift
            sent_to (int): ID of the user receiving the gift
            amount (int): Amount of the gift
            asset_id (str): ID of the asset of the gift
            
        Returns:
            Gift: The created gift object
            
        Raises:
            ValueError: If gift_details is missing required fields
            Exception: If token is invalid
        """
        with UnitOfWork() as uow:
            recipient = uow.users.get_by_email(email)
            if not recipient:
                raise ValueError("Invalid sender or recipient ID")

            gift = Gift.create(
                sent_from=user_id,
                sent_to=recipient.id,
                amount=amount,
                asset_id=asset_id
            )
            return gift

    @staticmethod
    def list_gifts_sent_to_user(user_id):
        with UnitOfWork() as uow:
            gifts = uow.gifts.all(sent_to=user_id)
            return [
                {
                    'id': gift.id,
                    'sent_from': gift.sent_from,
                    'sent_to': gift.sent_to,
                    'amount': gift.amount,
                    'created_at': gift.created_at,
                    'updated_at': gift.updated_at
                } for gift in gifts
            ]

    @staticmethod
    def list_gifts_sent_from_user(user_id):
        with UnitOfWork() as uow:
            gifts = uow.gifts.all(sent_from=user_id)
            formatted_gifts = []
            for gift in gifts:
                asset = uow.assets.get_by_id(gift.asset_id)
                formatted_gifts.append(
                    {
                    'id': gift.id,
                    'sent_from_name': gift.sent_from_user.full_name,
                    'sent_from_email': gift.sent_from_user.email,
                    'sent_from_profile_picture': gift.sent_from_user.profile_picture,
                    'sent_to_name': gift.sent_to_user.full_name,
                    'sent_to_email': gift.sent_to_user.email,
                    'sent_to_profile_picture': gift.sent_to_user.profile_picture,
                    'amount': gift.amount,
                    'stock': asset.name if asset else None,
                    'stock_url': asset.logo_url if asset else None,
                    'created_at': gift.created_at,
                    'updated_at': gift.updated_at
                }
            )
            return formatted_gifts

    @staticmethod
    def get_user_gift_counts(user_id):
        """
        Get count of gifts sent and received by a user
        
        Args:
            user_id: User's ID
            
        Returns:
            dict: Contains giftsReceived and giftsSent counts
            
        Raises:
            Exception: If token is invalid
        """
        with UnitOfWork() as uow:
            return {
                'giftsReceived': uow.gifts.get_gift_received_count(user_id),
                'giftsSent': uow.gifts.get_gift_sent_count(user_id)
            }