# Code Templates Reference

Copy-paste templates for common Panilo development patterns.

---

## Backend Templates

### Controller Template

```javascript
// controllers/[feature].controller.js
const Feature = require('../models/Feature');

class FeatureController {
  static async getAll(req, res, next) {
    try {
      const page = parseInt(req.query.page) || 1;
      const limit = parseInt(req.query.limit) || 10;
      const search = req.query.search?.trim() || null;

      const result = await Feature.findAll({ page, limit, search });

      res.json({
        success: true,
        message: 'Features retrieved successfully',
        data: result
      });
    } catch (error) {
      next(error);
    }
  }

  static async getById(req, res, next) {
    try {
      const { id } = req.params;
      const feature = await Feature.findById(id);

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
  }

  static async create(req, res, next) {
    try {
      const { name, description } = req.body;

      if (!name) {
        return res.status(400).json({
          success: false,
          message: 'Name is required'
        });
      }

      const id = await Feature.create({ name, description });

      res.status(201).json({
        success: true,
        data: { id },
        message: 'Feature created successfully'
      });
    } catch (error) {
      next(error);
    }
  }

  static async update(req, res, next) {
    try {
      const { id } = req.params;
      const { name, description } = req.body;

      const existing = await Feature.findById(id);
      if (!existing) {
        return res.status(404).json({
          success: false,
          message: 'Feature not found'
        });
      }

      await Feature.update(id, { name, description });

      res.json({
        success: true,
        message: 'Feature updated successfully'
      });
    } catch (error) {
      next(error);
    }
  }

  static async remove(req, res, next) {
    try {
      const { id } = req.params;

      const existing = await Feature.findById(id);
      if (!existing) {
        return res.status(404).json({
          success: false,
          message: 'Feature not found'
        });
      }

      await Feature.softDelete(id);

      res.json({
        success: true,
        message: 'Feature deleted successfully'
      });
    } catch (error) {
      next(error);
    }
  }
}

module.exports = FeatureController;
```

---

### Model Template

```javascript
// models/[Feature].js
const pool = require('../config/database');

class Feature {
  /**
   * Find all with pagination and search
   */
  static async findAll(options = {}) {
    const { page = 1, limit = 10, search = null } = options;
    const offset = (page - 1) * limit;

    let whereConditions = ['is_active = 1'];
    let queryParams = [];

    if (search) {
      whereConditions.push('(name LIKE ? OR description LIKE ?)');
      const searchPattern = `%${search}%`;
      queryParams.push(searchPattern, searchPattern);
    }

    const whereClause = `WHERE ${whereConditions.join(' AND ')}`;

    // Count
    const [countRows] = await pool.execute(
      `SELECT COUNT(*) as total FROM features ${whereClause}`,
      queryParams
    );
    const total = countRows[0].total;

    // Data
    const [rows] = await pool.execute(
      `SELECT id, name, description, is_active, created_at
       FROM features
       ${whereClause}
       ORDER BY created_at DESC
       LIMIT ? OFFSET ?`,
      [...queryParams, limit, offset]
    );

    const totalPages = Math.ceil(total / limit);

    return {
      items: rows,
      pagination: { page, limit, total, totalPages, hasMore: page < totalPages }
    };
  }

  static async findById(id) {
    const [rows] = await pool.execute(
      'SELECT * FROM features WHERE id = ? AND is_active = 1',
      [id]
    );
    return rows[0] || null;
  }

  static async create(data) {
    const [result] = await pool.execute(
      'INSERT INTO features (name, description) VALUES (?, ?)',
      [data.name, data.description]
    );
    return result.insertId;
  }

  static async update(id, data) {
    const [result] = await pool.execute(
      'UPDATE features SET name = ?, description = ?, updated_at = NOW() WHERE id = ?',
      [data.name, data.description, id]
    );
    return result.affectedRows > 0;
  }

  static async softDelete(id) {
    const [result] = await pool.execute(
      'UPDATE features SET is_active = 0, updated_at = NOW() WHERE id = ?',
      [id]
    );
    return result.affectedRows > 0;
  }
}

module.exports = Feature;
```

---

### Route Template

