# Backend Patterns Reference

Detailed patterns for Panilo backend development (Express/MySQL/JWT).

---

## Directory Structure

```
backend/src/
├── app.js                    # Entry point, middleware setup, route mounting
├── config/
│   ├── config.js             # Environment variables export
│   └── database.js           # MySQL pool configuration
├── controllers/              # Request handlers (business logic)
│   ├── auth.controller.js    # Login for all roles
│   ├── admin.controller.js   # Super admin operations
│   ├── shop.controller.js    # Shopkeeper operations
│   ├── rider.controller.js   # Rider delivery operations
│   ├── customer.controller.js # Customer-facing operations
│   ├── lookup.controller.js  # Configuration data
│   └── public.controller.js  # No-auth endpoints
├── models/                   # Data access layer
│   ├── User.js               # Users (admin, shopkeeper, rider)
│   ├── Shop.js               # Shop profiles
│   ├── Customer.js           # Customer profiles
│   ├── Batch.js              # Delivery batches
│   └── CustomerPricing.js    # Price history
├── routes/                   # Route definitions
│   ├── auth.routes.js
│   ├── admin.routes.js
│   ├── shop.routes.js
│   ├── rider.routes.js
│   ├── customer.routes.js
│   ├── lookup.routes.js
│   └── public.routes.js
├── middlewares/
│   ├── auth.middleware.js    # JWT verification, role auth
│   ├── security.middleware.js # Security headers
│   └── rateLimit.middleware.js # Login rate limiting
├── validations/
│   └── auth.validation.js    # Joi schemas
└── utils/
    ├── error.util.js         # Global error handler
    ├── cache.util.js         # In-memory cache
    └── lookup.util.js        # Lookup helpers
```

---

## Database Connection

```javascript
// config/database.js
const mysql = require('mysql2/promise');
const config = require('./config');

const pool = mysql.createPool({
  host: config.db.host,
  user: config.db.user,
  password: config.db.password,
  database: config.db.database,
  port: config.db.port,
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

module.exports = { pool };
```

**Usage**: Always use `pool.query()` for queries. Never create individual connections.

---

## Authentication Middleware Chain

### Order of Middleware (IMPORTANT)

```javascript
// For SHOPKEEPER routes:
router.use(authenticate);              // 1. Verify JWT token
router.use(authorize('SHOPKEEPER'));   // 2. Check role
router.use(verifyShopOwnership);       // 3. Verify shop access

// For SUPER_ADMIN routes:
router.use(authenticate);
router.use(authorize('SUPER_ADMIN'));
// No shop ownership check needed

// For RIDER routes:
router.use(authenticate);
router.use(authorize('RIDER'));
// Shop ID available in req.user.shop_id
```

### authenticate Middleware

```javascript
const authenticate = async (req, res, next) => {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader?.startsWith('Bearer ')) {
      return res.status(401).json({ success: false, message: 'No token provided' });
    }

    const token = authHeader.split(' ')[1];
    const decoded = jwt.verify(token, config.jwt.secret);

    // Cache check (5-min TTL)
    const cacheKey = `user:${decoded.id}`;
    let user = cache.get(cacheKey);

    if (!user) {
      user = await User.findById(decoded.id);
      if (user) cache.set(cacheKey, user);
    }

    if (!user || !user.is_active) {
      return res.status(401).json({ success: false, message: 'User not found or inactive' });
    }

    // CRITICAL: Verify token role matches DB role
    if (decoded.role !== user.role) {
      return res.status(403).json({ success: false, message: 'Role mismatch' });
    }

    req.user = { id: user.id, role: user.role, shop_id: user.shop_id, ... };
    next();
  } catch (error) {
    return res.status(401).json({ success: false, message: 'Invalid token' });
  }
};
```

### authorize Middleware

```javascript
const authorize = (...allowedRoles) => {
  return (req, res, next) => {
    if (!allowedRoles.includes(req.user.role)) {
      return res.status(403).json({ success: false, message: 'Access denied' });
    }
    next();
  };
};
```

### verifyShopOwnership Middleware

