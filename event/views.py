from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, filters
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now 
from django.db import transaction
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.conf import settings
   
from .models import *
from .serializers import *
from user.permissions import *

class EventCategoryViewSet(viewsets.ModelViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = [
        IsAuthenticated, IsAdminOrEventPlannerOrReadOnly
    ]

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'location']
    ordering_fields = ['date', 'title']
    permission_classes = [
        IsAuthenticated ,IsAdminOrEventPlannerOrReadOnly, IsAdminOrVendorOrReadOnly
    ]
    
    def get_serializer_class(self):
        method = self.request.method
        if method == 'PUT':
            return EventUpdateSerializer
        
        if method == 'PATCH':
            return EventUpdateSerializer
        
        elif method == 'POST':
            return EventCreateSerializer
        
        return EventSerializer
    
class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    ordering_fields = ('id',)
    permission_classes = [
        IsAuthenticated, IsAdminOrVendorOrReadOnly
    ]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Vendor.objects.none()
        
        return Vendor.objects.filter(user=user)
    
class CateringViewSet(viewsets.ModelViewSet):
    queryset = Catering.objects.all()
    serializer_class = CateringSerializer
    ordering_fields = ('id',)
    
    permission_classes = [
        IsAuthenticated, IsAdminOrEventPlannerOrReadOnly
    ]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Catering.objects.none()
        
        return Catering.objects.filter(user=user)

class EventLogisticViewSet(viewsets.ModelViewSet):
    queryset = EventLogistics.objects.all()
    serializer_class = EventLogisticViewSerializer
    permission_classes = [
        IsAuthenticated, IsAdminOrEventPlannerOrReadOnly
    ]
    
    def get_queryset(self):
        user = self.request.user
        return EventLogistics.objects.filter(user=user)
    
    def get_serializer_class(self):
        method = self.request.method
        if method == 'PUT':
            return UpdateEventLogisticSerializer
        
        if method == 'PATCH':
            return UpdateEventLogisticSerializer
        
        if method == 'POST':
            return CreateEventLogisticSerializer
        
        return EventLogisticViewSerializer
    
class EquipmentsViewSet(viewsets.ModelViewSet):
    queryset = Equipments.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [
        IsAuthenticated, IsAdminOrEventPlannerOrReadOnly
    ]
    
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservedEventViewSerializer
    permission_classes = [
        IsAuthenticated, IsAdminOrClientOrReadOnly
    ]
    
    def get_serializer_class(self):
        method = self.request.method
        if method == 'POST':
            return ReserveEventSerializer
        
        return ReservedEventViewSerializer
    
    http_method_names={
        'get', 'post',
    }
    
class CommunicationViewSet(viewsets.ModelViewSet):
    queryset = Communication.objects.all()
    serializer_class = CommunicationSerializer
    permission_classes = [
        IsAuthenticated, IsAdminOrClientOrReadOnly
    ]
    
    http_method_names={
        'get', 'post',
    }

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketViewSerializer
    permission_classes = [
        IsAuthenticated, IsAdminOrClientOrReadOnly
    ]
    
    def get_serializer_class(self):
        method = self.request.method
        if method == 'POST':
            return TicketPurchaseSerializer
        
        return TicketViewSerializer
    
    # http_method_names={
    #     'get', 'post', 'patch',
    # }

class AttendeeViewSet(viewsets.ModelViewSet):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeViewSerializer
    permission_classes = [
        IsAuthenticated, IsAdminOrClientOrReadOnly
    ]
    
    def get_queryset(self):
        user = self.request.user
        return Attendee.objects.filter(user=user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EventAttendeeCreateSerializer
        
        if self.action == 'update':
            return AttendeeUpdateSerializer
        
        if self.action == 'partial_update':
            return AttendeeUpdateSerializer
          
        return AttendeeViewSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        attendees = serializer.save(client=request.user)

        return Response({
            'attendees': AttendeeCreateSerializer(attendees, many=True).data,
        }, status=status.HTTP_201_CREATED)
    
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [
        IsAuthenticated, IsAdminOrClientOrReadOnly
    ]    

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()
    
    @transaction.atomic    
    def create(self, request, *args, **kwargs):
        attendee_id = request.data.get('attendee')
        ticket_id = request.data.get('ticket')

        if Invoice.objects.filter(attendee_id=attendee_id, ticket_id=ticket_id).exists():
            return Response({
                "error": "Invoice with this attendee and ticket already exists."
            }, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'create':
            return InvoiceSerializer
        
        return InvoiceViewSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [
        IsAuthenticated, IsAdminOrClientOrReadOnly
    ]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        amount_paid = serializer.validated_data['amount_paid']
        invoice = serializer.validated_data['invoice']
        
        if amount_paid != invoice.amount:
            raise serializers.ValidationError({
                "error":"Payment amount does not match the invoice amount."
            })
        
        payment = serializer.save(
        )

        attendee_email = payment.attendee.email
        # raise Exception(attendee_email)
        
        payment.invoice.is_paid = True
        payment.invoice.save()
        
        send_mail(
            subject='Payment Confirmation',
            message=f'You have successfully paid Rs. {amount_paid}',
            from_email='mindrisers@gmail.com',
            recipient_list=[
                attendee_email
            ]
        )
        # payment.invoice.delete()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentSerializer
        
        return PaymentViewSerializer
    
    http_method_names={
        'get', 'post'
    }
    
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticated, IsAdminOrClientOrReadOnly
    ]

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        attendee_id = self.request.data.get('attendee')
        
        try:
            attendee = Attendee.objects.get(id=attendee_id, client=user)
            # raise Exception(attendee)
            
        except Attendee.DoesNotExist:
            raise serializers.ValidationError("Attendee not found for the current user.")
        
        serializer.save(attendee=attendee)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewSerializer
        
        return ReviewViewSerializer
    
    http_method_names = {
        'get', 'post'
    }
 
class ReportViewSet(viewsets.ViewSet):    
    @action(detail=False, methods=['get'], url_path='attendance-report')
    def attendance_report(self, request):
        report = self.generate_attendance_report()
        return Response(report)

    @action(detail=False, methods=['get'], url_path='revenue-report')
    def revenue_report(self, request):
        report = self.generate_revenue_report()
        return Response(report)

    @action(detail=False, methods=['get'], url_path='vendor-performance-report')
    def vendor_performance_report(self, request):
        report = self.generate_vendor_performance_report()
        return Response(report)

    def generate_attendance_report(self):
        report = []
        total_event_attendees = 0
        events = Event.objects.all()
        for event in events:
            attendees = Attendee.objects.filter(event=event).count()
            total_event_attendees += attendees

            report.append({
                'event': event.title,
                'date': event.date,
                'attendees': attendees,
            })
            
        report.append({
            'total_event_attendees': total_event_attendees
        })
        
        return report

    def generate_revenue_report(self):
        report = []
        total_event_revenue = 0  
        
        events = Event.objects.all()
        for event in events:
            revenue = Payment.objects.filter(invoice__ticket__event=event).aggregate(
                total=models.Sum('amount_paid')
            )['total'] or 0  
            
            total_event_revenue += revenue

            report.append({
                'event': event.title,
                'date': event.date,
                'revenue': revenue,
            })

        report.append({
            'total_event_revenue': total_event_revenue
        })

        return report

    def generate_vendor_performance_report(self):
        report = []
        vendors = Vendor.objects.all()
        for vendor in vendors:
            associated_events = vendor.event_set.count()
            report.append({
                'vendor': vendor.name,
                'associated_events': associated_events,
            })
        return report