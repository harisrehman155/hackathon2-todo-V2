# Theme Reference

UI/UX patterns, colors, and component styling for Panilo dashboard.

---

## Color Palette

### Tailwind Colors (Primary)

```javascript
// tailwind.config.js
colors: {
  primary: '#007AFF',    // Blue - buttons, links, primary actions
  secondary: '#F0F0F0',  // Light gray - secondary buttons, backgrounds
  danger: '#FF3B30',     // Red - delete, error states
  success: '#34C759',    // Green - success states, active badges
}
```

### Semantic Usage

| Purpose | Tailwind Classes | Hex |
|---------|------------------|-----|
| Primary button | `bg-blue-600 hover:bg-blue-700` | #2563EB |
| Secondary button | `bg-gray-200 hover:bg-gray-300` | #E5E7EB |
| Danger button | `bg-red-600 hover:bg-red-700` | #DC2626 |
| Success text | `text-green-600` | #16A34A |
| Error text | `text-red-600` | #DC2626 |
| Muted text | `text-gray-500` | #6B7280 |
| Page background | `bg-gray-100` | #F3F4F6 |
| Card background | `bg-white` | #FFFFFF |
| Border | `border-gray-300` | #D1D5DB |

---

## Typography

### Headings

```jsx
// Page title
<h1 className="text-2xl font-bold text-gray-800">Page Title</h1>

// Section title
<h2 className="text-xl font-semibold text-gray-800">Section Title</h2>

// Subsection
<h3 className="text-lg font-medium text-gray-700">Subsection</h3>
```

### Body Text

```jsx
// Normal text
<p className="text-gray-700">Body text</p>

// Small/helper text
<span className="text-sm text-gray-500">Helper text</span>

// Label
<label className="block text-sm font-medium text-gray-700 mb-1">Label</label>
```

---

## Layout Patterns

### Page Structure

```jsx
<Layout>
  {/* Page Header */}
  <div className="mb-6 flex justify-between items-center">
    <h1 className="text-2xl font-bold text-gray-800">Page Title</h1>
    <div className="flex gap-2">
      <Button variant="secondary">Secondary Action</Button>
      <Button>Primary Action</Button>
    </div>
  </div>

  {/* Content Area */}
  <div className="bg-white rounded-lg shadow">
    {/* Content */}
  </div>
</Layout>
```

### Card

```jsx
// Basic card
<div className="bg-white rounded-lg shadow p-6">
  {/* Card content */}
</div>

// Card with header
<div className="bg-white rounded-lg shadow">
  <div className="px-6 py-4 border-b border-gray-200">
    <h2 className="text-lg font-semibold text-gray-800">Card Title</h2>
  </div>
  <div className="p-6">
    {/* Card content */}
  </div>
</div>
```

### Grid Layouts

```jsx
// Two column
<div className="grid grid-cols-2 gap-6">
  <div>Column 1</div>
  <div>Column 2</div>
</div>

// Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* Items */}
</div>

// Stats grid
<div className="grid grid-cols-2 md:grid-cols-4 gap-4">
  {/* Stat cards */}
</div>
```

### Form Layout

```jsx
// Single column form
<div className="max-w-2xl">
  <form className="space-y-4">
    <Input label="Field 1" ... />
    <Input label="Field 2" ... />

    <div className="flex gap-3 pt-4">
      <Button variant="secondary">Cancel</Button>
      <Button type="submit">Save</Button>
    </div>
  </form>
</div>

// Two column form
<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
  <Input label="First Name" ... />
  <Input label="Last Name" ... />
  <Input label="Email" className="md:col-span-2" ... />
</div>
```

---

## Component Styles

### Buttons

```jsx
// Primary (default)
<button className="px-6 py-3 rounded-lg font-semibold bg-blue-600 text-white hover:bg-blue-700 transition-colors duration-200">
  Primary
</button>

// Secondary
<button className="px-6 py-3 rounded-lg font-semibold bg-gray-200 text-gray-800 hover:bg-gray-300 transition-colors duration-200">
  Secondary
</button>

// Danger
<button className="px-6 py-3 rounded-lg font-semibold bg-red-600 text-white hover:bg-red-700 transition-colors duration-200">
  Delete
</button>

// Small button
<button className="px-4 py-2 text-sm rounded-lg ...">
  Small
</button>

// Disabled
<button className="... opacity-50 cursor-not-allowed" disabled>
  Disabled
</button>

// Loading
<button className="... opacity-70 cursor-wait">
  <span className="animate-spin mr-2">...</span>
  Loading
</button>
```

