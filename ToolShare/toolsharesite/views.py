from logging import Logger

from django.contrib.auth import authenticate, login, logout
from django.db.models.fields import Empty
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404, render_to_response
from django.template import loader, Context, RequestContext

from toolsharesite.forms import RegistrationForm, CommunityShedForm, \
    ToolRegistrationForm, ToolBorrowForm, UpdateProfileForm, ToolDetailsForm,CreateShedForm, FeedbackForm,\
    EditToolDetailsForm
from toolsharesite.models import ShareZone, ToolShareUser, CommunityShed, Tool, Category, \
    Transaction,Feedback
from django.utils import timezone
from _datetime import datetime
from notifications.signals import notify
from django.db.models import Count

from notifications.models import Notification
from notifications.models import NotificationQuerySet
from django.contrib.auth.models import User



# Create your views here.


def registration(request):
    return render(request,"toolsharesite/registration.html",{
        
        })
    
def Index(request):
    return render(request,"toolsharesite/Index.html",{
        })
    
def RegistrationSuccess(request):
    return render(request,"toolsharesite/registrationSuccess.html",{
        })
    
def RegisterUser(request):
    print('In register user**************')
    error = ''
    print(request.method)
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['confirmpass']
            add1 = form.cleaned_data['address_line1']
            add2 = form.cleaned_data['address_line2']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zip']
            tele = form.cleaned_data['phone_no']
            
            if password == password2:
                user = form.save(commit=False)
                # must use set_password to properly save password for authentication
                user.set_password(form.cleaned_data['password'])
#                 user.save()
                
                shareZone = ShareZone.getShareZoneByZipcode(zipcode)
                
                if shareZone is not None:
                    user.share_zone_id = shareZone.id
                    
                else:
                    shareZone = ShareZone(zipcode=zipcode)
                    shareZone.save()
                    user.share_zone_id = shareZone.id
                    
                user.save()
                
                if CommunityShed.getCommunityShedByShareZone(shareZone) is None:
                    userinfo_dict = {'address_line1': user.address_line1, 'address_line2': user.address_line2, 'city': user.city,
                     'state': user.state, 'zip': user.zip}
                    form = CreateShedForm(initial=userinfo_dict)
                    return render(request,'toolsharesite/createShed.html',{
                    'user':user,
#                     'msg':'Congratulations, you have successfully registered!',
                    'msg':'There is no community shed created for your share zone. You can create a community shed below.',
#                     'error':'There is no community shed created for your share zone. You can create a community shed below.',
                    'fromLogin':True,
                    'form':form
                    })
                            
                return render(request,'toolsharesite/registrationSuccess.html',{
                    'user':user
                    })
                
            else:
                error = "*Passwords must be identical."
    else:
        form = RegistrationForm() # an unbound form
        
    return render(request, 'toolsharesite/registration.html', {
        'form': form, 'error':error,
    })
    
# def getShareZoneByZipcode(userZipcode):
#     try:
#         return ShareZone.objects.filter(zipcode=userZipcode)[0]  
#     except ShareZone.DoesNotExist:
#         return None
    
def Login(request):
    error = ""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['user_id'] = user.id
                request.session.set_expiry(52000)
                user = ToolShareUser.objects.get(id=user.id)
                return render(request,'toolsharesite/dashboard.html',{
                    'user':user
                    })
                
#                 return HttpResponseRedirect('Dashboard',{
#                       'user':user  
#                     })
            else:
                print("The password is valid, but the account has been disabled")
        else:
            error = "*Invalid user name or password"

    user = request.POST.get('user')
    t = loader.get_template('toolsharesite/index.html')
    c = RequestContext(request, {'user': user, 'error': error})
    return HttpResponse(t.render(c))

def Logout(request):
    logout(request)
    request.session.flush()
    try:
        del request.session['user_id']
    except KeyError:
        pass
        
    return render(request,'toolsharesite/index.html',{
                    })
    
def Dashboard(request):
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)
    return render(request, 'toolsharesite/dashboard.html', {
        'user':user
        })

def Shed(request):
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)
    shareZoneId = user.share_zone_id
    shareZone = ShareZone.objects.get(id=shareZoneId)
