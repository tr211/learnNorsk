import sqlite3
import streamlit as st
import pandas as pd

class DatabaseManager:
    """Class for managing database connection and executing queries."""
    
    def __init__(self, db_name):
        self.db_name = db_name

    def get_data(self, query, params=()):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            data = cursor.fetchall()
        except sqlite3.OperationalError as e:
            st.error(f"Database Error: {e}")
            data = []
        conn.close()
        return data

class GrammarTests:
    """Class for managing grammar tests."""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.test_type = None
        self.tests = []

    def load_grammar_tests(self, test_type):
        """Load grammar tests based on the selected test type."""
        query = "SELECT id, question, correct_answer, options FROM tests WHERE test_type = ?"
        return self.db_manager.get_data(query, (test_type,))

    def display_test_selection(self):
        """Display the menu for selecting test types."""
        test_types = ["presens", "preteritum"]
        self.test_type = st.selectbox("Velg test type:", ["Velg test type"] + test_types)

        if self.test_type != "Velg test type":
            st.header(f"{self.test_type.capitalize()} Test")
            self.tests = self.load_grammar_tests(self.test_type)
            self.display_test()

    def display_test(self):
        """Displays the current test question and handles user interaction."""
        if 'current_test' not in st.session_state:
            st.session_state.current_test = 0
            st.session_state.results = []

        current_test = st.session_state.current_test
        if current_test < len(self.tests):
            test_id, question, correct_answer, options = self.tests[current_test]
            options_list = options.split(', ')
            st.write(question)
            user_answer = st.radio("Velg riktig svar:", options_list, key=f"radio_{test_id}")

            if st.button("Sjekk svar", key=f"check_{test_id}"):
                if user_answer == correct_answer:
                    st.session_state.results.append((question, user_answer, "Riktig"))
                    st.success("Riktig!")
                else:
                    st.session_state.results.append((question, user_answer, f"Feil. Riktig svar er: {correct_answer}"))
                    st.error(f"Feil. Riktig svar er: {correct_answer}")

        if st.button("Neste test"):
            if current_test + 1 < len(self.tests):
                st.session_state.current_test += 1
            else:
                st.write("Du har fullført alle testene!")
                st.session_state.current_test = 0
                st.session_state.results = []

        if st.session_state.current_test == 0 and st.session_state.results:
            st.subheader("Dine resultater:")
            results_df = pd.DataFrame(st.session_state.results, columns=["Spørsmål", "Svar", "Resultat"])
            st.table(results_df)

class OralThemes:
    """Class for managing oral themes."""
    
    def __init__(self):
        self.themes = self.load_oral_themes()

    def load_oral_themes(self):
        return {
            "Extreme Weather": "Examples of extreme weather conditions in Norway include heavy snowstorms and strong winds.",
            "My Hobbies": "Discussing hobbies like hiking, skiing, and reading popular Norwegian literature.",
            "Travel in Norway": "Information about popular travel destinations, such as the fjords and the northern lights."
        }

    def display_themes(self):
        theme_keys = list(self.themes.keys())
        selected_theme = st.selectbox("Choose a theme:", ["Select a theme"] + theme_keys)
        if selected_theme != "Select a theme":
            st.subheader(selected_theme)
            st.write(self.themes[selected_theme])

class VerbForms:
    """Class for managing and displaying verb forms."""

    @staticmethod
    def normalize_input(verb):
        """Normalize the input by removing 'å' only if it is at the beginning and converting to lowercase."""
        # Приводим к нижнему регистру и убираем 'å', если она стоит в начале
        normalized = verb.strip().lower()
        if normalized.startswith('å'):
            return normalized[1:].strip()
        return normalized

    @staticmethod
    def show_verb_forms(verb):
        """Show the verb forms from the database."""
        # Нормализация введенного глагола
        normalized_verb = VerbForms.normalize_input(verb)
        
        conn = sqlite3.connect('norwegian_language.db')
        cursor = conn.cursor()
        
        # Попробуем сначала найти глагол как есть, а затем без начальной 'å'
        query = '''
        SELECT verb, Presens, Preteritum, "Pres. perfektum"
        FROM verb_forms
        WHERE LOWER(verb) = ? OR LOWER(REPLACE(verb, 'å', '')) = ?
        '''
        
        cursor.execute(query, (normalized_verb, normalized_verb))
        forms = cursor.fetchone()
        conn.close()

        if forms:
            st.write("Formene til verbet:")
            form_names = ["Verb", "Presens", "Preteritum", "Presens perfektum"]

            df = pd.DataFrame({"Form": form_names, "Bøyning": forms})
            st.table(df)

            selected_form = st.selectbox("Velg form:", form_names)
            form_index = form_names.index(selected_form)
            st.write(f"{selected_form}: {forms[form_index]}")
        else:
            st.error("Formene til verbet ble ikke funnet i databasen.")