```javascript
// routes/admin/[feature].routes.js
const express = require('express');
const router = express.Router();
const { authenticate, authorize } = require('../../middlewares/auth.middleware');
const { requireSuperAdmin } = require('../../middlewares/security.middleware');
const controller = require('../../controllers/[feature].controller');

router.use(authenticate);
router.use(authorize('SUPER_ADMIN'));
router.use(requireSuperAdmin);

// IMPORTANT: Specific routes BEFORE parameterized routes
router.get('/', controller.getAll);
router.get('/stats', controller.getStats);    // Before /:id
router.get('/search', controller.search);     // Before /:id
router.get('/:id', controller.getById);
router.post('/', controller.create);
router.put('/:id', controller.update);
router.delete('/:id', controller.remove);

module.exports = router;
```

---

### Stats/Analytics Endpoint Template

```javascript
// In controller
static async getStats(req, res, next) {
  try {
    const stats = await Feature.getStats();
    res.json({ success: true, data: stats });
  } catch (error) {
    next(error);
  }
}

// In model
static async getStats() {
  const [rows] = await pool.execute(`
    SELECT
      COUNT(*) as total,
      SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END) as active,
      SUM(CASE WHEN is_active = 0 THEN 1 ELSE 0 END) as inactive,
      SUM(CASE WHEN DATE(created_at) = CURDATE() THEN 1 ELSE 0 END) as today,
      SUM(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) THEN 1 ELSE 0 END) as this_week,
      SUM(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 ELSE 0 END) as this_month
    FROM features
  `);
  return rows[0];
}
```

---

## Dashboard Templates

### Redux Action Template

```javascript
// redux/actions/[feature]Action/[Feature]Actions.js
import apiService from '../../../api/ApiService';
import { SET_FEATURES, SET_FEATURE_LOADING } from '../actionType';

export const getFeaturesAction = (params = {}) => async (dispatch) => {
  try {
    dispatch({ type: SET_FEATURE_LOADING, payload: true });

    const response = await apiService({
      method: 'GET',
      endPoint: '/admin/features',
      data: params,
    });

    if (response.success) {
      dispatch({ type: SET_FEATURES, payload: response.data });
    }
    return response;
  } catch (error) {
    console.error('Get features error:', error);
    return { success: false, message: error.message };
  } finally {
    dispatch({ type: SET_FEATURE_LOADING, payload: false });
  }
};

export const getFeatureByIdAction = (id) => async () => {
  try {
    const response = await apiService({
      method: 'GET',
      endPoint: `/admin/features/${id}`,
    });
    return response;
  } catch (error) {
    return { success: false, message: error.message };
  }
};

export const createFeatureAction = (data) => async () => {
  try {
    const response = await apiService({
      method: 'POST',
      endPoint: '/admin/features',
      data,
    });
    return response;
  } catch (error) {
    return { success: false, message: error.message };
  }
};

export const updateFeatureAction = (id, data) => async () => {
  try {
    const response = await apiService({
      method: 'PUT',
      endPoint: `/admin/features/${id}`,
      data,
    });
    return response;
  } catch (error) {
    return { success: false, message: error.message };
  }
};

export const deleteFeatureAction = (id) => async () => {
  try {
    const response = await apiService({
      method: 'DELETE',
      endPoint: `/admin/features/${id}`,
    });
    return response;
  } catch (error) {
    return { success: false, message: error.message };
  }
};
```

---

### Redux Reducer Template

```javascript
// redux/reducers/[Feature]Reducer.js
import { SET_FEATURES, SET_FEATURE_LOADING } from '../actions/actionType';

const initialState = {
  features: [],
  pagination: null,
  loading: false,
};

const FeatureReducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_FEATURES:
      return {
        ...state,
        features: action.payload.items || action.payload,
        pagination: action.payload.pagination || null,
      };
    case SET_FEATURE_LOADING:
      return { ...state, loading: action.payload };
    default:
      return state;
  }
};

export default FeatureReducer;
```

---

### List Page Template

