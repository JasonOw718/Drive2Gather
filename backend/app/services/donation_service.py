from app.models import db, Donation, User, Donor
from datetime import datetime
import logging
from app.utils.payment_adapter import get_payment_client

def create_donation(user_id, donor_id, amount, payment_method='stripe', description=None):
    """
    Create a new donation
    
    Args:
        user_id (int): ID of the user receiving the donation (driver)
        donor_id (int): ID of the donor (passenger)
        amount (float): Amount of the donation
        payment_method (str): Payment method ('paypal' or 'stripe')
        description (str, optional): Description or message for the donation
        
    Returns:
        tuple: (donation_data, error)
    """
    try:
        # Validate user exists
        user = User.query.get(user_id)
        if not user:
            return None, f"User with ID {user_id} not found"
        
        # Validate donor exists
        donor = User.query.get(donor_id)
        if not donor:
            return None, f"Donor with ID {donor_id} not found"
        
        # Check if donor record exists, create if not
        donor_record = Donor.query.get(donor_id)
        if not donor_record:
            donor_record = Donor(user_id=donor_id)
            db.session.add(donor_record)
        
        # Process payment using the adapter pattern
        payment_client = get_payment_client(payment_method)
        payment_result = payment_client.make_payment(float(amount))
        
        if not payment_result.get('success'):
            return None, f"Payment processing failed: {payment_result.get('error', 'Unknown error')}"
        
        # Create donation
        donation = Donation(
            user_id=user_id,
            donor_id=donor_id,
            amount=float(amount),
            date=datetime.utcnow(),
            description=description,
            payment_method=payment_method
        )
        
        db.session.add(donation)
        db.session.commit()
        
        # Format response
        donation_data = {
            "donationId": donation.donation_id,
            "userId": donation.user_id,
            "donorId": donation.donor_id,
            "amount": float(donation.amount),
            "date": donation.date.isoformat(),
            "description": donation.description,
            "paymentMethod": donation.payment_method,
            "transactionId": payment_result.get('transaction_id')
        }
        
        return donation_data, None
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error creating donation: {str(e)}")
        return None, str(e)

def get_user_donations(user_id, page=1, size=20):
    """
    Get donations received by a user
    
    Args:
        user_id (int): ID of the user
        page (int): Page number (default: 1)
        size (int): Page size (default: 20)
        
    Returns:
        dict: Dictionary containing donations and pagination info
    """
    # Calculate offset
    offset = (page - 1) * size
    
    # Get donations for the user
    donations_query = Donation.query.filter_by(user_id=user_id).order_by(Donation.date.desc())
    
    # Get total count
    total = donations_query.count()
    
    # Get paginated donations
    donations = donations_query.offset(offset).limit(size).all()
    
    # Format donations
    donations_data = []
    for donation in donations:
        # Get donor info
        donor = User.query.get(donation.donor_id)
        donor_name = donor.name if donor else "Anonymous"
        
        donations_data.append({
            "donationId": donation.donation_id,
            "donorId": donation.donor_id,
            "donorName": donor_name,
            "amount": float(donation.amount),
            "date": donation.date.isoformat(),
            "description": donation.description,
            "paymentMethod": donation.payment_method
        })
    
    # Calculate pagination values
    total_pages = (total + size - 1) // size if total > 0 else 1
    next_page = page + 1 if page < total_pages else None
    prev_page = page - 1 if page > 1 else None
    
    return {
        "donations": donations_data,
        "pagination": {
            "currentPage": page,
            "pageSize": size,
            "totalPages": total_pages,
            "totalDonations": total,
            "nextPage": next_page,
            "prevPage": prev_page
        }
    }

def get_donor_donations(donor_id, page=1, size=20):
    """
    Get donations made by a donor
    
    Args:
        donor_id (int): ID of the donor
        page (int): Page number (default: 1)
        size (int): Page size (default: 20)
        
    Returns:
        dict: Dictionary containing donations and pagination info
    """
    # Calculate offset
    offset = (page - 1) * size
    
    # Get donations for the donor
    donations_query = Donation.query.filter_by(donor_id=donor_id).order_by(Donation.date.desc())
    
    # Get total count
    total = donations_query.count()
    
    # Get paginated donations
    donations = donations_query.offset(offset).limit(size).all()
    
    # Format donations
    donations_data = []
    for donation in donations:
        # Get recipient info
        recipient = User.query.get(donation.user_id)
        recipient_name = recipient.name if recipient else "Unknown"
        
        donations_data.append({
            "donationId": donation.donation_id,
            "recipientId": donation.user_id,
            "recipientName": recipient_name,
            "amount": float(donation.amount),
            "date": donation.date.isoformat(),
            "description": donation.description,
            "paymentMethod": donation.payment_method
        })
    
    # Calculate pagination values
    total_pages = (total + size - 1) // size if total > 0 else 1
    next_page = page + 1 if page < total_pages else None
    prev_page = page - 1 if page > 1 else None
    
    return {
        "donations": donations_data,
        "pagination": {
            "currentPage": page,
            "pageSize": size,
            "totalPages": total_pages,
            "totalDonations": total,
            "nextPage": next_page,
            "prevPage": prev_page
        }
    } 