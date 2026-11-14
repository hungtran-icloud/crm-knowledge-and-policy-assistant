"""Domain exceptions — mapped to HTTP responses in exception handlers."""

class PolicyNotFound(Exception): pass
class AccessDenied(Exception): pass
class PolicyWithdrawn(Exception): pass
class InsufficientEvidence(Exception): pass
class CitationValidationFailed(Exception): pass
class CriticalFieldMissing(Exception): pass
class SourceConflict(Exception): pass
