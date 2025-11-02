import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { productsApi } from '@/lib/api';
import { Product } from '@/types';
import { Plus, Upload, Search, Package } from 'lucide-react';
import ProductForm from '@/components/features/ProductForm';
import CSVUpload from '@/components/features/CSVUpload';

export default function ProductsPage() {
  const [search, setSearch] = useState('');
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [showCSVDialog, setShowCSVDialog] = useState(false);
  const queryClient = useQueryClient();

  const { data: products, isLoading } = useQuery({
    queryKey: ['products', search],
    queryFn: async () => {
      const response = await productsApi.list({ search });
      return response.data;
    },
  });

  const syncMutation = useMutation({
    mutationFn: productsApi.sync,
    onSuccess: () => {
      alert('Products synced to ONDC successfully!');
    },
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Products</h1>
        <div className="flex gap-2">
          <Dialog open={showCSVDialog} onOpenChange={setShowCSVDialog}>
            <DialogTrigger asChild>
              <Button variant="outline">
                <Upload className="w-4 h-4 mr-2" />
                Import CSV
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Import Products from CSV</DialogTitle>
              </DialogHeader>
              <CSVUpload onSuccess={() => {
                setShowCSVDialog(false);
                queryClient.invalidateQueries({ queryKey: ['products'] });
              }} />
            </DialogContent>
          </Dialog>

          <Dialog open={showAddDialog} onOpenChange={setShowAddDialog}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="w-4 h-4 mr-2" />
                Add Product
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-2xl max-h-screen overflow-y-auto">
              <DialogHeader>
                <DialogTitle>Add New Product</DialogTitle>
              </DialogHeader>
              <ProductForm onSuccess={() => {
                setShowAddDialog(false);
                queryClient.invalidateQueries({ queryKey: ['products'] });
              }} />
            </DialogContent>
          </Dialog>

          <Button onClick={() => syncMutation.mutate()} disabled={syncMutation.isPending}>
            Sync to ONDC
          </Button>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
          <Input
            placeholder="Search products..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      {isLoading ? (
        <div className="text-center py-12">Loading products...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {products?.map((product: Product) => (
            <Card key={product.id}>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="truncate">{product.name}</span>
                  {product.stock < 10 && (
                    <span className="text-xs bg-red-100 text-red-600 px-2 py-1 rounded">
                      Low Stock
                    </span>
                  )}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Price:</span>
                  <span className="font-medium">₹{product.price}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">MRP:</span>
                  <span className="font-medium">₹{product.mrp}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Stock:</span>
                  <span className="font-medium">{product.stock} units</span>
                </div>
                {product.sku && (
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">SKU:</span>
                    <span className="font-medium">{product.sku}</span>
                  </div>
                )}
                {product.category && (
                  <div className="text-xs text-gray-500 mt-2">
                    Category: {product.category}
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
          {(!products || products.length === 0) && (
            <div className="col-span-full text-center py-12">
              <Package className="w-12 h-12 mx-auto text-gray-400 mb-4" />
              <p className="text-gray-500">No products found</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