```javascript
const verifyShopOwnership = async (req, res, next) => {
  if (req.user.role !== 'SHOPKEEPER') return next();

  const shopIdFromToken = req.user.shop_id;
  const user = await User.findById(req.user.id);

  if (user.shop_id !== shopIdFromToken) {
    return res.status(403).json({ success: false, message: 'Shop access denied' });
  }
  next();
};
```

---

## Controller Patterns

### Standard CRUD Controller

```javascript
// controllers/feature.controller.js
const { pool } = require('../config/database');
const Feature = require('../models/Feature');

// GET all (with shop scoping)
const getAll = async (req, res, next) => {
  try {
    const shopId = req.user.shop_id;
    const features = await Feature.findByShopId(shopId);

    res.json({
      success: true,
      data: features
    });
  } catch (error) {
    next(error);
  }
};

// GET by ID
const getById = async (req, res, next) => {
  try {
    const { id } = req.params;
    const shopId = req.user.shop_id;

    const feature = await Feature.findById(id, shopId);
    if (!feature) {
      return res.status(404).json({
        success: false,
        message: 'Feature not found'
      });
    }

    res.json({ success: true, data: feature });
  } catch (error) {
    next(error);
  }
};

// POST create
const create = async (req, res, next) => {
  try {
    const shopId = req.user.shop_id;
    const userId = req.user.id;
    const { name, description } = req.body;

    // Validation
    if (!name) {
      return res.status(400).json({
        success: false,
        message: 'Name is required'
      });
    }

    const id = await Feature.create({
      name,
      description,
      shopId,
      createdBy: userId
    });

    res.status(201).json({
      success: true,
      data: { id },
      message: 'Feature created successfully'
    });
  } catch (error) {
    next(error);
  }
};

// PUT update
const update = async (req, res, next) => {
  try {
    const { id } = req.params;
    const shopId = req.user.shop_id;
    const { name, description } = req.body;

    const existing = await Feature.findById(id, shopId);
    if (!existing) {
      return res.status(404).json({
        success: false,
        message: 'Feature not found'
      });
    }

    await Feature.update(id, { name, description }, shopId);

    res.json({
      success: true,
      message: 'Feature updated successfully'
    });
  } catch (error) {
    next(error);
  }
};

// DELETE (soft delete)
const remove = async (req, res, next) => {
  try {
    const { id } = req.params;
    const shopId = req.user.shop_id;

    const existing = await Feature.findById(id, shopId);
    if (!existing) {
      return res.status(404).json({
        success: false,
        message: 'Feature not found'
      });
    }

    await Feature.softDelete(id, shopId);

    res.json({
      success: true,
      message: 'Feature deleted successfully'
    });
  } catch (error) {
    next(error);
  }
};

module.exports = { getAll, getById, create, update, remove };
```

---

## Model Patterns

### Standard Model Class

```javascript
// models/Feature.js
const { pool } = require('../config/database');

class Feature {
  // Find by ID with shop scoping
  static async findById(id, shopId) {
    const [rows] = await pool.query(
      `SELECT * FROM features
       WHERE id = ? AND shop_id = ? AND is_active = 1`,
      [id, shopId]
    );
    return rows[0] || null;
  }

  // Find all by shop
  static async findByShopId(shopId, options = {}) {
    const { includeInactive = false, limit, offset } = options;

    let query = 'SELECT * FROM features WHERE shop_id = ?';
    const params = [shopId];

    if (!includeInactive) {
      query += ' AND is_active = 1';
    }

    query += ' ORDER BY created_at DESC';

    if (limit) {
      query += ' LIMIT ?';
      params.push(limit);
      if (offset) {
        query += ' OFFSET ?';
        params.push(offset);
      }
    }

    const [rows] = await pool.query(query, params);
    return rows;
  }

  // Create
  static async create(data) {
    const [result] = await pool.query(
      `INSERT INTO features (name, description, shop_id, created_by, created_at)
       VALUES (?, ?, ?, ?, NOW())`,
      [data.name, data.description, data.shopId, data.createdBy]
    );
    return result.insertId;
  }

  // Update
  static async update(id, data, shopId) {
    const [result] = await pool.query(
      `UPDATE features
       SET name = ?, description = ?, updated_at = NOW()
       WHERE id = ? AND shop_id = ?`,
      [data.name, data.description, id, shopId]
    );
    return result.affectedRows > 0;
  }

  // Soft delete (NEVER hard delete)
  static async softDelete(id, shopId) {
    const [result] = await pool.query(
      `UPDATE features SET is_active = 0, updated_at = NOW()
       WHERE id = ? AND shop_id = ?`,
      [id, shopId]
    );
    return result.affectedRows > 0;
  }

  // Reactivate (for restore functionality)
  static async reactivate(id, shopId) {
    const [result] = await pool.query(
      `UPDATE features SET is_active = 1, updated_at = NOW()
       WHERE id = ? AND shop_id = ?`,
      [id, shopId]
    );
    return result.affectedRows > 0;
  }
}

module.exports = Feature;
```

