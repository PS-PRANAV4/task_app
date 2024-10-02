from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
import random
from django.conf import settings
from django.contrib.auth.models import User
from .serializers import SignupSerializer,SendOtpSerializer,VerifyOtpSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import EmailOtp
from .utils import generate_unique_string

class SendMailOTp(APIView):
    @swagger_auto_schema(
        operation_description="Send an OTP to the provided email",
        request_body=SendOtpSerializer,
        responses={
            200: openapi.Response(description="OTP sent successfully"),
            400: openapi.Response(description="Invalid email or failed validation"),
            500: openapi.Response(description="Failed to send email due to server error")
        }
    )
    def post(self,request):
        email = request.data.get("email")
        if email == None:
            return Response({"msg":"Enter a valid email"},status=status.HTTP_400_BAD_REQUEST)
        email_validator = EmailValidator()

        try: 
            email_validator(email)
        except ValidationError:
            return Response({"msg": "Invalid email format"}, status=status.HTTP_400_BAD_REQUEST)
        

        try:
            otp = random.randint(100000, 999999)
            try:
                email_otp_obj = EmailOtp.objects.get(email=email)
                email_otp_obj.otp = otp
                email_otp_obj.save()
            except EmailOtp.DoesNotExist:
                email_otp_obj = EmailOtp.objects.create(email=email,otp=otp)
                
            subject = "task app email otp"
            message = f"Your OTP for the task app is {otp}"  # Generate a random OTP in a real application
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            return Response({"msg": "Failed to send email", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"msg": "OTP sent successfully"}, status=status.HTTP_200_OK)
    
class VerifyMailOtp(APIView):
    @swagger_auto_schema(
        operation_description="Verify OTP sent to the email and generate a unique signature",
        request_body=VerifyOtpSerializer,
        responses={
            200: openapi.Response(description="Email verified successfully", examples={"string_unique": "123abcXYZ"}),
            400: openapi.Response(description="Incorrect OTP or validation error"),
        }
    )
    def post(self,request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        try:
            email_otp_obj =  EmailOtp.objects.get(email=email,otp=otp)
        except EmailOtp.DoesNotExist:
            return Response({"msg":"incorrect otp"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"msg":"unknown error"},status=status.HTTP_400_BAD_REQUEST)
        while True:
            string_unique = generate_unique_string()
            if not EmailOtp.objects.filter(verify_signature=string_unique).exists():
                email_otp_obj.verify_signature = string_unique
                email_otp_obj.save()
                break
        return Response({"msg":"Email verified","string_unique":string_unique},status=status.HTTP_200_OK)





class Signup(APIView):
    @swagger_auto_schema(
        operation_description="Create a new user by providing username, email, and password",
        request_body=SignupSerializer,
        responses={
            201: openapi.Response(description="User created successfully"),
            400: openapi.Response(description="Invalid input or user already exists"),
        }
    )
    def post(self,request):
        user_name = request.data.get("user_name")
        email = request.data.get("email")
        password = request.data.get("password")
        uniq_key = request.data.get("key")
        if user_name is None or email is None or password is None:
            return Response({"msg":"please enter valid data"},status=status.HTTP_400_BAD_REQUEST)
        try:
            EmailOtp.objects.get(email=email,verify_signature=uniq_key)
        except EmailOtp.DoesNotExist:
            return Response({"msg":"email not found user not created"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"msg":"unknow error occured"},status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create_user(username=user_name,email=email,password=password)
        except:
            return Response({"msg":"please enter valid data"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg":"user created"},status=status.HTTP_201_CREATED)