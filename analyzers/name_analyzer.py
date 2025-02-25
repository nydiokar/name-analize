from analyzers.vibration import VibrationAnalyzer
from analyzers.llm_interpreter import NameInterpreter

class NameProfile:
    def __init__(self, name):
        self.name = name
        self.analyses = {
            'numerology': {},
            'phonetics': {},
            'vibration': {},
            'interpretation': {}  # Remove frequency and cultural, add interpretation
        }
        self.insights = []

    def add_analysis(self, category, results):
        if results is None:
            results = {}
        # Special handling for interpretation category
        if category == 'interpretation':
            self.analyses[category] = results  # Store interpretation directly
        else:
            # For other categories, maintain the existing behavior
            if isinstance(results, (str, list)):
                results = {'content': results}
            self.analyses[category].update(results)

    def add_insight(self, insight):
        if insight:
            self.insights.append(insight)

    def get_report(self):
        return {
            'name': self.name,
            'analyses': self.analyses,
            'insights': self.insights
        }

class NameAnalyzer:
    def __init__(self):
        self.vibration_analyzer = VibrationAnalyzer()
        self.interpreter = NameInterpreter()

    def analyze_name(self, name):
        try:
            profile = NameProfile(name)
            
            # Run individual analyses
            numerology_data = self._analyze_numerology(name)
            phonetics_data = self._analyze_phonetics(name)
            vibration_data = self._analyze_vibration(name)
            
            # Update profile with analyses
            profile.add_analysis('numerology', numerology_data)
            profile.add_analysis('phonetics', phonetics_data)
            profile.add_analysis('vibration', vibration_data)
            
            # Prepare complete analysis data for interpretation
            analysis_data = {
                'name': name,
                'numerology': numerology_data,
                'phonetics': phonetics_data,
                'vibration': vibration_data
            }
            
            # Generate interpretation
            try:
                interpretation = self.interpreter.generate_interpretation(analysis_data)
                if interpretation:
                    # Store interpretation directly without wrapping
                    profile.add_analysis('interpretation', interpretation)
                    # Add to insights if needed
                    if isinstance(interpretation, str):
                        profile.add_insight(interpretation)
            except Exception as e:
                print(f"Interpretation error: {str(e)}")
                profile.add_analysis('interpretation', {'error': str(e)})
            
            return profile
            
        except Exception as e:
            print(f"Analysis error: {str(e)}")
            profile = NameProfile(name)
            profile.add_analysis('error', {'message': str(e)})
            return profile

    def _analyze_numerology(self, name):
        try:
            number = sum(ord(c.lower()) - ord('a') + 1 for c in name if c.isalpha())
            return {
                'destiny_number': number % 9 or 9,
                'analysis_type': 'numerology'
            }
        except Exception as e:
            print(f"Numerology analysis error: {str(e)}")
            return {'error': str(e), 'analysis_type': 'numerology'}

    def _analyze_phonetics(self, name):
        try:
            consonants = sum(1 for c in name.lower() if c in 'bcdfghjklmnpqrstvwxyz')
            vowels = sum(1 for c in name.lower() if c in 'aeiou')
            return {
                'consonant_count': consonants,
                'vowel_count': vowels,
                'total_length': len(name),
                'analysis_type': 'phonetic'
            }
        except Exception as e:
            print(f"Phonetics analysis error: {str(e)}")
            return {'error': str(e), 'analysis_type': 'phonetic'}

    def _analyze_vibration(self, name):
        try:
            vibration_data = self.vibration_analyzer.analyze_name_vibration(name)
            if vibration_data:
                vibration_data['analysis_type'] = 'vibration'
            return vibration_data
        except Exception as e:
            print(f"Vibration analysis error: {str(e)}")
            return {'error': str(e), 'analysis_type': 'vibration'}
