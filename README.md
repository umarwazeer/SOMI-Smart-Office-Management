# SOMI — Smart Office Management & Intelligence

SOMI (Smart Office Management & Intelligence) is a modern web-based office and HR management platform developed as a Final Year Project (FYP).

The system combines traditional HRMS functionality with an intelligence layer for attendance, leave, tasks, performance, payroll, notifications, reporting, and AI-assisted natural-language interaction.

## Project Overview

SOMI is designed to help organizations manage day-to-day employee and office operations through a centralized platform.

The project follows a layered architecture:

```text
SOMI Frontend
    ↓
Django REST API
    ↓
SOMI Intelligence Engine
    ↓
Operational SOMI Data
```

The Intelligence Engine analyzes controlled application data and provides structured insights. An AI Assistant can then use those controlled insights to generate natural-language responses.

## Main Features

### HR & Employee Management
- Employee management
- Employee profiles
- Department management
- Role-based access
- Employee profile images
- Employee search and filtering

### Attendance Management
- Attendance records
- Check-in / check-out
- Present, absent, late, and on-leave statuses
- Attendance reports
- Attendance analytics
- Attendance pattern insights

### Leave Management
- Leave types
- Leave requests
- Leave approval workflow
- Pending, approved, and rejected requests
- Leave reporting
- Leave concentration insights

### Task Management
- Task creation and management
- Task assignment
- Task status tracking
- Priority management
- Pending and overdue task analysis
- Workload insights

### Performance Management
- Employee performance reviews
- Performance ratings
- Goals and review metrics
- Review status tracking
- Performance trends and observations

### Payroll Management
- Payroll records
- Salary information
- Allowances
- Deductions
- Department payroll summaries
- Payroll intelligence

### Notifications
- System notifications
- Intelligent operational alerts
- Context-aware information for users

### AI & Intelligence

SOMI is not designed as a simple chatbot. Its AI architecture separates deterministic business intelligence from natural-language generation.

Current intelligence areas include:

- Office overview
- Attendance intelligence
- Leave intelligence
- Task intelligence
- Performance intelligence
- Payroll intelligence
- Smart alerts
- Natural-language AI Assistant
- AI-ready architecture for future predictive intelligence
- AI report generation roadmap
- Knowledge/RAG assistant roadmap

## AI Architecture

```text
                    SOMI FRONTEND
                         │
              ┌──────────┴──────────┐
              │                     │
        AI Dashboard          AI Assistant
              │                     │
              └──────────┬──────────┘
                         ↓
                 AI API Layer
                  Django / DRF
                         ↓
             SOMI Intelligence Engine
                         │
       ┌─────────────────┼─────────────────┐
       ↓                 ↓                 ↓
 Attendance           Leave             Tasks
 Intelligence       Intelligence      Intelligence
       │                 │                 │
       └─────────────────┼─────────────────┘
                         ↓
             Performance / Payroll
                  Intelligence
                         ↓
                 SOMI Operational Data
                         │
      ┌──────────┬───────┼────────┬──────────┐
      ↓          ↓       ↓        ↓          ↓
 Employees  Departments Attendance Leave    Tasks
                         │
                  Performance
                         │
                      Payroll
```

### AI Design Principle

The AI layer does not receive unrestricted direct database access.

Instead:

1. SOMI application services collect controlled data.
2. The Intelligence Engine calculates structured metrics and observations.
3. Role permissions control what information a user can access.
4. The AI Assistant receives controlled SOMI information.
5. The LLM converts that information into a natural-language response.

This approach keeps business logic and access control inside the application rather than relying on the LLM to make authorization decisions.

## Technology Stack

### Frontend

- Vue.js 3
- Quasar Framework 2
- Vue Router
- Vuex
- Axios
- Chart.js
- JavaScript
- HTML5
- CSS

### Backend

- Python
- Django
- Django REST Framework
- Django Simple JWT
- MySQL
- Django ORM
- CORS support

### AI / Intelligence

- Python-based deterministic intelligence engine
- OpenAI API integration
- Local LLM support planned/being integrated through Ollama
- Controlled application-level AI data flow

### Development Tools

- Git
- GitHub
- Visual Studio Code
- PowerShell
- Postman / browser API testing

## User Roles

SOMI supports three primary roles:

| Role | Description |
|---|---|
| Admin | Full system and management access |
| Manager | Management and operational access according to permissions |
| Employee | Employee-level access to permitted information and functions |

Access control is enforced at the application/API level.

## Project Structure

