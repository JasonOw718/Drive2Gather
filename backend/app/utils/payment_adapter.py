from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

# Payment Processor Interface (Target)
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount, currency="MYR"):
        """
        Process a payment
        
        Args:
            amount (float): The payment amount
            currency (str): The currency code (default: MYR)
            
        Returns:
            dict: Payment result information
        """
        pass

# Adaptee: Existing classes with incompatible interfaces
class PayPalGateway:
    def pay(self, amount, currency="MYR"):
        """
        Process a payment through PayPal
        
        Args:
            amount (float): The payment amount
            currency (str): The currency code
            
        Returns:
            dict: Payment result information
        """
        logger.info(f"Processing ${amount} {currency} through PayPal")
        # In a real implementation, this would call the PayPal API
        return {
            "success": True,
            "transaction_id": "PP-" + str(hash(f"{amount}-{currency}"))[:10],
            "provider": "PayPal"
        }

class StripeGateway:
    def charge(self, amount, currency="MYR"):
        """
        Process a payment through Stripe
        
        Args:
            amount (float): The payment amount
            currency (str): The currency code
            
        Returns:
            dict: Payment result information
        """
        logger.info(f"Processing ${amount} {currency} through Stripe")
        # In a real implementation, this would call the Stripe API
        return {
            "success": True,
            "transaction_id": "ST-" + str(hash(f"{amount}-{currency}"))[:10],
            "provider": "Stripe"
        }

# Adapter: Adapts the Adaptee to the Target
class PayPalAdapter(PaymentProcessor):
    def __init__(self):
        self.paypal_gateway = PayPalGateway()
    
    def process_payment(self, amount, currency="MYR"):
        return self.paypal_gateway.pay(amount, currency)

class StripeAdapter(PaymentProcessor):
    def __init__(self):
        self.stripe_gateway = StripeGateway()
    
    def process_payment(self, amount, currency="MYR"):
        return self.stripe_gateway.charge(amount, currency)

# Payment Client
class PaymentClient:
    def __init__(self, payment_method="stripe"):
        """
        Initialize the payment client with the specified payment method
        
        Args:
            payment_method (str): The payment method to use ('paypal' or 'stripe')
        """
        self.set_payment_method(payment_method)
    
    def set_payment_method(self, payment_method):
        """
        Set the payment method
        
        Args:
            payment_method (str): The payment method to use ('paypal' or 'stripe')
        """
        if payment_method.lower() == "paypal":
            self.processor = PayPalAdapter()
        else:  # Default to Stripe
            self.processor = StripeAdapter()
    
    def make_payment(self, amount, currency="MYR"):
        """
        Make a payment using the configured processor
        
        Args:
            amount (float): The payment amount
            currency (str): The currency code
            
        Returns:
            dict: Payment result information
        """
        return self.processor.process_payment(amount, currency)

# Factory function to get a payment client
def get_payment_client(payment_method="stripe"):
    """
    Get a payment client for the specified payment method
    
    Args:
        payment_method (str): The payment method to use ('paypal' or 'stripe')
        
    Returns:
        PaymentClient: A payment client configured for the specified method
    """
    return PaymentClient(payment_method) 