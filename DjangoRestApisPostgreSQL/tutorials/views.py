# Create your views here.
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from tutorials.models import Tutorial, Classes
from tutorials.serializers import TutorialSerializer, ClassesSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework import viewsets

class TutorialViewSet(viewsets.ModelViewSet):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer   


@swagger_auto_schema(methods=['post'], request_body=TutorialSerializer)
@api_view(['GET', 'POST', 'DELETE'])
def tutorial_list(request):
    # GET list of tutorials, POST a new tutorial, DELETE all tutorials
    # Retrieve objects
    try:
        if request.method == 'GET':
            tutorials = Tutorial.objects.all()
            
            title = request.GET.get('title', None)
            if title is not None:
                tutorials = tutorials.filter(title__icontains=title)
            
            tutorials_serializer = TutorialSerializer(tutorials, many=True)
            return JsonResponse(tutorials_serializer.data, safe=False)
            # 'safe=False' for objects serialization
    
        # Create a new object        
        elif request.method == 'POST':        
            tutorial_data = JSONParser().parse(request)
            tutorial_serializer = TutorialSerializer(data=tutorial_data)
            if tutorial_serializer.is_valid():
                tutorial_serializer.save()
                return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
            return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Delete all objects
        elif request.method == 'DELETE':
            count = Tutorial.objects.all().delete()
            return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return JsonResponse({'message': 'An error occurred: {}'.format(str(e))}, status)
    

@swagger_auto_schema(methods=['put'], request_body=TutorialSerializer) 
@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, pk):
    # find tutorial by pk (id)
    try:
        tutorial = Tutorial.objects.get(pk=pk) 

        # Retrieve a single object
        if request.method == 'GET': 
            tutorial_serializer = TutorialSerializer(tutorial) 
            return JsonResponse(tutorial_serializer.data) 
        
        # Update a single object
        elif request.method == 'PUT': 
            tutorial_data = JSONParser().parse(request) 
            tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data) 
            if tutorial_serializer.is_valid(): 
                tutorial_serializer.save() 
                return JsonResponse(tutorial_serializer.data) 
            return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        # Delete a single object
        elif request.method == 'DELETE': 
            tutorial.delete() 
            return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    except Tutorial.DoesNotExist: 
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
        
@api_view(['GET'])
def tutorial_list_published(request):
    # GET all published tutorials
    tutorials = Tutorial.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
    
    
class ClassesViewSet(viewsets.ModelViewSet):
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer   


@swagger_auto_schema(methods=['post'], request_body=ClassesSerializer)
@api_view(['GET', 'POST', 'DELETE'])
def classes_list(request):
    # GET list of classes, POST a new class, DELETE all classes
    # Retrieve objects
    try:
        if request.method == 'GET':
            classes = Classes.objects.all()
            
            name = request.GET.get('name', None)
            if name is not None:
                classes = classes.filter(name__icontains=name)
            
            classes_serializer = ClassesSerializer(classes, many=True)
            return JsonResponse(classes_serializer.data, safe=False)
            # 'safe=False' for objects serialization
    
        # Create a new object        
        elif request.method == 'POST':        
            classes_data = JSONParser().parse(request)
            classes_serializer = ClassesSerializer(data=classes_data)
            if classes_serializer.is_valid():
                classes_serializer.save()
                return JsonResponse(classes_serializer.data, status=status.HTTP_201_CREATED) 
            return JsonResponse(classes_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Delete all objects
        elif request.method == 'DELETE':
            count = Classes.objects.all().delete()
            return JsonResponse({'message': '{} Classes were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return JsonResponse({'message': 'An error occurred: {}'.format(str(e))}, status)
    

@swagger_auto_schema(methods=['put'], request_body=ClassesSerializer) 
@api_view(['GET', 'PUT', 'DELETE'])
def classes_detail(request, pk):
    # find classes by pk (id)
    try:
        classes = Classes.objects.get(pk=pk) 

        # Retrieve a single object
        if request.method == 'GET': 
            classes_serializer = ClassesSerializer(classes) 
            return JsonResponse(classes_serializer.data) 
        
        # Update a single object
        elif request.method == 'PUT': 
            classes_data = JSONParser().parse(request) 
            classes_serializer = ClassesSerializer(classes, data=classes_data) 
            if classes_serializer.is_valid(): 
                classes_serializer.save() 
                return JsonResponse(classes_serializer.data) 
            return JsonResponse(classes_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        # Delete a single object
        elif request.method == 'DELETE': 
            classes.delete() 
            return JsonResponse({'message': 'Classes was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    except Tutorial.DoesNotExist: 
        return JsonResponse({'message': 'The classes does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
        
@api_view(['GET'])
def classes_list_grade(request, grade):
    # GET all classes by grade
    classes = Classes.objects.filter(grade=grade)
        
    if request.method == 'GET': 
        classes_serializer = ClassesSerializer(classes, many=True)
        return JsonResponse(classes_serializer.data, safe=False)