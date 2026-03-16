# MEMS - Modular Entity and Mapping System

A robust Django REST Framework application built to manage entities and their relationships.

## Features
- **Master Apps**: `vendor`, `product`, `course`, `certification`.
- **Mapping Apps**: `vendor_product_mapping`, `product_course_mapping`, `course_certification_mapping`.
- **Custom Built**: Strict usage of DRF `APIView` (no mixins, generics, or ViewSets).
- **Validation Rules**: Ensures mappings are unique per pair and limits "primary_mapping=True" to one per parent entity.
- **API Documentation**: Interactive Swagger (`/swagger/`) and ReDoc (`/redoc/`) via `drf-yasg`.

## Setup Instructions

### Prerequisites
- Python 3.9+
- Activated Virtual Environment

### Installation
1. Clone the repository and navigate into the project directory:
   ```bash
   cd mems
   ```
2. Install the required packages:
   ```bash
   pip install django djangorestframework drf-yasg
   ```

### Running the App
1. Apply migrations to set up the database:
   ```bash
   python manage.py makemigrations vendor product course certifications vendor_product_mapping product_course_mapping course_certification_mapping core
   python manage.py migrate
   ```
2. Seed the database with initial testing data using the custom command:
   ```bash
   python manage.py seed_data
   ```
3. Start the development server:
   ```bash
   python manage.py runserver
   ```

## API Usage Examples

APIs support standard List/Create and Retrieve/Update/Delete operations. 

### Documentation
Launch the server and browse to:
- **Swagger**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`

### Example: Vendors
- **GET** `/api/vendors/?name=Vendor&is_active=true` - List vendors with optional query filters.
- **POST** `/api/vendors/` - Create a new vendor.
  ```json
  {
      "name": "New Vendor",
      "code": "V005",
      "description": "Example description"
  }
  ```

### Example: Vendor -> Product Mapping
- **GET** `/api/vendor-product-mappings/?parent_id=1` - Get mappings for a specific vendor.
- **POST** `/api/vendor-product-mappings/` - Create a mapping. Requires validation rules to be met (No duplicate pairs, max one `primary_mapping` true).
  ```json
  {
      "parent": 1,
      "child": 2,
      "primary_mapping": true
  }
  ```

## Contact
This project is an example implementation of the Mems AICERT guidelines. Wait, memsAICERT rules were followed strictly.
