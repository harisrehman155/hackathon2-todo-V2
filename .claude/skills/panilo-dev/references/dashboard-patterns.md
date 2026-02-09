# Dashboard Patterns Reference

Detailed patterns for Panilo dashboard development (React/Redux/Tailwind+MUI).

---

## Directory Structure

```
dashboard/src/
├── api/
│   └── ApiService.js           # Axios instance with interceptors
├── assets/
│   └── react.svg
├── components/
│   ├── common/                  # Reusable UI components
│   │   ├── Button.jsx           # Styled button variants
│   │   ├── DataGrid.jsx         # MUI DataGrid wrapper
│   │   ├── Input.jsx            # Form input with validation
│   │   ├── Loader.jsx           # Loading spinner
│   │   ├── Modal.jsx            # Dialog component
│   │   ├── StatusBadge.jsx      # Status indicator
│   │   └── Table.jsx            # Basic table
│   └── layout/
│       ├── Header.jsx           # Top navigation bar
│       ├── Layout.jsx           # Main layout wrapper
│       ├── LookupLoader.jsx     # Global lookup data loader
│       └── Sidebar.jsx          # Navigation sidebar
├── constants/
│   ├── apiEndPoints.js          # API endpoint definitions
│   └── lookupHeaders.js         # Lookup header IDs
├── pages/
│   ├── admin/                   # Super Admin pages
│   │   ├── CreateShopkeeperPage.jsx
│   │   ├── EditShopPage.jsx
│   │   ├── LookupDetailsPage.jsx
│   │   ├── LookupHeadersPage.jsx
│   │   ├── ShopDetailPage.jsx
│   │   └── ShopsListPage.jsx
│   └── auth/
│       └── LoginPage.jsx
├── redux/
│   ├── actions/
│   │   ├── actionType/
│   │   │   └── index.js         # Action type constants
│   │   ├── adminAction/
│   │   │   └── AdminActions.js
│   │   ├── authAction/
│   │   │   └── AuthActions.js
│   │   └── lookupAction/
│   │       └── LookupActions.js
│   ├── reducers/
│   │   ├── AuthReducer.js
│   │   ├── LookupReducer.js
│   │   ├── ShopReducer.js
│   │   └── index.js             # Root reducer
│   └── store/
│       └── index.js             # Store configuration
├── utils/
│   └── lookupHelper.js          # Lookup accessor utilities
├── App.jsx                      # Root with routing
├── App.css
├── main.jsx                     # Entry point
└── index.css                    # Global styles
```

---

## API Service

### Axios Instance with Interceptors

```javascript
// api/ApiService.js
import axios from 'axios';
import { Store } from '../redux/store';

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3000',
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' }
});

// Request interceptor - auto-inject token
axiosInstance.interceptors.request.use(
  (config) => {
    const state = Store.getState();
    const token = state.AuthReducer?.userData?.accessToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
axiosInstance.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message = error.response?.data?.message || 'An error occurred';
    return Promise.reject({ success: false, message });
  }
);

// Main API function
const apiService = async ({ method, endPoint, data = {} }) => {
  const config = {
    method,
    url: endPoint,
    ...(method === 'GET' ? { params: data } : { data })
  };
  return axiosInstance(config);
};

export default apiService;
```

### Usage

```javascript
// GET request
const response = await apiService({
  method: 'GET',
  endPoint: '/admin/shops',
});

// POST request
const response = await apiService({
  method: 'POST',
  endPoint: '/admin/shopkeepers',
  data: { name: 'Shop Name', ... }
});

// GET with query params
const response = await apiService({
  method: 'GET',
  endPoint: '/admin/shops',
  data: { page: 1, limit: 10 }  // Becomes ?page=1&limit=10
});
```

---

## Redux Patterns

### Action Types

