-- Отримати всі завдання певного користувача.
SELECT * FROM tasks AS t
WHERE t.user_id = {...}

-- Вибрати завдання за певним статусом.
SELECT * FROM tasks AS t
WHERE t.status_id = (
	SELECT s.id FROM status AS s
	WHERE s.name = 'new'
)

select * from tasks;

-- Оновити статус конкретного завдання.
UPDATE tasks
SET status_id = (SELECT id FROM status WHERE name = 'in progress')
WHERE id = {...}

-- Отримати список користувачів, які не мають жодного завдання. 
SELECT * FROM users AS u
WHERE u.id NOT IN (
	SELECT t.user_id FROM tasks AS t
);

-- Додати нове завдання для конкретного користувача. 
INSERT INTO tasks (title, description, status_id, user_id)
VALUES ('Test title', 'Test description', 1, 14);

-- Отримати всі завдання, які ще не завершено.
SELECT * FROM tasks AS t
WHERE t.status_id <> (SELECT s.id FROM status AS s WHERE s.name = 'completed');

-- Видалити конкретне завдання.
DELETE FROM tasks AS t WHERE t.id = {...}

-- Знайти користувачів з певною електронною поштою.
SELECT * FROM users AS u
WHERE u.email LIKE '%.com'

-- Оновити ім'я користувача.
UPDATE users AS u
SET u.name = {...}
WHERE u.id = {...}

-- Отримати кількість завдань для кожного статусу.
SELECT t.status_id, COUNT(t.id) 
FROM tasks AS t
GROUP BY t.status_id;

-- Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти.
select * from tasks;

SELECT t.* FROM tasks AS t
JOIN users AS u ON 
	u.id = t.user_id AND
	u.email LIKE '%@example.com';

-- Отримати список завдань, що не мають опису. 
INSERT INTO tasks (title, description, status_id, user_id)
VALUES ('Test title', '', 1, 14);
INSERT INTO tasks (title, description, status_id, user_id)
VALUES ('Test title', NULL, 1, 14);
SELECT * FROM tasks AS t WHERE description IS NULL OR description = '';

-- Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
SELECT t.*, u.*
FROM tasks AS t
INNER JOIN users AS u ON t.user_id = u.id
WHERE t.status_id = (
	SELECT s.id 
	FROM status AS s 
	WHERE s.name = 'in progress'
);

-- Отримати користувачів та кількість їхніх завдань.
SELECT u.fullname AS user_name, COUNT(t.id) AS tasks
FROM users AS u
LEFT JOIN tasks AS t ON u.id = t.user_id
GROUP BY u.id;