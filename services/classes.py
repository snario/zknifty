
# SignedTransferTransaction object that user sends to operator aggregating orders 
#
class SignedTransferTransaction(object):
    
    ####
    # senderPubKey = []   := [x_key, y_key] of sender  
    # receiverPubKey = [] := [x_key, y_key] of receiver
    # tokenID = 0         := ID of token to transfer
    # R = []              := [R_x, R_y] R points of EDDCSA signature
    # S = 0               := S variable from EDDCSA signature
    ####
    
    def __init__(self, senderPubKey, receiverPubKey, tokenID, R, S):
      self.senderPubKey = senderPubKey
      self.receiverPubKey = receiverPubKey
      self.tokenID = tokenID
      self.R = R
      self.S = S
