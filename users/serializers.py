from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile, Post, Follow
from .supabase_utils import upload_avatar  # your utility function

User = get_user_model()


# --------------------------
# Register Serializer
# --------------------------
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )
        Profile.objects.create(user=user)
        return user



# --------------------------
# Login Serializer
# --------------------------
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()  # username or email
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        identifier = data.get("identifier")
        password = data.get("password")

        if not identifier:
            raise serializers.ValidationError({"identifier": "Username or email is required"})
        if not password:
            raise serializers.ValidationError({"password": "Password is required"})

        user = None

        # 1️⃣ Try login with username first
        user = authenticate(username=identifier, password=password)

        # 2️⃣ If username login fails, try email login
        if not user and "@" in identifier:
            users = User.objects.filter(email=identifier, is_active=True)
            if users.exists():
                # Pick the first active user
                user_obj = users.first()
                user = authenticate(username=user_obj.username, password=password)

        if not user:
            raise serializers.ValidationError({"detail": "Invalid credentials"})

        data['user'] = user
        return data

# --------------------------
# Profile Serializer
# --------------------------
class ProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.URLField(read_only=True)

    class Meta:
        model = Profile
        fields = ["bio", "avatar_url", "website", "location", "visibility"]


# --------------------------
# User Serializer with stats
# --------------------------
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "profile",
            "followers_count",
            "following_count",
            "posts_count",
        ]

    def get_followers_count(self, obj):
        return Follow.objects.filter(following=obj).count()

    def get_following_count(self, obj):
        return Follow.objects.filter(follower=obj).count()

    def get_posts_count(self, obj):
        return Post.objects.filter(user=obj).count()


# --------------------------
# Post Serializer
# --------------------------
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "user", "image_url", "caption", "created_at"]
        read_only_fields = ["id", "created_at", "user"]


from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    receiver = serializers.StringRelatedField()
    post = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = '__all__'

