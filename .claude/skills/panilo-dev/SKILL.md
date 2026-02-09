---
name: panilo-dev
description: |
  Full-stack development skill for Panilo Super Admin dashboard.
  This skill should be used when implementing features, fixing bugs, or extending
  the backend (Express/MySQL/JWT) or dashboard (React/Redux/Tailwind+MUI).
  Focuses on insights, analytics, and data management for Super Admin role.
---

# Panilo Development Skill

Build features for the PaaniGo Super Admin dashboard following established patterns.

## What This Skill Does

- Implements backend APIs (Express/MySQL/JWT) for Super Admin
- Implements dashboard screens (React/Redux/Tailwind+MUI)
- Creates insights and analytics features
- Ensures strict pattern consistency across codebase

## What This Skill Does NOT Do

- Mobile app development (separate codebase)
- Shopkeeper/Rider/Customer features (Super Admin only)
- Database migrations (manual process)
- Deployment/DevOps tasks

---

## Required Clarifications

Before implementing, gather these answers:

| Question | Why Needed |
|----------|------------|
| What data/insights should this feature show? | Determines API and UI design |
| Which tables/entities are involved? | Identifies models to create/modify |
| Is this new or modifying existing feature? | Determines file locations |
| Any filtering/search requirements? | Affects API params and UI components |

## Optional Clarifications

| Question | When to Ask |
|----------|-------------|
| Pagination requirements? | For list/table views |
| Export functionality needed? | For reports/analytics |
| Date range filtering? | For time-based insights |
| Specific chart types? | For visualization features |

---

## Before Implementation

| Source | Gather |
|--------|--------|
| **Codebase** | Existing patterns in similar features |
| **Conversation** | User's specific requirements |
| **Skill References** | Patterns from `references/` |
| **Database Schema** | Tables involved (check `panilo.sql`) |

---

## Official Documentation

| Resource | URL | Use For |
|----------|-----|---------|
| Express.js 4.x | https://expressjs.com/en/4x/api.html | Routes, middleware |
| mysql2 | https://github.com/sidorares/node-mysql2 | Database queries |
| React 19 | https://react.dev/reference/react | Components, hooks |
| Redux Toolkit | https://redux-toolkit.js.org/ | State management |
| MUI Components | https://mui.com/material-ui/ | UI components |
| MUI DataGrid | https://mui.com/x/react-data-grid/ | Tables/grids |
| Tailwind CSS | https://tailwindcss.com/docs | Styling |

---

## Quick Reference Search

Find patterns in reference files:

```bash
# Backend patterns
grep -n "authenticate\|authorize\|requireSuperAdmin" references/backend-patterns.md
grep -n "static async\|pool.execute" references/backend-patterns.md

# Dashboard patterns
grep -n "useDispatch\|useSelector\|dispatch" references/dashboard-patterns.md
grep -n "DataGrid\|columns\|renderCell" references/dashboard-patterns.md

# API endpoints
grep -n "GET\|POST\|PUT\|DELETE" references/api-reference.md

# Theme/UI
grep -n "className\|bg-\|text-" references/theme-reference.md
```

---

## Development Workflow

**MANDATORY**: Follow this sequence for all features.

```
1. PLAN → Define scope, tables, endpoints, screens
2. BACKEND → Model → Controller → Route → Register in app.js
3. DASHBOARD → Actions → Reducer → Page → Route in App.jsx
```

---

## Project Structure

### Backend
```
backend/src/
├── controllers/     # Request handlers (NO raw SQL)
├── models/          # Data access layer (ALL SQL here)
├── routes/          # Route definitions with middleware
├── middlewares/     # Auth, validation, security
└── validations/     # Joi schemas
```

### Dashboard
```
dashboard/src/
├── pages/admin/     # Page components
├── components/      # Reusable UI components
├── redux/
│   ├── actions/     # API calls + dispatches
│   └── reducers/    # State management
└── constants/       # API endpoints, configs
```

---

## Critical Rules

### Backend

> **NEVER write raw SQL in controllers. ALL queries MUST be in Model files.**

| Layer | Responsibility | Contains SQL? |
|-------|----------------|---------------|
| Controller | HTTP handling, validation, calling models | **NO** |
| Model | Data access, SQL queries, data formatting | **YES** |

> **Always place specific routes BEFORE parameterized routes.**

```javascript
router.get('/stats', controller.getStats);  // BEFORE /:id
router.get('/search', controller.search);   // BEFORE /:id
router.get('/:id', controller.getById);     // :id catches everything
```

### Dashboard

> **Always use searchable Autocomplete for entity filters (Shops, Riders, Customers).**

Minimum 3 characters required, with 300ms debounce.

---

## Backend Patterns

### Super Admin Middleware Chain

