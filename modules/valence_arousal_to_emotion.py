class ValenceArousalToEmotion:
    
    def __init__(self, valence_array, arousal_array):
        self.valence_array = valence_array
        self.arousal_array = arousal_array
        
        
    def convert_valencea_arousal_to_emotion(self):
        emotion_array = []
        
        for valence, arousal in zip (self.valence_array, self.arousal_array):
            intensify = ""
            if valence >= 60 or valence <= -60 or arousal >=80 or arousal <= 20:
                intensify = "extremely "

            if valence > 0:
                if arousal >= 50:
                    emotion = "happy and joyful"
                elif arousal < 50: 
                    emotion = "contentment"
            if valence < 0:
                    if arousal >= 50:
                        emotion = "angery or fearful"
                    elif arousal < 50: 
                        emotion = "sad"
            elif valence == 0:
                    if arousal == 0:
                        emotion = "neutral emotion"
            emotion_array.append(f"{intensify}{emotion}")
        
        
        print(emotion_array)
        return emotion_array