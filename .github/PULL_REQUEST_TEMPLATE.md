## Description
<!-- Provide a clear and concise summary of what this PR accomplishes. Mention the module/boundary affected. -->

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change adding functionality to a specific module)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Architectural / Refactoring / Performance improvement
- [ ] Documentation update

## Modular Monolith & Architecture Checklist
- [ ] My code adheres strictly to PEP8 (Backend) and clean TypeScript standards (Frontend).
- [ ] No business logic is placed inside Django API Views / ViewSets.
- [ ] No AI inference or ML logic is placed inside API Views or basic business services (only inside `ai_engine/`).
- [ ] All database queries and domain mutations pass through clean `Service -> Repository` layers.
- [ ] New or modified environment variables have been documented in `.env.example`.
- [ ] All automated tests (`pytest`, `npm run type-check`, `lint`) pass locally.
- [ ] I have verified that no large files (>500 lines) were introduced without proper separation of concerns.

## Screenshots / API Payloads
<!-- If this introduces visual changes or API endpoint modifications, attach screenshots or JSON request/response payloads here. -->
