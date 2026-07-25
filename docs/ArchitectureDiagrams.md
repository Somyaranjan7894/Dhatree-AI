# Dhatree AI System Architecture Diagrams

This document contains visual representations of the Dhatree AI v1.0.0 architecture. These diagrams are generated using Mermaid.js and represent the strict Modular Monolith patterns and Free-Tier cloud infrastructure.

## 1. High-Level System Architecture

```mermaid
graph TD
    Client[Web Browser / React Frontend] -->|HTTPS / REST API| API_GW[Django REST Framework]
    
    subgraph "Backend System (Modular Monolith)"
        API_GW --> Auth[Authentication Module]
        API_GW --> Core[Core & User Management]
        API_GW --> Farms[Farms & Soil Module]
        API_GW --> CropRec[Crop Recommendation Module]
        API_GW --> FertRec[Fertilizer Recommendation Module]
        API_GW --> DiseaseDet[Disease Detection Module]
        API_GW --> AIAssist[AI Assistant & Analytics]
        
        CropRec -->|Interface| AIEngine[AI Engine]
        FertRec -->|Interface| AIEngine
        DiseaseDet -->|Interface| AIEngine
        AIAssist -->|Interface| AIEngine
    end
    
    subgraph "AI Engine (Decoupled)"
        AIEngine --> CropModel[(RandomForest Crop Model)]
        AIEngine --> FertModel[(Fertilizer Logic/Models)]
        AIEngine --> CNNModel[(PyTorch/TF CNN Model)]
        AIEngine --> RAG[(Knowledge Base Engine)]
    end
    
    subgraph "Data Persistence Layer"
        Auth --> DB[(PostgreSQL)]
        Core --> DB
        Farms --> DB
        CropRec --> DB
        FertRec --> DB
        DiseaseDet --> DB
        AIAssist --> DB
        
        DiseaseDet --> Cloudinary[Cloudinary Media Storage]
    end
    
    subgraph "Asynchronous & Event Layer"
        API_GW --> Celery[Celery Worker]
        Celery --> Redis[(Redis Broker)]
        Celery --> Notifications[Push / Email Service]
    end
```

## 2. Database Entity-Relationship (ER) Diagram

```mermaid
erDiagram
    USER ||--o{ FARM : owns
    USER ||--o{ CROP_RECOMMENDATION : requests
    USER ||--o{ DISEASE_PREDICTION : requests
    USER ||--o{ FERTILIZER_RECOMMENDATION : requests
    USER ||--o{ CHAT_SESSION : has
    
    FARM ||--o{ SOIL_RECORD : contains
    FARM ||--o{ WEATHER_RECORD : contains
    FARM ||--o{ FARM_ACTIVITY : logs
    
    DISEASE_PREDICTION ||--|| KNOWLEDGE_BASE : diagnoses
    
    USER {
        uuid id PK
        string email
        string password
        string role
        boolean is_active
    }
    
    FARM {
        uuid id PK
        uuid user_id FK
        string name
        float size_hectares
        string location
    }
    
    CROP_RECOMMENDATION {
        uuid id PK
        uuid user_id FK
        uuid farm_id FK
        float n_p_k
        float ph
        string predicted_crop
        float confidence
    }
    
    DISEASE_PREDICTION {
        uuid id PK
        uuid user_id FK
        uuid farm_id FK
        string image_url
        string predicted_disease
        float confidence
    }
    
    KNOWLEDGE_BASE {
        uuid id PK
        string disease_name
        string symptoms
        string treatment
        string prevention
    }
```

## 3. System Component Diagram (Service Layer Pattern)

```mermaid
graph LR
    subgraph "HTTP Layer (Controllers)"
        V_Crop[CropRecommendationView]
        V_Disease[DiseaseDetectionView]
    end

    subgraph "Service Layer (Business Logic)"
        S_Crop[CropRecommendationService]
        S_Disease[DiseaseDetectionService]
        S_Audit[Audit/Notification Service]
    end

    subgraph "Repository Layer (Data Access)"
        R_Crop[CropRecommendationRepository]
        R_Disease[DiseasePredictionRepository]
        R_Farm[FarmRepository]
    end

    subgraph "External Systems"
        AI_Registry[AI Model Registry]
        DB[(PostgreSQL)]
    end

    V_Crop -->|DTO| S_Crop
    V_Disease -->|DTO + File| S_Disease
    
    S_Crop --> R_Crop
    S_Crop --> R_Farm
    S_Crop --> AI_Registry
    S_Crop --> S_Audit
    
    S_Disease --> R_Disease
    S_Disease --> AI_Registry
    S_Disease --> S_Audit
    
    R_Crop --> DB
    R_Disease --> DB
    R_Farm --> DB
```

## 4. Free-Tier Deployment Architecture

```mermaid
graph TD
    Internet((Internet / End Users)) --> Vercel[Vercel CDN]
    
    subgraph "Vercel (Frontend Hosting)"
        Vercel --> React[React + Vite SPA]
    end
    
    React -->|HTTPS REST API| Render[Render Web Service]
    
    subgraph "Render (Backend Hosting)"
        Render --> Gunicorn[Gunicorn + Django]
        Render --> WhiteNoise[WhiteNoise Static Server]
    end
    
    subgraph "Serverless Infrastructure"
        Gunicorn --> Neon[(Neon PostgreSQL - Free Tier)]
        Gunicorn --> Upstash[(Upstash Redis - Cache/Celery)]
        Gunicorn --> Cloudinary[Cloudinary - Media/Image Storage]
    end
    
    subgraph "CI/CD Pipeline"
        GitHub[GitHub Repo] -->|Actions| Tests[Pytest & Vitest]
        Tests -->|Deploy Trigger| Vercel
        Tests -->|Deploy Trigger| Render
    end
```
