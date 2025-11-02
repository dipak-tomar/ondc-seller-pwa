# ONDC Seller PWA API Contract

## Authentication

### POST /api/v1/auth/request-otp
Request OTP for login.

**Request:**
```json
{
  "email": "user@example.com",
  "phone": "+919876543210"
}
```

**Response:**
```json
{
  "message": "OTP sent successfully",
  "otp": "123456"
}
```

### POST /api/v1/auth/verify-otp
Verify OTP and get access token.

**Request:**
```json
{
  "email": "user@example.com",
  "otp": "123456"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

## Products

### GET /api/v1/products
List all products for the authenticated user's store.

**Query Parameters:**
- `category` (optional): Filter by category
- `search` (optional): Search by product name
- `in_stock` (optional): Filter by stock availability

**Response:**
```json
[
  {
    "id": "uuid",
    "store_id": "uuid",
    "name": "Product Name",
    "description": "Product description",
    "sku": "SKU123",
    "hsn_code": "1234",
    "price": 100.0,
    "mrp": 120.0,
    "stock": 50,
    "category": "Electronics",
    "images": ["https://..."],
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### POST /api/v1/products
Create a new product.

**Request:**
```json
{
  "name": "Product Name",
  "description": "Product description",
  "sku": "SKU123",
  "hsn_code": "1234",
  "price": 100.0,
  "mrp": 120.0,
  "stock": 50,
  "category": "Electronics"
}
```

### POST /api/v1/products/bulk
Bulk upload products via CSV.

**Request:** Multipart form data with CSV file

**Response:**
```json
{
  "message": "Uploaded 100 products",
  "products_created": 100,
  "errors": []
}
```

## Images

### POST /api/v1/images/presign
Get presigned URL for image upload.

**Request:**
```json
{
  "product_id": "uuid",
  "filename": "image.jpg"
}
```

**Response:**
```json
{
  "upload_url": "https://...",
  "object_key": "products/uuid/image.jpg",
  "image_url": "https://..."
}
```

### POST /api/v1/images/products/{product_id}/upload
Upload product image directly.

**Request:** Multipart form data with image file

**Response:**
```json
{
  "message": "Image uploaded successfully",
  "image_url": "https://...",
  "product_id": "uuid"
}
```

## Orders

### GET /api/v1/orders
List all orders.

**Query Parameters:**
- `status` (optional): Filter by order status

**Response:**
```json
[
  {
    "id": "uuid",
    "store_id": "uuid",
    "customer_name": "John Doe",
    "customer_phone": "+919876543210",
    "customer_email": "john@example.com",
    "total_amount": 1000.0,
    "status": "pending",
    "items": [...],
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### POST /api/v1/orders/{order_id}/confirm
Confirm an order and update inventory.

**Response:**
```json
{
  "message": "Order confirmed",
  "order_id": "uuid"
}
```

## Webhooks

### POST /api/v1/webhooks/ondc/order
Handle ONDC order webhooks.

### POST /api/v1/webhooks/ondc/catalog
Handle ONDC catalog webhooks.

### POST /api/v1/webhooks/payment/razorpay
Handle Razorpay payment webhooks.

## Pricing Rules

### GET /api/v1/pricing-rules
List all pricing rules.

### POST /api/v1/pricing-rules
Create a new pricing rule.

**Request:**
```json
{
  "name": "Bulk Discount",
  "rule_type": "bulk",
  "discount_percentage": 10.0,
  "conditions": {
    "min_quantity": 10
  }
}
```

## Analytics

### GET /api/v1/analytics/sales
Get sales analytics.

**Query Parameters:**
- `days` (optional, default: 30): Number of days to analyze

### GET /api/v1/analytics/top-products
Get top selling products.

**Query Parameters:**
- `limit` (optional, default: 10): Number of products to return
