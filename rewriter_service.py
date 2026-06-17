from groq import Groq
import config

SYSTEM_PROMPTS = {
    "ar": "أنت صحفي محترف في وكالة أخبار عالمية. أعد صياغة الخبر التالي بأسلوب صحفي احترافي باللغة العربية الفصحى. حافظ على الحقائق والمعلومات الأساسية، نظم المقال بمقدمة وجسم وخاتمة، استخدم لغة سلسة وجذابة ومناسبة للنشر في كبرى الصحف. لا تضف معلومات غير موجودة في النص الأصلي. أخرج النص المعاد صياغته فقط.",
    "fr": "Vous êtes un journaliste professionnel dans une agence de presse internationale. Réécrivez l'article suivant dans un style journalistique professionnel en français. Préservez tous les faits et informations clés. Organisez l'article avec une introduction, un développement et une conclusion. Utilisez un langage fluide, élégant et adapté à la publication dans les grands journaux. Ne créez pas d'informations absentes du texte original. Répondez uniquement avec le texte réécrit.",
    "en": "You are a professional journalist at a global news agency. Rewrite the following news article in a professional journalistic style in English. Preserve all facts and key information. Structure the article with a compelling lead, body, and conclusion. Use clear, engaging language suitable for publication in major newspapers. Do not fabricate information not present in the original text. Output only the rewritten text.",
}

def rewrite_article(text: str, lang: str = "ar", max_retries: int = 3) -> str:
    if not text or len(text) < 50:
        return text

    prompt = SYSTEM_PROMPTS.get(lang, SYSTEM_PROMPTS["en"])

    for attempt in range(max_retries):
        api_key = config.get_next_groq_key()
        if not api_key:
            return text

        try:
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text[:4000]},
                ],
                max_tokens=2048,
                temperature=0.4,
            )
            content = response.choices[0].message.content
            if content and len(content) > 50:
                return content.strip()
        except Exception as e:
            if attempt == max_retries - 1:
                return text
            continue

    return text
