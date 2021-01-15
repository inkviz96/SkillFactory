"# SkillFactory"


Registration company app (User registration and authorization on a django API with djoser and JSON web tokens):

1. /auth/users/	- Зарегистрировать нового пользователя (компанию)

2. /auth/users/me/	- получить/обновить зарегистрированного пользователя (компанию)

3. /auth/jwt/create/ - создать JWT, передав действующему пользователю в запросе post эту конечную точку

4. /auth/jwt/refresh/ -	получить новый JWT по истечении времени жизни ранее сгенерированного

5. /api/registration/all-companies-profiles/	- получить все профили компаний и создать новый
    
    На данный момент для создания профиля и отправки заявки на email компании не обязательно быть зарегестрированным пользователем. 
    Заявка отправляется на почту менеджера при создании профиля компании (реализовано вo view).
    
6. /api/registration/company-profile/id/- подробный вид профиля компании по id