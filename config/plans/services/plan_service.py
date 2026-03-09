from plans.models import PlanSubscription
from plans.repository.plan_repository import PlanRepository


class PlanService:

    @staticmethod
    def purchase_plan(user,plan_id,stripe_subscription_id=None):
        plan = PlanRepository.get_plan_by_id(plan_id)
        if not plan:
            raise ValueError('Plan does not Exist.')

        if PlanRepository.get_active_subscription(plan,user):
            raise ValueError('Already subscribed to this Plan.')

        subscription = PlanRepository.create_subscription(
            user=user,
            plan=plan,
            stripe_subscription_id=stripe_subscription_id
        )
        return subscription

    @staticmethod
    def cancel_plan_subscription(user,subscription_id):
        subscription = PlanSubscription.objects.filter(
            id=subscription_id,
            user=user,
            status='ACTIVE' # to avoid cancelling already cancelled subscription
        ).first()
        if not subscription:
            raise ValueError('No active subscription found.')

        return PlanRepository.cancel_subscription(subscription)