```jsx
// pages/admin/[Feature]Page.jsx
import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { DataGrid } from '@mui/x-data-grid';
import { IconButton } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import VisibilityIcon from '@mui/icons-material/Visibility';
import Layout from '../../components/layout/Layout';
import Button from '../../components/common/Button';
import Loader from '../../components/common/Loader';
import { getFeaturesAction, deleteFeatureAction } from '../../redux/actions/featureAction/FeatureActions';

const FeaturePage = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { features, loading } = useSelector((state) => state.FeatureReducer);

  useEffect(() => {
    dispatch(getFeaturesAction());
  }, [dispatch]);

  const columns = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'name', headerName: 'Name', flex: 1 },
    {
      field: 'is_active',
      headerName: 'Status',
      width: 120,
      renderCell: (params) => (
        <span className={`px-2 py-1 rounded text-sm font-medium ${
          params.value ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        }`}>
          {params.value ? 'Active' : 'Inactive'}
        </span>
      ),
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 150,
      sortable: false,
      renderCell: (params) => (
        <div className="flex gap-1">
          <IconButton size="small" onClick={() => navigate(`/admin/features/${params.row.id}`)}>
            <VisibilityIcon fontSize="small" />
          </IconButton>
          <IconButton size="small" onClick={() => navigate(`/admin/features/${params.row.id}/edit`)}>
            <EditIcon fontSize="small" />
          </IconButton>
          <IconButton size="small" color="error" onClick={() => handleDelete(params.row.id)}>
            <DeleteIcon fontSize="small" />
          </IconButton>
        </div>
      ),
    },
  ];

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this?')) {
      const result = await dispatch(deleteFeatureAction(id));
      if (result.success) dispatch(getFeaturesAction());
      else alert(result.message || 'Delete failed');
    }
  };

  if (loading) return <Layout><Loader /></Layout>;

  return (
    <Layout>
      <div className="mb-6 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">Features</h1>
        <Button onClick={() => navigate('/admin/features/create')}>Add Feature</Button>
      </div>
      <div className="bg-white rounded-lg shadow">
        <DataGrid
          rows={features}
          columns={columns}
          pageSize={10}
          rowsPerPageOptions={[10, 25, 50]}
          autoHeight
          disableSelectionOnClick
        />
      </div>
    </Layout>
  );
};

export default FeaturePage;
```

---

### Create/Edit Page Template

```jsx
// pages/admin/Create[Feature]Page.jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import Layout from '../../components/layout/Layout';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import Loader from '../../components/common/Loader';
import {
  getFeatureByIdAction,
  createFeatureAction,
  updateFeatureAction
} from '../../redux/actions/featureAction/FeatureActions';

const CreateFeaturePage = () => {
  const { id } = useParams();
  const isEdit = Boolean(id);
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [loading, setLoading] = useState(isEdit);
  const [submitting, setSubmitting] = useState(false);
  const [formData, setFormData] = useState({ name: '', description: '' });
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (isEdit) loadFeature();
  }, [id]);

  const loadFeature = async () => {
    const result = await dispatch(getFeatureByIdAction(id));
    if (result.success) {
      setFormData({ name: result.data.name || '', description: result.data.description || '' });
    }
    setLoading(false);
  };

  const handleChange = (field) => (e) => {
    setFormData({ ...formData, [field]: e.target.value });
    setErrors({ ...errors, [field]: '' });
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.name.trim()) newErrors.name = 'Name is required';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setSubmitting(true);
    const action = isEdit ? updateFeatureAction(id, formData) : createFeatureAction(formData);
    const result = await dispatch(action);

    if (result.success) navigate('/admin/features');
    else alert(result.message || 'Operation failed');
    setSubmitting(false);
  };

  if (loading) return <Layout><Loader /></Layout>;

  return (
    <Layout>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-800">
          {isEdit ? 'Edit Feature' : 'Create Feature'}
        </h1>
      </div>
      <div className="bg-white rounded-lg shadow p-6 max-w-2xl">
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input label="Name" value={formData.name} onChange={handleChange('name')} error={errors.name} required />
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              rows={4}
              value={formData.description}
              onChange={handleChange('description')}
            />
          </div>
          <div className="flex gap-3 pt-4">
            <Button type="button" variant="secondary" onClick={() => navigate('/admin/features')}>Cancel</Button>
            <Button type="submit" loading={submitting}>{isEdit ? 'Update' : 'Create'}</Button>
          </div>
        </form>
      </div>
    </Layout>
  );
};

export default CreateFeaturePage;
```