```javascript
// redux/actions/actionType/index.js
// Auth
export const IS_LOGIN = 'IS_LOGIN';
export const LOGOUT = 'LOGOUT';

// Shops
export const SET_SHOPS = 'SET_SHOPS';
export const SET_SHOP_PROFILE = 'SET_SHOP_PROFILE';
export const SET_SHOP_LOADING = 'SET_SHOP_LOADING';

// Lookup
export const SET_LOOKUP_DETAILS = 'SET_LOOKUP_DETAILS';
export const SET_LOOKUP_HEADERS = 'SET_LOOKUP_HEADERS';

// Add new types here following pattern:
// export const SET_[FEATURE]S = 'SET_[FEATURE]S';
// export const SET_[FEATURE]_LOADING = 'SET_[FEATURE]_LOADING';
```

### Action Creators (Thunks)

```javascript
// redux/actions/featureAction/FeatureActions.js
import apiService from '../../../api/ApiService';
import { SET_FEATURES, SET_FEATURE_LOADING } from '../actionType';

// Get all
export const getFeaturesAction = () => async (dispatch) => {
  try {
    dispatch({ type: SET_FEATURE_LOADING, payload: true });

    const response = await apiService({
      method: 'GET',
      endPoint: '/admin/features',
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

// Get by ID
export const getFeatureByIdAction = (id) => async (dispatch) => {
  try {
    const response = await apiService({
      method: 'GET',
      endPoint: `/admin/features/${id}`,
    });
    return response;
  } catch (error) {
    console.error('Get feature error:', error);
    return { success: false, message: error.message };
  }
};

// Create
export const createFeatureAction = (data) => async (dispatch) => {
  try {
    const response = await apiService({
      method: 'POST',
      endPoint: '/admin/features',
      data,
    });
    return response;
  } catch (error) {
    console.error('Create feature error:', error);
    return { success: false, message: error.message };
  }
};

// Update
export const updateFeatureAction = (id, data) => async (dispatch) => {
  try {
    const response = await apiService({
      method: 'PUT',
      endPoint: `/admin/features/${id}`,
      data,
    });
    return response;
  } catch (error) {
    console.error('Update feature error:', error);
    return { success: false, message: error.message };
  }
};

// Delete
export const deleteFeatureAction = (id) => async (dispatch) => {
  try {
    const response = await apiService({
      method: 'DELETE',
      endPoint: `/admin/features/${id}`,
    });
    return response;
  } catch (error) {
    console.error('Delete feature error:', error);
    return { success: false, message: error.message };
  }
};
```

### Reducer

```javascript
// redux/reducers/FeatureReducer.js
import { SET_FEATURES, SET_FEATURE_LOADING } from '../actions/actionType';

const initialState = {
  features: [],
  loading: false,
};

const FeatureReducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_FEATURES:
      return { ...state, features: action.payload };
    case SET_FEATURE_LOADING:
      return { ...state, loading: action.payload };
    default:
      return state;
  }
};

export default FeatureReducer;
```

### Register Reducer

```javascript
// redux/reducers/index.js
import { combineReducers } from 'redux';
import AuthReducer from './AuthReducer';
import ShopReducer from './ShopReducer';
import LookupReducer from './LookupReducer';
import FeatureReducer from './FeatureReducer'; // Add new reducer

const rootReducer = combineReducers({
  AuthReducer,
  ShopReducer,
  LookupReducer,
  FeatureReducer, // Register here
});

export default rootReducer;
```

---

## Page Component Patterns

### List Page

