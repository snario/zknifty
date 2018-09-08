class InvalidTxSignatureException(Exception):
    """the signature of a tx is invalid"""

class RequestFailedException(Exception):
    """request failed without success http status"""
