from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()

router.register('events', EventViewSet)
router.register('categories', EventCategoryViewSet)
router.register('vendors', VendorViewSet, basename='vendor')
router.register('event_logistics', EventLogisticViewSet, basename='event_logistic')
router.register('caterings', CateringViewSet, basename='catering')
router.register('equipments', EquipmentsViewSet, basename='equipments')

router.register('attendees', AttendeeViewSet)
router.register('communications', CommunicationViewSet)
router.register('ticketings', TicketViewSet)
router.register('reservations', ReservationViewSet)
router.register('invoices', InvoiceViewSet)
router.register('receipts', PaymentViewSet, basename='receipt')
router.register('reviews', ReviewViewSet, basename='review')
router.register('reports', ReportViewSet, basename='reports')

urlpatterns = [

]+router.urls