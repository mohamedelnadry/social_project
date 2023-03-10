from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.exceptions import AuthenticationFailed
from .serializers import RegisterSerializer, TokenSerializer
from .models import User,UserToken
import jwt,datetime


class Register(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class Create(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        usertoken =  UserToken.objects.filter(user=user.id).first()
        if user is None:
            raise AuthenticationFailed('User Not Found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password!')
        
        if not usertoken == None:
            try:
                JWT_token = jwt.api_jwt.decode_complete(usertoken.token,'secret',algorithms=['HS256'], options=None)
                return Response({
                    "jwt":usertoken.token
                })
            except jwt.exceptions.ExpiredSignatureError:
                usertoken.delete()
            
        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload,'secret',algorithm='HS256')

        serializer_data = {
            "token":token,
            'user':user.id,
        }
        print(serializer_data)
        serializer = TokenSerializer(data = serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response()
        response.data = {
            'jwt':token
        }
        return response


class Refresh(APIView):
    def get(self,request):
        usertoken =  request.headers['Authorization']
        try:
            payload = jwt.decode(usertoken, 'secret', algorithms=["HS256"],options={
                "verify_exp":False
            })
            user = User.objects.filter(id=payload['id']).first()
            usertoken =  UserToken.objects.filter(user=user.id).first()
            usertoken.delete()
            payload = {
                'id':user.id,
                'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat':datetime.datetime.utcnow()
            }
            token = jwt.encode(payload,'secret',algorithm='HS256')

            serializer_data = {
                "token":token,
                'user':user.id,
            }
            print(serializer_data)
            serializer = TokenSerializer(data = serializer_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = Response()
            response.data = {
                'jwt':token
            }
            
        except jwt.exceptions.DecodeError:
            return Response({
                "error":"Invaled Token"
            })

        return response


class Revoke(APIView):

    def get(self, request):
        usertoken =  request.headers['Authorization']
        try:
            payload = jwt.decode(usertoken, 'secret', algorithms=["HS256"],options={
                "verify_exp":False
            })
            
            user = User.objects.filter(id=payload['id']).first()
            usertoken =  UserToken.objects.filter(user=user.id).first()
            if usertoken == None:
                return Response({
                    "jwt":"this token is revoked"
                })

            usertoken.delete()


        except jwt.exceptions.DecodeError:
            return Response({
                "error":"Invaled Token"
            })
        return Response({
            "jwt":"Token revoked please create another one"
        })



class UserView(APIView):
    def get(self,request):
        token= request.headers['Authorization']
        try:
            JWT_token = jwt.api_jwt.decode_complete(token,'secret',algorithms=['HS256'], options=None)
            payload = JWT_token["payload"]
            user = User.objects.filter(id=payload['id']).first()
            serializer = RegisterSerializer(user)
        except jwt.exceptions.ExpiredSignatureError:
            return Response({
                "error":"Expired Token"
            })
        except jwt.exceptions.DecodeError:
            return Response({
                "error":"Invalid Token"
            })

        return Response(serializer.data)


