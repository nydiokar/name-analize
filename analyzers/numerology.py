import numpy as np
from nameparser import HumanName

class NumerologyAnalyzer:
    # Master numbers have special significance
    MASTER_NUMBERS = {
        11: "Master intuition and spiritual insight",
        22: "Master builder and manifestation",
        33: "Master teacher and healer"
    }
    
    # Karmic debt numbers indicate lessons to learn
    KARMIC_DEBT = {
        13: "Overcoming laziness and taking responsibility",
        14: "Breaking free from restrictions and learning moderation",
        16: "Overcoming ego and accepting life changes",
        19: "Learning independence and self-reliance"
    }
    
    @staticmethod
    def calculate_number(name):
        """Calculate numerological value of a name with special number recognition."""
        # Parse the name properly
        parsed_name = HumanName(name)
        # Use full name for calculation
        full_name = f"{parsed_name.first} {parsed_name.middle} {parsed_name.last}".strip()
        
        # A=1, B=2, etc. using numpy
        values = {chr(i): (i - 96) for i in range(97, 123)}
        
        # Calculate values for each part of the name
        first_value = sum(values.get(char.lower(), 0) for char in parsed_name.first if char.isalpha())
        middle_value = sum(values.get(char.lower(), 0) for char in parsed_name.middle if char.isalpha())
        last_value = sum(values.get(char.lower(), 0) for char in parsed_name.last if char.isalpha())
        
        # Total value
        total = first_value + middle_value + last_value
        
        # Check for karmic debt before reduction
        karmic_debt = None
        if total in NumerologyAnalyzer.KARMIC_DEBT:
            karmic_debt = {
                "number": total,
                "meaning": NumerologyAnalyzer.KARMIC_DEBT[total]
            }
        
        # Reduce to final number
        destiny = total
        while destiny > 9:
            # Check for master numbers before reduction
            if destiny in NumerologyAnalyzer.MASTER_NUMBERS:
                break
            destiny = sum(int(d) for d in str(destiny))
        
        # Calculate challenge numbers
        challenge_numbers = NumerologyAnalyzer.calculate_challenge_numbers(
            parsed_name.first, parsed_name.last
        )
        
        return {
            "total": total,
            "destiny": destiny,
            "is_master_number": destiny in NumerologyAnalyzer.MASTER_NUMBERS,
            "master_number_meaning": NumerologyAnalyzer.MASTER_NUMBERS.get(destiny),
            "karmic_debt": karmic_debt,
            "name_parts": {
                "first": parsed_name.first,
                "first_value": first_value,
                "middle": parsed_name.middle,
                "middle_value": middle_value,
                "last": parsed_name.last,
                "last_value": last_value
            },
            "challenge_numbers": challenge_numbers
        }
    
    @staticmethod
    def calculate_challenge_numbers(first_name, last_name):
        """Calculate challenge numbers from first and last name."""
        def reduce_number(num):
            while num > 9:
                num = sum(int(d) for d in str(num))
            return num
        
        if not first_name or not last_name:
            return None
            
        # Calculate reduced values
        first_reduced = reduce_number(sum(ord(c.lower()) - 96 
                                        for c in first_name if c.isalpha()))
        last_reduced = reduce_number(sum(ord(c.lower()) - 96 
                                       for c in last_name if c.isalpha()))
        
        # Challenge numbers
        first_challenge = abs(first_reduced - last_reduced)
        second_challenge = abs(sum(int(d) for d in str(first_reduced)) - 
                             sum(int(d) for d in str(last_reduced)))
                             
        return {
            "first_challenge": first_challenge,
            "second_challenge": second_challenge,
            "overall_challenge": reduce_number(first_challenge + second_challenge)
        }

def get_numerology(name):
    """Get complete numerological analysis of a name."""
    result = NumerologyAnalyzer.calculate_number(name)
    return {
        "total_number": result["total"],
        "destiny_number": result["destiny"],
        "is_master_number": result["is_master_number"],
        "master_number_meaning": result["master_number_meaning"],
        "karmic_debt": result["karmic_debt"],
        "name_breakdown": result["name_parts"],
        "challenges": result["challenge_numbers"]
    }
