from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from fileinput import filename


class ShareZone(models.Model):
    zipcode = models.IntegerField()
    created_date = models.DateField(default=timezone.now)
    
#     def __init__(self,zipc):
#         super(ShareZone,self).__init__()
#         self.zipcode=zipc
    
    @staticmethod
    def getShareZoneByZipcode(userZipcode):
        try:
            return ShareZone.objects.get(zipcode=userZipcode)
        except ShareZone.DoesNotExist:
            return None
        
class Role(models.Model):
    role_name = models.CharField(max_length=50)
    created_date = models.DateField(default=timezone.now)
    updated_date = models.DateField(default=timezone.now)

class ToolShareUser(User):
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length = 50)
#     email = models.CharField(max_length = 100)
    address_line1 = models.CharField(max_length = 100)
    address_line2 = models.CharField(max_length = 100,null=True,blank=True)
    city = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)
    zip = models.IntegerField()
    phone_no = models.BigIntegerField()
    created_date = models.DateField(null=True,blank=True,default=timezone.now)
    updated_date = models.DateField(null=True,blank=True,default=timezone.now)
    share_zone = models.ForeignKey(ShareZone,null=True,blank=True)
    roles=(
        ('US','User'),
        ('SC','Shed Coordinator'),
        ('AD','Admin')
        )
    role = models.CharField(max_length=2,choices=roles,default='US')
#     pickUpPref = models.CharField(max_length = 100)


class CommunityShed(models.Model):
    share_zone = models.ForeignKey(ShareZone,null=True,blank=True)
    address_line1 = models.CharField(max_length = 100)
    address_line2 = models.CharField(max_length = 100,null=True,blank=True)
    city = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)
    zip = models.IntegerField()
    shed_coordinator = models.ForeignKey(ToolShareUser,null=True,blank=True)
    created_date = models.DateField(default=timezone.now)
    updated_date = models.DateField(default=timezone.now)
    
    @staticmethod
    def getCommunityShedByShareZone(shareZone):
        try:
            return CommunityShed.objects.get(share_zone=shareZone)
        except CommunityShed.DoesNotExist:
            return None 
    

class Category(models.Model):
    type = models.TextField()
    created_date = models.DateField(default=timezone.now)
    updated_date = models.DateField(default=timezone.now)
    
def upload_location(instance,filename):
    return 'user_{0}/{1}'.format(instance.owner.id, filename)

class Tool(models.Model):
    name = models.CharField(max_length=200)
    categoryList = (
        ('OT','Other'),
        ('CV','Clamps & Vises'),
        ('AC','Air Compressors'),
        ('FT','Fastener Tools'),
        ('HT','Hand Tools'),
        ('KS','Knives, Blades & Sharpeners'),
        ('LT','Layout & Measuring Tools'),
        ('FL','Flashlights & Portable Lighting'),
        ('PT','Power Tools'),
        ('PE','Protective & Safety Equipment'),
        ('TS','Tool Holders & Storage'),
        ('WV','Wet/Dry Vacuums'),
        ('WS','Work Benches & Sawhorses'),
        ('TS','Tile Saws'),
    )
    category = models.CharField(max_length=2,choices=categoryList,default='OT')
    description = models.CharField(max_length=500)
    owner = models.ForeignKey(ToolShareUser,null=True,blank=True)
    share_zone = models.ForeignKey(ShareZone,null=True,blank=True)
#     community_shed = models.ForeignKey(CommunityShed,null=True,blank=True)
    created_date = models.DateField(default=timezone.now)
    updated_date = models.DateField(default=timezone.now)
    active = models.BooleanField(default=True)
    statusList = (
        ('AV','Available'),
        ('BO','Borrowed'),
        ('DA','Deactivated'),
        ('RE','Reserved')
    )
    status = models.CharField(max_length=2,choices=statusList,default='AV')
#     image = models.ImageField(upload_to='uploads/')
    image = models.ImageField(upload_to='documents/',
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    height_field=models.IntegerField(default=0)
    width_field=models.IntegerField(default=0)
    
    locationList = (
        ('H','Home'),
        ('S','Community Shed')
    )
    location = models.CharField(max_length=1,choices=locationList,default='H')
    conditionList = (
        ('G','Good'),
        ('A','Average'),
        ('B','Bad')
    )
    condition = models.CharField(max_length=1,choices=conditionList,default='G')
    special_instruction = models.CharField(max_length=500,null=True,blank=True)
    pick_up_preference = models.CharField(max_length = 100)
    
    @staticmethod
    def getToolsByCommunityShedId(commShedId):
        return Tool.objects.filter(community_shed_id=commShedId)
    


class Transaction(models.Model):
    created_date = models.DateField(default=timezone.now)
    updated_date = models.DateField(default=timezone.now)
    lender = models.ForeignKey(ToolShareUser,related_name='lender',null=True,blank=True)
    borrower = models.ForeignKey(ToolShareUser,related_name='borrower',null=True,blank=True)
    tool = models.ForeignKey(Tool,null=True,blank=True)
    borrow_days = models.IntegerField(default=0)
    borrow_message = models.CharField(max_length=200)
    tool_lend_date = models.DateField(default=timezone.now)
    tool_return_date = models.DateField(default=timezone.now)
    tool_returned_date = models.DateField(null=True,blank=True)
    transactionStatusList = (
        ('PE','Pending'),
        ('AC','Accepted'),
        ('RJ','Rejected'),
        ('RE','Released'),
        ('CO','Complete')
    )
    status = models.CharField(max_length=2,choices=transactionStatusList,default='PE')
#     community_shed=models.ForeignKey(CommunityShed,null=True,blank=True)
    share_zone = models.ForeignKey(ShareZone,null=True,blank=True)


class Feedback(models.Model):
    user=models.ForeignKey(ToolShareUser,null=True,blank=True)
    objects = models.Manager()
    user = models.ForeignKey(ToolShareUser, null=True, blank=True)
    tool = models.ForeignKey(Tool,null=True,blank=True)
    comment = models.CharField(max_length=500,null=True,blank=True)
    created_date = models.DateField(default=timezone.now)
    updated_date = models.DateField(default=timezone.now)
    transaction = models.ForeignKey(Transaction, null=True, blank=True)
    
