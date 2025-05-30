# API Диаграммы и Описание

В этой папке содержатся PlantUML-диаграммы для каждого основного эндпоинта системы HR.

## Оглавление
- [Аутентификация и пользователи](#аутентификация-и-пользователи)
- [Вакансии](#вакансии)
- [Кандидаты](#кандидаты)

---

## Аутентификация и пользователи

### POST /api/auth/register/
Регистрация нового пользователя. Требует email, пароль и роль (HR или MANAGER). Возвращает данные пользователя.

### POST /api/auth/login/
Аутентификация пользователя. Принимает email и пароль, возвращает JWT access/refresh токены, email, роль и user_id.

---

## Вакансии

### GET /api/vacancies/
Получение списка вакансий. HR видит только открытые, MANAGER — все.

### POST /api/vacancies/
Создание новой вакансии (только MANAGER).

### GET /api/vacancies/{id}/
Детали вакансии.

### PUT/PATCH /api/vacancies/{id}/
Редактирование вакансии (только MANAGER).

### DELETE /api/vacancies/{id}/
Удаление вакансии (только MANAGER).

### GET /api/vacancies/all_stats/
Статистика по всем вакансиям (количество кандидатов, принятых, в процессе).

### PUT /api/vacancies/{id}/publish/
Открыть вакансию (статус OPEN).

### PUT /api/vacancies/{id}/close/
Закрыть вакансию (статус CLOSED).

---

## Кандидаты

### GET /api/candidates/
Список кандидатов. HR видит всех, MANAGER — только финальные статусы.

### POST /api/candidates/
Создание кандидата (только HR).

### GET /api/candidates/{id}/
Детали кандидата.

### PUT/PATCH /api/candidates/{id}/
Редактирование кандидата (только HR).

### DELETE /api/candidates/{id}/
Удаление кандидата (только HR).

### GET /api/candidates/stats/
Статистика по кандидатам (всего, принятых, отклонённых).

### POST /api/candidates/{id}/move_to_tech/
Перевести кандидата на этап технического собеседования (только HR).

### POST /api/candidates/{id}/reject/
Отклонить кандидата (HR — на этапе HR, MANAGER — на финальном этапе).

### POST /api/candidates/{id}/change_status/
Сменить статус кандидата (логика зависит от роли и текущего статуса).

### PATCH /api/candidates/{id}/update_hr_comment/
Обновить комментарий HR (только HR).

### PATCH /api/candidates/{id}/update_tech_comment/
Обновить комментарий тех. специалиста (только MANAGER).

---

Каждому эндпоинту соответствует отдельная диаграмма PlantUML в этом каталоге. 