# utils/language_utils.py

# Shared language constants
LANGUAGES = {
    'English': 'en',
    'Chinese': 'zh-CN',
    'Spanish': 'es',
    'French': 'fr',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Russian': 'ru',
    'Arabic': 'ar',
    'Hindi': 'hi',
    'German': 'de'
}

# Semantic context definitions
SEMANTIC_CONTEXT = {
    'animal': {
        'English': ['animal', 'pet', 'creature', 'mammal', 'wildlife', 'companion'],
        'Chinese': ['动物', '宠物', '生物', '哺乳动物', '野生动物', '伙伴'],
        'Spanish': ['animal', 'mascota', 'criatura', 'mamífero', 'fauna', 'compañero'],
        'French': ['animal', 'animal de compagnie', 'créature', 'mammifère', 'faune', 'compagnon'],
        'Japanese': ['動物', 'ペット', '生き物', '哺乳類', '野生動物', '仲間']
    },
    'human': {
        'English': ['person', 'human', 'individual', 'people', 'adult', 'being'],
        'Chinese': ['人', '人类', '个人', '人们', '成人', '生命'],
        'Spanish': ['persona', 'humano', 'individuo', 'gente', 'adulto', 'ser'],
        'French': ['personne', 'humain', 'individu', 'gens', 'adulte', 'être'],
        'Japanese': ['人', '人間', '個人', '人々', '大人', '存在']
    },
    'object': {
        'English': ['thing', 'object', 'item', 'material', 'substance', 'matter'],
        'Chinese': ['东西', '物体', '物品', '材料', '物质', '事物'],
        'Spanish': ['cosa', 'objeto', 'elemento', 'material', 'sustancia', 'materia'],
        'French': ['chose', 'objet', 'article', 'matériel', 'substance', 'matière'],
        'Japanese': ['物', '物体', '品物', '材料', '物質', '事物']
    }
}

# Example pairs for testing
EXAMPLE_PAIRS = {
    'Gender': {'English': 'man', 'Chinese': '男人', 'Spanish': 'hombre', 'French': 'homme', 'Japanese': '男'},
    'Family': {'English': 'family', 'Chinese': '家庭', 'Spanish': 'familia', 'French': 'famille', 'Japanese': '家族'},
    'Person': {'English': 'person', 'Chinese': '人', 'Spanish': 'persona', 'French': 'personne', 'Japanese': '人'}
}