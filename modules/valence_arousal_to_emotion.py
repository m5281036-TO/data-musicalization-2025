class ValenceArousalToEmotion:
    
    def __init__(self, valence_matrix, arousal_matrix):
        """
        valence_matrix, arousal_matrix:
            2 次元配列（list of lists、または同等の構造）を受け取る
        """
        self.valence_matrix = valence_matrix
        self.arousal_matrix = arousal_matrix
        
    def convert_valence_arousal_to_emotion(self):
        emotion_matrix = []

        for valence_row, arousal_row in zip(self.valence_matrix, self.arousal_matrix):
            row_result = []
            for valence, arousal in zip(valence_row, arousal_row):

                intensify = ""
                if valence >= 60 or valence <= -60 or arousal >= 80 or arousal <= 20:
                    intensify = "extremely "

                if valence > 0:
                    if arousal >= 50:
                        emotion = "happy"
                    else:
                        emotion = "content"
                elif valence < 0:
                    if arousal >= 50:
                        emotion = "fearful"
                    else:
                        emotion = "sad"
                else:
                    if arousal == 0:
                        emotion = "neutral emotion"
                    else:
                        emotion = "neutral emotion"

                row_result.append(f"{intensify}{emotion}")

            emotion_matrix.append(row_result)

        return emotion_matrix
