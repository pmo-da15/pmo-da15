# B2B Website AI Auditor

Инструмент на базе искусственного интеллекта для автоматического анализа главных страниц B2B-сайтов. Система парсит страницу, очищает контент от шума, оценивает её по маркетинговым критериям и генерирует конкретные рекомендации по улучшению конверсии.
    
**Технологии**: Python, Crawl4AI, Llama.cpp / OpenRouter, Pydantic.

# Возможности

- **Умный парсинг**: Превращает любой веб-сайт в чистый Markdown, удаляя навигацию, футеры и GDPR-баннеры.

- **Контекстный анализ**: Использует механизм скользящего окна  для обработки страниц любой длины без потери контекста.

- **Структурирование данных**: Извлекает только важные элементы: Заголовки, Описания продуктов, CTA и Social Proof.

- **Оценка и рекомендации**: Действует как B2B-маркетолог — выставляет оценки и дает советы, почему стоит изменить заголовок или добавить метрики.

- **Гибкость LLM**: Поддерживает работу с локальными моделями и облачными API.

# Архитектура решения

Процесс анализа проходит в 3 этапа:

1. **Scraping**: Браузер рендерит страницу, удаляет картинки и возвращает сырой Markdown.

2. **Extraction**:

    - Текст разбивается на перекрывающиеся окна.

    - LLM проходит по каждому окну, удаляя мусор и классифицируя контент по ролям (Header, CTA, Features).

    - Используется json_schema для гарантии валидного формата ответа.

3. **Summarization**:

    - Все чистые фрагменты склеиваются.

    - LLM получает роль "Маркетолога", анализирует структуру и выдает финальный отчет.

# Установка и настройка

## 1. Установка зависимостей

Установите необходимые библиотеки:

```
uv sync
```

После установки crawl4ai необходимо установить браузеры для Playwright:

```
playwright install
```

## 2. Запуск локальной модели

Запустите сервер в отдельном терминале:

```
./scripts/run_llama_cpp qwen3-4b-instruct q6
```

Скрипт автоматически скачает модель и поднимет сервер на порту 8080.

# Использование

Создайте базовый конфиг для локальной работы (`config.json`):

```json
{
    "llms": {
        "llm": {
            "type": "llama.cpp",
            "model": "unsloth/Qwen3-4B-Instruct-2507-GGUF:Q6_K"
        }
    },
    "extractor": "llm",
    "summarizer": "llm"
}
```

Запустите систему через CLI:

```bash
uv run cli -c ./config.json https://slack.com --output-markdown ./out.md
```

Вы можете указать несколько выводов - поддерживается формат JSON для удобной обработки (`--output-json <FILE>`), а так же Markdown (`--output-markdown <FILE>`). Так же можно указать вместо `<FILE>` `-` - тогда вывод информации произойдет в stdout.

<details>
<summary>Пример JSON-вывода</summary>

```json
{
    "criterions": {
        "value_proposition_clarity": {
            "score": 9,
            "comment": "The value proposition is clear and instantly understandable: Slack brings people, apps, and AI agents together within a unified platform. The subheadline effectively communicates the core benefit—integrating existing tools (over 2,600 apps) to automate workflows like customer feedback or IT tickets. The messaging is scannable, focused on outcomes (time saved, productivity), and avoids jargon. A first-time visitor can grasp what Slack does and why it matters in under 5 seconds."
        },
        "value_proposition_uniqueness": {
            "score": 7,
            "comment": "Slack differentiates itself through deep integration of AI agents (Agentforce, Claude, Google Agent Space) and automation capabilities within a messaging platform. This positions it as a central hub for intelligent workflows—not just communication. However, the uniqueness is somewhat generic compared to niche players in AI productivity or workflow automation (e.g., Notion AI, ClickUp, Microsoft Copilot). The claim of 'bringing AI agents into Slack' is compelling, but lacks a clear, specific competitive edge over alternatives that offer similar integrations. More differentiation around use cases (e.g., agent-led decision-making, autonomous task execution) would strengthen this."
        },
        "trust_strength": {
            "score": 8,
            "comment": "Social proof is strong and varied: includes quantified metrics (97 min saved weekly, 35% time saved), user satisfaction stats (87% say it improves collaboration), and notable reach (700M messages/day, 4M Connect users). The mention of Fortune 100 usage and G2 market leadership adds credibility. However, some metrics are repeated or appear unverified (e.g., '43 apps used on average' may be inflated). Real-world case studies with specific outcomes would add more persuasive trust. While impressive, the proof leans toward vanity metrics rather than deep, outcome-driven storytelling."
        },
        "cta_strength": {
            "score": 6,
            "comment": "The CTA section is cluttered and inconsistent. Multiple buttons (Watch demo, Download Slack, Request a demo, Get started, Find Your Plan) create confusion. 'Get Started' appears twice, and the links are not clearly prioritized. A single, compelling primary CTA (e.g., 'Start Free Trial' or 'Request Demo') would be more effective. The presence of 'Download Slack' is misleading—Slack is a SaaS product, not downloadable software—this could confuse visitors. A clearer path to next steps with role-based options (e.g., 'See how AI helps Sales', 'Get a demo for IT teams') would improve conversion."
        },
        "seo_friendliness": {
            "score": 8,
            "comment": "The page is well-structured with clear headings (COLLABORATION, CRM, PROJECT MANAGEMENT, etc.) and keyword-rich content such as 'AI in Slack', 'automate tasks', 'Slack Connect', 'agentforce', 'workflows'. The use of semantic keywords supports search visibility. Sections like 'By Department' and 'By Industry' help with long-tail SEO targeting. However, there’s a lack of targeted meta descriptions or H1/H2 optimization for specific pain points (e.g., 'How to save 97 minutes weekly with AI'). More focused, benefit-driven page titles and structured schema would further improve SEO."
        },
        "audience_fit": {
            "score": 9,
            "comment": "The messaging directly addresses real B2B pain points: fragmentation of tools, inefficient workflows, lack of access to past decisions, and time wasted in meetings. It speaks to cross-functional teams (Engineering, Sales, HR) and specific roles like IT and Project Management. The focus on AI agents and automation aligns with modern enterprise demands for intelligent productivity. Pain points such as 'remembering past decisions' or 'managing multi-step tasks' resonate deeply with operations and management teams. The content is tailored to decision-makers who care about efficiency, compliance, and scalability."
        }
    },
    "recommendations": [
        "Simplify and prioritize the CTA: Replace multiple buttons with a single, high-converting primary action (e.g., 'Start Free Trial' or 'Request Demo') and include role-specific variants (e.g., 'See how AI helps Sales Teams').",
        "Add more outcome-driven case studies: Include detailed customer stories with measurable results (e.g., 'Rivian reduced onboarding time by 40% using Slack agents') to build deeper trust and credibility.",
        "Clarify the AI agent differentiation: Explicitly state how Agentforce or Slack’s AI outperforms competitors in specific use cases like code generation, strategy drafting, or customer service automation.",
        "Improve value proposition clarity with a dedicated hero section that answers three questions: Who is it for? What problem does it solve? What results do users see?"
    ]
}
```
</details>