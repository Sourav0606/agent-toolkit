---
name: clean-architecture
description: Enforces clean separation of concerns, Hexagonal Architecture (Ports and Adapters), and domain isolation. Use when designing backend services, separating business logic from frameworks, or structuring multi-layer applications.
---

# Clean Architecture & Domain Isolation

A pragmatic guide for organizing backend systems so business logic remains testable, decoupled from web frameworks, and resilient to database/library churn.

---

## 1. The Core Dependency Rule

Dependencies must point **inward** toward the core domain logic:

```
[ Frameworks & Drivers ]   -> (HTTP routes, DB drivers, CLI, message queues)
       │
       ▼
[ Adapters / Gateways ]    -> (Repositories, API clients, serializers)
       │
       ▼
[ Application Services ]   -> (Use-cases, orchestration, transactions)
       │
       ▼
[ Domain Core ]            -> (Entities, value objects, business rules)
```

- **Domain Core**: Pure data structures and business validation rules. Has **zero** imports from web frameworks (FastAPI, Express) or ORMs (SQLAlchemy, Prisma).
- **Application Services**: Coordinates use cases (e.g. `RegisterUserUseCase`). Calls repositories via interfaces/protocols.
- **Adapters**: Implements interfaces (e.g. `PostgresUserRepository`, `StripePaymentGateway`).
- **Frameworks**: Entry points (FastAPI routers, CLI commands, Celery tasks).

---

## 2. Component Structure (Python Example)

```
src/
  domain/
    models.py             # User, Order, Money (Pure dataclasses / value objects)
    exceptions.py         # InsufficientFundsError, UserNotFoundError
  application/
    interfaces.py         # Protocols: UserRepository, EmailSender
    use_cases/
      checkout.py         # CheckoutUseCase(user_repo, payment_gateway)
  infrastructure/
    database/
      models.py           # SQLAlchemy / ORM table mappings
      user_repository.py  # Implements UserRepository protocol
    gateways/
      stripe_client.py    # Implements PaymentGateway protocol
  entrypoints/
    api/
      v1/
        checkout_router.py # FastAPI route handlers
```

---

## 3. The Repository Protocol Pattern

Define interfaces in `application/interfaces.py` using Python's `Protocol` (structural subtyping) so domain and use cases remain decoupled from concrete ORMs:

```python
from typing import Protocol, Optional
from src.domain.models import User

class UserRepository(Protocol):
    def get_by_id(self, user_id: str) -> Optional[User]:
        ...
    def save(self, user: User) -> None:
        ...
```

---

## 4. The Ponytail Balance

Avoid over-abstraction:
- Do not create a repository interface for an entity that only has trivial CRUD operations and will never switch databases.
- Start simple: Keep use-cases as plain functions (`def checkout(order_id: str, db: Session)`) and extract formal ports and adapters only when complexity, multi-provider integrations, or unit-test mock friction justifies it.