class Prepositions:
    """Class for managing and displaying prepositions and examples of their use."""

    def __init__(self):
        self.prepositions = self.load_prepositions()

    def load_prepositions(self):
        return {
            "på": "Brukes for å indikere posisjon på overflaten, tid (dager, datoer). Eksempel: Jeg står på gulvet.",
            "i": "Brukes for å indikere posisjon inne i noe, tid (måneder, år). Eksempel: Jeg bor i Norge.",
            "om": "Brukes for å indikere fremtid, tid (uker, måneder). Eksempel: Vi møtes om en uke.",
            "under": "Brukes for å indikere posisjon under noe. Eksempel: Katten er under bordet.",
            "ved": "Brukes for å indikere nærhet til noe. Eksempel: Jeg står ved siden av deg.",
            "over": "Brukes for å indikere posisjon over noe. Eksempel: Fuglen flyr over huset.",
            "bak": "Brukes for å indikere posisjon bak noe. Eksempel: Han står bak døren.",
            "foran": "Brukes for å indikere posisjon foran noe. Eksempel: Bilen står foran huset.",
            "mellom": "Brukes for å indikere posisjon mellom to objekter. Eksempel: Jeg står mellom to trær.",
            "utenfor": "Brukes for å indikere posisjon utenfor noe. Eksempel: Vi møtes utenfor butikken.",
            "innenfor": "Brukes for å indikere posisjon innenfor noe. Eksempel: Han bor innenfor bymuren.",
            "langs": "Brukes for å indikere langs noe. Eksempel: Vi går langs elven.",
            "mot": "Brukes for å indikere retning mot noe. Eksempel: Han går mot skolen.",
            "rundt": "Brukes for å indikere rundt noe. Eksempel: Vi går rundt parken.",
            "til": "Brukes for å indikere retning til noe. Eksempel: Jeg skal til Oslo.",
        }

    def display_prepositions(self):
        st.header("Tema: Predloger")
        for prep, example in self.prepositions.items():
            st.subheader(prep)
            st.write(example)

class App:
    """Main class of the application, managing the display logic."""

    def __init__(self):
        self.db_manager = DatabaseManager('norwegian_language.db')
        self.grammar_tests = GrammarTests(self.db_manager)
        self.oral_themes = OralThemes()
        self.prepositions = Prepositions()
        self.verb_forms = VerbForms()

    def display_verb_forms(self):
        """Display the verb forms interface."""
        st.header("Verb Forms")
        verb = st.text_input("Skriv inn verb:")
        if verb:
            self.verb_forms.show_verb_forms(verb)

    def run(self):
        st.title("Learn Norwegian")
        st.sidebar.header("Select menu")

        # Split menu into "Grammar" and "Other topics"
        grammar_menu = st.sidebar.selectbox("Grammar:", ["Select grammar test", None])
        other_menu = st.sidebar.selectbox("Other topics:", ["Select topic", "Oral Themes", "Prepositions", "Verb Forms"])

        # Check for grammar menu selection
        if grammar_menu == "Select grammar test":
            st.header("Grammar")
            self.grammar_tests.display_test_selection()

        # Check for other topics menu selection
        if other_menu == "Oral Themes":
            st.header("Oral Themes")
            self.oral_themes.display_themes()
        elif other_menu == "Prepositions":
            st.header("Prepositions")
            self.prepositions.display_prepositions()
        elif other_menu == "Verb Forms":
            self.display_verb_forms()

if __name__ == "__main__":
    app = App()
    app.run()
