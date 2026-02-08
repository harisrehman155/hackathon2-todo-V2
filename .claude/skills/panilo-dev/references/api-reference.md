# API Reference

Complete API endpoint documentation for Panilo backend.

---

## Base URL

```
Development: http://localhost:3000
Production:  [Configure in .env]
```

---

## Authentication

All protected endpoints require:
```
Authorization: Bearer <access_token>
```

Token is obtained from `/auth/login` response.

---

## Response Format

### Success
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional message"
}
```

### Error
```json
{
  "success": false,
  "message": "Error description"
}
```

---

## Auth Endpoints

### POST /auth/login
Login for Super Admin, Shopkeeper, or Rider.

**Auth**: None

**Request**:
```json
{
  "phone_number": "03048108664",
  "password": "123456"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "full_name": "Admin User",
      "phone_number": "03048108664",
      "role": "SUPER_ADMIN",
      "shop_id": null
    },
    "accessToken": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

---

### POST /auth/customer/login
Customer login (phone + shop, no password).

**Auth**: None

**Request**:
```json
{
  "phone_number": "03001234567",
  "shop_id": 1
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "customer": { ... },
    "shop": { ... },
    "products": [ ... ],
    "riders": [ ... ],
    "accessToken": "..."
  }
}
```

---

### GET /auth/profile
Get current user profile.

**Auth**: Required (any role)

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "full_name": "User Name",
    "phone_number": "03048108664",
    "role": "SUPER_ADMIN",
    "shop_id": null
  }
}
```

---

## Admin Endpoints

**Auth**: Required (SUPER_ADMIN only)

### GET /admin/profile
Get super admin profile.

### GET /admin/verify-session
Verify admin session validity.

---

### GET /admin/shops
List all shops.

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Shop Name",
      "phone": "03001234567",
      "address": "123 Street",
      "city": "Lahore",
      "is_active": 1,
      "created_at": "2024-01-01T00:00:00.000Z",
      "shopkeeper": {
        "id": 2,
        "full_name": "Shopkeeper Name",
        "phone_number": "03009876543"
      }
    }
  ]
}
```

---

### GET /admin/shops/:id
Get shop by ID.

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Shop Name",
    "phone": "03001234567",
    "address": "123 Street",
    "city": "Lahore",
    "is_active": 1,
    "platform_fee_plan_id": 1,
    "shopkeeper": { ... },
    "products": [ ... ],
    "stats": {
      "total_customers": 50,
      "total_riders": 3,
      "total_deliveries": 1200
    }
  }
}
```

---

### POST /admin/shopkeepers
Create new shop with shopkeeper.

**Request**:
```json
{
  "shopName": "New Shop",
  "phone": "03001234567",
  "address": "456 Street",
  "city": "Karachi",
  "platform_fee_plan_id": 1,
  "username": "03009876543",
  "password": "password123",
  "fullName": "Shopkeeper Name",
  "products": [
    {
      "product_name": "19L Bottle",
      "unit_label": "bottle",
      "default_price": 80
    }
  ]
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "shop_id": 5,
    "shopkeeper_id": 10
  },
  "message": "Shopkeeper created successfully"
}
```

---

### PUT /admin/shops/:id
Update shop details.

**Request**:
```json
{
  "name": "Updated Name",
  "phone": "03001234567",
  "address": "New Address",
  "city": "Lahore",
  "platform_fee_plan_id": 2
}
```

---

### DELETE /admin/shops/:id
Deactivate shop (soft delete).

---

### PATCH /admin/shops/:id/status
Toggle shop active/inactive status.

---

### PUT /admin/shops/:shopId/shopkeeper
Update or change shop's shopkeeper.

**Request**:
```json
{
  "full_name": "New Name",
  "phone_number": "03001234567",
  "password": "newpassword"
}
```

---

### GET /admin/lookup/headers
List all lookup headers.

**Response**:
```json
{
  "success": true,
  "data": [
    { "id": 1, "name": "USER_ROLE", "description": "User roles" },
    { "id": 2, "name": "DELIVERY_ENTRY_METHOD", "description": "..." }
  ]
}
```

---

### GET /admin/lookup/details
Get lookup details (paginated).

**Query Params**: `header_id`, `page`, `limit`

---

### POST /admin/lookup/details
Create lookup detail.

**Request**:
```json
{
  "header_id": 2,
  "name": "New Option",
  "key": "NEW_OPTION",
  "value": "new_option",
  "sort_order": 5
}
```

---

### PUT /admin/lookup/details/:id
Update lookup detail.

---

### DELETE /admin/lookup/details/:id
Delete lookup detail.

---

### GET /admin/platform-fee-plans
Get platform fee plans.

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Standard",
      "fee_type": "PERCENTAGE",
      "fee_value": 5,
      "is_active": 1
    }
  ]
}
```

