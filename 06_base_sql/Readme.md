# Знакомство с базой данных
___
## Описание проекта - Исследование успешности игр в разные вехи
В самостоятельном проекте этого курса вы будете работать с базой данных, которая хранит информацию
о венчурных фондах и инвестициях в компании-стартапы. Эта база данных основана на датасете [Startup Investments](https://www.kaggle.com/datasets/justinas/startup-investments),
опубликованном на популярной платформе для соревнований по исследованию данных `Kaggle`.


### Данные

![Таблица](Image.png)

**Таблица `acquisition`**   
Содержит информацию о покупках одних компаний другими.

- `id` — идентификатор или уникальный номер покупки;
- `acquiring_company_id` — ссылается на таблицу `company` — идентификатор компании-покупателя, то есть той, что покупает другую компанию;
- `acquired_company_id` — ссылается на таблицу `company` — идентификатор компании, которую покупают;
- `term_code` — способ оплаты сделки:
- `cash` — наличными;
- `stock` — акциями компании;
- `cash_and_stock` — смешанный тип оплаты: наличные и акции.
- `price_amount` — сумма покупки в долларах;
- `acquired_at` — дата совершения сделки;
- `created_at` — дата и время создания записи в таблице;
- `updated_at` — дата и время обновления записи в таблице.

**Таблица `company`**

Содержит информацию о компаниях-стартапах.
- `id` — идентификатор, или уникальный номер компании;
- `name` — название компании;
- `category_code` — категория деятельности компании
- `status` — статус компании;
- `founded_at` — дата основания компании;
- `closed_at` — дата закрытия компании, которую указывают в том случае, если компании больше не существует;
- `domain` — домен сайта компании;
- `twitter_username` — название профиля компании в твиттере;
- `country_code` — код страны, например, `USA` для США, `GBR` для Великобритании;
- `investment_rounds` — число раундов, в которых компания участвовала как инвестор;
- `funding_rounds` — число раундов, в которых компания привлекала инвестиции;
- `funding_total` — сумма привлечённых инвестиций в долларах;
- `milestones` — количество важных этапов в истории компании;
- `created_at` — дата и время создания записи в таблице;
- `updated_at` — дата и время обновления записи в таблице.

**Таблица `education`**

Хранит информацию об уровне образования сотрудников компаний.
- `id` — уникальный номер записи с информацией об образовании;
- `person_id` — ссылается на таблицу `people` — идентификатор человека, информация о котором представлена в записи;
- `degree_type` — учебная степень
- `instituition` — учебное заведение, название университета;
- `graduated_at` — дата завершения обучения, выпуска;
- `created_at` — дата и время создания записи в таблице;
- `updated_at` — дата и время обновления записи в таблице.

**Таблица `fund`**

Хранит информацию о венчурных фондах.
- `id` — уникальный номер венчурного фонда;
- `name` — название венчурного фонда;
- `founded_at` — дата основания фонда;
- `domain` — домен сайта фонда;
- `twitter_username` — профиль фонда в твиттере;
- `country_code` — код страны фонда;
- `investment_rounds` — число инвестиционных раундов, в которых фонд принимал участие;
- `invested_companies` — число компаний, в которые инвестировал фонд;
- `milestones` — количество важных этапов в истории фонда;
- `created_at` — дата и время создания записи в таблице;
- `updated_at` — дата и время обновления записи в таблице.

**Таблицп `funding_round`**

Содержит информацию о раундах инвестиций.
- `id` — уникальный номер инвестиционного раунда;
- `company_id` — ссылается на таблицу `company` — уникальный номер компании, участвовавшей в инвестиционном раунде;
- `funded_at` — дата проведения раунда;
- `funding_round_type` — тип инвестиционного раунда
- `raised_amount` — сумма инвестиций, которую привлекла компания в этом раунде в долларах;
- `pre_money_valuation` — предварительная, проведённая до инвестиций оценка стоимости компании в долларах;
- `participants` — количество участников инвестиционного раунда;
- `is_first_round` — является ли этот раунд первым для компании;
- `is_last_round` — является ли этот раунд последним для компании;
- `created_at` — дата и время создания записи в таблице;
- `updated_at` — дата и время обновления записи в таблице.

**Таблица `investment`**

Содержит информацию об инвестициях венчурных фондов в компании-стартапы.
- `id` — уникальный номер инвестиции;
- `funding_round_id` — ссылается на таблицу `funding_round` — уникальный номер раунда инвестиции;
- `company_id` — ссылается на таблицу `company` — уникальный номер компании-стартапа, в которую инвестируют;
- `fund_id` — ссылается на таблицу `fund` — уникальный номер фонда, инвестирующего в компанию-стартап;
- `created_at` — дата и время создания записи в таблице;
- `updated_at` — дата и время обновления записи в таблице.

**Таблица `people`**

Содержит информацию о сотрудниках компаний-стартапов.
- `id` — уникальный номер сотрудника;
- `first_name` — имя сотрудника;
- `last_name` — фамилия сотрудника;
- `company_id` — ссылается на таблицу company — уникальный номер компании-стартапа;
- `twitter_username` — профиль сотрудника в твиттере;
- `created_at` — дата и время создания записи в таблице;
- `updated_at` — дата и время обновления записи в таблице.

### Используемые инструменты
*PostgreSQL*