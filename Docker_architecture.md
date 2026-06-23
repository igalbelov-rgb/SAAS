## 🐳 Docker Containers Architecture & Roles

Our SaaS platform is built using a microservices architecture, where each component runs inside its own isolated Docker container. Below is the breakdown of each container's role and how they interact within the internal network (`saas-network`).

---

### 1. `nginx` (The Gatekeeper & Reverse Proxy)
* **Image:** Custom build from `./nginx/Dockerfile`
* **Ports Exposed:** `80` (HTTP) & `443` (HTTPS)
* **Role:** This is the **only** container facing the public internet (alongside n8n's visual port if exposed). It acts as a traffic controller:
  * When a user requests web pages (e.g., `/dashboard`), Nginx serves the static **Frontend** files.
  * When the frontend makes API requests (e.g., `/api/v1/...`), Nginx securely routes them internally to the **Backend** service.

### 2. `frontend` (The User Interface)
* **Image:** Custom build from `./frontend/Dockerfile` (React + Vite Build)
* **Role:** Manages everything the user sees in their browser. This includes the product layout grids, responsive input fields for links, interactive copywriting cards, user authentication screens (Login/Register), and billing status layouts. It communicates strictly via HTTP requests routed through Nginx.

### 3. `backend` (The Core Engine & Brain)
* **Image:** Custom build from `./backend/Dockerfile` (FastAPI)
* **Role:** Handles the entire core business logic of the SaaS application:
  * Manages JWT authentication and user sessions.
  * Triggers asynchronous scrapers (`ProductScraper`) to extract details from raw e-commerce links.
  * Communicates with the **Groq API** (Llama 3) to instantly generate English marketing copy.
  * Saves or retrieves application data from the PostgreSQL database.

### 4. `postgres-db` (The Vault & Persistent Storage)
* **Image:** `postgres:16-alpine`
* **Role:** The long-term database storage for the entire application. It securely maintains user records (hashed credentials), processed product histories, dynamic affiliate parameters, and active Stripe subscription states. A built-in `healthcheck` ensures the Backend service will not fully boot until this database is stable and ready to accept connections.

### 5. `n8n` (The Automation & Dispatch Engine)
* **Image:** `docker.n8n.io/n8nio/n8n:latest`
* **Ports Exposed:** `5678` (Visual Admin Dashboard)
* **Role:** Operates as our decentralized event dispatcher. Instead of bloating our Python Backend with multiple third-party social media SDKs, credential tokens, and complex retry logics for external platform crashes, FastAPI simply throws a fast Webhook request to n8n. n8n then handles the heavy lifting of seamlessly publishing posts to Telegram, Facebook, or Pinterest via its visual pipeline architecture.

---

## 🗺️ Architectural Workflow Flowchart

Below is a conceptual visualization of how data flows through our containers:

1. **User Interaction:** User clicks "Publish" on the React Client (`frontend`).
2. **Proxy Routing:** Request hits the `nginx` proxy and gets redirected to the FastAPI `backend`.
3. **Data Retrieval:** Backend updates the user status inside `postgres-db`.
4. **Automation Trigger:** Backend sends a fast HTTP POST payload containing the Groq-generated text to `n8n`.
5. **Social Dispatch:** `n8n` securely picks up the payload and immediately broadcasts it to the respective social media networks.