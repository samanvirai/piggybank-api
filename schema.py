import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import User as UserModel
from services.auth_service import AuthService
from services.gift_service import GiftService
from services.unit_of_work import UnitOfWork
from services.user_service import UserService

class GiftCounts(graphene.ObjectType):
    gifts_received = graphene.Int()
    gifts_sent = graphene.Int()

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

class Gift(graphene.ObjectType):
    id = graphene.ID()
    sent_from_name = graphene.String()
    sent_from_email = graphene.String()
    sent_from_profile_picture = graphene.String()
    sent_to_name = graphene.String()
    sent_to_email = graphene.String()
    sent_to_profile_picture = graphene.String()
    amount = graphene.Int()
    stock = graphene.String()
    stock_url = graphene.String()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()

class Asset(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    ticker = graphene.String()

def require_auth(func):
    def wrapper(self, info, *args, **kwargs):
        auth_header = info.context.headers.get('Authorization')
        if not auth_header:
            raise Exception('Authentication required')
            
        token = auth_header.split(' ')[1]  # Assuming 'Bearer <token>' format
        user = UserService.get_user_by_token(token)
        
        if not user:
            raise Exception('Invalid token')
        
        # Add the token and user to the context for the resolver
        info.context.token = token
        info.context.user = user
        
        return func(self, info, *args, **kwargs)
    return wrapper

# token - eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMjhhZjJhZjUtNDVjYy00MDUzLWI5NzMtNmJjMDAzZmIzZjg2IiwiZXhwIjoxNzM5MzkxMDk4fQ.7gzZ6YYOdysNyvwjCCyXhJVivrlVGCkCelyYU2QM5Nc

class Query(graphene.ObjectType):
    user = graphene.Field(User)
    gift_counts = graphene.Field(GiftCounts)
    sent_gifts = graphene.List(Gift)
    received_gifts = graphene.List(Gift)
    assets = graphene.List(Asset)

    @require_auth
    def resolve_user(self, info):
        return info.context.user

    @require_auth
    def resolve_gift_counts(self, info):
        counts = GiftService.get_user_gift_counts(info.context.user.id)
        return GiftCounts(
            gifts_received=counts['giftsReceived'],
            gifts_sent=counts['giftsSent']
        )

    @require_auth
    def resolve_sent_gifts(self, info):
        sent_gifts = GiftService.list_gifts_sent_from_user(info.context.user.id)
        return [Gift(**gift) for gift in sent_gifts]
    
    @require_auth
    def resolve_received_gifts(self, info):
        received_gifts = GiftService.list_gifts_sent_to_user(info.context.user.id)
        return [Gift(**gift) for gift in received_gifts]

    def resolve_assets(self, info):
        with UnitOfWork() as uow:
            assets = uow.assets.all()
            return [
                {
                    'id': asset.id,
                    'name': asset.name,
                    'ticker': asset.ticker
                } for asset in assets
            ]

class SignUp(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        phone_number = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(lambda: User)
    token = graphene.String()

    def mutate(self, info, first_name, last_name, phone_number, email, password):
        user = AuthService.sign_up(first_name, last_name, phone_number, email, password)
        token = AuthService.login(email, password)
        return SignUp(user=user, token=token)

class Login(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()

    def mutate(self, info, email, password):
        token = AuthService.login(email, password)
        if token:
            return Login(token=token)
        raise Exception("Invalid credentials")
    
class SendGift(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        amount = graphene.Int(required=True)
        asset_id = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    @require_auth
    def mutate(self, info, email, amount, asset_id):
        try:
            GiftService.send_gift(info.context.user.id, email, amount, asset_id)
            return SendGift(success=True, error=None)
            
        except Exception as e:
            return SendGift(success=False, error=str(e))

class Mutation(graphene.ObjectType):
    sign_up = SignUp.Field()
    send_gift = SendGift.Field()
    login = Login.Field()

schema = graphene.Schema(query=Query, mutation=Mutation) 