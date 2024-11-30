from rest_framework import serializers
from .models import *
from django.db import transaction

''' This is used for all '''
class EventMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'title',
            'event_price'
        ]  

class AttendeeMinimalSerializer(serializers.ModelSerializer):
    event = EventMinimalSerializer(read_only=True)  

    class Meta:
        model = Attendee
        fields = [
            'name',
            'event'
        ] 

#? Used in REservation, Attendee
class AttendeeMinimalSerializer1(serializers.ModelSerializer):
    event = EventMinimalSerializer(read_only=True)  

    class Meta:
        model = Attendee
        fields = [
            'name',
            'address',
            'phone',
            'event'
        ] 

#? Event Category Part
class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = [
            'id',
            'event_name'
        ]       

class VendorSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())     
    class Meta:
        model = Vendor
        fields = [
            'id',
            'user',
            'name',
            'email',
            'address',
            'phone',
            'vendor_fee'
        ]

class EventSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault()) 
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=EventCategory.objects.all(),
        source='category',
        write_only=True
    )
    vendor_id = serializers.PrimaryKeyRelatedField(
        queryset=Vendor.objects.all(),
        source='vendor',
        write_only=True
    )
    category = EventCategorySerializer(read_only=True)
    vendor = VendorSerializer(read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id',
            'user',
            'title',
            'date',
            'location',
            'description',
            'event_price',
            'category_id',
            'category',
            'vendor_id',
            'vendor'
        ]
        
class EventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'vendor',
            'title',
            'date',
            'location',
            'description',
        ]
        
class EventCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault()) 
    class Meta:
        model = Event
        fields = [
            'id',
            'user',
            'category',
            'title',
            'date',
            'location',
            'description',
            'event_price',
            'vendor'
        ]

class CateringSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Catering
        fields = [
            'id',
            'user',
            'name',
            'address',
            'phone',
            'catering_fee'
        ]
        
class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipments
        fields = [
            'id',
            'name',
        ]

#? EventLogistics Part Starts Here        
class CreateEventLogisticSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault()) 
    # raise Exception(user)   
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(),
        source='event'
    )
    
    catering_id = serializers.PrimaryKeyRelatedField(
        queryset=Catering.objects.all(),
        source='catering'
    )
    
    equipment_id = serializers.PrimaryKeyRelatedField(
        queryset=Equipments.objects.all(),
        source='equipments',
        many=True
    )
    
    class Meta:
        model = EventLogistics
        fields = [
            'id',
            'user',
            'event_id',
            'catering_id',
            'equipment_id',
            'transportation',
            'transportation_fee',
            'total_expenses'
        ]
        
    def validate(self, data):
        event = data.get('event')
        catering = data.get('catering')
        
        if EventLogistics.objects.filter(event=event, catering=catering).exists():
            raise serializers.ValidationError({
                'errors':
                "In this event, this catering is already assigned."
            })
        
        return data
     
    @transaction.atomic    
    def create(self, validated_data):
        equipments = validated_data.pop('equipments')
        event_logistics = EventLogistics.objects.create(**validated_data)        
        event_logistics.equipments.set(equipments)
                
        return event_logistics

class UpdateEventLogisticSerializer(serializers.ModelSerializer):  
    class Meta:
        model = EventLogistics
        fields = [
            'id',
            'event',
            'catering',
            'equipments',
            'transportation',
        ]

class EventLogisticViewSerializer(serializers.ModelSerializer): 
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())       
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(),
        source='event',
        write_only=True
    )
    
    catering_id = serializers.PrimaryKeyRelatedField(
        queryset=Catering.objects.all(),
        source='catering',
        write_only=True
    )
    
    equipment_id = serializers.PrimaryKeyRelatedField(
        queryset=Equipments.objects.all(),
        source='equipments',
        many=True,
        write_only=True
    )
    
    event = EventSerializer(read_only=True)
    catering = CateringSerializer(read_only=True)
    equipments = EquipmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = EventLogistics
        fields = [
            'id',
            'user',
            'event_id',
            'event',
            'catering_id',
            'catering',
            'equipment_id',
            'equipments',
            'transportation',
            'transportation_fee',
            'total_expenses'
        ]