```text
SOMI-Smart-Office-Management/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── router/
│   │   ├── store/
│   │   └── boot/
│   ├── package.json
│   └── quasar.conf.js
│
├── somi-backend/
│   ├── accounts/
│   ├── attendance/
│   ├── departments/
│   ├── employees/
│   ├── intelligence/
│   ├── leave/
│   ├── notifications/
│   ├── payroll/
│   ├── performance/
│   ├── tasks/
│   ├── config/
│   ├── manage.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

## Backend API

The backend runs locally at:

```text
http://127.0.0.1:8000
```

API base:

```text
http://127.0.0.1:8000/api
```

### Authentication

```text
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/token/refresh/
GET  /api/auth/me/
POST /api/auth/logout/
```

### Intelligence

```text
GET  /api/intelligence/
POST /api/intelligence/assistant/
```

The intelligence overview endpoint provides structured SOMI intelligence data.

The assistant endpoint accepts a natural-language question and returns an AI-generated response based on controlled SOMI intelligence data.

## Local Development Setup

### 1. Clone the Repository

```powershell
git clone https://github.com/umarwazeer/SOMI-Smart-Office-Management.git
cd SOMI-Smart-Office-Management
```

### 2. Backend Setup

Open PowerShell in the project root:

```powershell
cd .\somi-backend\
```

Create and activate the virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Configure the required environment variables.

Example:

```text
OPENAI_API_KEY=your_api_key_here
SOMI_AI_MODEL=your_model_name
```

Do not commit real API keys or other secrets to GitHub.

Run migrations:

```powershell
python manage.py migrate
```

Check the Django project:

```powershell
python manage.py check
```

Start the backend:

```powershell
python manage.py runserver
```

Backend:

```text
http://127.0.0.1:8000
```

### 3. Frontend Setup

Open another PowerShell window:

```powershell
cd .\frontend\
```

Install dependencies:

```powershell
npm install
```

Start the Quasar development server:

```powershell
npm run dev
```

The frontend is configured to run on the project's development port.

## Environment Variables

Secrets must be stored outside Git.

Example environment configuration:

```text
OPENAI_API_KEY=your_api_key_here
SOMI_AI_MODEL=your_model_name
```

The repository intentionally does not contain real API credentials.

For local AI providers such as Ollama, the model runtime can be configured locally without committing model files to GitHub.

## Security

SOMI follows several security principles:

- JWT-based authentication
- Role-based permissions
- Backend API authorization
- Controlled AI data access
- No unrestricted database access for LLMs
- Environment variables for API credentials
- Secrets excluded through `.gitignore`
- Local AI model files excluded from Git
- Sensitive payroll information restricted by role

Never commit:

```text
.env
API keys
database passwords
JWT secrets
local model files
private credentials
```

## AI Implementation Strategy

SOMI uses a hybrid intelligence approach.

### Deterministic Intelligence

Traditional Python/Django application logic calculates reliable metrics such as:

- Attendance rates
- Absence rates
- Late frequency
- Leave counts
- Leave concentration
- Task completion
- Workload distribution
- Performance averages
- Payroll totals
- Operational alerts

### LLM Layer

The LLM is used primarily for:

- Natural-language answers
- Human-readable summaries
- Explanation of structured intelligence
- Natural-language reporting

This separation makes the system easier to test, explain, and demonstrate during the FYP viva.

## Example AI Questions

The SOMI AI Assistant is designed to answer questions such as:

```text
How is attendance this month?

Which department has the highest leave activity?

Show me the current pending tasks.

What are the main operational alerts?

Give me a short summary of this month's office performance.
```

The assistant should only answer organization-specific questions using information available through the controlled SOMI intelligence layer.

## Future Intelligence Roadmap

Planned extensions include:

- Predictive attendance intelligence
- Leave demand forecasting
- Workload forecasting
- Advanced anomaly detection
- AI-generated monthly office reports
- Natural-language reporting
- Smart employee search
- Intelligent notifications
- Department intelligence dashboards
- Office operational status dashboard
- AI knowledge assistant
- RAG-based HR policy and SOP assistant
- Local/free LLM provider support
- Multi-provider AI architecture

## Academic Project

SOMI is developed as a university Final Year Project.

### Project Name

**SOMI — Smart Office Management & Intelligence**

### Project Type

**Final Year Project (FYP)**

### Primary Objective

To develop a modern office and HR management platform that combines conventional business management functionality with data-driven intelligence and AI-assisted interaction.

## Current Development Status

The project is under active development.

Implemented areas include:

- Authentication
- Role-based access
- Employee management
- Department management
- Attendance management
- Leave management
- Task management
- Performance management
- Payroll management
- Notifications
- Intelligence Engine
- Smart Alerts
- AI Assistant API
- Modern Quasar frontend
- Django REST backend
- Git/GitHub monorepo architecture

Future modules and advanced AI capabilities will continue to be developed as part of the project roadmap.

## Repository

GitHub:

https://github.com/umarwazeer/SOMI-Smart-Office-Management

## License

This project is developed as an academic Final Year Project.

Unless otherwise stated, the project source code is intended for academic and educational use.
