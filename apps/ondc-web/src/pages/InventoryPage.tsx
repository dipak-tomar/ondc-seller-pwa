import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { inventoryApi } from '@/lib/api';
import { InventoryItem } from '@/types';
import { Package, AlertTriangle } from 'lucide-react';

export default function InventoryPage() {
  const [selectedProduct, setSelectedProduct] = useState<InventoryItem | null>(null);
  const [adjustment, setAdjustment] = useState({ quantity: '', reason: '' });
  const [showDialog, setShowDialog] = useState(false);
  const queryClient = useQueryClient();

  const { data: inventory, isLoading } = useQuery({
    queryKey: ['inventory'],
    queryFn: async () => {
      const response = await inventoryApi.list();
      return response.data;
    },
  });

  const adjustMutation = useMutation({
    mutationFn: inventoryApi.adjust,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['inventory'] });
      queryClient.invalidateQueries({ queryKey: ['products'] });
      setShowDialog(false);
      setAdjustment({ quantity: '', reason: '' });
      setSelectedProduct(null);
    },
  });

  const handleAdjust = () => {
    if (selectedProduct && adjustment.quantity && adjustment.reason) {
      adjustMutation.mutate({
        product_id: selectedProduct.product_id,
        quantity_change: parseInt(adjustment.quantity),
        reason: adjustment.reason,
      });
    }
  };

  const lowStockItems = inventory?.filter((item: InventoryItem) => item.current_stock < 10) || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Inventory</h1>
      </div>

      {lowStockItems.length > 0 && (
        <Card className="border-yellow-200 bg-yellow-50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-yellow-800">
              <AlertTriangle className="w-5 h-5" />
              Low Stock Alert
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-yellow-700">
              {lowStockItems.length} product{lowStockItems.length !== 1 ? 's' : ''} running low on stock
            </p>
          </CardContent>
        </Card>
      )}

      {isLoading ? (
        <div className="text-center py-12">Loading inventory...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {inventory?.map((item: InventoryItem) => (
            <Card key={item.product_id} className={item.current_stock < 10 ? 'border-yellow-200' : ''}>
              <CardHeader>
                <CardTitle className="text-lg flex items-center justify-between">
                  <span className="truncate">{item.product_name}</span>
                  {item.current_stock < 10 && (
                    <AlertTriangle className="w-4 h-4 text-yellow-500 flex-shrink-0" />
                  )}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm text-gray-500">Current Stock</p>
                  <p className="text-3xl font-bold">{item.current_stock}</p>
                </div>
                {item.sku && (
                  <div>
                    <p className="text-sm text-gray-500">SKU</p>
                    <p className="font-medium">{item.sku}</p>
                  </div>
                )}
                <Button
                  variant="outline"
                  className="w-full"
                  onClick={() => {
                    setSelectedProduct(item);
                    setShowDialog(true);
                  }}
                >
                  Adjust Stock
                </Button>
              </CardContent>
            </Card>
          ))}
          {(!inventory || inventory.length === 0) && (
            <div className="col-span-full text-center py-12">
              <Package className="w-12 h-12 mx-auto text-gray-400 mb-4" />
              <p className="text-gray-500">No inventory items found</p>
            </div>
          )}
        </div>
      )}

      <Dialog open={showDialog} onOpenChange={setShowDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Adjust Stock - {selectedProduct?.product_name}</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-500">Current Stock</p>
              <p className="text-2xl font-bold">{selectedProduct?.current_stock}</p>
            </div>

            <div>
              <Label htmlFor="quantity">Quantity Change</Label>
              <Input
                id="quantity"
                type="number"
                placeholder="Enter positive or negative number"
                value={adjustment.quantity}
                onChange={(e) => setAdjustment({ ...adjustment, quantity: e.target.value })}
              />
              <p className="text-xs text-gray-500 mt-1">
                Use positive numbers to add stock, negative to reduce
              </p>
            </div>

            <div>
              <Label htmlFor="reason">Reason</Label>
              <Input
                id="reason"
                placeholder="e.g., Restocked, Damaged, Sold"
                value={adjustment.reason}
                onChange={(e) => setAdjustment({ ...adjustment, reason: e.target.value })}
              />
            </div>

            <Button
              onClick={handleAdjust}
              disabled={!adjustment.quantity || !adjustment.reason || adjustMutation.isPending}
              className="w-full"
            >
              {adjustMutation.isPending ? 'Adjusting...' : 'Adjust Stock'}
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