```jsx
// pages/admin/FeaturesPage.jsx
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

const FeaturesPage = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { features, loading } = useSelector((state) => state.FeatureReducer);

  useEffect(() => {
    loadFeatures();
  }, []);

  const loadFeatures = () => {
    dispatch(getFeaturesAction());
  };

  const columns = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'name', headerName: 'Name', flex: 1, minWidth: 150 },
    { field: 'description', headerName: 'Description', flex: 2, minWidth: 200 },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
      renderCell: (params) => (
        <span className={`px-2 py-1 rounded text-sm font-medium ${
          params.row.is_active
            ? 'bg-green-100 text-green-800'
            : 'bg-red-100 text-red-800'
        }`}>
          {params.row.is_active ? 'Active' : 'Inactive'}
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
          <IconButton
            size="small"
            onClick={() => navigate(`/admin/features/${params.row.id}`)}
            title="View"
          >
            <VisibilityIcon fontSize="small" />
          </IconButton>
          <IconButton
            size="small"
            onClick={() => navigate(`/admin/features/${params.row.id}/edit`)}
            title="Edit"
          >
            <EditIcon fontSize="small" />
          </IconButton>
          <IconButton
            size="small"
            color="error"
            onClick={() => handleDelete(params.row.id)}
            title="Delete"
          >
            <DeleteIcon fontSize="small" />
          </IconButton>
        </div>
      ),
    },
  ];

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this feature?')) {
      const result = await dispatch(deleteFeatureAction(id));
      if (result.success) {
        loadFeatures();
      } else {
        alert(result.message || 'Failed to delete');
      }
    }
  };

  if (loading) {
    return (
      <Layout>
        <Loader />
      </Layout>
    );
  }

  return (
    <Layout>
      {/* Page Header */}
      <div className="mb-6 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">Features</h1>
        <Button onClick={() => navigate('/admin/features/create')}>
          Add Feature
        </Button>
      </div>

      {/* Data Table */}
      <div className="bg-white rounded-lg shadow">
        <DataGrid
          rows={features}
          columns={columns}
          pageSize={10}
          rowsPerPageOptions={[10, 25, 50]}
          autoHeight
          disableSelectionOnClick
          sx={{
            border: 'none',
            '& .MuiDataGrid-cell:focus': { outline: 'none' },
          }}
        />
      </div>
    </Layout>
  );
};

export default FeaturesPage;
```

### Detail Page

```jsx
// pages/admin/FeatureDetailPage.jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import Layout from '../../components/layout/Layout';
import Button from '../../components/common/Button';
import Loader from '../../components/common/Loader';
import { getFeatureByIdAction } from '../../redux/actions/featureAction/FeatureActions';

const FeatureDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [feature, setFeature] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFeature();
  }, [id]);

  const loadFeature = async () => {
    setLoading(true);
    const result = await dispatch(getFeatureByIdAction(id));
    if (result.success) {
      setFeature(result.data);
    }
    setLoading(false);
  };

  if (loading) {
    return <Layout><Loader /></Layout>;
  }

  if (!feature) {
    return (
      <Layout>
        <div className="text-center py-10">
          <p className="text-gray-500">Feature not found</p>
          <Button onClick={() => navigate('/admin/features')} className="mt-4">
            Back to List
          </Button>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      {/* Page Header */}
      <div className="mb-6 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">{feature.name}</h1>
        <div className="flex gap-2">
          <Button
            variant="secondary"
            onClick={() => navigate('/admin/features')}
          >
            Back
          </Button>
          <Button onClick={() => navigate(`/admin/features/${id}/edit`)}>
            Edit
          </Button>
        </div>
      </div>

      {/* Detail Card */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="grid grid-cols-2 gap-6">
          <div>
            <label className="text-sm text-gray-500">Name</label>
            <p className="text-gray-800 font-medium">{feature.name}</p>
          </div>
          <div>
            <label className="text-sm text-gray-500">Status</label>
            <p>
              <span className={`px-2 py-1 rounded text-sm ${
                feature.is_active
                  ? 'bg-green-100 text-green-800'
                  : 'bg-red-100 text-red-800'
              }`}>
                {feature.is_active ? 'Active' : 'Inactive'}
              </span>
            </p>
          </div>
          <div className="col-span-2">
            <label className="text-sm text-gray-500">Description</label>
            <p className="text-gray-800">{feature.description || '-'}</p>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default FeatureDetailPage;
```

### Create/Edit Page