---

## Shop Endpoints

**Auth**: Required (SHOPKEEPER only, with shop ownership)

### POST /shop/customers
Create customer for shop.

**Request**:
```json
{
  "full_name": "Customer Name",
  "phone": "03001234567",
  "address": "Customer Address",
  "assigned_rider_id": 3,
  "default_qty": 2,
  "weekly_days": "1,3,5",
  "product_id": 1,
  "price_per_unit": 80
}
```

---

### GET /shop/customers
List shop's customers.

**Query Params**: `page`, `limit`, `search`, `rider_id`

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "full_name": "Customer Name",
      "phone": "03001234567",
      "address": "Address",
      "assigned_rider": {
        "id": 3,
        "full_name": "Rider Name"
      },
      "default_qty": 2,
      "weekly_days": "1,3,5",
      "price_per_unit": 80
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 50,
    "pages": 3
  }
}
```

---

### GET /shop/customers/:id
Get customer details.

---

### PUT /shop/customers/:id
Update customer.

---

### DELETE /shop/customers/:id
Deactivate customer (soft delete).

---

### POST /shop/riders
Create rider for shop.

**Request**:
```json
{
  "full_name": "Rider Name",
  "phone_number": "03001234567",
  "password": "rider123"
}
```

---

### GET /shop/riders
List shop's riders.

---

### GET /shop/riders/:id
Get rider details.

---

### PUT /shop/riders/:id
Update rider.

---

### DELETE /shop/riders/:id
Deactivate rider.

---

### GET /shop/products
List shop's products.

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "product_name": "19L Bottle",
      "unit_label": "bottle",
      "default_price": 80,
      "is_active": 1
    }
  ]
}
```

---

### POST /shop/batches
Create batch (bottles for rider).

**Request**:
```json
{
  "rider_id": 3,
  "shop_product_id": 1,
  "batch_date": "2024-01-15",
  "bottles_out": 50,
  "notes": "Morning batch"
}
```

---

### GET /shop/batches
List shop's batches.

**Query Params**: `date`, `rider_id`, `status`

---

### GET /shop/batches/:id
Get batch details.

---

### PUT /shop/batches/:id
Update batch (returns, etc.).

**Request**:
```json
{
  "bottles_return_empty": 45,
  "bottles_return_filled": 3,
  "status_id": 2,
  "notes": "2 bottles missing"
}
```

---

### DELETE /shop/batches/:id
Delete batch (same-day only, no deliveries).

---

### GET /shop/riders/:rider_id/batches
Get rider's batches by date.

**Query Params**: `date`

---

### GET /shop/dashboard
Get shop dashboard statistics.

**Response**:
```json
{
  "success": true,
  "data": {
    "total_customers": 50,
    "active_customers": 48,
    "total_riders": 3,
    "today_deliveries": 25,
    "pending_deliveries": 15,
    "monthly_deliveries": 600,
    "revenue_this_month": 48000
  }
}
```

---

## Rider Endpoints

**Auth**: Required (RIDER only)

### GET /rider/customers/:customer_id
Get customer for delivery (QR scan).