#     communityShed = CommunityShed.getCommunityShedByShareZone(shareZone)
#     if communityShed is None:
#         return render(request, 'toolsharesite/shed.html', {
#             'user' : user,
#             'shedIndicator' : False,
#             })
#     else:
        #get all list of tools available in the shed
    toolList = Tool.objects.filter(share_zone=shareZone).exclude(status='DA')
    return render(request, 'toolsharesite/shed.html', {
        'user' : user,
        'shedIndicator' : True,
        'tools':toolList,
#         'shed':communityShed,
        })
   
def CreateShed(request):
    error = ''
    msg = ''
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)

    userinfo_dict = {'address_line1': user.address_line1, 'address_line2': user.address_line2, 'city': user.city,
                     'state': user.state, 'zip': user.zip}
    form = CreateShedForm(initial=userinfo_dict)

    return render(request, 'toolsharesite/createShed.html', {'user': user, 'form': form, 'error': error, 'msg': msg})

    # return render(request, 'toolsharesite/createShed.html',{
    #    'user':user
    #    })

def CreateCommunityShed(request, id):
    error = ''
    msg = ''
    user = ToolShareUser.objects.get(id=id)
    if request.method == 'POST':
        form = CreateShedForm(data=request.POST)
        if form.is_valid():
            shedZipcode = form.cleaned_data['zip']
            #             print(shedZipcode)
            #             print(user.zip)
            #             if shedZipcode!=user.zip:
            #                 error = "The shed location should be within the share zone"

            #             else:
            communityShed = form.save()
            communityShed.share_zone_id = user.share_zone_id
            communityShed.shed_coordinator = user
            communityShed.save()
            user.role = 'SC'
            user.save()

            return render(request, 'toolsharesite/registrationSuccess.html', {
                'user': user,
                'error': error,
                'msg': msg
                #                     'shedIndicator' : True,
                #                     'tools' : [],
                #                     'shed' : communityShed,
            })

        else:
            error = "An error occurred, please try again."
            userinfo_dict = {'address_line1': user.address_line1, 'address_line2': user.address_line2, 'city': user.city,
                     'state': user.state, 'zip': user.zip}
            form = CreateShedForm(initial=userinfo_dict)

            return render(request, 'toolsharesite/createShed.html', {'user': user, 'form': form, 'error': error, 'msg': msg})

        # CreateShed(request);

        return render(request, 'toolsharesite/createShed.html', {
            'user': user,
            'shedIndicator': False,
            'error': error,
            'msg': msg
        })


def CreateShedHome(request):
    error = ''
    msg = ''
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)
    communityShed = CommunityShed.getCommunityShedByShareZone(user.share_zone)

    if (communityShed is None):
        userinfo_dict = {'address_line1': user.address_line1, 'address_line2': user.address_line2, 'city': user.city,
                     'state': user.state, 'zip': user.zip}
        form = CreateShedForm(initial=userinfo_dict)

        return render(request, 'toolsharesite/CreateShedHome.html', {'user': user, 'form': form, 'error': error, 'msg': msg})
    else:
        return render(request, 'toolsharesite/ViewShed.html', {
            'user': user,
            'shedIndicator': True,
            'communityShed': communityShed,
            'error': error,
            'msg': msg
        })

def CreateCommunityShedHome(request):
    error = ''
    msg = ''
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)

    if request.method == 'POST':
            form = CreateShedForm(data=request.POST)
            if form.is_valid():
                shedZipcode = form.cleaned_data['zip']
                #             print(shedZipcode)
                #             print(user.zip)
                #             if shedZipcode!=user.zip:
                #                 error = "The shed location should be within the share zone"

                #             else:
                communityShed = form.save()
                communityShed.share_zone_id = user.share_zone_id
                communityShed.shed_coordinator = user
                communityShed.save()
                user.role = 'SC'
                user.save()
                msg='Community Shed created successfully.'
                return render(request, 'toolsharesite/dashboard.html', {
                    'user': user,
                    'error': error,
                    'msg': msg
                    #                     'shedIndicator' : True,
                    #                     'tools' : [],
                    #                     'shed' : communityShed,
                })

            else:
                error = "An error occurred, please try again."

                #         CreateShed(request);
            return render(request, 'toolsharesite/CreateShedHome.html', {
                'user': user,
                'shedIndicator': False,
                'error': error,
                'msg': msg
            })