```jsx
// pages/admin/CreateFeaturePage.jsx (or EditFeaturePage.jsx)
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
  const { id } = useParams(); // undefined for create, set for edit
  const isEdit = Boolean(id);
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [loading, setLoading] = useState(isEdit);
  const [submitting, setSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
  });
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (isEdit) {
      loadFeature();
    }
  }, [id]);

  const loadFeature = async () => {
    const result = await dispatch(getFeatureByIdAction(id));
    if (result.success) {
      setFormData({
        name: result.data.name || '',
        description: result.data.description || '',
      });
    }
    setLoading(false);
  };

  const handleChange = (field) => (e) => {
    setFormData({ ...formData, [field]: e.target.value });
    setErrors({ ...errors, [field]: '' });
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setSubmitting(true);
    const action = isEdit
      ? updateFeatureAction(id, formData)
      : createFeatureAction(formData);

    const result = await dispatch(action);

    if (result.success) {
      navigate('/admin/features');
    } else {
      alert(result.message || 'Operation failed');
    }
    setSubmitting(false);
  };

  if (loading) {
    return <Layout><Loader /></Layout>;
  }

  return (
    <Layout>
      {/* Page Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-800">
          {isEdit ? 'Edit Feature' : 'Create Feature'}
        </h1>
      </div>

      {/* Form Card */}
      <div className="bg-white rounded-lg shadow p-6 max-w-2xl">
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Name"
            value={formData.name}
            onChange={handleChange('name')}
            error={errors.name}
            required
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              rows={4}
              value={formData.description}
              onChange={handleChange('description')}
            />
          </div>

          {/* Form Actions */}
          <div className="flex gap-3 pt-4">
            <Button
              type="button"
              variant="secondary"
              onClick={() => navigate('/admin/features')}
            >
              Cancel
            </Button>
            <Button type="submit" loading={submitting}>
              {isEdit ? 'Update' : 'Create'}
            </Button>
          </div>
        </form>
      </div>
    </Layout>
  );
};

export default CreateFeaturePage;
```

---

## Routing Pattern

### Add Routes in App.jsx

```jsx
// App.jsx
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Provider, useSelector } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import { Store, Persister } from './redux/store';

// Pages
import LoginPage from './pages/auth/LoginPage';
import FeaturesPage from './pages/admin/FeaturesPage';
import FeatureDetailPage from './pages/admin/FeatureDetailPage';
import CreateFeaturePage from './pages/admin/CreateFeaturePage';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { userData } = useSelector((state) => state.AuthReducer);
  const isLogin = userData?.isLogin;
  const userRole = userData?.profile?.role;

  if (!isLogin || userRole !== 'SUPER_ADMIN') {
    return <Navigate to="/login" replace />;
  }
  return children;
};

const AppRoutes = () => {
  return (
    <Routes>
      {/* Public */}
      <Route path="/login" element={<LoginPage />} />

      {/* Protected Admin Routes */}
      <Route path="/admin/features" element={
        <ProtectedRoute><FeaturesPage /></ProtectedRoute>
      } />
      <Route path="/admin/features/create" element={
        <ProtectedRoute><CreateFeaturePage /></ProtectedRoute>
      } />
      <Route path="/admin/features/:id" element={
        <ProtectedRoute><FeatureDetailPage /></ProtectedRoute>
      } />
      <Route path="/admin/features/:id/edit" element={
        <ProtectedRoute><CreateFeaturePage /></ProtectedRoute>
      } />

      {/* Default redirect */}
      <Route path="*" element={<Navigate to="/admin/shops" replace />} />
    </Routes>
  );
};

const App = () => {
  return (
    <Provider store={Store}>
      <PersistGate loading={null} persistor={Persister}>
        <Router>
          <LookupLoader />
          <AppRoutes />
        </Router>
      </PersistGate>
    </Provider>
  );
};

export default App;
```

---

## Common Components Usage

### Button

```jsx
import Button from '../../components/common/Button';

// Primary (default)
<Button onClick={handleClick}>Save</Button>

// Secondary
<Button variant="secondary" onClick={handleCancel}>Cancel</Button>

// Danger
<Button variant="danger" onClick={handleDelete}>Delete</Button>

// With loading
<Button loading={isSubmitting}>Submit</Button>

// Disabled
<Button disabled>Disabled</Button>
```

### Input

```jsx
import Input from '../../components/common/Input';

<Input
  label="Email"
  type="email"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  error={errors.email}
  required
  placeholder="Enter email"
/>
```

### Loader

```jsx
import Loader from '../../components/common/Loader';

// Full page (inside Layout)
if (loading) {
  return <Layout><Loader /></Layout>;
}

// Inline
{loading && <Loader />}
```

### Layout

```jsx
import Layout from '../../components/layout/Layout';

const MyPage = () => {
  return (
    <Layout>
      {/* Page content goes here */}
    </Layout>
  );
};
```