### Model with Transactions

```javascript
// For multi-table operations
static async createWithRelated(data) {
  const connection = await pool.getConnection();
  try {
    await connection.beginTransaction();

    // Insert main record
    const [mainResult] = await connection.query(
      'INSERT INTO features (name, shop_id) VALUES (?, ?)',
      [data.name, data.shopId]
    );
    const featureId = mainResult.insertId;

    // Insert related records
    for (const item of data.items) {
      await connection.query(
        'INSERT INTO feature_items (feature_id, item_name) VALUES (?, ?)',
        [featureId, item.name]
      );
    }

    await connection.commit();
    return featureId;
  } catch (error) {
    await connection.rollback();
    throw error;
  } finally {
    connection.release();
  }
}
```

---

## Route Patterns

### SHOPKEEPER Route File

```javascript
// routes/feature.routes.js
const express = require('express');
const router = express.Router();
const { authenticate, authorize, verifyShopOwnership } = require('../middlewares/auth.middleware');
const controller = require('../controllers/feature.controller');

// Apply middleware to all routes
router.use(authenticate);
router.use(authorize('SHOPKEEPER'));
router.use(verifyShopOwnership);

// Routes
router.get('/', controller.getAll);
router.get('/:id', controller.getById);
router.post('/', controller.create);
router.put('/:id', controller.update);
router.delete('/:id', controller.remove);

module.exports = router;
```

### SUPER_ADMIN Route File

```javascript
// routes/admin-feature.routes.js
const express = require('express');
const router = express.Router();
const { authenticate, authorize } = require('../middlewares/auth.middleware');
const { requireSuperAdmin } = require('../middlewares/security.middleware');
const controller = require('../controllers/admin-feature.controller');

router.use(authenticate);
router.use(authorize('SUPER_ADMIN'));
router.use(requireSuperAdmin); // Extra DB check for super admin

router.get('/features', controller.getAll);
router.post('/features', controller.create);
// ...

module.exports = router;
```

### Register in app.js

```javascript
// app.js
const featureRoutes = require('./routes/feature.routes');
const adminFeatureRoutes = require('./routes/admin-feature.routes');

// Mount routes
app.use('/shop/features', featureRoutes);      // /shop/features/*
app.use('/admin', adminFeatureRoutes);         // /admin/features/*
```

---

## Error Handling

### Global Error Handler

```javascript
// utils/error.util.js
const errorHandler = (err, req, res, next) => {
  console.error('Error:', err);

  // Joi validation error
  if (err.isJoi) {
    return res.status(400).json({
      success: false,
      message: 'Validation error',
      errors: err.details.map(d => d.message)
    });
  }

  // MySQL duplicate entry
  if (err.code === 'ER_DUP_ENTRY') {
    return res.status(409).json({
      success: false,
      message: 'Duplicate entry'
    });
  }

  // MySQL foreign key error
  if (err.code === 'ER_NO_REFERENCED_ROW_2') {
    return res.status(400).json({
      success: false,
      message: 'Referenced record not found'
    });
  }

  // JWT errors
  if (err.name === 'JsonWebTokenError' || err.name === 'TokenExpiredError') {
    return res.status(401).json({
      success: false,
      message: 'Invalid or expired token'
    });
  }

  // Default
  res.status(500).json({
    success: false,
    message: 'Internal server error'
  });
};

module.exports = { errorHandler };
```