#? Attendee Part Starts
class AttendeeViewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault()) 
    event = EventMinimalSerializer(read_only=True) 
    class Meta:
        model = Attendee
        fields = [
            'user_id',
            'user',
            'id',
            'name',
            'address',
            'email',
            'phone',
            'event',
            'registered_at',
            'message'
        ]
        
class AttendeeCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault()) 
    class Meta:
        model = Attendee
        fields = [
            'id',
            'user',
            'name',
            'address',
            'email',
            'phone',
            'event',
            'registered_at',
            'message'
        ]
        
class AttendeeUpdateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault()) 
    phone = serializers.IntegerField(required=False)
    class Meta:
        model = Attendee
        fields = [
            'id',
            'user',
            'email',
            'address',
            'phone',
            'update_message'
        ]

#? EventPart Starts
class EventAttendeeCreateSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    event_id = serializers.IntegerField()
    attendees = AttendeeCreateSerializer(many=True)  
    
    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        event_id = validated_data.get('event_id')
        # raise Exception(event_id)
        attendees_data = validated_data.get('attendees')

        event = Event.objects.get(id=event_id)
        attendee_list = []
        
        for attendee_data in attendees_data:
            attendee_data.pop('event', None)
            attendee = Attendee.objects.create(
                event=event,
                **attendee_data
            )
            attendee_list.append(attendee)

        return attendee_list

#? Communication Part Starts
class CommunicationAttendeeMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = [
            'name',
            'address',
            'phone'
        ]
        
class CommunicationSerializer(serializers.ModelSerializer):
    attendee_details = CommunicationAttendeeMinimalSerializer(source='attendee', read_only=True)
    class Meta:
        model = Communication
        fields = [
            'id',
            'attendee_details',
            'sent_at',
            'message',
            'client_response'
        ]
        
class CommunicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Communication
        fields = [
            'id',
            'attendee',
            'sent_at',
            'message',
            'client_response',
        ]
        
#? Reservation Part Starts                 
class ReservedEventViewSerializer(serializers.ModelSerializer): 
    attendee = AttendeeMinimalSerializer1(read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id',
            'attendee',
            'reserved_at',
            'message'
        ]

class ReserveEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            'id',
            'event',
            'attendee',
            'reserved_at',
            'message'
        ]

#? Ticketing Part Starts
class TicketViewSerializer(serializers.ModelSerializer):    
    attendee = AttendeeMinimalSerializer(read_only=True)
    
    class Meta:
        model = Ticket
        fields = [
            'id',
            'attendee',
            'ticket_type',
            'ticket_number',
            'ticket_quantity',
            'ticket_price',
            'total_price',
            'issued_at',
        ]

class TicketPurchaseSerializer(serializers.ModelSerializer):
    reservation_id = serializers.PrimaryKeyRelatedField(
        queryset=Reservation.objects.all(),
        required=False,
        allow_null=True
    )
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(),
        source='event',
        required=False,
        allow_null=True
    )
    attendee_id = serializers.PrimaryKeyRelatedField(
        queryset=Attendee.objects.all(),
        source='attendee',
        required=False,
        allow_null=True
    )

    class Meta:
        model = Ticket
        fields = [
            'id',
            'reservation_id',
            'attendee_id',
            'event_id',
            'ticket_type',
            'ticket_number',
            'ticket_quantity',
            'ticket_price',
            'issued_at'
        ]
     
    def validate(self, attrs):
        reservation_id = attrs.get('reservation_id', None)
        event = attrs.get('event', None)
        attendee = attrs.get('attendee', None)

        if reservation_id:
            if event or attendee:
                raise serializers.ValidationError(
                    "Event and attendee should not be provided when reservation_id is used."
                )
            
            reservation = Reservation.objects.get(id=reservation_id.id)
            attrs['event'] = reservation.event
            attrs['attendee'] = reservation.attendee
        else:
            if not event or not attendee:
                raise serializers.ValidationError(
                    "Event and attendee are required if no reservation is provided."
                )
        
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        reservation_id = validated_data.pop('reservation_id', None)
        ticket_quantity = validated_data.get('ticket_quantity', 1)  
        
        if reservation_id:
            reservation = Reservation.objects.get(id=reservation_id.id)
            validated_data['event'] = reservation.event
            validated_data['attendee'] = reservation.attendee
            
            reservation.delete()
            
        else:
            validated_data['event'] = validated_data['event']
            validated_data['attendee'] = validated_data['attendee']
        
        existing_ticket = Ticket.objects.filter(
            event=validated_data['event'],
            attendee=validated_data['attendee'],
            ticket_type=validated_data['ticket_type']
        ).first()

        if existing_ticket:
            existing_ticket.ticket_quantity += ticket_quantity
            existing_ticket.save()
            return existing_ticket
        
        return Ticket.objects.create(**validated_data)