### DataGrid (MUI)

```jsx
import { DataGrid } from '@mui/x-data-grid';

const columns = [
  { field: 'id', headerName: 'ID', width: 70 },
  { field: 'name', headerName: 'Name', flex: 1 },
  {
    field: 'actions',
    headerName: 'Actions',
    width: 150,
    sortable: false,
    renderCell: (params) => (
      <div className="flex gap-2">
        {/* Action buttons */}
      </div>
    ),
  },
];

<DataGrid
  rows={data}
  columns={columns}
  pageSize={10}
  rowsPerPageOptions={[10, 25, 50]}
  autoHeight
  disableSelectionOnClick
/>
```

---

## Form Patterns

### Form State Management

```jsx
const [formData, setFormData] = useState({
  name: '',
  email: '',
  type_id: '',
});

const [errors, setErrors] = useState({});

const handleChange = (field) => (e) => {
  setFormData({ ...formData, [field]: e.target.value });
  setErrors({ ...errors, [field]: '' }); // Clear error on change
};

// For select/dropdown
const handleSelectChange = (field) => (e) => {
  setFormData({ ...formData, [field]: e.target.value });
};
```

### Form Validation

```jsx
const validate = () => {
  const newErrors = {};

  if (!formData.name.trim()) {
    newErrors.name = 'Name is required';
  }

  if (!formData.email.trim()) {
    newErrors.email = 'Email is required';
  } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
    newErrors.email = 'Invalid email format';
  }

  if (!formData.type_id) {
    newErrors.type_id = 'Please select a type';
  }

  setErrors(newErrors);
  return Object.keys(newErrors).length === 0;
};
```

### Form Submission

```jsx
const [submitting, setSubmitting] = useState(false);

const handleSubmit = async (e) => {
  e.preventDefault();

  if (!validate()) return;

  setSubmitting(true);
  try {
    const result = await dispatch(createFeatureAction(formData));
    if (result.success) {
      navigate('/admin/features');
    } else {
      alert(result.message || 'Operation failed');
    }
  } finally {
    setSubmitting(false);
  }
};
```

---

## Error Handling

### API Error Display

```jsx
const handleSubmit = async () => {
  const result = await dispatch(someAction(data));

  if (result.success) {
    // Success handling
    navigate('/somewhere');
  } else {
    // Error handling
    alert(result.message || 'An error occurred');
    // Or set form errors
    if (result.errors) {
      setErrors(result.errors);
    }
  }
};
```

### Loading States

```jsx
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);

useEffect(() => {
  loadData();
}, []);

const loadData = async () => {
  setLoading(true);
  setError(null);
  try {
    const result = await dispatch(getDataAction());
    if (!result.success) {
      setError(result.message);
    }
  } catch (err) {
    setError('Failed to load data');
  } finally {
    setLoading(false);
  }
};

// In render
if (loading) return <Layout><Loader /></Layout>;
if (error) return <Layout><div className="text-red-500">{error}</div></Layout>;
```

---

## Lookup Data Access

```javascript
// utils/lookupHelper.js
import { Store } from '../redux/store';

export const getLookupByHeaderName = (headerName) => {
  const state = Store.getState();
  return state.LookupReducer?.lookupDetails?.byName?.[headerName] || [];
};

export const getLookupById = (headerName, id) => {
  const items = getLookupByHeaderName(headerName);
  return items.find(item => item.id === id);
};

export const getLookupByKey = (headerName, key) => {
  const items = getLookupByHeaderName(headerName);
  return items.find(item => item.key === key);
};
```

### Usage in Components

```jsx
import { useSelector } from 'react-redux';

const MyComponent = () => {
  const { lookupDetails } = useSelector((state) => state.LookupReducer);
  const featureTypes = lookupDetails?.byName?.FEATURE_TYPE || [];

  return (
    <select value={formData.type_id} onChange={handleChange('type_id')}>
      <option value="">Select Type</option>
      {featureTypes.map((type) => (
        <option key={type.id} value={type.id}>
          {type.name}
        </option>
      ))}
    </select>
  );
};
```
