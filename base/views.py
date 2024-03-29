from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
import random, time, json
from .models import RoomMember
from django.views.decorators.csrf import csrf_exempt

def lobby(request):
    return render(request, 'base/lobby.html')

def room(request):
    return render(request, 'base/room.html')

def getToken(request):
    appId = '97838d8b13374e0199db48d047245a20'
    appCertificate = '6a424722589244aaa3e30a8c97820f3b'
    channelName = request.GET.get('channel')
    uid = random.randint(1, 450)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1
    
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token, 'uid':uid}, safe=False)

@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    
    member, created = RoomMember.objects.get_or_create(
        name = data['name'],
        uid = data['UID'],
        room_name = data['room_name']
    )
    return JsonResponse({'name' : data['name']}, safe = False)

def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')
    
    member = RoomMember.objects.get(
        uid = uid,
        room_name = room_name
    )
    
    return JsonResponse({'name' : member.name}, safe = False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    
    member = RoomMember.objects.get(
        name = data['name'],
        uid = data['UID'],
        room_name = data['room_name']
    )
    member.delete()
    return JsonResponse('Member was deleted', safe = False)