# API & Database Permissions

## Database Permissions (Sqlite)

Superusers (Pocketbase) have access to database. Currently member from &effect are superusers.

## Vector Database Permission (Qdrant)

&effect members have full database administration rights. The database can be publicly accessed, but it is protected via API Key. Currently, the database cannot be limited to a distinct IP range.

## Pocketbase API Rules

**Access Control**: &effect members have superuser privileges with full database administration rights. Application access is restricted to authenticated users from &effect and GIZ organizations, while unauthenticated users have public read-only access to submissions and topics.

### User Table

- **List/Search**: Authenticated Users
- **View**: Authenticated Users  
- **Create**: Authenticated Users
- **Update**: Authenticated Users
- **Delete**: Authenticated Users

### API Tokens Table

- **List/Search**: Superuser only
- **View**: Superuser only
- **Create**: Superuser only
- **Update**: Superuser only
- **Delete**: Superuser only

### Topics Table

- **List/Search**: Public
- **View**: Public
- **Create**: Authenticated Users, Token-based
- **Update**: Authenticated Users, Token-based
- **Delete**: Authenticated Users, Token-based

### Submissions

- **List/Search**: Public
- **View**: Public
- **Create**: Authenticated Users, Token-based
- **Update**: Authenticated Users, Token-based
- **Delete**: Authenticated Users, Token-based

### Submissions Per Session View

- **List/Search**: Public
- **View**: Public

### Submissions Per Topics View

- **List/Search**: Public
- **View**: Public
  
## API Endpoints

### Authentication Required

- `/api/synchronize-submission` - Token-based
- `/api/process-submission` - Token-based
- `/api/delete-submission-vector` - Token-based

### Public Endpoints

- `/api/ping`
- `/api/query-submission` - Rate Limiting (20 per minute, 5 per second)
- `/api/summarize-key-element` - Rate Limited (20 per minute, 5 per second)