### Inputs

```jsx
// Text input
<input
  type="text"
  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors"
  placeholder="Enter value"
/>

// With error
<input
  className="w-full px-3 py-2 border border-red-500 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 outline-none"
/>
<p className="mt-1 text-sm text-red-600">Error message</p>

// Textarea
<textarea
  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none resize-none"
  rows={4}
/>

// Select
<select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none bg-white">
  <option value="">Select option</option>
  <option value="1">Option 1</option>
</select>
```

### Status Badges

```jsx
// Active/Success
<span className="px-2 py-1 rounded text-sm font-medium bg-green-100 text-green-800">
  Active
</span>

// Inactive/Error
<span className="px-2 py-1 rounded text-sm font-medium bg-red-100 text-red-800">
  Inactive
</span>

// Warning/Pending
<span className="px-2 py-1 rounded text-sm font-medium bg-yellow-100 text-yellow-800">
  Pending
</span>

// Info
<span className="px-2 py-1 rounded text-sm font-medium bg-blue-100 text-blue-800">
  Info
</span>

// Neutral
<span className="px-2 py-1 rounded text-sm font-medium bg-gray-100 text-gray-800">
  Neutral
</span>
```

### Tables (DataGrid)

```jsx
import { DataGrid } from '@mui/x-data-grid';

<DataGrid
  rows={data}
  columns={columns}
  pageSize={10}
  rowsPerPageOptions={[10, 25, 50]}
  autoHeight
  disableSelectionOnClick
  sx={{
    border: 'none',
    '& .MuiDataGrid-cell:focus': {
      outline: 'none',
    },
    '& .MuiDataGrid-columnHeaders': {
      backgroundColor: '#F9FAFB',
      borderBottom: '1px solid #E5E7EB',
    },
    '& .MuiDataGrid-row:hover': {
      backgroundColor: '#F9FAFB',
    },
  }}
/>
```

### Modals

```jsx
// Using MUI Dialog
import { Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';

<Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
  <DialogTitle className="text-lg font-semibold">
    Modal Title
  </DialogTitle>
  <DialogContent>
    <div className="pt-4">
      {/* Modal content */}
    </div>
  </DialogContent>
  <DialogActions className="p-4 pt-0">
    <Button variant="secondary" onClick={handleClose}>Cancel</Button>
    <Button onClick={handleConfirm}>Confirm</Button>
  </DialogActions>
</Dialog>
```

---

## Icons

### MUI Icons (Primary)

```jsx
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import VisibilityIcon from '@mui/icons-material/Visibility';
import AddIcon from '@mui/icons-material/Add';
import SearchIcon from '@mui/icons-material/Search';
import CloseIcon from '@mui/icons-material/Close';
import CheckIcon from '@mui/icons-material/Check';
import WarningIcon from '@mui/icons-material/Warning';
import InfoIcon from '@mui/icons-material/Info';

// Usage with IconButton
import { IconButton } from '@mui/material';

<IconButton size="small" onClick={handleEdit} title="Edit">
  <EditIcon fontSize="small" />
</IconButton>

<IconButton size="small" color="error" onClick={handleDelete} title="Delete">
  <DeleteIcon fontSize="small" />
</IconButton>
```

### React Icons (Alternative)

```jsx
import { FiEdit, FiTrash2, FiEye, FiPlus } from 'react-icons/fi';

<button className="p-2 hover:bg-gray-100 rounded">
  <FiEdit className="w-4 h-4" />
</button>
```

---

## Common UI Patterns

### Page Header with Actions

```jsx
<div className="mb-6 flex justify-between items-center">
  <div>
    <h1 className="text-2xl font-bold text-gray-800">Page Title</h1>
    <p className="text-sm text-gray-500 mt-1">Page description</p>
  </div>
  <div className="flex gap-2">
    <Button variant="secondary" onClick={handleExport}>
      Export
    </Button>
    <Button onClick={() => navigate('/admin/features/create')}>
      Add New
    </Button>
  </div>
</div>
```

### Search/Filter Bar