def ToolRegistration(request):
    error=''
    msg=''
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)
    if request.method=='POST':
        toolRegForm = ToolRegistrationForm(request.POST,request.FILES)
        if toolRegForm.is_valid():
            shareZoneId = user.share_zone_id
            shareZone=ShareZone.objects.get(id=shareZoneId)
#             communityShed = CommunityShed.objects.get(share_zone=shareZone)
            tool = toolRegForm.save();
            tool.owner=user
            tool.share_zone=shareZone
#             tool.community_shed = communityShed
            tool.save()
            userTools = Tool.objects.filter(owner=user)
            borrowTransactions = Transaction.objects.filter(borrower=user)
            msg='Tool Registered successfully!'
            return render(request, 'toolsharesite/toolManagement.html', {
                'toolRegistrationForm' : toolRegForm,
                'tools':userTools,
                'borrowedToolTransactions':borrowTransactions,
                'msg' : msg,
                'user' :user
                }) 
        else:
            error='An error occurred, please try again.'
     
    toolRegForm = ToolRegistrationForm() 
    if CommunityShed.getCommunityShedByShareZone(user.share_zone) is None:
        toolRegForm = ToolRegistrationForm(no_shed=True)      
#     toolRegForm = ToolRegistrationForm()
    return render(request, 'toolsharesite/toolRegistration.html', {
                'toolRegistrationForm' : toolRegForm,
                'error' : error,
                'user' : user
                }) 

def ToolManagement(request):
    error=""
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)
    shareZoneId = user.share_zone_id
    shareZone=ShareZone.objects.get(id=shareZoneId)
#     try:
#         communityShed = CommunityShed.objects.get(share_zone=shareZone)
#     except CommunityShed.DoesNotExist:
#         communityShed = None
#     
#     if communityShed is None:
#         return render(request, 'toolsharesite/toolManagement.html', {
#         'shed':communityShed,
#         'user' : user,
#         'error' : '''There is no community shed created for your share zone.
#             You can create a community shed for your share zone in the 'Shed' option''',
#             }) 
    
    userTools = Tool.objects.filter(owner=user)
    borrowTransactions = Transaction.objects.filter(borrower=user).filter(status='AC').exclude(status='DA')
    return render(request, 'toolsharesite/toolManagement.html', {
        'tools':userTools,
        'borrowedToolTransactions':borrowTransactions,
#         'shed':communityShed,
        'user' : user
            }) 
    
    
def DeactivateTool(request,id):
    error=''
    msg=''
    tool = Tool.objects.get(id=id)
    if tool.status == 'BO' or tool.status == 'RE':
        error = 'You cannot deactivate a borrowed or reserved tool.'
    elif tool.status == 'DA':
        tool.status='AV'
        msg='Tool activated successfully.'
        tool.save()
    else:
        tool.status='DA'
        msg='Tool deactivated successfully.'
        tool.save()
        
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)
    shareZoneId = user.share_zone_id
    shareZone=ShareZone.objects.get(id=shareZoneId)
#     communityShed = CommunityShed.objects.get(share_zone=shareZone)
    userTools = Tool.objects.filter(owner=user)
    borrowTransactions = Transaction.objects.filter(borrower=user)
    
    return render(request, 'toolsharesite/toolManagement.html', {
            'tools':userTools,
            'borrowedToolTransactions':borrowTransactions,
#             'shed':communityShed,
            'error':error,
            'msg' : msg,
            'user' : user
            })
    
def DeleteTool(request,id):
    error=''
    msg=''
    tool = Tool.objects.get(id=id)
    if tool.status == 'BO' or tool.status == 'RE':
        error = 'You cannot delete a borrowed or reserved tool.'
    else:
        tool.delete()
        msg='Tool deleted successfully.'
        
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)
    shareZoneId = user.share_zone_id
    shareZone=ShareZone.objects.get(id=shareZoneId)
