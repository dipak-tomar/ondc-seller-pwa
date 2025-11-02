import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { productsApi } from '@/lib/api';
import { useOfflineStore } from '@/store/offlineStore';

interface ProductFormProps {
  onSuccess: () => void;
}

export default function ProductForm({ onSuccess }: ProductFormProps) {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    sku: '',
    hsn_code: '',
    price: '',
    mrp: '',
    stock: '',
    category: '',
  });

  const { isOnline, addDraft } = useOfflineStore();

  const createMutation = useMutation({
    mutationFn: productsApi.create,
    onSuccess: () => {
      onSuccess();
    },
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const productData = {
      ...formData,
      price: parseFloat(formData.price),
      mrp: parseFloat(formData.mrp),
      stock: parseInt(formData.stock),
      images: [],
    };

    if (!isOnline) {
      await addDraft(productData);
      alert('Product saved as draft (offline)');
      onSuccess();
      return;
    }

    createMutation.mutate(productData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <Label htmlFor="name">Product Name *</Label>
        <Input
          id="name"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          required
        />
      </div>

      <div>
        <Label htmlFor="description">Description</Label>
        <Textarea
          id="description"
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          rows={3}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="sku">SKU</Label>
          <Input
            id="sku"
            value={formData.sku}
            onChange={(e) => setFormData({ ...formData, sku: e.target.value })}
          />
        </div>

        <div>
          <Label htmlFor="hsn_code">HSN Code</Label>
          <Input
            id="hsn_code"
            value={formData.hsn_code}
            onChange={(e) => setFormData({ ...formData, hsn_code: e.target.value })}
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="price">Price *</Label>
          <Input
            id="price"
            type="number"
            step="0.01"
            value={formData.price}
            onChange={(e) => setFormData({ ...formData, price: e.target.value })}
            required
          />
        </div>

        <div>
          <Label htmlFor="mrp">MRP *</Label>
          <Input
            id="mrp"
            type="number"
            step="0.01"
            value={formData.mrp}
            onChange={(e) => setFormData({ ...formData, mrp: e.target.value })}
            required
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="stock">Stock *</Label>
          <Input
            id="stock"
            type="number"
            value={formData.stock}
            onChange={(e) => setFormData({ ...formData, stock: e.target.value })}
            required
          />
        </div>

        <div>
          <Label htmlFor="category">Category</Label>
          <Input
            id="category"
            value={formData.category}
            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
          />
        </div>
      </div>

      {!isOnline && (
        <div className="bg-yellow-50 border border-yellow-200 rounded p-3 text-sm text-yellow-800">
          You are offline. Product will be saved as draft.
        </div>
      )}

      <Button type="submit" disabled={createMutation.isPending} className="w-full">
        {createMutation.isPending ? 'Creating...' : isOnline ? 'Create Product' : 'Save as Draft'}
      </Button>
    </form>
  );
}
