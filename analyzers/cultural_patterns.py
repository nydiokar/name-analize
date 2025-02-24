from collections import defaultdict
import re

class CulturalAnalyzer:
    """Analyzer for cultural name patterns and their significance."""
    
    # Cultural patterns and their meanings
    PATTERNS = {
        'slavic': {
            'endings': {
                'iya': ('feminine', 'grace and wisdom'),
                'ya': ('feminine', 'spiritual connection'),
                'av': ('masculine', 'strength and protection'),
                'slav': ('masculine', 'glory and honor'),
                'mir': ('masculine', 'peace and greatness'),
                'ana': ('feminine', 'grace and favor'),
                'ko': ('diminutive', 'warmth and familiarity')
            },
            'roots': {
                'mir': 'peace',
                'slav': 'glory',
                'vit': 'life',
                'rad': 'joy',
                'mil': 'grace',
                'sviat': 'holy'
            }
        },
        'germanic': {
            'elements': {
                'ald': 'old, wise',
                'bert': 'bright',
                'fried': 'peace',
                'helm': 'protection',
                'wald': 'rule'
            }
        },
        'celtic': {
            'elements': {
                'donald': ('world ruler', 'proud chief'),
                'ken': 'born of fire',
                'malcolm': 'devotee of Saint Columba',
                'alan': 'harmony, stone'
            }
        },
        'latin': {
            'elements': {
                'victor': 'conqueror',
                'clara': 'bright',
                'paul': 'small, humble',
                'mar': 'sea'
            }
        }
    }
    
    # Special character combinations and their meanings
    COMBINATIONS = {
        'double_letters': {
            'll': 'spiritual enlightenment',
            'nn': 'inner strength',
            'tt': 'determination',
            'ss': 'mystical insight'
        },
        'consonant_pairs': {
            'st': 'stability and strength',
            'th': 'wisdom and thought',
            'ch': 'spiritual protection',
            'ph': 'mystic knowledge'
        }
    }
    
    # Name structure patterns
    STRUCTURES = {
        r'^[aeiou].*[aeiou]$': 'opens and closes with flowing energy',
        r'^[^aeiou].*[aeiou]$': 'grounded start with spiritual ending',
        r'^[aeiou].*[^aeiou]$': 'spiritual beginning with earthly completion',
        r'([^aeiou])\1': 'contains doubled power',
        r'([aeiou])\1': 'contains spiritual resonance'
    }

    @staticmethod
    def analyze_cultural_elements(name):
        """Analyze cultural elements in a name."""
        name = name.lower()
        results = {
            'patterns': [],
            'cultural_roots': set(),
            'special_meanings': [],
            'structure_notes': [],
            'dominant_culture': None,
            'character_essence': []
        }
        
        # Check for cultural patterns
        for culture, patterns in CulturalAnalyzer.PATTERNS.items():
            matches = []
            
            # Check endings and elements
            for section in ['endings', 'elements']:
                if section in patterns:
                    for pattern, meaning in patterns[section].items():
                        if pattern in name:
                            matches.append({
                                'type': section,
                                'pattern': pattern,
                                'meaning': meaning
                            })
                            results['cultural_roots'].add(culture)
            
            # Check roots if available
            if 'roots' in patterns:
                for root, meaning in patterns['roots'].items():
                    if root in name:
                        matches.append({
                            'type': 'root',
                            'pattern': root,
                            'meaning': meaning
                        })
                        results['cultural_roots'].add(culture)
            
            if matches:
                results['patterns'].extend(matches)
        
        # Analyze special combinations
        for comb_type, combinations in CulturalAnalyzer.COMBINATIONS.items():
            for pattern, meaning in combinations.items():
                if pattern in name:
                    results['special_meanings'].append({
                        'type': comb_type,
                        'pattern': pattern,
                        'meaning': meaning
                    })
        
        # Analyze name structure
        for pattern, meaning in CulturalAnalyzer.STRUCTURES.items():
            if re.search(pattern, name):
                results['structure_notes'].append(meaning)
        
        # Determine character essence based on first and last letters
        first_char = name[0]
        last_char = name[-1]
        
        if first_char in 'aeiou':
            results['character_essence'].append("Begins with spiritual energy")
        else:
            results['character_essence'].append("Begins with grounding force")
            
        if last_char in 'aeiou':
            results['character_essence'].append("Concludes with open possibilities")
        else:
            results['character_essence'].append("Concludes with practical manifestation")
        
        # Determine dominant culture if any
        if results['cultural_roots']:
            results['dominant_culture'] = max(results['cultural_roots'], 
                                           key=lambda x: sum(1 for p in results['patterns'] 
                                                          if p.get('type') in ['endings', 'roots']))
        
        results['cultural_roots'] = list(results['cultural_roots'])
        return results

    @staticmethod
    def get_unique_interpretation(name, patterns):
        """Generate unique interpretation based on name patterns."""
        name = name.lower()
        interpretations = []
        
        # Get cultural analysis
        analysis = CulturalAnalyzer.analyze_cultural_elements(name)
        
        # Add cultural essence
        if analysis['dominant_culture']:
            if analysis['dominant_culture'] == 'slavic':
                if any(p['type'] == 'endings' for p in analysis['patterns']):
                    if len(set(name)) > len(name) * 0.7:
                        interpretations.append("Your name carries a unique blend of Slavic tradition with individual character")
                    else:
                        interpretations.append("Your name embodies classical Slavic values while maintaining its own gentle strength")
            elif analysis['dominant_culture'] == 'germanic':
                interpretations.append("Your name reflects Germanic strength and wisdom")
            elif analysis['dominant_culture'] == 'celtic':
                interpretations.append("Your name carries Celtic nobility and natural power")
            elif analysis['dominant_culture'] == 'latin':
                interpretations.append("Your name embodies Classical dignity and clarity")
        
        # Add structural insights
        if analysis['structure_notes']:
            interpretations.append(analysis['structure_notes'][0])
        
        # Add character essence
        if analysis['character_essence']:
            interpretations.append(" and ".join(analysis['character_essence']))
        
        # Add special combinations
        if analysis['special_meanings']:
            special = analysis['special_meanings'][0]
            interpretations.append(f"The {special['pattern']} in your name suggests {special['meaning']}")
        
        return interpretations
