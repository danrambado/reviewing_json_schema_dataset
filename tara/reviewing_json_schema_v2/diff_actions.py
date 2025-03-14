from tara.lib.action import Action
import difflib
class DiffAction(Action):
    def __init__(self):
        super().__init__()
    def generate_word_diff(text1, text2):
        """
        Generate a diff showing only the words that have changed between two strings.
        
        :param text1: The original string.
        :param text2: The modified string.
        :return: A formatted diff string with only changes.
        """
        text1_words = text1.split()
        text2_words = text2.split()
        
        diff = difflib.SequenceMatcher(None, text1_words, text2_words)
        
        diff_output = []
        for tag, i1, i2, j1, j2 in diff.get_opcodes():
            if tag == 'replace':
                diff_output.append(f"-{' '.join(text1_words[i1:i2])} +{' '.join(text2_words[j1:j2])}")
            elif tag == 'insert':
                diff_output.append(f"+{' '.join(text2_words[j1:j2])}")
            elif tag == 'delete':
                diff_output.append(f"-{' '.join(text1_words[i1:i2])}")

        return "\n".join(diff_output)

    def eval_diff(self,row) -> str:
        if row['FIXED_PROMPT'] is None or not isinstance(row['FIXED_PROMPT'], str): return ''
        return DiffAction.generate_word_diff(row['ORIGINAL_PROMPT'],row['FIXED_PROMPT'])