#     communityShed = CommunityShed.objects.get(share_zone=shareZone)
    userTools = Tool.objects.filter(owner=user)
    borrowTransactions = Transaction.objects.filter(borrower=user)
    
    return render(request, 'toolsharesite/toolManagement.html', {
            'tools':userTools,
            'borrowedToolTransactions':borrowTransactions,
#             'shed':communityShed,
            'error':error,
            'msg' : msg,
            'user' : user
            })
        
def RequestTool(request,id):
    error=''
    msg=''
    tool = Tool.objects.get(id=id)
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)
    if request.method=='POST':
        toolBorrowForm = ToolBorrowForm(request.POST)
        if(toolBorrowForm.is_valid()):
            transaction = toolBorrowForm.save(commit=False)
            if transaction.tool_lend_date > transaction.tool_return_date:
                error='End date has to be after start date!'
            elif transaction.tool_lend_date < datetime.today().date():
                error='Start date cannot be in past'
            elif Transaction.objects.filter(borrower=user).filter(tool=tool).filter(status='RJ').count()>0:
                error='You have already been rejected for this tool. You cannot request this tool again'
            else:
                transaction.lender=tool.owner
                transaction.borrower=user
                transaction.tool = tool
                shareZone=ShareZone.objects.get(id=user.share_zone_id)
                transaction.share_zone=shareZone
                
#                 communityShed = CommunityShed.objects.get(share_zone=shareZone)
#                 transaction.community_shed=communityShed
                
                if tool.location == 'S':
                    transaction.status = 'AC'
                    transaction.lender=fetchShedCoordinatorUsingShareZone(shareZone)
                    tool=transaction.tool
                    tool.status='BO'
                    tool.save()
                    msg = 'You have successfully borrowed the tool. Please pick up the tool from Community Shed.'
                    notify.send(user, recipient=tool.owner, verb='User '+user.username+' has borrowed your tool '+tool.name+' from shed')
#                     send notification to user
                else:
                    
                    transaction.status = 'PE'
                    msg='Your borrow request has been submitted to the owner. A decision will be made soon'
                    notify.send(user, recipient=tool.owner, verb='User '+user.username+' has sent a borrow request for tool '+tool.name)
                transaction.save()
                toolList = Tool.objects.filter(share_zone=shareZone)
                
                return render(request, 'toolsharesite/shed.html', {
                    'tools':toolList,
#                     'shedIndicator':True,
                    'msg' : msg,
                    'user' : user
                    })
            
        else:
            error='An error occurred, please try again' 
            
    else:
        result = checkIfAlreadyRequested(user, tool)
        print(result)
        if result:
            print('inside if')
            return ViewToolDetails(request, tool.id, 'You have already sent a borrow request for this tool.')
            
        toolBorrowForm = ToolBorrowForm()
        
    
    return render(request, 'toolsharesite/toolRequest.html',{
        'user':user,
        'toolBorrowForm':toolBorrowForm,
        'error':error,
        'toolId':id,
        })
    
    
def checkIfAlreadyRequested(user,tool):
    transaction = Transaction.objects.filter(borrower=user).filter(tool=tool).filter(status='PE')
    if transaction:
        return True
    else:
        return False
    
def fetchShedCoordinatorUsingShareZone(shareZone):
    communityShed = CommunityShed.getCommunityShedByShareZone(shareZone)
    if communityShed:
        return communityShed.shed_coordinator
    
    
def ManageRequest(request):
    error=''
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)
    shareZone=ShareZone.objects.get(id=user.share_zone_id)
#     communityShed = CommunityShed.objects.get(share_zone=shareZone)
    transaction = Transaction.objects.filter(lender=user).order_by('-created_date')
    return render(request, 'toolsharesite/manageRequests.html',{
        'user':user,
        'transaction':transaction,
        'error':error,
        })

def AcceptRequest(request,id):
    error=''
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)
    transaction = Transaction.objects.get(id=id)
    transaction.status='AC'
#     transaction.tool_lend_date=timezone.now
    transaction.save()
    tool=transaction.tool
    tool.status='BO'
    tool.save();
    shareZone=ShareZone.objects.get(id=user.share_zone_id)
