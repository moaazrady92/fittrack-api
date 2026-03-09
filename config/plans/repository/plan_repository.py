from plans.models import Plan, PlanSubscription
from django.utils import timezone
from datetime import timedelta

class PlanRepository:

    @staticmethod
    def get_active_plans():
        return Plan.objects.filter(is_active=True)

    @staticmethod
    def get_plan_by_id(plan_id):
        return Plan.objects.get(pk=plan_id).first()

    @staticmethod
    def get_coach_plans(coach):
        return Plan.objects.filter(coach=coach)

    @staticmethod
    def get_active_subscription(user,plan):
        return PlanSubscription.objects.filter(
            user=user,
            plan=plan,
            status='ACTIVE'
        ).first()

    @staticmethod
    def create_subscription(user,plan,stripe_subscription_id=None): #empty for now before because stripe payment id is generated after payment succeeds we cant pass
        #something that didn't exist yet
        end_date = timezone.now().date() + timedelta(weeks=plan.duration_weeks)
        subscription = PlanSubscription.objects.create(
            user=user,
            plan=plan,
            stripe_subscription_id=plan.stripe_subscription_id,
            start_date=end_date,
            status='ACTIVE',
        )
        plan.subscriber_count = plan.subscription.filter(status='ACTIVE').count()
        plan.save(update_fields=['subscriber_count'])
        return subscription

    @staticmethod
    def cancel_subscription(subscription):
        subscription.status = 'CANCELED'
        subscription.cancelled_date = timezone.now().date()
        subscription.save(update_fields=['status', 'cancelled_date'])
        plan = subscription.plan
        plan.subscriber_count = plan.subscription.filter(status='ACTIVE').count()
        plan.save(update_fields=['subscriber_count'])
        return subscription