def get_syllable_count(word):
    """Calculate syllable count using vowel groups."""
    word = word.lower()
    count = 0
    vowels = 'aeiouy'
    prev_char_is_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_char_is_vowel:
            count += 1
        prev_char_is_vowel = is_vowel
        
    # Handle special cases
    if word.endswith('e'):
        count -= 1
    if count == 0:
        count = 1
        
    return count

def analyze_phonetics(name):
    """Analyze phonetic patterns in a name."""
    # Define sound categories
    soft_sounds = set('aeiouy')
    hard_sounds = set('bcdfghjklmnpqrstvwxz')
    
    # Convert to lowercase for analysis
    name = name.lower()
    
    # Count soft and hard sounds
    soft_count = sum(1 for char in name if char in soft_sounds)
    hard_count = sum(1 for char in name if char in hard_sounds)
    
    # Generate sound code (enhanced version)
    sound_code = name[0].upper()
    prev_sound = None
    sound_groups = {
        'labial': 'bfmpvw',    # Lip sounds
        'dental': 'dtnl',      # Teeth sounds
        'guttural': 'gkh',     # Throat sounds
        'sibilant': 'szx',     # Hissing sounds
        'liquid': 'lr',        # Flowing sounds
    }
    
    for char in name[1:]:
        if char in hard_sounds:
            # Determine sound group
            current_sound = next(
                (group[0] for group, chars in sound_groups.items() 
                 if char in chars),
                char
            )
            if current_sound != prev_sound:
                sound_code += current_sound
                prev_sound = current_sound
    
    # Calculate syllable count for first word
    first_word = name.split()[0] if name.split() else name
    syllable_count = get_syllable_count(first_word)
    
    # Determine dominant sound type
    dominant_type = "soft" if soft_count > hard_count else "hard"
    sound_balance = f"{soft_count/(soft_count + hard_count):.2%}" if (soft_count + hard_count) > 0 else "0%"
    
    return {
        "soft_sounds": soft_count,
        "hard_sounds": hard_count,
        "sound_code": sound_code,
        "syllables": syllable_count,
        "phonetic_description": {
            "syllable_count": str(syllable_count),
            "dominant_type": dominant_type,
            "sound_balance": f"{sound_balance} soft sounds"
        }
    }
