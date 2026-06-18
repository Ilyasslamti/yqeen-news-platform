from groq import Groq
import config

SYSTEM_PROMPTS = {
    "ar": (
        "أعد صياغة الخبر التالي بأسلوب صحفي احترافي. غير الجمل والتركيب لكن حافظ على كل المعلومات.\n"
        "مثال:\n"
        "الأصل: 'أعلنت وزارة الصحة المغربية اليوم تسجيل 45 إصابة جديدة بكورونا.'\n"
        "بعد الصياغة: 'كشفت وزارة الصحة بالمغرب، اليوم الأربعاء، عن تسجيل 45 حالة إصابة جديدة بفيروس كورونا المستجد، حسب ما جاء في بلاغها الرسمي.'\n"
        "أعد الصياغة فقط."
    ),
    "fr": (
        "Réécrivez la dépêche suivante dans un style journalistique AFP professionnel. Changez les phrases et la structure mais gardez toutes les informations.\n"
        "Exemple:\n"
        "Original: 'Le ministère de la Santé a annoncé 45 nouveaux cas de Covid-19.'\n"
        "Réécrit: 'Quarante-cinq nouvelles contaminations au Covid-19 ont été enregistrées, a indiqué mercredi le ministère de la Santé dans son bilan quotidien.'\n"
        "Réécrivez uniquement."
    ),
    "en": (
        "Rewrite the following news text in professional journalistic style. Change the sentences and structure but keep all information.\n"
        "Example:\n"
        "Original: 'The Health Ministry announced 45 new Covid-19 cases today.'\n"
        "Rewritten: 'Forty-five new coronavirus infections were recorded on Wednesday, the Health Ministry said in its daily update.'\n"
        "Output only the rewritten text."
    ),
}

def rewrite_article(text: str, lang: str = "ar", max_retries: int = 2) -> str:
    if not text or len(text) < 50:
        return text

    prompt = SYSTEM_PROMPTS.get(lang, SYSTEM_PROMPTS["en"])
    trimmed = text[:5000]

    for attempt in range(max_retries):
        api_key = config.get_next_groq_key()
        if not api_key:
            return text

        try:
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": trimmed},
                ],
                max_tokens=2048,
                temperature=0.6,
            )
            content = response.choices[0].message.content
            if content and len(content) > 50:
                return content.strip()
        except:
            continue

    return text