#     communityShed = CommunityShed.objects.get(share_zone=shareZone)
    transactions = Transaction.objects.filter(lender=user).order_by('-created_date')
    borrower=transaction.borrower
    notify.send(user, recipient=borrower, verb='Your borrow request for tool'+tool.name+' has been accepted')
    return render(request, 'toolsharesite/manageRequests.html',{
        'user':user,
        'transaction':transactions,
        'error':error,
        })
    
def RejectRequest(request,id):
    error=''
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)
    transaction = Transaction.objects.get(id=id)
    transaction.status='RJ'
    transaction.save()
    shareZone=ShareZone.objects.get(id=user.share_zone_id)
#     communityShed = CommunityShed.objects.get(share_zone=shareZone)
    transactions = Transaction.objects.filter(lender=user).order_by('-created_date')
    borrower=transaction.borrower
    notify.send(user, recipient=borrower, verb='Your borrow request for tool'+transaction.tool.name+' has been rejected')
    return render(request, 'toolsharesite/manageRequests.html',{
        'user':user,
        'transaction':transactions,
        'error':error,
        })

def UpdateProfile(request):
    error = ''
    msg = ''
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)
    if request.method == "POST":
        form = UpdateProfileForm(data=request.POST, instance=user)
        if form.is_valid():
            newuserdata = form.save(commit=False)
            newuserdata.save()
            msg = 'Profile updated successfully!'
            return render(request, 'toolsharesite/dashboard.html', {
                'user': user,
                'error' : error,
                'msg' : msg
            })
        error='An error occurred, please try again later'
        return render(request,'toolsharesite/UpdateProfile.html',{'form': form,'user':user,'error':error,'msg':msg})
    else:
        form = UpdateProfileForm(initial={'username':user.username,'first_name':user.first_name, 'last_name':user.last_name,'email':user.email,
                                          'address_line1':user.address_line1,'address_line2':user.address_line2,'city':user.city,'state':user.state,
                                          'zip':user.zip,'phone_no':user.phone_no})
        return render(request,'toolsharesite/UpdateProfile.html', {'user':user,'form':form,'error':error,'msg':msg})
    
    
def ViewToolDetails(request,id,error=''):
    print('inside ViewToolDetails')
    msg=''
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)
    tool = Tool.objects.get(id=id)
    community_shed = CommunityShed.getCommunityShedByShareZone(tool.share_zone);

    return render(request, 'toolsharesite/toolDetails.html',{
        'user':user,
#         'toolForm':toolForm,
        'error':error,
        'msg':msg,
        'tool':tool,
        'community_shed':community_shed
        })

def EditTools(request,id):
    print('inside EditToolDetails')
    msg=''
    error=''
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)
    tool = Tool.objects.get(id=id)
    print(tool.name)
    community_shed = CommunityShed.getCommunityShedByShareZone(tool.share_zone);
    if request.method == "POST":
        form = EditToolDetailsForm(data=request.POST, instance = tool)
        if form.is_valid():
            newuserdata = form.save(commit=False)
            newuserdata.save()
            userTools = Tool.objects.filter(owner=user)
            borrowTransactions = Transaction.objects.filter(borrower=user)
            msg = 'Tool details has been edited successfully!'
            return render(request, 'toolsharesite/toolManagement.html', {
                'user': user,
                'tools': userTools,
                'borrowedToolTransactions': borrowTransactions,
                'error': error,
                'msg': msg
            })
        error = 'An error occurred, please try again later'
        return render(request, 'toolsharesite/EditTools.html',
                      {'form': form, 'user': user, 'error': error, 'msg': msg})
    else:
        toolinfo_dict = {'name': tool.name, 'category': tool.category, 'description': tool.description,
                     'condition': tool.condition, 'location': tool.location, 'special_instruction':tool.special_instruction,
                     'pick_up_preference': tool.pick_up_preference}
        form = EditToolDetailsForm(initial=toolinfo_dict)

        return render(request, 'toolsharesite/EditTools.html',{
        'user':user,
        'form':form,
        'error':error,
        'msg':msg,
        'tool':tool,
        'community_shed':community_shed
        })

