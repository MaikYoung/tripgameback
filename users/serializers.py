from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'trip_level', 'based_on', 'profile_pic')


class UserDetailSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'trip_level', 'based_on', 'description',
            'birthday', 'profile_pic', 'followers', 'following'
        )

    @staticmethod
    def get_followers(obj):
        if len(obj.followers) == 0:
            return 0
        return len(obj.followers)

    @staticmethod
    def get_following(obj):
        if len(obj.following) == 0:
            return 0
        return len(obj.following)


class UserCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    username = serializers.CharField( max_length=100)
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=400)
    birthday = serializers.DateField()
    trip_level = serializers.CharField(max_length=2)
    based_on = serializers.CharField(max_length=50)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.description = validated_data.get('description', instance.description)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.based_on = validated_data.get('based_on', instance.based_on)
        instance.save()
        return instance


class UserUploadProfilePicSerializer(serializers.Serializer):
    profile_pic = serializers.URLField()

    def update(self, instance, validated_data):
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.save()
        return instance


class UserFollowersSerializer(serializers.Serializer):
    following = serializers.ListField(child=serializers.IntegerField())
    followers = serializers.ListField(child=serializers.IntegerField())

    def update(self, instance, validated_data):
        instance.following = validated_data.get('following', instance.following)
        instance.followers = validated_data.get('followers', instance.followers)
        instance.save()
        return instance