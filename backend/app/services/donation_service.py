from app.models import db, Donation, User, Donor
from datetime import datetime
import logging
from app.utils.payment_adapter import get_payment_client
from sqlalchemy import func, desc

def create_donation(user_id, donor_id, amount, payment_method='stripe', description=None):
    """
    Create a new donation
    
    Args:
        user_id (int or None): ID of the user receiving the donation (driver), None for system donations
        donor_id (int): ID of the donor (passenger)
        amount (float): Amount of the donation
        payment_method (str): Payment method ('paypal' or 'stripe')
        description (str, optional): Description or message for the donation
        
    Returns:
        tuple: (donation_data, error)
    """
    try:
        # Validate user exists (if not a system donation)
        if user_id is not None:
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

def get_donor_stats(donor_id):
    """
    Get donation statistics for a donor
    
    Args:
        donor_id (int): ID of the donor
        
    Returns:
        dict: Dictionary containing donation statistics
    """
    try:
        # Get total donations count
        total_donations = Donation.query.filter_by(donor_id=donor_id).count()
        
        # Get total amount donated
        total_amount_result = db.session.query(func.sum(Donation.amount)).filter_by(donor_id=donor_id).first()
        total_amount = float(total_amount_result[0]) if total_amount_result[0] else 0.0
        
        # Get last donation date
        last_donation = Donation.query.filter_by(donor_id=donor_id).order_by(desc(Donation.date)).first()
        last_donation_date = last_donation.date.isoformat() if last_donation else None
        
        return {
            "totalDonations": total_donations,
            "totalAmount": total_amount,
            "lastDonationDate": last_donation_date
        }
    except Exception as e:
        logging.error(f"Error fetching donor stats: {str(e)}")
        return {
            "totalDonations": 0,
            "totalAmount": 0.0,
            "lastDonationDate": None
        }

def get_system_donations(page=1, size=20):
    """
    Get all donations made to the system (where user_id is null)
    
    Args:
        page (int): Page number (default: 1)
        size (int): Page size (default: 20)
        
    Returns:
        dict: Dictionary containing donations and pagination info
    """
    # Calculate offset
    offset = (page - 1) * size
    
    # Get donations where user_id is null (system donations)
    donations_query = Donation.query.filter(Donation.user_id.is_(None)).order_by(Donation.date.desc())
    
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

def get_system_donation_stats():
    """
    Get statistics for system donations (where user_id is null)
    
    Returns:
        dict: Dictionary containing system donation statistics
    """
    try:
        # Get total system donations count
        total_donations = Donation.query.filter(Donation.user_id.is_(None)).count()
        
        # Get total amount donated to system
        total_amount_result = db.session.query(func.sum(Donation.amount)).filter(Donation.user_id.is_(None)).first()
        total_amount = float(total_amount_result[0]) if total_amount_result[0] else 0.0
        
        # Get last donation date
        last_donation = Donation.query.filter(Donation.user_id.is_(None)).order_by(desc(Donation.date)).first()
        last_donation_date = last_donation.date.isoformat() if last_donation else None
        
        # Get donations per month (last 6 months)
        current_date = datetime.utcnow()
        monthly_donations = []
        
        for i in range(5, -1, -1):  # Last 6 months
            month = ((current_date.month - i - 1) % 12) + 1
            year = current_date.year - ((current_date.month - i - 1) // 12)
            
            # Count donations for this month
            count_result = db.session.query(func.count(Donation.donation_id)).filter(
                Donation.user_id.is_(None),
                func.extract('month', Donation.date) == month,
                func.extract('year', Donation.date) == year
            ).scalar()
            
            # Calculate total amount for this month
            amount_result = db.session.query(func.sum(Donation.amount)).filter(
                Donation.user_id.is_(None),
                func.extract('month', Donation.date) == month,
                func.extract('year', Donation.date) == year
            ).scalar()
            
            month_name = datetime(year, month, 1).strftime('%b')
            
            monthly_donations.append({
                "month": f"{month_name} {year}",
                "count": count_result or 0,
                "amount": float(amount_result) if amount_result else 0.0
            })
        
        return {
            "totalDonations": total_donations,
            "totalAmount": total_amount,
            "lastDonationDate": last_donation_date,
            "monthlyDonations": monthly_donations
        }
    except Exception as e:
        logging.error(f"Error fetching system donation stats: {str(e)}")
        return {
            "totalDonations": 0,
            "totalAmount": 0.0,
            "lastDonationDate": None,
            "monthlyDonations": []
        } 