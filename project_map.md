saas/                               # Root directory of the project
├── .github/                        # GitHub configuration directory
│   └── workflows/                  # CI/CD pipelines folder
│       └── deploy.yml              # GitHub Actions pipeline for automated deployment
│
├── nginx/                          # Reverse proxy and web server directory
│   ├── Dockerfile                  # Container blueprint for building the Nginx image
│   └── nginx.conf                  # Routes traffic incoming to Frontend, Backend, and n8n
│
├── frontend/                       # User Interface layer built with React and Vite
│   ├── public/                     # Static assets served directly to the browser
│   │   ├── favico.svg              # Browser favorite icon for the application
│   │   └── icons.svg               # SVG sprite sheet containing shared UI icons
│   │
│   ├── src/                        # Core React application source code
│   │   ├── assets/                 # Global visual media and image files
│   │   │   └── *.svg               # Raw application graphics and vector assets
│   │   │
│   │   ├── components/             # Reusable UI parts and modular presentation building blocks
│   │   │   ├── ui/                 # Atomic design system atoms (shadcn/buttons/inputs)
│   │   │   ├── ProductPreview.jsx  # Interactive view showing how a product will look live
│   │   │   └── PublishControl.jsx  # Panel with controls to trigger distribution pipelines
│   │   │
│   │   ├── contexts/               # React global state management contexts
│   │   │   └── AuthContext.jsx     # Manages global user login state, tokens, and permissions
│   │   │
│   │   ├── pages/                  # Main application views mapped to router paths
│   │   │   ├── Dashboard.jsx       # Central metrics, user overview, and control panel screen
│   │   │   ├── Login.jsx           # User authentication screen for signing in
│   │   │   └── Register.jsx        # Account onboarding and registration screen
│   │   │
│   │   ├── services/               # Outbound network request abstraction layer
│   │   │   └── api.js              # Axios/Fetch client configured to hit backend API endpoints
│   │   │
│   │   ├── App.css                 # Global application style layout modifications
│   │   ├── App.jsx                 # Main application shell housing routing and providers
│   │   ├── index.css               # Tailwind CSS declarations and base style layers
│   │   └── main.jsx                # Application entry point binding React to the DOM HTML
│   │
│   ├── .env.development            # Environment variables tailored for local developer usage
│   ├── .env.production             # Client environment variables targeted for production builds
│   ├── .gitignore                  # Specifies frontend-specific files to ignore in Git
│   ├── Dockerfile                  # Container blueprint for serving production static files
│   ├── eslint.config.js            # Code linter configurations ensuring strict code quality
│   ├── index.html                  # Single Page Application root markup skeleton file
│   ├── package-lock.json           # Locked exact dependency tree version history log
│   ├── package.json                # Project node metadata scripts and dependency list manifest
│   ├── vite.config.js              # Bundler builder configurations for development server
│   └── readme.md                   # Documentation guide specifically for frontend setup
│
├── backend/                        # Central business logic REST API built with FastAPI
│   ├── app/                        # Main Python core execution logic folder
│   │   ├── __init__.py             # Initializes the app folder as a python package module
│   │   ├── main.py                 # Core initialization entry point bootstrapping FastAPI
│   │   ├── config.py               # Evaluates and enforces system environment variable schemas
│   │   ├── crypto.py               # Password hashing utilities and cryptographical token generation
│   │   ├── database.py             # Configures database client connections and session lifecycle
│   │   ├── models.py               # SQLModel/SQLAlchemy definitions mapping tables to database
│   │   └── schemas.py              # Pydantic data modeling enforcing request validation structures
│   │   
│   ├── services/
│   │   ├── __init__.py             # Initializes the app folder as a python package module
│   │   ├── n8n_service.py
│   │   └── product_service.py
|   |
│   ├── api/                        # Route controller segment grouping specific endpoints
│   │   ├── __init__.py             # Exposes the API endpoint route packages
│   │   ├── auth.py                 # Handles registration, secure login, and JWT state issuance
│   │   └── products.py             # Business routing managing link generation algorithms
│   │   
│   ├── scrapers/                   # Web scraping data extraction services
│   │   ├── __init__.py             # Makes scraping modules available for imports
│   │   └── product_scrapers.py     # Parses third-party target URLs extraction scripts
│   │
│   ├── ai_services/                # Machine learning API integration modules
│   │   ├── __init__.py             # Formulates AI services as accessible code modules
│   │   └── open_ai.py              # Manages API requests directed towards OpenAI engines
│   │
│   ├── .env.production             # Protected production database secrets (never commit to git!)
│   ├── requirements.txt            # Explicit list of Python third-party dependencies needed
│   └── Dockerfile                  # Container blueprint for building the FastAPI runtime
│
├── n8n-automation/                 # Low-code automated workflow and dispatch distribution engine
│   └── workflows/                  # Storage folder for automated pipelines
│       └── publish_pipeline.json   # Exported JSON representing active n8n automation flow
│
├── docker-compose.yml              # Master orchestrator file linking all app container engines
├── .gitignore                      # Specifies global system-level files to ignore in Git
└── readme.md                       # Comprehensive guide covering the entire SaaS architecture