---

## Validation with Joi

```javascript
// validations/feature.validation.js
const Joi = require('joi');

const createFeatureSchema = Joi.object({
  name: Joi.string().min(2).max(100).required(),
  description: Joi.string().max(500).optional(),
  type_id: Joi.number().integer().positive().required()
});

const validateCreateFeature = (req, res, next) => {
  const { error } = createFeatureSchema.validate(req.body);
  if (error) {
    return res.status(400).json({
      success: false,
      message: error.details[0].message
    });
  }
  next();
};

module.exports = { validateCreateFeature };
```

---

## SQL Query Patterns

### Always Use Parameterized Queries

```javascript
// CORRECT - Parameterized
const [rows] = await pool.query(
  'SELECT * FROM users WHERE phone_number = ? AND shop_id = ?',
  [phoneNumber, shopId]
);

// WRONG - String interpolation (SQL injection risk!)
const [rows] = await pool.query(
  `SELECT * FROM users WHERE phone_number = '${phoneNumber}'`
);
```

### Common Query Patterns

```javascript
// Select with JOIN
const [rows] = await pool.query(`
  SELECT c.*, cs.assigned_rider_id, u.full_name as rider_name
  FROM customers c
  JOIN customer_shops cs ON c.id = cs.customer_id
  LEFT JOIN users u ON cs.assigned_rider_id = u.id
  WHERE cs.shop_id = ? AND c.is_active = 1
`, [shopId]);

// Insert and get ID
const [result] = await pool.query(
  'INSERT INTO features (name, shop_id) VALUES (?, ?)',
  [name, shopId]
);
const newId = result.insertId;

// Update with affected rows check
const [result] = await pool.query(
  'UPDATE features SET name = ? WHERE id = ? AND shop_id = ?',
  [name, id, shopId]
);
const updated = result.affectedRows > 0;

// Count
const [[{ total }]] = await pool.query(
  'SELECT COUNT(*) as total FROM features WHERE shop_id = ?',
  [shopId]
);
```

---

## Response Format

### Success Response

```javascript
// Single item
res.json({
  success: true,
  data: { id: 1, name: 'Feature' }
});

// List
res.json({
  success: true,
  data: [{ id: 1 }, { id: 2 }]
});

// With message
res.status(201).json({
  success: true,
  data: { id: 1 },
  message: 'Feature created successfully'
});
```

### Error Response

```javascript
// Validation error
res.status(400).json({
  success: false,
  message: 'Name is required'
});

// Not found
res.status(404).json({
  success: false,
  message: 'Feature not found'
});

// Unauthorized
res.status(401).json({
  success: false,
  message: 'Invalid credentials'
});

// Forbidden
res.status(403).json({
  success: false,
  message: 'Access denied'
});
```

---

## Rate Limiting Pattern

```javascript
// middlewares/rateLimit.middleware.js
const rateLimitMap = new Map();

const createRateLimit = (maxAttempts, windowMs, lockoutMs) => {
  return (req, res, next) => {
    const identifier = req.body.phone_number || req.body.username;
    const ip = req.ip;
    const key = `${identifier}:${ip}`;

    const record = rateLimitMap.get(key) || { attempts: 0, firstAttempt: Date.now() };

    // Check if locked out
    if (record.lockedUntil && Date.now() < record.lockedUntil) {
      return res.status(429).json({
        success: false,
        message: 'Too many attempts. Try again later.'
      });
    }

    // Reset if window expired
    if (Date.now() - record.firstAttempt > windowMs) {
      record.attempts = 0;
      record.firstAttempt = Date.now();
    }

    record.attempts++;

    if (record.attempts > maxAttempts) {
      record.lockedUntil = Date.now() + lockoutMs;
      rateLimitMap.set(key, record);
      return res.status(429).json({
        success: false,
        message: 'Too many attempts. Account locked temporarily.'
      });
    }

    rateLimitMap.set(key, record);
    next();
  };
};

const loginRateLimit = createRateLimit(5, 15 * 60 * 1000, 15 * 60 * 1000);
const superAdminRateLimit = createRateLimit(3, 15 * 60 * 1000, 30 * 60 * 1000);
```