---

### Stats Dashboard Card Template

```jsx
// components/admin/StatsCard.jsx
const StatsCard = ({ title, value, icon: Icon, trend, trendLabel }) => (
  <div className="bg-white rounded-lg shadow p-6">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm text-gray-500">{title}</p>
        <p className="text-2xl font-bold text-gray-800">{value}</p>
      </div>
      {Icon && (
        <div className="p-3 bg-blue-100 rounded-full">
          <Icon className="w-6 h-6 text-blue-600" />
        </div>
      )}
    </div>
    {trend !== undefined && (
      <div className="mt-4 flex items-center text-sm">
        <span className={trend >= 0 ? 'text-green-600' : 'text-red-600'}>
          {trend >= 0 ? '+' : ''}{trend}%
        </span>
        <span className="text-gray-500 ml-2">{trendLabel}</span>
      </div>
    )}
  </div>
);

// Usage
<div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
  <StatsCard title="Total Shops" value={stats.total_shops} trend={12} trendLabel="vs last month" />
  <StatsCard title="Active Shops" value={stats.active_shops} />
  <StatsCard title="Total Deliveries" value={stats.total_deliveries} />
  <StatsCard title="Revenue" value={`Rs ${stats.revenue}`} />
</div>
```

---

### Searchable Autocomplete Template

```jsx
import { Autocomplete, TextField, CircularProgress } from '@mui/material';

const SearchableDropdown = ({ label, value, onChange, searchAction, getOptionLabel }) => {
  const dispatch = useDispatch();
  const [options, setOptions] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (inputValue.length < 3) {
      setOptions([]);
      return;
    }

    const timer = setTimeout(async () => {
      setLoading(true);
      const results = await dispatch(searchAction(inputValue));
      setOptions(results || []);
      setLoading(false);
    }, 300);

    return () => clearTimeout(timer);
  }, [inputValue, dispatch]);

  return (
    <Autocomplete
      size="small"
      sx={{ minWidth: 250 }}
      options={options}
      getOptionLabel={getOptionLabel}
      value={value}
      onChange={(_, newValue) => onChange(newValue)}
      inputValue={inputValue}
      onInputChange={(_, newInputValue) => setInputValue(newInputValue)}
      loading={loading}
      noOptionsText={inputValue.length < 3 ? 'Type at least 3 characters' : 'No results'}
      renderInput={(params) => (
        <TextField
          {...params}
          label={label}
          InputProps={{
            ...params.InputProps,
            endAdornment: (
              <>
                {loading && <CircularProgress size={20} />}
                {params.InputProps.endAdornment}
              </>
            ),
          }}
        />
      )}
      isOptionEqualToValue={(option, val) => option.id === val?.id}
    />
  );
};
```

---

## App.jsx Route Template

```jsx
// Add to App.jsx
import FeaturePage from './pages/admin/FeaturePage';
import FeatureDetailPage from './pages/admin/FeatureDetailPage';
import CreateFeaturePage from './pages/admin/CreateFeaturePage';

// Inside Routes:
<Route path="/admin/features" element={<ProtectedRoute><FeaturePage /></ProtectedRoute>} />
<Route path="/admin/features/create" element={<ProtectedRoute><CreateFeaturePage /></ProtectedRoute>} />
<Route path="/admin/features/:id" element={<ProtectedRoute><FeatureDetailPage /></ProtectedRoute>} />
<Route path="/admin/features/:id/edit" element={<ProtectedRoute><CreateFeaturePage /></ProtectedRoute>} />
```

---

## Reducer Registration

```javascript
// redux/reducers/index.js
import FeatureReducer from './FeatureReducer';

const rootReducer = combineReducers({
  // ... existing reducers
  FeatureReducer,
});
```

---

## Action Types

```javascript
// redux/actions/actionType/index.js
export const SET_FEATURES = 'SET_FEATURES';
export const SET_FEATURE_LOADING = 'SET_FEATURE_LOADING';
```
