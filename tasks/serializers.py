# from rest_framework import serializers

# from .models import Task


# class TaskSerializer(serializers.ModelSerializer):
#     """
#     Serializer for the Task model.
#     """
    
#     class Meta:
#         model = Task
#         fields = ('id', 'owner', 'title', 'description', 'done', 'created')
#         read_only_fields = ['owner', 'created']
    
    
#     def create(self, validated_data):
#         request = self.context.get('request')
#         validated_data['owner'] = request.user
#         task = Task.objects.create(**validated_data)
        
#         return task
