export interface Product {
  id: string;
  store_id: string;
  name: string;
  description?: string;
  sku?: string;
  hsn_code?: string;
  price: number;
  mrp: number;
  stock: number;
  category?: string;
  images: string[];
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Order {
  id: string;
  store_id: string;
  customer_name?: string;
  customer_phone?: string;
  customer_email?: string;
  total_amount: number;
  status: string;
  items: OrderItem[];
  created_at: string;
  updated_at: string;
}

export interface OrderItem {
  product_id: string;
  product_name: string;
  quantity: number;
  price: number;
  total: number;
}

export interface InventoryItem {
  product_id: string;
  product_name: string;
  current_stock: number;
  sku?: string;
}

export interface SalesDataPoint {
  date: string;
  sales: number;
  orders: number;
}

export interface TopProduct {
  product_id: string;
  product_name: string;
  total_sales: number;
  units_sold: number;
}