**Response**:
```json
{
  "success": true,
  "data": {
    "customer_id": 1,
    "customer_shop_id": 1,
    "full_name": "Customer Name",
    "address": "Customer Address",
    "phone": "03001234567",
    "default_qty": 2,
    "price_per_unit": 80,
    "last_delivery": "2024-01-14"
  }
}
```

---

### GET /rider/orders/today
Get today's pending + completed deliveries.

**Response**:
```json
{
  "success": true,
  "data": {
    "pending": [
      {
        "customer_id": 1,
        "full_name": "Customer Name",
        "address": "Address",
        "default_qty": 2
      }
    ],
    "completed": [
      {
        "delivery_id": 100,
        "customer_id": 2,
        "full_name": "Another Customer",
        "qty_delivered": 3,
        "delivered_at": "2024-01-15T10:30:00.000Z"
      }
    ]
  }
}
```

---

### POST /rider/deliveries
Record delivery entry.

**Request**:
```json
{
  "customer_shop_id": 1,
  "qty_delivered": 2,
  "delivery_date": "2024-01-15",
  "notes": "Left at door"
}
```

---

### GET /rider/deliveries
Get rider's delivery history.

**Query Params**: `from_date`, `to_date`, `page`, `limit`

---

## Customer Endpoints

**Auth**: Required (CUSTOMER only)

### GET /customer/deliveries
Get customer's deliveries.

**Query Params**: `from_date`, `to_date`

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 100,
      "qty_delivered": 2,
      "delivery_date": "2024-01-15",
      "rider_name": "Rider Name",
      "amount": 160
    }
  ]
}
```

---

## Public Endpoints

**Auth**: None

### GET /public/shops
List active shops (for customer app).

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Shop Name",
      "address": "Shop Address",
      "city": "Lahore"
    }
  ]
}
```

---

### GET /public/shops/:id
Get shop by ID (QR code scan).

---

## Lookup Endpoints

**Auth**: None

### GET /lookup
Get lookup by header IDs.

**Query Params**: `headerIds=1,2,3`

**Response**:
```json
{
  "success": true,
  "data": {
    "byId": {
      "1": [ { "id": 1, "name": "ADMIN", "key": "ADMIN" } ]
    },
    "byName": {
      "USER_ROLE": [ { "id": 1, "name": "ADMIN", "key": "ADMIN" } ]
    }
  }
}
```

---

### GET /lookup/by-name
Get lookup by header names.

**Query Params**: `headerNames=USER_ROLE,DELIVERY_METHOD`

---

### GET /lookup/headers
List all lookup headers.

---

## Health Check

### GET /health
Server health check.

**Response**:
```json
{
  "success": true,
  "message": "Server is running"
}
```

---

## Database Tables Reference

### Core Tables

| Table | Purpose |
|-------|---------|
| `users` | Admin, shopkeeper, rider accounts |
| `shops` | Shop profiles |
| `customers` | Customer profiles |
| `customer_shops` | Customer-shop relationship (multi-shop support) |
| `shop_products` | Products per shop |
| `customer_product_plan` | Customer pricing per product |
| `batches` | Bottle batches given to riders |
| `deliveries` | Delivery records |

### Lookup Tables

| Table | Purpose |
|-------|---------|
| `lookup_headers` | Lookup category definitions |
| `lookup_details` | Lookup values |
| `platform_fee_plans` | Fee plan configurations |

### Key Relationships

```
users.shop_id → shops.id
customer_shops.customer_id → customers.id
customer_shops.shop_id → shops.id
customer_shops.assigned_rider_id → users.id (RIDER)
batches.rider_id → users.id (RIDER)
batches.shop_id → shops.id
deliveries.customer_shop_id → customer_shops.id
deliveries.rider_id → users.id (RIDER)
```

---

## Error Codes

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (no/invalid token) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not Found |
| 409 | Conflict (duplicate entry) |
| 429 | Too Many Requests (rate limited) |
| 500 | Internal Server Error |