def ReturnTool(request, id):
    error = ''
    msg = ''
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)
    transaction = Transaction.objects.get(id=id)
    tool = transaction.tool
    lender = transaction.lender
    date = transaction.tool_return_date
    if request.method == "POST":
        form = FeedbackForm(data=request.POST)

        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.transaction = transaction
            transaction.tool_returned_date = datetime.today().date()
            transaction.status = "RE"
            transaction.save()
            feedback = form.save()
            if transaction.tool.location=="H":
                msg = 'Tool returned successfully'
                notify.send(user, recipient=tool.owner, verb='Tool '+tool.name+' has been returned to you by user '+transaction.borrower.username)
            else:
                msg = 'Tool returned successfully. Shed coordinator has been notified.'
                notify.send(user, recipient=tool.owner, verb='Tool '+tool.name+' has been returned to Shed by user '+transaction.borrower.username)
            return render(request, 'toolsharesite/toolManagement.html', {
                'error': error,
                'msg': msg,
                'user': user
            })
        error = 'An error occured, please try again later'
        return render(request, 'toolsharesite/toolReturn.html', {
            'form': form,
            'error': error,
            'msg': msg,
            'user': user,
            'transaction': transaction
        })
    else:
        form = FeedbackForm()
        return render(request, 'toolsharesite/toolReturn.html', {
            'form': form,
            'error': error,
            'msg': msg,
            'user': user,
            'transaction': transaction
        })


def ToolReturnAccept(request, id):
    error = ''
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)
    transaction = Transaction.objects.get(id=id)
    tool = transaction.tool
    tool.status = 'AV'
    tool.save()
    transaction.status = 'CO'
    transaction.save()
    transactions = Transaction.objects.filter(lender=user).order_by('-created_date')
    borrower=transaction.borrower
    notify.send(user, recipient=borrower, verb='Return of tool '+tool.name+' has been acknowledged by user '+user.username)
    return render(request, 'toolsharesite/manageRequests.html', {
        'user': user,
        'transaction': transactions,
        'error': error,
    })


def ViewComment(request, id):
    error = ''
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)
    transaction = Transaction.objects.get(id=id)
    feedback = Feedback.objects.get(transaction_id=id)
    return render(request, 'toolsharesite/viewcomment.html', {
        'user': user,
        'transaction': transaction,
        'feedback': feedback,
        'error': error,
    })

def getNotifications(request):
    error = ''
    msg = ''
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)
#     unreadNotification = user.notifications.unread()
#     readNotification = user.notifications.read()
#     notifications = unreadNotification+readNotification
#     notifications = notifications.order_by('-timestamp')

#     user.notifications.unread().mark_all_as_read()
#     notifications = user.notifications.read().order_by('-timestamp')
    print(user)
    alerts= Notification.objects.unread()
    myalerts = []
    for alert in alerts:
        if(alert.recipient_id==userId):
            myalerts.append(alert)  
            
#     alerts = user.notifications.unread()
    
    print('printing notifications')
    print(alerts)
    return render(request, 'toolsharesite/notification.html', {
        'user': user,
        'notifications': myalerts,
        'msg': msg,
        'error': error,
    })
    
def CommunityStatistics(request):
    error=''
    userId = request.session.get('user_id')
    user = ToolShareUser.objects.get(id=userId)
    shareZone = ShareZone.objects.get(id=user.share_zone_id)
    Top_Tools =Transaction.objects.filter(share_zone=shareZone).values_list('tool__name','tool__owner__username','tool__location').annotate(tool_count=Count('tool__name')).order_by('-tool_count')[:5]
    Top_Borrowers = Transaction.objects.filter(share_zone=shareZone).values_list('borrower__first_name', 'borrower__last_name','borrower__username').annotate(borrow_count=Count('borrower__username')).order_by('-borrow_count')[:5]
    Top_Lenders = Transaction.objects.filter(share_zone=shareZone).values_list('lender__first_name', 'lender__last_name','lender__username').annotate(lend_count=Count('lender__username')).order_by('-lend_count')[:5]
    transactions=Transaction.objects.all()
    print(Top_Tools)
    print(Top_Borrowers)
    print(Top_Lenders)
    return render(request,'toolsharesite/CommunityStatistics.html',
    {
        'topborrowers':Top_Borrowers,
        'toplenders':Top_Lenders,
        'toptools':Top_Tools,
        'transactions':transactions
    })