# Data Model: User Authentication (MongoDB)

## Collections

### users

**Description**: Stores user account information.

**Fields**:
- `_id`: MongoDB ObjectId (Primary Key)
- `email`: Email Address (unique, string, validated format)
- `hashed_password`: Hashed Password (string, stores Argon2 hash)
- `registration_date`: Registration Date (timestamp)
- `last_login_date`: Last Login Date (timestamp, nullable)

**Indexes**:
- `email`: Unique index to ensure email addresses are unique.

**Validation Rules**:
- `email`: Must be a valid and unique email format.
- `hashed_password`: Must be a valid Argon2 hash.

### sessions

**Description**: Stores active user authentication sessions or tokens.

**Fields**:
- `_id`: MongoDB ObjectId (Primary Key, or could use JWT `jti` for token-based)
- `user_id`: Reference to `users._id` (links to the User document)
- `token`: Session/Token Value (string, unique, for refresh tokens or session IDs)
- `expiration_timestamp`: Expiration Timestamp (timestamp)
- `creation_timestamp`: Creation Timestamp (timestamp)
- `ip_address`: IP Address (string, nullable)

**Indexes**:
- `user_id`: Index for efficient lookup of sessions by user.
- `token`: Unique index for session/token value.
- `expiration_timestamp`: Index for efficient cleanup of expired sessions.

**Validation Rules**:
- `expiration_timestamp`: Must be a future timestamp.
