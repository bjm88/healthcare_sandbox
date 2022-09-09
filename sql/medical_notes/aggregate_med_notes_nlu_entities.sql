SELECT
	entities.entity_item ->> 'Type' AS EntityType,
	entities.entity_item ->> 'Category' AS category,
	entities.entity_item ->> 'Text' AS TextValue,
	COUNT(1) AS NumItems
FROM
	medical_notes,
	JSONB_ARRAY_ELEMENTS(entity_extraction) WITH ORDINALITY entities(entity_item, POSITION)
WHERE
	entity_extraction IS NOT NULL
GROUP BY
	EntityType,
	category,
	TextValue
ORDER BY
	NumItems DESC;