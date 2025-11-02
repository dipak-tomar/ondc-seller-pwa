import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { ordersApi } from '@/lib/api';
import { Order } from '@/types';
import { CheckCircle, Clock, Package } from 'lucide-react';

export default function OrdersPage() {
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const queryClient = useQueryClient();

  const { data: orders, isLoading } = useQuery({
    queryKey: ['orders', statusFilter],
    queryFn: async () => {
      const params = statusFilter !== 'all' ? { status: statusFilter } : {};
      const response = await ordersApi.list(params);
      return response.data;
    },
  });

  const confirmMutation = useMutation({
    mutationFn: ordersApi.confirm,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
      alert('Order confirmed successfully!');
    },
  });

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending':
        return <Clock className="w-4 h-4 text-yellow-500" />;
      case 'confirmed':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      default:
        return <Package className="w-4 h-4 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'confirmed':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Orders</h1>
        <Button variant="outline" onClick={() => ordersApi.export()}>
          Export CSV
        </Button>
      </div>

      <div className="flex items-center gap-4">
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-48">
            <SelectValue placeholder="Filter by status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Orders</SelectItem>
            <SelectItem value="pending">Pending</SelectItem>
            <SelectItem value="confirmed">Confirmed</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {isLoading ? (
        <div className="text-center py-12">Loading orders...</div>
      ) : (
        <div className="space-y-4">
          {orders?.map((order: Order) => (
            <Card key={order.id}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">
                    Order #{order.id.slice(0, 8)}
                  </CardTitle>
                  <div className="flex items-center gap-2">
                    {getStatusIcon(order.status)}
                    <span className={`text-xs px-2 py-1 rounded ${getStatusColor(order.status)}`}>
                      {order.status}
                    </span>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  {order.customer_name && (
                    <div>
                      <span className="text-gray-500">Customer:</span>
                      <p className="font-medium">{order.customer_name}</p>
                    </div>
                  )}
                  {order.customer_phone && (
                    <div>
                      <span className="text-gray-500">Phone:</span>
                      <p className="font-medium">{order.customer_phone}</p>
                    </div>
                  )}
                  {order.customer_email && (
                    <div>
                      <span className="text-gray-500">Email:</span>
                      <p className="font-medium">{order.customer_email}</p>
                    </div>
                  )}
                  <div>
                    <span className="text-gray-500">Date:</span>
                    <p className="font-medium">
                      {new Date(order.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>

                <div className="border-t pt-4">
                  <p className="font-medium mb-2">Items:</p>
                  <div className="space-y-2">
                    {order.items.map((item: any, idx: number) => (
                      <div key={idx} className="flex justify-between text-sm">
                        <span>
                          {item.product_name} x {item.quantity}
                        </span>
                        <span className="font-medium">₹{item.total.toFixed(2)}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="border-t pt-4 flex items-center justify-between">
                  <div>
                    <span className="text-gray-500">Total Amount:</span>
                    <p className="text-xl font-bold">₹{order.total_amount.toFixed(2)}</p>
                  </div>
                  {order.status === 'pending' && (
                    <Button
                      onClick={() => confirmMutation.mutate(order.id)}
                      disabled={confirmMutation.isPending}
                    >
                      Confirm Order
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
          {(!orders || orders.length === 0) && (
            <div className="text-center py-12">
              <Package className="w-12 h-12 mx-auto text-gray-400 mb-4" />
              <p className="text-gray-500">No orders found</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
