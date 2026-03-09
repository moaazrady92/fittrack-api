from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from plans.models import Plan
from .serializers import PlanSerializer , PlanDetailSerializer
from users.permissons import IsCoachOrReadOnly
from plans.services.plan_service import PlanService

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.filter(is_active=True)
    serializer_class = PlanSerializer
    permission_classes = [IsCoachOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['plan_type','difficulty','is_featured']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PlanDetailSerializer
        return PlanSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role.is_coach():
            if self.action in ['update','partial_update','destroy']: #only coaches can edit,delete,update their own plans others can only see them
                return Plan.objects.filter(coach=user)
        return Plan.objects.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(coach=self.request.user) #automatically sets the user's name when creating a plan


    @action(detail=True, methods=['get'],permission_classes=[IsAuthenticated])
    def purchase(self,request,pk=None):
        user = request.user
        try:
            subscription = PlanService.purchase_subscription(user,plan_id=pk)
            return Response({
                'message' : 'Purchased successfully',
                'subscription_id' : subscription.id,
                'plan' : subscription.plan.id,
                'checkout_url' : '/api/stripe/create-checkout'
            })
        except ValueError as e:
            return Response({'error': str(e)},status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'] , permission_classes=[IsAuthenticated])
    def my_plan(self,request):
        user = request.user
        if user.role.is_coach():
            return Response({
                'error' : 'Only Coaches can access this. '
            },status=status.HTTP_403_FORBIDDEN)
        plans = Plan.objects.filter(coach=user)
        serializer= PlanSerializer(plans,many=True)
        return Response(serializer.data)