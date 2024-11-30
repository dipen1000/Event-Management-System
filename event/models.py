from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from random import randint

User = get_user_model()

class EventCategory(models.Model):
    CONFERENCE = 'Conference'
    WEDDING = 'Wedding'
    PARTY = 'Party'
    RECEPTION = 'Reception'
    CONCERT = 'Concert'
    OTHER = 'Other'
    
    CATEGORY_CHOICES = [
        (CONFERENCE, 'CONFERENCE'),
        (WEDDING, 'WEDDING'),
        (PARTY, 'PARTY'),
        (RECEPTION, 'RECEPTION'),
        (CONCERT, 'CONCERT'),
        (OTHER, 'OTHER'),
    ]
    event_name = models.CharField(max_length=10, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.event_name

class Vendor(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=30)
    phone = models.IntegerField()
    vendor_fee = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Event(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)  
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(EventCategory, related_name='events', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property    
    def event_price(self) -> int:
        if self.category.event_name == 'Wedding':
            return 500
        
        elif self.category.event_name == 'Conference':
            return 1000
        
        elif self.category.event_name == 'Concert':
            return 2000
        
        elif self.category.event_name == 'Party':
            return 500   
        
        elif self.category.event_name == 'Reception':
            return 1500
        
        else: 
            return 100
        
    def __str__(self):
        return self.title

class Catering(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    phone = models.PositiveIntegerField()
    catering_fee = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Equipments(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class EventLogistics(models.Model):
    BUS = 'Bus'
    CAR = 'Car'
    VAN = 'Van'
    SCORPIO = 'Scorpio'
    
    TRANSPORTATION_CHOICES = [
        ('BUS', BUS),
        ('CAR', CAR),
        ('VAN', VAN),
        ('SCORPIO', SCORPIO),
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    catering = models.ForeignKey(Catering, on_delete=models.CASCADE)
    equipments = models.ManyToManyField(Equipments)
    transportation = models.CharField(max_length=9, choices=TRANSPORTATION_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    @property
    def transportation_fee(self):
        if self.transportation == 'BUS':
            return 500
        
        elif self.transportation == 'VAN':
            return 1000
        
        elif self.transportation == 'CAR':
            return 1000
        
        else:
            return 1500
        
    @property
    def total_expenses(self):
        expenses = self.event.event_price + self.transportation_fee + self.catering.catering_fee + self.event.vendor.vendor_fee 
        return expenses
    
    def __str__(self):
        return self.event.title
    
class Attendee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.PositiveIntegerField()
    event = models.ForeignKey(Event, related_name='attendees', on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    def message(self) -> str:
        return 'Attendee Successfully Registered.'
    
    def update_message(self) -> str:
        return 'Attendee Successfully Updated.'
    
    def __str__(self):
        return f'{self.name} - {self.event.title}'
    
class Communication(models.Model):
    attendee = models.ForeignKey(Attendee, related_name='communications', on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def client_response(self) -> str:
        return 'Thankyou for your time we are looking forward to it.'

    def __str__(self):
        return f'{self.attendee.name} - {self.sent_at}'

class Reservation(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  

    def message(self) -> str:
        return 'You have successfully reserved your event.'
    
class Ticket(models.Model):  
    VIP = 'Vip'
    GENERAL = 'General'
    
    TICKET_TYPE_CHOICES = [
        ('VIP', VIP),
        ('GENERAL', GENERAL),
    ]
    
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE,  null=True, blank=True)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='tickets', on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=10, choices=TICKET_TYPE_CHOICES, default=GENERAL)
    ticket_number = models.CharField(max_length=100, unique=True)
    ticket_quantity = models.PositiveIntegerField(default=1)
    issued_at = models.DateTimeField(auto_now_add=True)
    
    def ticket_number(self):
        get_ticket_number = randint(0000,9999)
        
        return get_ticket_number
    
    @property
    def event_price(self) -> int:
        return self.event.event_price

    @property
    def ticket_price(self) -> int:
        if self.ticket_type == 'VIP':
            return 500
        else:
            return 0
    
    @property
    def total_price(self) -> int:
        if self.ticket_type == 'VIP':
            return self.ticket_price + self.event_price
        
        else:
            return self.event_price        
    
    def __str__(self):
        return f'{self.ticket_type} - {self.event.title} - {self.attendee.user.username}'

class Invoice(models.Model):
    attendee = models.ForeignKey('Attendee', on_delete=models.CASCADE)
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50, unique=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('attendee', 'ticket')  
    
    @property
    def amount(self):
        return self.ticket.total_price
    
    def __str__(self):
        return f"Invoice {self.id} for {self.attendee}"

class Payment(models.Model):
    ESEWA = 'Esewa'
    KHALTI = 'Khalti'
    IMEPAY = 'ImePay'
    BANK_TRANSFER = 'BankTransfer'
    OTHER = 'Other'
    
    PAYMENT_MODE_CHOICES = [
        ('ESEWA', ESEWA),
        ('KHALTI', KHALTI),
        ('IMEPAY', IMEPAY),
        ('BANK_TRANSFER', BANK_TRANSFER),
        ('OTHER', OTHER),
    ]
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_mode = models.CharField(max_length=15, choices=PAYMENT_MODE_CHOICES, default=ESEWA)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('attendee', 'invoice')  

    def __str__(self):
        return f"Payment {self.attendee} for Invoice {self.invoice.id}"
    
class Review(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField() 
    feedback = models.TextField()  
    reviewed_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f'Review by {self.attendee.name} for {self.event.title}'