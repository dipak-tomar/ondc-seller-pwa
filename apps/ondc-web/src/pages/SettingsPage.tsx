import { useQuery, useMutation } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { billingApi } from '@/lib/api';
import { useAuthStore } from '@/store/authStore';
import { CheckCircle, Crown } from 'lucide-react';

export default function SettingsPage() {
  const { user, logout } = useAuthStore();

  const { data: billingStatus } = useQuery({
    queryKey: ['billing-status'],
    queryFn: async () => {
      const response = await billingApi.status();
      return response.data;
    },
  });

  const subscribeMutation = useMutation({
    mutationFn: billingApi.subscribe,
    onSuccess: (response) => {
      window.open(response.data.payment_link, '_blank');
    },
  });

  const plans = [
    {
      name: 'Free',
      price: '₹0',
      features: ['Up to 50 products', 'Basic analytics', 'Email support'],
    },
    {
      name: 'Basic',
      price: '₹499/mo',
      features: ['Up to 500 products', 'Advanced analytics', 'Priority support', 'WhatsApp notifications'],
    },
    {
      name: 'Premium',
      price: '₹999/mo',
      features: ['Unlimited products', 'Real-time analytics', '24/7 support', 'All integrations', 'Custom branding'],
    },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Settings</h1>

      <Card>
        <CardHeader>
          <CardTitle>Account Information</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          {user?.email && (
            <div>
              <span className="text-sm text-gray-500">Email:</span>
              <p className="font-medium">{user.email}</p>
            </div>
          )}
          {user?.phone && (
            <div>
              <span className="text-sm text-gray-500">Phone:</span>
              <p className="font-medium">{user.phone}</p>
            </div>
          )}
          <div>
            <span className="text-sm text-gray-500">Current Plan:</span>
            <p className="font-medium capitalize">{billingStatus?.plan || 'Free'}</p>
          </div>
          <Button variant="outline" onClick={logout} className="mt-4">
            Logout
          </Button>
        </CardContent>
      </Card>

      <div>
        <h2 className="text-2xl font-bold mb-4">Subscription Plans</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {plans.map((plan) => (
            <Card key={plan.name} className={plan.name === 'Premium' ? 'border-blue-500' : ''}>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  {plan.name}
                  {plan.name === 'Premium' && <Crown className="w-5 h-5 text-yellow-500" />}
                </CardTitle>
                <CardDescription>
                  <span className="text-2xl font-bold text-gray-900">{plan.price}</span>
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <ul className="space-y-2">
                  {plan.features.map((feature, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-sm">
                      <CheckCircle className="w-4 h-4 text-green-500 flex-shrink-0 mt-0.5" />
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
                <Button
                  onClick={() => subscribeMutation.mutate(plan.name.toLowerCase())}
                  disabled={billingStatus?.plan === plan.name.toLowerCase() || subscribeMutation.isPending}
                  className="w-full"
                  variant={billingStatus?.plan === plan.name.toLowerCase() ? 'outline' : 'default'}
                >
                  {billingStatus?.plan === plan.name.toLowerCase() ? 'Current Plan' : 'Upgrade'}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