''' Ticket Part Ends Here'''

#? Invoice Part Starts
class InvoiceViewSerializer(serializers.ModelSerializer):
    ticket = TicketViewSerializer(read_only=True)
    
    class Meta:
        model = Invoice
        fields = [
            'id',
            'ticket',
            'invoice_number',
            'is_paid',
            'created_at',
            'amount',
        ]
 
#? To create Invoice        
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            'id',
            'attendee',
            'ticket',
            'invoice_number',
            'is_paid',
            'created_at',
            'amount',
        ]
        read_only_fields = ['invoice_number', 'created_at', 'amount']
        
    def validate(self, data):
        attendee = data.get('attendee')
        ticket = data.get('ticket')
        
        if not Ticket.objects.filter(attendee=attendee, id=ticket.id).exists():
            raise serializers.ValidationError({
                "errors":"The provided attendee does not have the specified ticket."
            })

        return data
    
    @transaction.atomic
    def create(self, validated_data):
        invoice_number = f'INV-{validated_data["attendee"].id}-{timezone.now().strftime("%Y%m%d%H%M%S")}'
        
        invoice = Invoice.objects.create(
            invoice_number=invoice_number,
            **validated_data
        )
        return invoice

#? Payment Part Starts
class InvoiceMinimalSerializer(serializers.ModelSerializer):
    attendee = AttendeeMinimalSerializer(read_only=True)  

    class Meta:
        model = Invoice
        fields = [
            'id',
            'attendee',
            'invoice_number',
            'is_paid',
            'amount',
            'created_at'
        ] 

#? Payment Part Starts         
class PaymentViewSerializer(serializers.ModelSerializer):
    invoice = InvoiceMinimalSerializer(read_only=True)        
    class Meta:
        model = Payment
        fields = [
            'id',
            'invoice',
            'payment_mode',
            'amount_paid',
            'payment_date'
        ]

class PaymentSerializer(serializers.ModelSerializer):
    invoice_id = serializers.PrimaryKeyRelatedField(
        queryset=Invoice.objects.all(), 
        source='invoice', 
        write_only=True
    )
    attendee_id = serializers.PrimaryKeyRelatedField(
        queryset=Attendee.objects.all(), 
        source='attendee', 
        write_only=True
    )
    
    def validate(self, data):
        attendee = data.get('attendee')
        invoice = data.get('invoice')
        
        if not Invoice.objects.filter(attendee=attendee, id=invoice.id).exists():
            raise serializers.ValidationError({
                "errors":"The provided attendee does not have the specified invoice."
            })
        
        if Payment.objects.filter(attendee=attendee, invoice=invoice).exists():
            raise serializers.ValidationError({
                "errors": "This invoice has already been paid by this attendee."
            })

        return data
    
    class Meta:
        model = Payment
        fields = [
            'id',
            'attendee_id',
            'invoice_id',
            'payment_mode',
            'amount_paid',
            'payment_date'
        ]
        read_only_fields = ['payment_date']

#? Review Part Starts
class ReviewViewSerializer(serializers.ModelSerializer):
    attendee = AttendeeMinimalSerializer(read_only=True)
    class Meta:
        model = Review
        fields = [
            'id',
            'attendee',
            'rating',
            'feedback',
            'reviewed_at'
        ]
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id',
            'attendee',
            'event',
            'rating',
            'feedback',
            'reviewed_at'
        ]

    def validate(self, data):
        event = data.get('event')
        attendee = data.get('attendee')
        # raise Exception(event, attendee)

        if not Ticket.objects.filter(attendee=attendee, event=event).exists():
            raise serializers.ValidationError({
                'errors': ['You can only review events you have purchased tickets for.']
            })

        if Review.objects.filter(attendee=attendee, event=event).exists():
            raise serializers.ValidationError({
                'errors': ['You have already reviewed this event.']
            })
                
        return data