```jsx
<div className="bg-white rounded-lg shadow p-4 mb-4">
  <div className="flex gap-4 items-end">
    <div className="flex-1">
      <Input
        label="Search"
        placeholder="Search by name..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
    </div>
    <div className="w-48">
      <label className="block text-sm font-medium text-gray-700 mb-1">
        Status
      </label>
      <select
        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
        value={statusFilter}
        onChange={(e) => setStatusFilter(e.target.value)}
      >
        <option value="">All</option>
        <option value="active">Active</option>
        <option value="inactive">Inactive</option>
      </select>
    </div>
    <Button onClick={handleSearch}>Search</Button>
  </div>
</div>
```

### Detail View Grid

```jsx
<div className="bg-white rounded-lg shadow p-6">
  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
      <label className="text-sm text-gray-500">Field Label</label>
      <p className="text-gray-800 font-medium">{data.field}</p>
    </div>
    <div>
      <label className="text-sm text-gray-500">Status</label>
      <p>
        <span className={`px-2 py-1 rounded text-sm ${
          data.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        }`}>
          {data.is_active ? 'Active' : 'Inactive'}
        </span>
      </p>
    </div>
    <div className="md:col-span-2">
      <label className="text-sm text-gray-500">Description</label>
      <p className="text-gray-800">{data.description || '-'}</p>
    </div>
  </div>
</div>
```

### Empty State

```jsx
<div className="bg-white rounded-lg shadow p-12 text-center">
  <div className="text-gray-400 mb-4">
    <InfoIcon style={{ fontSize: 48 }} />
  </div>
  <h3 className="text-lg font-medium text-gray-800 mb-2">No items found</h3>
  <p className="text-gray-500 mb-4">Get started by creating your first item.</p>
  <Button onClick={() => navigate('/admin/features/create')}>
    Create Feature
  </Button>
</div>
```

### Confirmation Dialog

```jsx
const handleDelete = (id) => {
  if (window.confirm('Are you sure you want to delete this item?')) {
    dispatch(deleteAction(id));
  }
};

// Or with MUI Dialog
const [deleteId, setDeleteId] = useState(null);

<Dialog open={!!deleteId} onClose={() => setDeleteId(null)}>
  <DialogTitle>Confirm Delete</DialogTitle>
  <DialogContent>
    Are you sure you want to delete this item? This action cannot be undone.
  </DialogContent>
  <DialogActions>
    <Button variant="secondary" onClick={() => setDeleteId(null)}>
      Cancel
    </Button>
    <Button variant="danger" onClick={() => confirmDelete(deleteId)}>
      Delete
    </Button>
  </DialogActions>
</Dialog>
```

### Stats Card

```jsx
<div className="bg-white rounded-lg shadow p-6">
  <div className="flex items-center justify-between">
    <div>
      <p className="text-sm text-gray-500">Total Customers</p>
      <p className="text-2xl font-bold text-gray-800">{stats.total}</p>
    </div>
    <div className="p-3 bg-blue-100 rounded-full">
      <UsersIcon className="w-6 h-6 text-blue-600" />
    </div>
  </div>
  <div className="mt-4 flex items-center text-sm">
    <span className="text-green-600">+12%</span>
    <span className="text-gray-500 ml-2">from last month</span>
  </div>
</div>
```

---

## Spacing Reference

| Class | Value | Usage |
|-------|-------|-------|
| `p-4` | 16px | Card padding (compact) |
| `p-6` | 24px | Card padding (standard) |
| `mb-4` | 16px | Element margin |
| `mb-6` | 24px | Section margin |
| `gap-2` | 8px | Button group gap |
| `gap-4` | 16px | Form field gap |
| `gap-6` | 24px | Grid gap |
| `space-y-4` | 16px | Vertical form spacing |

---

## Responsive Breakpoints

| Prefix | Min Width | Usage |
|--------|-----------|-------|
| (none) | 0px | Mobile first |
| `sm:` | 640px | Small tablets |
| `md:` | 768px | Tablets |
| `lg:` | 1024px | Laptops |
| `xl:` | 1280px | Desktops |

```jsx
// Example
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* 1 col mobile, 2 cols tablet, 3 cols desktop */}
</div>

<div className="hidden md:block">
  {/* Hidden on mobile, visible on tablet+ */}
</div>
```

---

## Animation Classes

```jsx
// Transitions
<button className="transition-colors duration-200">
  Smooth color change
</button>

<div className="transition-all duration-300">
  Smooth all properties
</div>

// Loading spinner
<div className="animate-spin h-5 w-5 border-2 border-blue-600 border-t-transparent rounded-full" />

// Pulse (for loading states)
<div className="animate-pulse bg-gray-200 h-4 rounded" />
```