```javascript
router.use(authenticate);
router.use(authorize('SUPER_ADMIN'));
router.use(requireSuperAdmin);
```

### Response Format

```javascript
// Success
res.json({ success: true, data: result, message: 'Optional message' });

// Error
res.status(400).json({ success: false, message: 'Error description' });
```

### Model Pattern (Summary)

```javascript
class Feature {
  static async findAll(options) { /* pagination, search, filters */ }
  static async findById(id) { /* single record */ }
  static async create(data) { /* returns insertId */ }
  static async update(id, data) { /* returns boolean */ }
  static async softDelete(id) { /* is_active = 0 */ }
  static async getStats() { /* aggregations for insights */ }
}
```

See `references/code-templates.md` for full templates.

### Stats/Analytics Pattern

```javascript
static async getStats() {
  const [rows] = await pool.execute(`
    SELECT
      COUNT(*) as total,
      SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END) as active,
      SUM(CASE WHEN DATE(created_at) = CURDATE() THEN 1 ELSE 0 END) as today
    FROM table_name
  `);
  return rows[0];
}
```

---

## Dashboard Patterns

### Redux Action Pattern (Summary)

```javascript
export const getFeaturesAction = () => async (dispatch) => {
  dispatch({ type: SET_LOADING, payload: true });
  const response = await apiService({ method: 'GET', endPoint: '/admin/features' });
  if (response.success) dispatch({ type: SET_DATA, payload: response.data });
  dispatch({ type: SET_LOADING, payload: false });
  return response;
};
```

See `references/code-templates.md` for full templates.

### Page Component Pattern (Summary)

```jsx
const FeaturePage = () => {
  const dispatch = useDispatch();
  const { features, loading } = useSelector((state) => state.FeatureReducer);

  useEffect(() => { dispatch(getFeaturesAction()); }, [dispatch]);

  if (loading) return <Layout><Loader /></Layout>;

  return (
    <Layout>
      <div className="mb-6 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">Title</h1>
        <Button onClick={() => navigate('/admin/features/create')}>Add</Button>
      </div>
      <div className="bg-white rounded-lg shadow">
        <DataGrid rows={features} columns={columns} autoHeight />
      </div>
    </Layout>
  );
};
```

### Stats Card Pattern

```jsx
<div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
  <div className="bg-white rounded-lg shadow p-6">
    <p className="text-sm text-gray-500">Total</p>
    <p className="text-2xl font-bold text-gray-800">{stats.total}</p>
  </div>
</div>
```

---

## UI Theme Quick Reference

### Colors
| Purpose | Classes |
|---------|---------|
| Primary button | `bg-blue-600 hover:bg-blue-700 text-white` |
| Secondary button | `bg-gray-200 hover:bg-gray-300 text-gray-800` |
| Danger button | `bg-red-600 hover:bg-red-700 text-white` |
| Active badge | `bg-green-100 text-green-800` |
| Inactive badge | `bg-red-100 text-red-800` |
| Card | `bg-white rounded-lg shadow p-6` |

### Common Layout
```jsx
// Page header
<div className="mb-6 flex justify-between items-center">
  <h1 className="text-2xl font-bold text-gray-800">Title</h1>
  <Button>Action</Button>
</div>

// Card container
<div className="bg-white rounded-lg shadow p-6">
  {/* content */}
</div>
```

---

## Feature Completeness Checklist

### Backend
- [ ] Model file with all data access methods
- [ ] Controller using Model (NO raw SQL)
- [ ] Route with Super Admin middleware chain
- [ ] Route registered in app.js
- [ ] Parameterized SQL (prevent injection)
- [ ] Soft delete (is_active = 0)

### Dashboard
- [ ] Redux actions + reducer
- [ ] Action types in actionType/index.js
- [ ] Reducer registered in reducers/index.js
- [ ] Page component with Layout wrapper
- [ ] Loading state with Loader
- [ ] Route in App.jsx with ProtectedRoute
- [ ] DataGrid for lists
- [ ] Button/Input components (not raw HTML)

### Integration
- [ ] API endpoint matches action call
- [ ] Response format handled correctly
- [ ] Error states displayed

---

## Reference Files

| File | Content | Lines |
|------|---------|-------|
| `references/backend-patterns.md` | Auth middleware, controllers, models, routes, error handling | ~720 |
| `references/dashboard-patterns.md` | Redux, pages, components, forms, routing | ~1020 |
| `references/api-reference.md` | All API endpoints with request/response examples | ~790 |
| `references/theme-reference.md` | Colors, typography, layouts, component styles | ~540 |
| `references/code-templates.md` | Copy-paste templates for common patterns | ~400 |

---

## Quick Commands

```bash
# Backend
cd backend && npm run dev

# Dashboard
cd dashboard && npm run dev

# Test API
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone_number":"03048108664","password":"123456"}'
```
